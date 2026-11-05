/** Diagnóstico de permisos del token de Netlify y creación del sitio con cuenta. */

const TOKEN = process.env.NETLIFY_TOKEN;
const cabeceras = { Authorization: `Bearer ${TOKEN}`, "User-Agent": "dsh-landing" };

const api = async (ruta, opciones = {}) => {
  const r = await fetch(`https://api.netlify.com/api/v1${ruta}`, {
    headers: { ...cabeceras, ...(opciones.headers ?? {}) },
    ...opciones,
  });
  const t = await r.text();
  let d = null;
  try {
    d = t ? JSON.parse(t) : null;
  } catch {
    d = null;
  }
  return { status: r.status, datos: d, texto: t };
};

async function main() {
  const cuentas = await api("/accounts");
  console.log("GET /accounts:", cuentas.status);
  const lista = Array.isArray(cuentas.datos) ? cuentas.datos : [];
  for (const c of lista) {
    console.log("  cuenta:", c.slug, "|", c.name, "| tipo:", c.type_name ?? c.type);
  }

  const sitios = await api("/sites?per_page=100");
  console.log("GET /sites:", sitios.status, "| cantidad:", Array.isArray(sitios.datos) ? sitios.datos.length : "—");

  if (!lista.length) {
    console.log("\nEl token no tiene cuentas accesibles: probablemente es de solo lectura.");
    return;
  }

  const slug = lista[0].slug;
  const nombre = "silverado-ferreterias";

  console.log("\nPOST /sites con account_slug:", slug);
  const creado = await api(`/sites?account_slug=${encodeURIComponent(slug)}`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ name: nombre, account_slug: slug }),
  });
  console.log("  status:", creado.status);
  if (creado.status >= 400) {
    console.log("  detalle:", (creado.texto ?? "").slice(0, 300));
  } else {
    console.log("  sitio:", creado.datos.ssl_url ?? creado.datos.url);
    console.log("SITE_ID=" + creado.datos.id);
  }
}

main();
