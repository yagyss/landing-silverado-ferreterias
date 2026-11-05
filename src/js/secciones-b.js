/**
 * ============================================================================
 *  SECCIÓN B · Hidratación de contenido e interacciones
 * ============================================================================
 *  Secciones: transformación, oferta, comparativa, testimonios, FAQ y cierre.
 *
 *  · Todos los textos comerciales se leen de SITE (src/data/site.js).
 *  · Se exporta `initSeccionesB()`, que main.js invoca con el DOM listo.
 *    La función es idempotente y tolerante a que falte alguna sección.
 *  · El marcado se construye con textContent (sin inyectar datos como HTML);
 *    sólo los iconos SVG son cadenas estáticas controladas por este módulo.
 *  · Respeta `prefers-reduced-motion` en carrusel y apariciones.
 * ============================================================================
 */

import { SITE } from "../data/site.js";
import { $, $$, sinMovimiento } from "./dom.js";

/* ------------------------------------------------------------------ Iconos */
const SVG = {
  check:
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><path d="M5 12.5l4.2 4.3L19 6.8" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  linea:
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><path d="M6 12h12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
  candado:
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><rect x="5" y="10" width="14" height="10" rx="2" stroke="currentColor" stroke-width="1.5"/><path d="M8.5 10V7.5a3.5 3.5 0 0 1 7 0V10" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/></svg>',
  sello:
    '<svg viewBox="0 0 24 24" fill="none" aria-hidden="true" focusable="false"><path d="M12 2.8l7.5 3v6.1c0 4.4-3.1 8.2-7.5 9.3-4.4-1.1-7.5-4.9-7.5-9.3V5.8l7.5-3z" stroke="currentColor" stroke-width="1.5" stroke-linejoin="round"/><path d="M8.6 12.1l2.4 2.4 4.4-4.6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/></svg>',
};

/** Avatar genérico: indica "espacio reservado", nunca simula una persona real. */
function monograma() {
  return `<svg class="testimonios__monograma" viewBox="0 0 48 48" fill="none" aria-hidden="true" focusable="false">
    <circle cx="24" cy="24" r="22" stroke="currentColor" stroke-width="1.1" opacity=".35"/>
    <circle cx="24" cy="19" r="6.2" stroke="currentColor" stroke-width="1.5" opacity=".8"/>
    <path d="M12.5 37.5c1.6-6.4 6-9.6 11.5-9.6s9.9 3.2 11.5 9.6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" opacity=".8"/>
  </svg>`;
}

/* ------------------------------------------------------------- Utilidades */
function crear(etiqueta, atributos = {}, hijos = []) {
  const nodo = document.createElement(etiqueta);

  Object.entries(atributos).forEach(([clave, valor]) => {
    if (valor === null || valor === undefined || valor === false) return;
    if (clave === "class") nodo.className = valor;
    else if (clave === "text") nodo.textContent = valor;
    else if (clave === "html") nodo.innerHTML = valor;
    else nodo.setAttribute(clave, valor === true ? "" : String(valor));
  });

  (Array.isArray(hijos) ? hijos : [hijos]).forEach((hijo) => {
    if (hijo === null || hijo === undefined || hijo === false) return;
    nodo.append(hijo instanceof Node ? hijo : document.createTextNode(String(hijo)));
  });

  return nodo;
}

/** Escribe texto plano y oculta el nodo si el dato está vacío (sin inventar). */
function pintarTexto(nodo, valor) {
  if (!nodo) return;
  const texto = String(valor ?? "").trim();
  if (texto) {
    nodo.textContent = texto;
    nodo.hidden = false;
  } else {
    nodo.textContent = "";
    nodo.hidden = true;
  }
}

function ejecutarSeguro(nombre, tarea) {
  try {
    tarea();
  } catch (error) {
    console.warn(`[secciones-b] No se pudo iniciar «${nombre}»:`, error);
  }
}

/* ==================================================== 06 · TRANSFORMACIÓN */
function hidratarTransformacion() {
  const raiz = document.getElementById("transformacion");
  if (!raiz) return;

  const datos = SITE.transformacion ?? {};
  pintarListaTransformacion(raiz, "[data-transformacion-antes]", datos.antes, "antes");
  pintarListaTransformacion(raiz, "[data-transformacion-despues]", datos.despues, "despues");
  pintarTexto($("[data-transformacion-nota]", raiz), datos.nota);
}

