/** Simula exactamente lo que hace el navegador: preflight y POST simple. */

const URL =
  "https://script.google.com/macros/s/AKfycbyo3rlLi4VGjD7-Kz-OsWSViRAPOasfpyCG6DornXqCwzOT_aXb1W-WtlM7znlLCAI-/exec";
const ORIGEN = "https://yagyss.github.io";

const cuerpo = {
  nombre: "Prueba navegador",
  whatsapp: "55" + String(Date.now()).slice(-8),
  correo: "prueba@ejemplo.com",
  plan: "Contado",
  mensaje: "Simulación de envío desde el navegador.",
  privacidad: true,
  origen: { utm_source: "simulacion-browser" },
};

const main = async () => {
  // 1. Preflight CORS (lo que hace Chrome antes del POST con JSON)
  console.log("OPTIONS (preflight)…");
  try {
    const opt = await fetch(URL, {
      method: "OPTIONS",
      headers: {
        Origin: ORIGEN,
        "Access-Control-Request-Method": "POST",
        "Access-Control-Request-Headers": "content-type",
      },
    });
    console.log("  status:", opt.status);
    console.log("  allow-origin:", opt.headers.get("access-control-allow-origin") ?? "(ninguno)");
    console.log("  allow-methods:", opt.headers.get("access-control-allow-methods") ?? "(ninguno)");
  } catch (e) {
    console.log("  falló:", e.message);
  }

  // 2. POST con content-type application/json (modo cors)
  console.log("\nPOST application/json (modo cors)…");
  try {
    const r = await fetch(URL, {
      method: "POST",
      headers: { Origin: ORIGEN, "content-type": "application/json" },
      body: JSON.stringify(cuerpo),
    });
    const t = await r.text();
    console.log("  status:", r.status, "| allow-origin:", r.headers.get("access-control-allow-origin") ?? "(ninguno)");
    console.log("  respuesta:", t.slice(0, 220));
  } catch (e) {
    console.log("  falló:", e.message);
  }

  // 3. POST con content-type text/plain (modo no-cors)
  console.log("\nPOST text/plain (modo no-cors)…");
  try {
    const r = await fetch(URL, {
      method: "POST",
      headers: { Origin: ORIGEN, "content-type": "text/plain;charset=utf-8" },
      body: JSON.stringify({ ...cuerpo, whatsapp: "55" + String(Date.now()).slice(-8) }),
    });
    const t = await r.text();
    console.log("  status:", r.status);
    console.log("  respuesta:", t.slice(0, 220));
  } catch (e) {
    console.log("  falló:", e.message);
  }
};

main();
