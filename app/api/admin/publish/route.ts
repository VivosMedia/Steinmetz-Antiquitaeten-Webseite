import { NextRequest, NextResponse } from "next/server";

const REPO   = "VivosMedia/Steinmetz-Antiquitaeten-Webseite";
const BRANCH = "master";
const FILE   = "public/products.json";

const GH_API = "https://api.github.com";
const GH_HEADERS = {
  Authorization: `Bearer ${process.env.GITHUB_TOKEN}`,
  Accept: "application/vnd.github.v3+json",
  "Content-Type": "application/json",
};

function cors(res: NextResponse) {
  res.headers.set("Access-Control-Allow-Origin", "*");
  res.headers.set("Access-Control-Allow-Methods", "POST, OPTIONS");
  res.headers.set("Access-Control-Allow-Headers", "Content-Type");
  return res;
}

export async function OPTIONS() {
  return cors(new NextResponse(null, { status: 204 }));
}

type PublishBody = {
  passwordHash: string;
  additions: { cat: string; product: Product }[];
  deletions: { cat: string; id: string }[];
  images?: { path: string; content: string }[]; // content = reines Base64, ohne data:-Prefix
};

type Product = Record<string, unknown> & { id: string };
type ProductCatalog = Record<string, Product[]>;

function isProduct(value: unknown): value is Product {
  return typeof value === "object"
    && value !== null
    && !Array.isArray(value)
    && typeof (value as { id?: unknown }).id === "string";
}

function isProductAddition(value: unknown): value is { cat: string; product: Product } {
  return typeof value === "object"
    && value !== null
    && !Array.isArray(value)
    && typeof (value as { cat?: unknown }).cat === "string"
    && isProduct((value as { product?: unknown }).product);
}

function isProductDeletion(value: unknown): value is { cat: string; id: string } {
  return typeof value === "object"
    && value !== null
    && !Array.isArray(value)
    && typeof (value as { cat?: unknown }).cat === "string"
    && typeof (value as { id?: unknown }).id === "string";
}

function isProductCatalog(value: unknown): value is ProductCatalog {
  return typeof value === "object"
    && value !== null
    && !Array.isArray(value)
    && Object.values(value).every(
      (items) => Array.isArray(items) && items.every(isProduct)
    );
}

async function getFileSha(path: string): Promise<string | null> {
  const r = await fetch(`${GH_API}/repos/${REPO}/contents/${path}?ref=${BRANCH}`, {
    headers: GH_HEADERS,
  });
  if (!r.ok) return null;
  const data = await r.json();
  return data.sha ?? null;
}

async function getCurrentProducts(): Promise<{ sha: string; products: ProductCatalog }> {
  const r = await fetch(`${GH_API}/repos/${REPO}/contents/${FILE}?ref=${BRANCH}`, {
    headers: GH_HEADERS,
  });
  if (!r.ok) {
    const e = await r.json().catch(() => ({}));
    throw new Error(`GitHub-Fehler beim Lesen von ${FILE}: ${e.message || r.status}`);
  }

  const data = await r.json();
  if (typeof data.sha !== "string" || data.encoding !== "base64" || typeof data.content !== "string") {
    throw new Error(`GitHub lieferte keinen lesbaren Inhalt für ${FILE}.`);
  }

  const parsed: unknown = JSON.parse(Buffer.from(data.content.replace(/\s/g, ""), "base64").toString("utf-8"));
  if (!isProductCatalog(parsed)) {
    throw new Error(`${FILE} hat ein ungültiges Produktformat.`);
  }

  return { sha: data.sha, products: parsed };
}

async function putFile(path: string, content: string, message: string, currentSha?: string | null) {
  const sha = currentSha === undefined ? await getFileSha(path) : currentSha;
  const body: Record<string, unknown> = { message, content, branch: BRANCH };
  if (sha) body.sha = sha;

  const r = await fetch(`${GH_API}/repos/${REPO}/contents/${path}`, {
    method: "PUT",
    headers: GH_HEADERS,
    body: JSON.stringify(body),
  });
  if (!r.ok) {
    const e = await r.json().catch(() => ({}));
    throw new Error(`GitHub-Fehler bei ${path}: ${e.message || r.status}`);
  }
  return r.json();
}

export async function POST(request: NextRequest) {
  try {
    const body = (await request.json()) as PublishBody;

    if (!process.env.ADMIN_PASSWORD_HASH || body.passwordHash !== process.env.ADMIN_PASSWORD_HASH) {
      return cors(NextResponse.json({ success: false, error: "Falsches Passwort." }, { status: 401 }));
    }
    if (!process.env.GITHUB_TOKEN) {
      return cors(NextResponse.json({ success: false, error: "Server nicht konfiguriert (GITHUB_TOKEN fehlt)." }, { status: 500 }));
    }

    if (
      !Array.isArray(body.additions)
      || !body.additions.every(isProductAddition)
      || !Array.isArray(body.deletions)
      || !body.deletions.every(isProductDeletion)
    ) {
      return cors(NextResponse.json({
        success: false,
        error: "Das Admin-Panel ist veraltet oder die Produktänderungen sind ungültig. Bitte neu laden.",
      }, { status: 400 }));
    }
    const additions = body.additions;
    const deletions = body.deletions;

    // 1) Ausstehende Fotos hochladen
    for (const img of body.images ?? []) {
      await putFile(img.path, img.content, `Foto hochgeladen: ${img.path}`);
    }

    // Apply changes to the GitHub version, not a possibly stale static-site copy.
    const current = await getCurrentProducts();
    for (const deletion of deletions) {
      current.products[deletion.cat] = (current.products[deletion.cat] || [])
        .filter((product) => product.id !== deletion.id);
    }
    for (const addition of additions) {
      if (deletions.some((deletion) => deletion.cat === addition.cat && deletion.id === addition.product.id)) {
        continue;
      }
      const category = current.products[addition.cat] ?? (current.products[addition.cat] = []);
      if (!category.some((product) => product.id === addition.product.id)) {
        category.unshift(addition.product);
      }
    }

    // 2) products.json aktualisieren
    const json = JSON.stringify(current.products, null, 2);
    const contentB64 = Buffer.from(json, "utf-8").toString("base64");
    await putFile(FILE, contentB64, "Produkte aktualisiert via Admin-Panel", current.sha);

    return cors(NextResponse.json({ success: true, products: current.products }));
  } catch (err) {
    return cors(
      NextResponse.json(
        { success: false, error: err instanceof Error ? err.message : "Unbekannter Fehler" },
        { status: 500 }
      )
    );
  }
}
