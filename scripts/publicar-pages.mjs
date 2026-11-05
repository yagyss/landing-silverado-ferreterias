/**
 * Activa GitHub Pages y revisa el estado del workflow de publicación.
 */

const TOKEN = process.env.GH_TOKEN;
const DUEÑO = "yagyss";
const REPO = "landing-silverado-ferreterias";

const cabeceras = {
  Authorization: `Bearer ${TOKEN}`,
  Accept: "application/vnd.github+json",
  "User-Agent": "dsh-landing",
  "X-GitHub-Api-Version": "2022-11-28",
};

const api = async (ruta, opciones = {}) => {
  const respuesta = await fetch(`https://api.github.com/repos/${DUEÑO}/${REPO}${ruta}`, {
    headers: cabeceras,
    ...opciones,
  });
  const texto = await respuesta.text();
  let datos = null;
  try {
    datos = texto ? JSON.parse(texto) : null;
  } catch {
    datos = null;
  }
  return { status: respuesta.status, datos };
};

const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  // 1. Estado actual de Pages
  const actual = await api("/pages");
  console.log("Pages (antes):", actual.status, actual.datos?.message ?? actual.datos?.html_url ?? "");

  if (actual.status === 404) {
    const creado = await api("/pages", {
      method: "POST",
      body: JSON.stringify({ build_type: "workflow" }),
    });
    console.log("Activar Pages:", creado.status, creado.datos?.message ?? creado.datos?.html_url ?? "");
  }

  // 2. Workflows disponibles
  const workflows = await api("/actions/workflows");
  const lista = workflows.datos?.workflows ?? [];
  for (const wf of lista) {
    console.log("  workflow:", wf.name, "| id:", wf.id, "| estado:", wf.state);
  }

  // 3. Disparar el workflow manualmente (por si el push no lo lanzó)
  const objetivo = lista.find((w) => String(w.path).includes("deploy.yml"));
  if (objetivo) {
    const disparo = await api(`/actions/workflows/${objetivo.id}/dispatches`, {
      method: "POST",
      body: JSON.stringify({ ref: "main" }),
    });
    console.log("Disparo manual:", disparo.status);
  }

  // 4. Esperar el resultado
  let url = "";
  for (let intento = 1; intento <= 24; intento++) {
    await esperar(10_000);
    const runs = await api("/actions/runs?per_page=1");
    const run = runs.datos?.workflow_runs?.[0];
    if (!run) {
      console.log("sin ejecuciones todavía…");
      continue;
    }
    console.log(`  intento ${intento}: ${run.status} / ${run.conclusion ?? "en curso"}`);
    if (run.status === "completed") {
      console.log("  resultado:", run.conclusion, "|", run.html_url);
      const pages = await api("/pages");
      url = pages.datos?.html_url ?? "";
      if (!url) url = `https://${DUEÑO}.github.io/${REPO}/`;
      break;
    }
  }

  console.log("\nURL publicada:", url || "(aún no disponible)");
}

main();