function pintarListaTransformacion(raiz, selector, textos, tipo) {
  const contenedor = $(selector, raiz);
  if (!contenedor) return;

  if (!Array.isArray(textos) || !textos.length) {
    contenedor.hidden = true;
    return;
  }

  const marca = tipo === "despues" ? SVG.check : SVG.linea;

  contenedor.replaceChildren(
    ...textos.map((texto) =>
      crear("li", { class: `transform__item transform__item--${tipo}` }, [
        crear("span", { class: "transform__marca", "aria-hidden": "true", html: marca }),
        crear("span", { class: "transform__texto", text: String(texto) }),
      ])
    )
  );
}

/* ========================================================== 07 · OFERTA */
function hidratarOferta() {
  const raiz = document.getElementById("oferta");
  if (!raiz) return;

  const datos = SITE.oferta;
  if (!datos || datos.activa === false) {
    raiz.hidden = true;
    return;
  }

  const titulo = $("[data-oferta-titulo]", raiz);
  if (titulo && datos.titulo) titulo.textContent = datos.titulo;

  pintarTexto($("[data-oferta-subtitulo]", raiz), datos.subtitulo);

  const vigencia = $("[data-oferta-vigencia]", raiz);
  if (vigencia) {
    const texto = String(datos.vigencia ?? "").trim();
    if (texto) {
      vigencia.textContent = texto;
      vigencia.hidden = false;
    } else {
      /* Sin fecha definida no se muestra nada: nunca se inventa una vigencia. */
      vigencia.textContent = "";
      vigencia.hidden = true;
    }
  }

  const contenedor = $("[data-oferta-beneficios]", raiz);
  const beneficios = Array.isArray(datos.beneficios) ? datos.beneficios : [];
  if (contenedor) {
    if (!beneficios.length) {
      contenedor.hidden = true;
    } else {
      contenedor.replaceChildren(
        ...beneficios.map((beneficio, indice) => crearTarjetaBeneficio(beneficio, indice))
      );
    }
  }

  const etiquetaCta = $("[data-oferta-cta-label]", raiz);
  if (etiquetaCta && datos.cta) etiquetaCta.textContent = datos.cta;

  pintarTexto($("[data-oferta-nota-corta]", raiz), datos.notaCorta);
  pintarTexto($("[data-oferta-nota-legal]", raiz), datos.notaLegal);
}

function crearTarjetaBeneficio(beneficio, indice) {
  const piezas = [];

  if (beneficio?.etiqueta) {
    piezas.push(crear("p", { class: "oferta__etiqueta", text: String(beneficio.etiqueta) }));
  }
  if (beneficio?.titulo) {
    piezas.push(crear("p", { class: "oferta__titulo", text: String(beneficio.titulo) }));
  }
  if (beneficio?.detalle) {
    piezas.push(crear("p", { class: "oferta__detalle", text: String(beneficio.detalle) }));
  }

  return crear("article", { class: "oferta__card" }, [
    crear("span", {
      class: "oferta__numero",
      "aria-hidden": "true",
      text: String(indice + 1).padStart(2, "0"),
    }),
    ...piezas,
  ]);
}

/* ======================================================= 08 · COMPARATIVA */
const NIVELES = {
  alto: { etiqueta: "Nivel alto", barras: 3 },
  medio: { etiqueta: "Nivel medio", barras: 2 },
  bajo: { etiqueta: "Nivel bajo", barras: 1 },
};

function hidratarComparativa() {
  const raiz = document.getElementById("comparativa");
  if (!raiz) return;

  const datos = SITE.comparativa;
  const contenedor = $("[data-comparativa]", raiz);
  const columnas = Array.isArray(datos?.columnas) ? datos.columnas : [];
  const filas = Array.isArray(datos?.filas) ? datos.filas : [];

  if (contenedor) {
    if (!columnas.length || !filas.length) {
      contenedor.hidden = true;
    } else {
      contenedor.replaceChildren(construirTabla(columnas, filas));
    }
  }

  pintarTexto($("[data-comparativa-nota]", raiz), datos?.nota);
}

