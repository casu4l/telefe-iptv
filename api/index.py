export default async function handler(req, res) {
  const r = await fetch("PEGA_ACA_LA_URL_DE_LA_PAGINA_DEL_VIVO", {
    headers: { "User-Agent": "Mozilla/5.0" }
  });
  const html = await r.text();
  const m = html.match(/https?:[^"'\s\\]+\.m3u8[^"'\s\\]*/);
  if (!m) return res.status(502).send("No encontré el link");
  const url = m[0].replace(/\\u0026/g, "&").replace(/\\\//g, "/");
  res.redirect(302, url);
