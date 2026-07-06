import { NextRequest, NextResponse } from "next/server";
import { Resend } from "resend";

const resend = new Resend(process.env.RESEND_API_KEY);

export async function GET(request: NextRequest) {
  // 1. Absicherung: nur Vercel (via CRON_SECRET) darf diese Route aufrufen
  const authHeader = request.headers.get("authorization");
  if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
    return new NextResponse("Unauthorized", { status: 401 });
  }

  try {
    // 2. Bei Umami einloggen und Token holen
    const loginRes = await fetch(`${process.env.UMAMI_HOST}/api/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        username: process.env.UMAMI_USERNAME,
        password: process.env.UMAMI_PASSWORD,
      }),
    });

    if (!loginRes.ok) {
      throw new Error(`Umami-Login fehlgeschlagen: ${loginRes.status}`);
    }

    const { token } = await loginRes.json();

    // 3. Zeitraum berechnen: gestern 00:00 bis heute 00:00
    const endAt = new Date();
    endAt.setHours(0, 0, 0, 0);
    const startAt = new Date(endAt);
    startAt.setDate(startAt.getDate() - 1);

    // 4. Stats von Umami abrufen
    const statsRes = await fetch(
      `${process.env.UMAMI_HOST}/api/websites/${process.env.UMAMI_WEBSITE_ID}/stats?startAt=${startAt.getTime()}&endAt=${endAt.getTime()}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (!statsRes.ok) {
      throw new Error(`Umami-Stats-Abruf fehlgeschlagen: ${statsRes.status}`);
    }

    const stats = await statsRes.json();

    // Umami gibt Werte teils als { value: number } zurück – wir fangen beide Formate ab
    const getValue = (field: any): number =>
      typeof field === "object" && field !== null ? field.value ?? 0 : field ?? 0;

    const visitors = getValue(stats.visitors);
    const visits = getValue(stats.visits);
    const pageviews = getValue(stats.pageviews);
    const bounces = getValue(stats.bounces);
    const bounceRate = visits > 0 ? ((bounces / visits) * 100).toFixed(1) : "0.0";

    const dateLabel = startAt.toLocaleDateString("de-DE", {
      weekday: "long",
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
    });

    // 5. E-Mail über Resend verschicken
    const { error } = await resend.emails.send({
      from: "Analytics Report <daily_report@vivos.media>", // Test-Domain, siehe README
      to: process.env.REPORT_EMAIL_TO!,
      subject: `📊 Analytics Report – ${dateLabel}`,
      html: `
        <div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
          <h2 style="margin-bottom: 4px;">Deine Besucherzahlen von gestern</h2>
          <p style="color: #666; margin-top: 0;">${dateLabel}</p>
          <table style="width: 100%; border-collapse: collapse; margin-top: 16px;">
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 8px 0;">Besucher</td>
              <td style="padding: 8px 0; text-align: right; font-weight: bold;">${visitors}</td>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 8px 0;">Sessions</td>
              <td style="padding: 8px 0; text-align: right; font-weight: bold;">${visits}</td>
            </tr>
            <tr style="border-bottom: 1px solid #eee;">
              <td style="padding: 8px 0;">Pageviews</td>
              <td style="padding: 8px 0; text-align: right; font-weight: bold;">${pageviews}</td>
            </tr>
            <tr>
              <td style="padding: 8px 0;">Bounce Rate</td>
              <td style="padding: 8px 0; text-align: right; font-weight: bold;">${bounceRate}%</td>
            </tr>
          </table>
        </div>
      `,
    });

    if (error) {
      throw new Error(`Resend-Versand fehlgeschlagen: ${JSON.stringify(error)}`);
    }

    return NextResponse.json({ success: true, visitors, visits, pageviews });
  } catch (err) {
    console.error("Daily Report Cron Fehler:", err);
    return NextResponse.json(
      { success: false, error: err instanceof Error ? err.message : "Unbekannter Fehler" },
      { status: 500 }
    );
  }
}
