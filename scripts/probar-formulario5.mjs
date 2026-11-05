/**
 * Prueba del formulario simplificado (nombre, celular, correo, plan, mensaje).
 * Requiere `node server.mjs` corriendo.
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

const post = async (cuerpo) => {
  const r = await fetch(`${BASE}/api/cotizacion`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify(cuerpo),
  });
  let datos = {};
  try {
    datos = await r.json();
  } catch {
    datos = {};
  }
  return { status: r.status, datos };
};

const base = {
  nombre: "Laura Méndez Ruiz",
  whatsapp: "5588776655",
  correo: "laura@ferreteria.mx",
  plan: "Financiamiento",
  mensaje: "Necesito mover material entre dos sucursales y saber si incluye enganche.",
  privacidad: true,
  iniciadoEn: Date.now() - 60_000,
};

console.log("\n== Alta con los 5 campos ==");
const alta = await post(base);
ok(alta.status === 201, "responde 201", `status=${alta.status}`);
ok(Boolean(alta.datos.folio), "devuelve folio", alta.datos.folio);

console.log("\n== Sin plan ni correo ==");
const incompleto = await post({ ...base, whatsapp: "5599001122", plan: "", correo: "" });
ok(incompleto.status === 422, "responde 422", `status=${incompleto.status}`);
ok(Boolean(incompleto.datos.errores?.plan), "exige plan");
ok(Boolean(incompleto.datos.errores?.correo), "exige correo");

console.log("\n== Correo inválido ==");
const correoMalo = await post({ ...base, whatsapp: "5599001133", correo: "laura@" });
ok(correoMalo.status === 422, "responde 422");
ok(Boolean(correoMalo.datos.errores?.correo), "detecta correo inválido");

console.log("\n== Persistencia de plan y mensaje ==");
const lineas = (await readFile(ARCHIVO, "utf8")).split("\n").filter(Boolean).map((l) => JSON.parse(l));
const registro = lineas.find((l) => l.datos?.whatsapp === "5588776655");
ok(Boolean(registro), "el prospecto está guardado");
ok(registro?.datos?.plan === "Financiamiento", "guarda el plan", registro?.datos?.plan);
ok(Boolean(registro?.datos?.mensaje), "guarda el mensaje");
ok(registro?.datos?.correo === "laura@ferreteria.mx", "guarda el correo");

console.log(fallos === 0 ? "\n  Todo OK\n" : `\n  ${fallos} fallo(s)\n`);
process.exitCode = fallos === 0 ? 0 : 1;
