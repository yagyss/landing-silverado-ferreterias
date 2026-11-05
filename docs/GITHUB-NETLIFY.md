# Publicar con GitHub + Netlify (deploy automático)

Con esto, cada `git push` reconstruye y publica el sitio solo. No hay que arrastrar
carpetas nunca más.

```
GitHub (repositorio)  →  Netlify (build)  →  sitio publicado
                                   └─ proxy /api/cotizacion → Google Apps Script
```

---

## 1. Crear el repositorio en GitHub

1. Entra a <https://github.com/new>.
2. Nombre sugerido: `landing-silverado-ferreterias`.
3. **Privado** (recomendado: contiene material del cliente).
4. No marques “Add README” (ya lo tenemos local).

## 2. Subir el proyecto (desde esta carpeta)

La carpeta ya está inicializada como repositorio Git con el primer commit hecho.
Solo falta conectar tu cuenta:

```bash
git remote add origin https://github.com/TU-USUARIO/landing-silverado-ferreterias.git
git branch -M main
git push -u origin main
```

Si te pide credenciales, GitHub ya no acepta contraseña: usa un **Personal Access Token**
(Settings → Developer settings → Tokens → Generate new token, permiso `repo`) o GitHub Desktop.

> Alternativa sin consola: en GitHub, “Add file → Upload files” y subir la carpeta completa
> (excluye `dist/`, `node_modules` y `data/prospectos.jsonl`, que están en `.gitignore`).

## 3. Conectar Netlify con el repositorio

1. Entra a <https://app.netlify.com> → **Add new site → Import an existing project**.
2. **GitHub** → autoriza → elige el repositorio.
3. Netlify detecta `netlify.toml` y queda así:
   - **Build command:** `node build.mjs`
   - **Publish directory:** `dist`
4. **Deploy site**. El primer build tarda ~1 minuto.

## 4. De aquí en adelante

- Cada `git push` a `main` → Netlify reconstruye y publica automáticamente.
- Cambios de contenido (`src/data/site.js`, textos, imágenes) → commit + push → listo.
- Si un deploy falla, Netlify muestra el log y conserva el último sitio publicado.

## 5. Actualizar la URL del formulario

El proxy vive en `netlify.toml` → `[[redirects]]`. Si cambias de implementación de
Apps Script, actualiza `to = "…/exec"`, haz commit y push.

Comprobar que quedó bien:

```bash
# desde tu computadora
curl -s https://TU-SITIO.netlify.app/api/cotizacion
```

Debe responder JSON del Apps Script (`{"ok":true,…}` o método no permitido), no un 404.

---

## Archivos que NO deben subirse (ya están en `.gitignore`)

| Ruta | Motivo |
| --- | --- |
| `dist/` | Netlify lo genera en cada build |
| `data/prospectos.jsonl` | Datos personales de prospectos |
| `assets/vehiculos/silverado/_originales/` | PNG pesados de trabajo |
| `demo-*.html`, `*-dom.html`, `qa-*.png` | Artefactos de revisión |

## Comandos útiles

```bash
git status                 # qué cambió
git add -A                 # preparar todo
git commit -m "texto"      # guardar
git push                   # publicar (Netlify reconstruye)
node build.mjs             # probar el build localmente
node server.mjs            # revisar en local con API real
```
