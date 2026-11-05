/** Prueba crear el sitio por la ruta de la cuenta (equipo). */

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
  } catch {}
  return { status: r.status, datos: d, texto: t };
};

async function main() {
  const cuentas = await api("/accounts");
  const cuenta = (Array.isArray(cuentas.datos) ? cuentas.datos : [])[0];
  if (!cuenta) {
    console.log("sin cuentas");
    return;
  }
  console.log("cuenta:", cuenta.slug, "| id:", cuenta.id);

  const intentos = [
    ["POST /accounts/{id}/sites", `/accounts/${cuenta.id}/sites`, { name: "silverado-ferreterias" }],
    ["POST /sites (sin nombre)", "/sites", {}],
  ];

  for (const [etiqueta, ruta, cuerpo] of intentos) {
    const r = await api(ruta, {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify(cuerpo),
    });
    console.log(`\n${etiqueta}: ${r.status}`);
    if (r.status < 400) {
      console.log("  sitio:", r.datos.ssl_url ?? r.datos.url);
      console.log("  SITE_ID=" + r.datos.id);
      return;
    }
    console.log("  detalle:", (r.texto ?? "").slice(0, 220));
  }

  console.log(
    "\nEl token puede leer pero no crear sitios.\n" +
      "Causa típica: token de solo lectura o sin rol de Owner/Developer en el equipo.",
  );
}

main();