function construirTabla(columnas, filas) {
  const tabla = crear("table", { class: "comparativa__tabla" });
  tabla.append(
    crear("caption", {
      class: "sr-only",
      text: "Comparación cualitativa entre la Chevrolet Silverado y otros vehículos para el trabajo diario de una ferretería.",
    })
  );

  /* ---------------------------------------------------------------- Cabeza */
  const cabeza = crear("thead", { class: "comparativa__cabeza" });
  const filaCabeza = crear("tr", { class: "comparativa__fila comparativa__fila--cabeza" });
  filaCabeza.append(
    crear("th", { scope: "col", class: "comparativa__esquina" }, [
      crear("span", { class: "sr-only", text: "Criterio" }),
    ])
  );

  columnas.forEach((columna) => {
    const celda = crear("th", {
      scope: "col",
      class: `comparativa__columna${columna.destacada ? " comparativa__columna--destacada" : ""}`,
    });
    celda.append(crear("span", { class: "comparativa__vehiculo", text: String(columna.nombre ?? "") }));
    if (columna.destacada) {
      celda.append(crear("span", { class: "comparativa__insignia", text: "TU HERRAMIENTA DE TRABAJO" }));
    }
    filaCabeza.append(celda);
  });
  cabeza.append(filaCabeza);

  /* ----------------------------------------------------------------- Cuerpo */
  const cuerpo = crear("tbody");
  filas.forEach((fila) => {
    const tr = crear("tr", { class: "comparativa__fila" });
    tr.append(crear("th", { scope: "row", class: "comparativa__criterio", text: String(fila.criterio ?? "") }));

    columnas.forEach((columna, indice) => {
      const celda = crear("td", {
        class: `comparativa__celda${columna.destacada ? " comparativa__celda--destacada" : ""}`,
        "data-label": String(columna.nombre ?? ""),
      });
      celda.append(crear("p", { class: "comparativa__valor", text: String(fila.valores?.[indice] ?? "") }));
      celda.append(crearNivel(fila.evaluacion?.[indice]));
      tr.append(celda);
    });

    cuerpo.append(tr);
  });

  tabla.append(cabeza, cuerpo);
  return tabla;
}

function crearNivel(nivel) {
  const definicion = NIVELES[nivel];
  if (!definicion) return crear("span", { class: "comparativa__nivel", hidden: true });

  const barras = crear("span", { class: "comparativa__barras", "aria-hidden": "true" });
  for (let indice = 0; indice < 3; indice += 1) {
    const llena = indice < definicion.barras;
    barras.append(crear("span", { class: `comparativa__barra${llena ? " comparativa__barra--llena" : ""}` }));
  }

  return crear("span", { class: "comparativa__nivel", "data-nivel": nivel }, [
    barras,
    crear("span", { class: "comparativa__nivel-texto", text: definicion.etiqueta }),
  ]);
}

/* ======================================================= 09 · TESTIMONIOS */
function hidratarTestimonios() {
  const raiz = document.getElementById("testimonios");
  if (!raiz) return;

  const datos = SITE.testimonios ?? {};
  pintarTexto($("[data-testimonios-titulo]", raiz), datos.titulo);

  const pista = $("[data-testimonios-pista]", raiz);
  if (!pista) return;

  const publicados =
    datos.estado === "publicado" && Array.isArray(datos.items)
      ? datos.items.filter((item) => item && item.autorizado === true && item.comentario)
      : [];
  const ejemplos =
    datos.estado === "borrador" && Array.isArray(datos.items)
      ? datos.items.filter((item) => item && item.comentario)
      : [];
  const hayReales = publicados.length > 0;
  const hayEjemplos = !hayReales && ejemplos.length > 0;
  const total = hayReales ? publicados.length : hayEjemplos ? ejemplos.length : 3;

  const tarjetas = hayReales
    ? publicados.map((item, indice) => crearTestimonioReal(item, indice, total))
    : hayEjemplos
      ? ejemplos.map((item, indice) => crearTestimonioEjemplo(item, indice, total))
      : Array.from({ length: 3 }, (_, indice) => crearTestimonioPendiente(indice, 3));

  pista.replaceChildren(...tarjetas.map((tarjeta) => crear("li", { class: "testimonios__slide" }, [tarjeta])));

  const puntos = $("[data-testimonios-puntos]", raiz);
  if (puntos) {
    if (total <= 1) {
      puntos.hidden = true;
      puntos.replaceChildren();
    } else {
      puntos.hidden = false;
      puntos.replaceChildren(
        ...Array.from({ length: total }, (_, indice) =>
          crear("button", {
            type: "button",
            class: "testimonios__punto",
            "aria-label": `Ver testimonio ${indice + 1} de ${total}`,
            "aria-current": indice === 0 ? "true" : "false",
          })
        )
      );
    }
  }

  const nota = $("[data-testimonios-nota]", raiz);
  if (nota) {
    if (hayReales) pintarTexto(nota, "");
    else if (hayEjemplos) pintarTexto(nota, datos.notaEjemplos);
    else pintarTexto(nota, datos.notaPendiente);
  }

  const contenedorResenas = $("[data-testimonios-resenas]", raiz);
  if (contenedorResenas) {
    const bloque = construirResenasVerificadas(datos.resenasVerificadas);
    if (bloque) contenedorResenas.replaceChildren(bloque);
  }

  configurarCarrusel({
    viewport: $("[data-testimonios-viewport]", raiz),
    slides: $$(".testimonios__slide", pista),
    botonPrev: $("[data-testimonios-prev]", raiz),
    botonNext: $("[data-testimonios-next]", raiz),
    puntos: $$(".testimonios__punto", raiz),
    estado: $("[data-testimonios-estado]", raiz),
  });
}

