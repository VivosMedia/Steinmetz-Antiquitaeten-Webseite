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
  products: unknown;
  images?: { path: string; content: string }[]; // content = reines Base64, ohne data:-Prefix
};

async function getFileSha(path: string): Promise<string | null> {
  const r = await fetch(`${GH_API}/repos/${REPO}/contents/${path}?ref=${BRANCH}`, {
    headers: GH_HEADERS,
  });
  if (!r.ok) return null;
  const data = await r.json();
  return data.sha ?? null;
}

async function putFile(path: string, content: string, message: string) {
  const sha = await getFileSha(path);
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

    // 1) Ausstehende Fotos hochladen
    for (const img of body.images ?? []) {
      await putFile(img.path, img.content, `Foto hochgeladen: ${img.path}`);
    }

    // 2) products.json aktualisieren
    const json = JSON.stringify(body.products, null, 2);
    const contentB64 = Buffer.from(json, "utf-8").toString("base64");
    await putFile(FILE, contentB64, "Produkte aktualisiert via Admin-Panel");

    return cors(NextResponse.json({ success: true }));
  } catch (err) {
    return cors(
      NextResponse.json(
        { success: false, error: err instanceof Error ? err.message : "Unbekannter Fehler" },
        { status: 500 }
      )
    );
  }
}
