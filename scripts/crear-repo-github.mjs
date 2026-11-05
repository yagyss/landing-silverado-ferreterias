/**
 * Crea (si no existe) el repositorio en GitHub y devuelve la URL de clonado.
 * El token se lee de la variable de entorno GH_TOKEN; nunca se imprime.
 */

const TOKEN = process.env.GH_TOKEN;
if (!TOKEN) {
  console.error("Falta GH_TOKEN en el entorno.");
  process.exit(1);
}

const NOMBRE = "landing-silverado-ferreterias";
const DESCRIPCION = "Landing de Chevrolet Silverado para ferreterías de CDMX";

const cabeceras = {
  Authorization: `Bearer ${TOKEN}`,
  Accept: "application/vnd.github+json",
  "User-Agent": "dsh-landing",
  "X-GitHub-Api-Version": "2022-11-28",
};

async function api(ruta, opciones = {}) {
  const respuesta = await fetch(`https://api.github.com${ruta}`, { headers: cabeceras, ...opciones });
  const texto = await respuesta.text();
  let datos = null;
  try {
    datos = texto ? JSON.parse(texto) : null;
  } catch {
    datos = null;
  }
  return { status: respuesta.status, datos, texto };
}

async function main() {
  const yo = await api("/user");
  if (yo.status !== 200) {
    console.error("Token inválido o sin permisos:", yo.status, (yo.datos?.message ?? "").slice(0, 160));
    process.exit(1);
  }
  const usuario = yo.datos.login;
  console.log("  usuario:", usuario);
  console.log("  plan:", yo.datos.plan?.name ?? "—");

  const existente = await api(`/repos/${usuario}/${NOMBRE}`);
  if (existente.status === 200) {
    console.log("  el repositorio ya existía:", existente.datos.html_url);
  } else {
    const creado = await api("/user/repos", {
      method: "POST",
      body: JSON.stringify({
        name: NOMBRE,
        description: DESCRIPCION,
        private: true,
        has_issues: true,
        has_wiki: false,
        auto_init: false,
      }),
    });
    if (creado.status === 201) {
      console.log("  repositorio creado:", creado.datos.html_url);
    } else {
      console.error("  no se pudo crear:", creado.status, (creado.datos?.message ?? "").slice(0, 200));
      process.exit(1);
    }
  }

  console.log("  remoto:", `https://github.com/${usuario}/${NOMBRE}.git`);
}

main();