function crearTestimonioPendiente(indice, total) {
  return crear(
    "article",
    {
      class: "testimonios__tarjeta testimonios__tarjeta--pendiente",
      role: "group",
      "aria-roledescription": "diapositiva",
      "aria-label": `Espacio para testimonio ${indice + 1} de ${total}, pendiente de autorización`,
    },
    [
      crear("div", { class: "testimonios__avatar", "aria-hidden": "true", html: monograma(indice) }),
      crear("p", { class: "testimonios__estado-pendiente" }, [
        crear("span", { class: "testimonios__estado-icono", "aria-hidden": "true", html: SVG.candado }),
        crear("span", { text: "Contenido pendiente de autorización" }),
      ]),
      crear("p", {
        class: "testimonios__placeholder",
        text: "Aquí se publicará el testimonio de un empresario ferretero.",
      }),
      crear("div", { class: "testimonios__esqueleto", "aria-hidden": "true" }, [
        crear("span"),
        crear("span"),
        crear("span"),
      ]),
    ]
  );
}

/**
 * Testimonio de muestra: misma estructura que el real, con una etiqueta visible
 * de "ejemplo" para que nunca se confunda con una recomendación auténtica.
 */
function crearTestimonioEjemplo(item, indice, total) {
  const rol = String(item.rol ?? "").trim();
  const zona = String(item.zona ?? "").trim();
  const sucursales = String(item.sucursales ?? "").trim();

  const datosAutor = [];
  if (rol) datosAutor.push(crear("cite", { class: "testimonios__nombre", text: rol }));
  const meta = [zona, sucursales].filter(Boolean).map(String).join(" · ");
  if (meta) datosAutor.push(crear("span", { class: "testimonios__meta", text: meta }));

  return crear(
    "article",
    {
      class: "testimonios__tarjeta testimonios__tarjeta--ejemplo",
      role: "group",
      "aria-roledescription": "diapositiva",
      "aria-label": `Testimonio de ejemplo ${indice + 1} de ${total}, pendiente de sustituir por uno autorizado`,
    },
    [
      crear("span", { class: "testimonios__chip", text: "Ejemplo editable" }),
      crear("blockquote", { class: "testimonios__cita" }, [
        crear("span", { class: "testimonios__comilla", "aria-hidden": "true", text: "\u201C" }),
        crear("p", { text: String(item.comentario) }),
      ]),
      crear("footer", { class: "testimonios__autor" }, [
        crear("div", { class: "testimonios__avatar", "aria-hidden": "true", html: monograma() }),
        crear("div", { class: "testimonios__autor-datos" }, datosAutor),
      ]),
    ]
  );
}

