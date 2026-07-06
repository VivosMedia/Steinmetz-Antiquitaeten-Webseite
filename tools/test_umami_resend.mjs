// Eigenständiges Testskript für die Umami+Resend-Konfiguration.
// Bildet die Logik von app/api/cron/daily-report/route.ts nach,
// ohne dass Next.js/Vercel dafür laufen muss.
import { config } from 'dotenv';
import { Resend } from 'resend';
import path from 'node:path';

config({ path: path.join(process.cwd(), '.env.local') });

const required = ['UMAMI_HOST', 'UMAMI_USERNAME', 'UMAMI_PASSWORD', 'UMAMI_WEBSITE_ID', 'RESEND_API_KEY', 'REPORT_EMAIL_TO'];
const missing = required.filter(k => !process.env[k]);
if (missing.length) {
  console.error('❌ Fehlende Variablen in .env.local:', missing.join(', '));
  process.exit(1);
}

const { UMAMI_HOST, UMAMI_USERNAME, UMAMI_PASSWORD, UMAMI_WEBSITE_ID, RESEND_API_KEY, REPORT_EMAIL_TO } = process.env;

async function main() {
  console.log('1) Umami-Login …');
  const loginRes = await fetch(`${UMAMI_HOST}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username: UMAMI_USERNAME, password: UMAMI_PASSWORD }),
  });
  if (!loginRes.ok) {
    console.error(`❌ Umami-Login fehlgeschlagen: HTTP ${loginRes.status}`);
    console.error(await loginRes.text());
    process.exit(1);
  }
  const { token } = await loginRes.json();
  console.log('   ✓ Login erfolgreich, Token erhalten.');

  console.log('2) Umami-Stats abrufen …');
  const endAt = new Date();
  endAt.setHours(0, 0, 0, 0);
  const startAt = new Date(endAt);
  startAt.setDate(startAt.getDate() - 1);

  const statsRes = await fetch(
    `${UMAMI_HOST}/api/websites/${UMAMI_WEBSITE_ID}/stats?startAt=${startAt.getTime()}&endAt=${endAt.getTime()}`,
    { headers: { Authorization: `Bearer ${token}` } }
  );
  if (!statsRes.ok) {
    console.error(`❌ Stats-Abruf fehlgeschlagen: HTTP ${statsRes.status}`);
    console.error(await statsRes.text());
    process.exit(1);
  }
  const stats = await statsRes.json();
  const getValue = (f) => (typeof f === 'object' && f !== null ? f.value ?? 0 : f ?? 0);
  const visitors = getValue(stats.visitors);
  const visits = getValue(stats.visits);
  const pageviews = getValue(stats.pageviews);
  const bounces = getValue(stats.bounces);
  const bounceRate = visits > 0 ? ((bounces / visits) * 100).toFixed(1) : '0.0';
  console.log(`   ✓ Stats erhalten: ${visitors} Besucher, ${visits} Sessions, ${pageviews} Pageviews, ${bounceRate}% Bounce Rate.`);

  console.log('3) Test-E-Mail via Resend senden …');
  const resend = new Resend(RESEND_API_KEY);
  const dateLabel = startAt.toLocaleDateString('de-DE', { weekday: 'long', day: '2-digit', month: '2-digit', year: 'numeric' });
  const { data, error } = await resend.emails.send({
    from: 'Analytics Report <daily_report@vivos.media>',
    to: REPORT_EMAIL_TO,
    subject: `[TEST] 📊 Analytics Report – ${dateLabel}`,
    html: `<div style="font-family: sans-serif; max-width: 480px; margin: 0 auto;">
      <h2>Test: Deine Besucherzahlen von gestern</h2>
      <p style="color:#666;">${dateLabel}</p>
      <table style="width:100%; border-collapse:collapse; margin-top:16px;">
        <tr style="border-bottom:1px solid #eee;"><td style="padding:8px 0;">Besucher</td><td style="padding:8px 0; text-align:right; font-weight:bold;">${visitors}</td></tr>
        <tr style="border-bottom:1px solid #eee;"><td style="padding:8px 0;">Sessions</td><td style="padding:8px 0; text-align:right; font-weight:bold;">${visits}</td></tr>
        <tr style="border-bottom:1px solid #eee;"><td style="padding:8px 0;">Pageviews</td><td style="padding:8px 0; text-align:right; font-weight:bold;">${pageviews}</td></tr>
        <tr><td style="padding:8px 0;">Bounce Rate</td><td style="padding:8px 0; text-align:right; font-weight:bold;">${bounceRate}%</td></tr>
      </table>
    </div>`,
  });
  if (error) {
    console.error('❌ Resend-Versand fehlgeschlagen:', JSON.stringify(error));
    process.exit(1);
  }
  console.log(`   ✓ E-Mail gesendet (Resend-ID: ${data.id}) an ${REPORT_EMAIL_TO}.`);
  console.log('\n✅ Gesamter Test erfolgreich!');
}

main().catch(err => {
  console.error('❌ Unerwarteter Fehler:', err);
  process.exit(1);
});
