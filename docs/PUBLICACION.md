# Publicación del sitio

## URL en vivo

**https://yagyss.github.io/landing-silverado-ferreterias/**

Se publica automáticamente con **GitHub Actions** (`.github/workflows/deploy.yml`):
cada `git push` a `main` compila el sitio (`node build.mjs`) y lo publica en GitHub Pages.

## Cómo actualizar contenido

1. Edita lo que necesites:
   - Textos y promoción → `src/data/site.js`
   - Secciones → `src/sections/*.html`
   - Estilos → `src/styles/*.css`
2. Prueba en local: `node server.mjs` → <http://127.0.0.1:4173>
3. Publica:
   ```bash
   git add -A
   git commit -m "descripción del cambio"
   git push
   ```
4. GitHub Actions reconstruye en ~1 minuto. Progreso en la pestaña **Actions** del repositorio.

## Consideraciones de GitHub Pages

- El sitio vive en una **subcarpeta** (`/landing-silverado-ferreterias/`), por eso el build
  usa **rutas relativas** (`RELATIVE_PATHS=1` en el workflow). Si publicas en Netlify o en
  un dominio raíz, se usa el build normal (sin esa variable).
- El repositorio es **público** porque el plan gratuito de GitHub no permite Pages en
  repositorios privados.

## Formulario

En GitHub Pages no existe el proxy de Netlify, así que la página envía **directo al
Apps Script** (la URL está en `src/data/site.js` → `endpointRemoto`). El Apps Script sí
devuelve `Access-Control-Allow-Origin: *`, por lo que el navegador **lee la respuesta** y
se muestra el folio.

Verificado:

| Prueba | Resultado |
| --- | --- |
| `GET` del sitio | 200 |
| Imágenes, CSS y JS | 200 desde la subcarpeta |
| `POST` al Apps Script con origen del sitio | 200 + `Access-Control-Allow-Origin: *` |
| Registro de prueba | folio `SV-20261104-PJ88` en la hoja |

## Riesgo por repositorio público

Al ser público, la URL del Apps Script queda visible y alguien podría enviar registros
falsos. Mitigaciones ya incluidas: validación, deduplicación por celular, campo trampa y
tiempo mínimo. Si aparece spam:

1. Cambia de implementación en Apps Script (URL nueva) y actualiza
   `netlify.toml` + `src/data/site.js`.
2. O vuelve a repositorio privado y publica en Netlify (necesita token con permisos de
   escritura).

## Dominio propio (opcional)

En GitHub: **Settings → Pages → Custom domain**. Agrega el dominio, crea el registro
`CNAME` en tu proveedor y activa *Enforce HTTPS*.