function crearTestimonioReal(item, indice, total) {
  const nombre = String(item.nombre ?? "").trim();
  const iniciales = nombre
    ? nombre
        .split(/\s+/)
        .slice(0, 2)
        .map((parte) => parte.charAt(0).toUpperCase())
        .join("")
    : "—";

  const avatar = item.foto
    ? crear("div", { class: "testimonios__avatar testimonios__avatar--foto" }, [
        crear("img", {
          src: String(item.foto),
          alt: nombre ? `Retrato de ${nombre}` : "",
          loading: "lazy",
          decoding: "async",
        }),
      ])
    : crear("div", { class: "testimonios__avatar", "aria-hidden": "true", text: iniciales });

  const datosAutor = [];
  if (nombre) datosAutor.push(crear("cite", { class: "testimonios__nombre", text: nombre }));
  const meta = [item.negocio, item.sucursales].filter(Boolean).map(String).join(" · ");
  if (meta) datosAutor.push(crear("span", { class: "testimonios__meta", text: meta }));

  return crear(
    "article",
    {
      class: "testimonios__tarjeta",
      role: "group",
      "aria-roledescription": "diapositiva",
      "aria-label": `Testimonio ${indice + 1} de ${total}`,
    },
    [
      crear("blockquote", { class: "testimonios__cita" }, [
        crear("span", { class: "testimonios__comilla", "aria-hidden": "true", text: "\u201C" }),
        crear("p", { text: String(item.comentario) }),
      ]),
      crear("footer", { class: "testimonios__autor" }, [
        avatar,
        crear("div", { class: "testimonios__autor-datos" }, datosAutor),
      ]),
    ]
  );
}

function construirResenasVerificadas(datos) {
  if (!datos) return null;

  const cuerpo = crear("div", { class: "testimonios__resenas-cuerpo" });
  cuerpo.append(
    crear("h3", {
      class: "testimonios__resenas-titulo",
      text: String(datos.titulo || "Reseñas verificadas del distribuidor"),
    })
  );

  if (datos.estado === "pendiente") {
    cuerpo.append(crear("p", { class: "tag testimonios__resenas-tag", text: "Pendiente de integración" }));
  }
  if (datos.nota) cuerpo.append(crear("p", { class: "testimonios__resenas-nota", text: String(datos.nota) }));
  if (datos.fuente) cuerpo.append(crear("p", { class: "disclaimer", text: `Fuente: ${datos.fuente}` }));

  return crear("div", { class: "testimonios__resenas-card" }, [
    crear("span", { class: "testimonios__resenas-icono", "aria-hidden": "true", html: SVG.sello }),
    cuerpo,
  ]);
}

function configurarCarrusel({ viewport, slides, botonPrev, botonNext, puntos, estado }) {
  if (!viewport || !slides?.length) return;

  const total = slides.length;
  const alFinal = () => Math.max(0, viewport.scrollWidth - viewport.clientWidth);
  const indiceActual = () => {
    const posicion = viewport.scrollLeft;
    let indice = 0;
    let distancia = Infinity;
    slides.forEach((slide, i) => {
      const diferencia = Math.abs(slide.offsetLeft - posicion);
      if (diferencia < distancia) {
        distancia = diferencia;
        indice = i;
      }
    });
    return indice;
  };

  const ir = (indice, suave = true) => {
    const destino = slides[Math.max(0, Math.min(indice, total - 1))];
    if (!destino) return;
    const izquierda = Math.min(Math.max(0, destino.offsetLeft), alFinal());
    const comportamiento = suave && !sinMovimiento() ? "smooth" : "auto";
    if (typeof viewport.scrollTo === "function") {
      viewport.scrollTo({ left: izquierda, behavior: comportamiento });
    } else {
      viewport.scrollLeft = izquierda;
    }
  };

  let pendiente = false;
  const actualizar = () => {
    pendiente = false;
    const indice = indiceActual();
    const maximo = alFinal();

    puntos.forEach((boton, i) => boton.setAttribute("aria-current", i === indice ? "true" : "false"));
    if (botonPrev) botonPrev.disabled = viewport.scrollLeft <= 1;
    if (botonNext) botonNext.disabled = viewport.scrollLeft >= maximo - 1;
    if (estado) estado.textContent = `Testimonio ${indice + 1} de ${total}`;
  };

  const alScroll = () => {
    if (pendiente) return;
    pendiente = true;
    window.requestAnimationFrame(actualizar);
  };

  viewport.addEventListener("scroll", alScroll, { passive: true });
  window.addEventListener("resize", alScroll);

  botonPrev?.addEventListener("click", () => ir(indiceActual() - 1));
  botonNext?.addEventListener("click", () => ir(indiceActual() + 1));
  puntos.forEach((boton, indice) => boton.addEventListener("click", () => ir(indice)));

  /* Teclado: flechas, Inicio y Fin cuando el carrusel tiene el foco. */
  viewport.addEventListener("keydown", (evento) => {
    let destino = null;
    if (evento.key === "ArrowLeft") destino = indiceActual() - 1;
    else if (evento.key === "ArrowRight") destino = indiceActual() + 1;
    else if (evento.key === "Home") destino = 0;
    else if (evento.key === "End") destino = total - 1;
    if (destino === null) return;
    evento.preventDefault();
    ir(destino);
  });

  /* Arrastre con ratón (en táctil ya funciona el desplazamiento nativo). */
  let arrastre = null;
  viewport.addEventListener("pointerdown", (evento) => {
    if (evento.pointerType !== "mouse" || evento.button !== 0) return;
    arrastre = { x: evento.clientX, scroll: viewport.scrollLeft, movido: false };
    viewport.classList.add("is-arrastrando");
    if (typeof viewport.setPointerCapture === "function") {
      try {
        viewport.setPointerCapture(evento.pointerId);
      } catch {
        /* Algunos navegadores no permiten capturar; el arrastre sigue funcionando. */
      }
    }
  });

  viewport.addEventListener("pointermove", (evento) => {
    if (!arrastre) return;
    const delta = evento.clientX - arrastre.x;
    if (Math.abs(delta) > 4) arrastre.movido = true;
    viewport.scrollLeft = arrastre.scroll - delta;
  });

  const soltar = () => {
    if (!arrastre) return;
    const { movido } = arrastre;
    arrastre = null;
    viewport.classList.remove("is-arrastrando");
    if (movido) ir(indiceActual());
    actualizar();
  };

  viewport.addEventListener("pointerup", soltar);
  viewport.addEventListener("pointercancel", soltar);

  actualizar();
}

