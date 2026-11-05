/**
 * Pruebas funcionales del endpoint de cotizaciones.
 * Requiere el servidor local corriendo (node server.mjs).
 *
 *   node scripts/probar-api.mjs
 */

import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const BASE = process.env.BASE ?? "http://127.0.0.1:4173";
const ARCHIVO = resolve(import.meta.dirname, "..", "data", "prospectos.jsonl");

let fallos = 0;
const ok = (condicion, etiqueta, extra = "") => {
  console.log(`  ${condicion ? "✓" : "✗"} ${etiqueta}${extra ? ` · ${extra}` : ""}`);
  if (!condicion) fallos += 1;
};

async function post(cuerpo) {
  const respuesta = await fetch(`${BASE}/api/cotizacion`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(cuerpo),
  });
  let datos = {};
  try {
    datos = await respuesta.json();
  } catch {
    datos = {};
  }
  return { status: respuesta.status, datos };
}

const base = {
  nombre: "María Fernanda López",
  whatsapp: "5512345678",
  correo: "maria@ferreteria.mx",
  ciudad: "Coyoacán",
  ferreteria: "Ferretería El Tornillo",
  sucursales: "2 sucursales",
  usoVehiculo: "No, todavía no",
  interes: "Financiamiento",
  privacidad: true,
  iniciadoEn: Date.now() - 60_000,
  pagina: "http://localhost/",
  referrer: "https://facebook.com/",
  origen: { utm_source: "facebook", utm_medium: "paid_social", utm_campaign: "silverado-ferreterias" },
};

console.log("\n== POST válido ==");
const creado = await post(base);
ok(creado.status === 201, "responde 201", `status=${creado.status}`);
ok(Boolean(creado.datos.folio), "devuelve folio", creado.datos.folio);
ok(creado.datos.ok === true, "ok=true");

console.log("\n== Duplicado (mismo WhatsApp) ==");
const duplicado = await post(base);
ok(duplicado.status === 200, "responde 200", `status=${duplicado.status}`);
ok(duplicado.datos.duplicado === true, "marca duplicado=true");

console.log("\n== Validación ==");
const invalido = await post({ ...base, nombre: "A", whatsapp: "123", ciudad: "Atlantis" });
ok(invalido.status === 422, "responde 422", `status=${invalido.status}`);
ok(Boolean(invalido.datos.errores?.nombre), "detecta nombre inválido");
ok(Boolean(invalido.datos.errores?.whatsapp), "detecta WhatsApp inválido");
ok(Boolean(invalido.datos.errores?.ciudad), "detecta ciudad fuera de catálogo");

console.log("\n== Anti-spam ==");
const trampa = await post({ ...base, whatsapp: "5599998888", honeypot: "soy-un-bot" });
ok(trampa.status === 422, "rechaza honeypot", `status=${trampa.status}`);
const rapido = await post({ ...base, whatsapp: "5599997777", iniciadoEn: Date.now() });
ok(rapido.status === 422 || rapido.status === 429, "rechaza envío instantáneo", `status=${rapido.status}`);

console.log("\n== Métodos ==");
const get = await fetch(`${BASE}/api/cotizacion`);
ok(get.status === 405, "GET devuelve 405", `status=${get.status}`);

console.log("\n== Persistencia ==");
const lineas = (await readFile(ARCHIVO, "utf8"))
  .split("\n")
  .filter(Boolean)
  .map((linea) => JSON.parse(linea));
const registro = lineas.find((linea) => linea.datos.whatsapp === "5512345678");
ok(Boolean(registro), "el prospecto quedó guardado");
ok(registro?.datos?.nombre === "María Fernanda López", "acentos intactos", registro?.datos?.nombre);
ok(registro?.origen?.utm_source === "facebook", "guarda UTM de campaña");
ok(registro?.campana?.length > 0, "asocia la campaña", registro?.campana);
ok(registro?.seguimiento?.eventoMeta === "Lead", "prepara evento Meta Lead");

console.log("\n== Estado ==");
const estado = await fetch(`${BASE}/api/estado`).then((r) => r.json());
ok(typeof estado.prospectosRegistrados === "number", "endpoint de estado disponible", `${estado.prospectosRegistrados} prospectos`);

console.log(fallos === 0 ? "\n  Todo OK\n" : `\n  ${fallos} fallo(s)\n`);
process.exitCode = fallos === 0 ? 0 : 1;
