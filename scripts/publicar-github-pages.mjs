/**
 * Hace público el repositorio, activa GitHub Pages y espera la publicación.
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
  const r = await fetch(`https://api.github.com${ruta}`, { headers: cabeceras, ...opciones });
  const t = await r.text();
  let d = null;
  try {
    d = t ? JSON.parse(t) : null;
  } catch {}
  return { status: r.status, datos: d, texto: t };
};

const esperar = (ms) => new Promise((r) => setTimeout(r, ms));

async function main() {
  /* 1. Repositorio público */
  const publico = await api(`/repos/${DUEÑO}/${REPO}`, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ private: false }),
  });
  console.log("Repositorio público:", publico.status, publico.datos?.private === false ? "OK" : (publico.datos?.message ?? ""));

  /* 2. Activar Pages */
  const pages = await api(`/repos/${DUEÑO}/${REPO}/pages`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ build_type: "workflow" }),
  });
  console.log("Pages:", pages.status, pages.datos?.html_url ?? pages.datos?.message ?? "");

  /* 3. Disparar workflow */
  const workflows = await api(`/repos/${DUEÑO}/${REPO}/actions/workflows`);
  const wf = (workflows.datos?.workflows ?? []).find((w) => String(w.path).includes("deploy.yml"));
  if (!wf) {
    console.log("No encontré el workflow de deploy.");
    return;
  }
  const disparo = await api(`/repos/${DUEÑO}/${REPO}/actions/workflows/${wf.id}/dispatches`, {
    method: "POST",
    headers: { "content-type": "application/json" },
    body: JSON.stringify({ ref: "main" }),
  });
  console.log("Workflow disparado:", disparo.status);

  /* 4. Esperar la ejecución */
  let exito = false;
  for (let i = 1; i <= 30; i++) {
    await esperar(10_000);
    const runs = await api(`/repos/${DUEÑO}/${REPO}/actions/runs?per_page=1`);
    const run = runs.datos?.workflow_runs?.[0];
    if (!run) {
      console.log("  sin ejecuciones…");
      continue;
    }
    console.log(`  ${i * 10}s → ${run.status} / ${run.conclusion ?? "en curso"}`);
    if (run.status === "completed") {
      exito = run.conclusion === "success";
      console.log("  ejecución:", run.conclusion, run.html_url);
      break;
    }
  }

  /* 5. URL */
  const info = await api(`/repos/${DUEÑO}/${REPO}/pages`);
  const url = info.datos?.html_url ?? `https://${DUEÑO}.github.io/${REPO}/`;
  console.log("\nURL:", url);
  console.log("Resultado:", exito ? "publicado" : "revisar acciones");

  if (exito) {
    await esperar(20_000);
    try {
      const pagina = await fetch(url, { redirect: "follow" });
      const html = await pagina.text();
      console.log("Verificación:", pagina.status, "| bytes:", html.length);
      console.log("  tiene el hero:", html.includes("hero--cine") || html.includes("Silverado"));
      console.log("  usa rutas relativas:", !/(?:src|href)="\/assets/.test(html));
    } catch (e) {
      console.log("Verificación falló:", e.message);
    }
  }
}

main();