/* ============================================================= 10 · FAQ */
function hidratarFaq() {
  const raiz = document.getElementById("preguntas");
  if (!raiz) return;

  const datos = SITE.faq ?? {};
  pintarTexto($("[data-faq-titulo]", raiz), datos.titulo);

  const lista = $("[data-faq]", raiz);
  const items = Array.isArray(datos.items) ? datos.items.filter((item) => item && item.p) : [];

  if (lista) {
    if (!items.length) {
      lista.hidden = true;
    } else {
      lista.replaceChildren(...items.map((item, indice) => crearItemFaq(item, indice, indice === 0)));
      activarTecladoFaq(lista);
    }
  }

  pintarTexto($("[data-faq-nota]", raiz), datos.nota);
}

function crearItemFaq(item, indice, abiertoPorDefecto) {
  const idBoton = `faq-boton-${indice}`;
  const idPanel = `faq-panel-${indice}`;

  const boton = crear(
    "button",
    {
      type: "button",
      class: "faq__boton",
      id: idBoton,
      "aria-expanded": abiertoPorDefecto ? "true" : "false",
      "aria-controls": idPanel,
    },
    [
      crear("span", { class: "faq__texto", text: String(item.p) }),
      crear("span", { class: "faq__icono", "aria-hidden": "true" }),
    ]
  );

  const panel = crear(
    "div",
    {
      class: "faq__panel",
      id: idPanel,
      role: "region",
      "aria-labelledby": idBoton,
    },
    [
      crear("div", { class: "faq__panel-inner" }, [
        crear("p", { class: "faq__respuesta", text: String(item.r ?? "") }),
      ]),
    ]
  );

  const contenedor = crear("div", { class: `faq__item${abiertoPorDefecto ? " is-open" : ""}` }, [
    crear("h3", { class: "faq__pregunta" }, [boton]),
    panel,
  ]);

  const alternar = (abrir) => {
    contenedor.classList.toggle("is-open", abrir);
    boton.setAttribute("aria-expanded", abrir ? "true" : "false");
  };

  boton.addEventListener("click", () => {
    const estaAbierto = contenedor.classList.contains("is-open");
    const lista = contenedor.parentElement;
    /* Un solo panel abierto a la vez; el panel abierto también puede cerrarse. */
    if (!estaAbierto && lista) {
      $$(".faq__item.is-open", lista).forEach((otro) => {
        if (otro === contenedor) return;
        otro.classList.remove("is-open");
        $(".faq__boton", otro)?.setAttribute("aria-expanded", "false");
      });
    }
    alternar(!estaAbierto);
  });

  return contenedor;
}

function activarTecladoFaq(lista) {
  lista.addEventListener("keydown", (evento) => {
    const botones = $$(".faq__boton", lista);
    const actual = botones.indexOf(document.activeElement);
    if (actual < 0) return;

    let destino = null;
    if (evento.key === "ArrowDown") destino = (actual + 1) % botones.length;
    else if (evento.key === "ArrowUp") destino = (actual - 1 + botones.length) % botones.length;
    else if (evento.key === "Home") destino = 0;
    else if (evento.key === "End") destino = botones.length - 1;
    if (destino === null) return;

    evento.preventDefault();
    botones[destino].focus();
  });
}

/* =========================================================== 12 · CIERRE */
function hidratarCierre() {
  const raiz = document.getElementById("cierre");
  if (!raiz) return;

  const legales = SITE.legales ?? {};
  pintarTexto($("[data-cierre-disclaimer]", raiz), legales.disclaimerGeneral);

  const aviso = $("[data-cierre-aviso]", raiz);
  if (aviso && legales.avisoPrivacidadTitulo) aviso.textContent = legales.avisoPrivacidadTitulo;

  const marca = $("[data-cierre-marca]", raiz);
  if (marca) {
    const nombre = SITE.marca?.nombre ?? "Chevrolet";
    const modelo = SITE.marca?.modelo ?? "Silverado";
    const anio = String(SITE.marca?.anio ?? "").trim();
    marca.textContent = [nombre, modelo].filter(Boolean).join(" ") + (anio ? ` · ${anio}` : "");
  }

  /* La fotografía se toma de la configuración central (respaldo en el HTML). */
  const galeria = SITE.galeria ?? {};
  const fuente = $("[data-cierre-source]", raiz);
  const imagen = $("[data-cierre-img]", raiz);
  if (fuente && galeria.cierreCine) fuente.setAttribute("srcset", galeria.cierreCine);
  if (imagen && galeria.cierreCineMovil) imagen.setAttribute("src", galeria.cierreCineMovil);
}

/* ==================================================== Aparición al scroll */
const IDS_SECCION_B = ["transformacion", "oferta", "comparativa", "testimonios", "preguntas", "cierre"];

/**
 * Refuerza el reveal de esta sección: main.js ya observó los bloques estáticos,
 * pero la hidratación ocurre después, así que aquí se observan los nodos nuevos.
 */
function activarRevelados() {
  const objetivos = [];
  IDS_SECCION_B.forEach((id) => {
    const raiz = document.getElementById(id);
    if (!raiz) return;
    $$(".reveal, .stagger", raiz).forEach((nodo) => {
      if (!nodo.classList.contains("is-in")) objetivos.push(nodo);
    });
  });

  if (!objetivos.length) return;

  if (sinMovimiento() || !("IntersectionObserver" in window)) {
    objetivos.forEach((nodo) => nodo.classList.add("is-in"));
    return;
  }

  const observador = new IntersectionObserver(
    (entradas) => {
      entradas.forEach((entrada) => {
        if (!entrada.isIntersecting) return;
        entrada.target.classList.add("is-in");
        observador.unobserve(entrada.target);
      });
    },
    { rootMargin: "0px 0px -10% 0px", threshold: 0.08 }
  );

  objetivos.forEach((nodo) => observador.observe(nodo));
}

/* ====================================================== Punto de entrada */
let iniciado = false;

function arrancar() {
  if (iniciado) return;
  iniciado = true;

  ejecutarSeguro("transformación", hidratarTransformacion);
  ejecutarSeguro("oferta", hidratarOferta);
  ejecutarSeguro("comparativa", hidratarComparativa);
  ejecutarSeguro("testimonios", hidratarTestimonios);
  ejecutarSeguro("preguntas frecuentes", hidratarFaq);
  ejecutarSeguro("cierre", hidratarCierre);
  ejecutarSeguro("aparición al scroll", activarRevelados);
}

export function initSeccionesB() {
  if (iniciado) return;

  /* Defensivo: main.js la invoca con el DOM listo, pero si se adelanta se espera. */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", arrancar, { once: true });
    return;
  }

  arrancar();
}
