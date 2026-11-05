/**
 * ============================================================================
 *  CONFIGURACIÓN CENTRAL · Landing Chevrolet Silverado para ferreterías (CDMX)
 * ============================================================================
 *  TODO el contenido comercial, textos legales, datos de contacto, colores,
 *  promoción, preguntas frecuentes y seguimiento se edita en ESTE archivo.
 *  Los componentes no contienen datos comerciales quemados.
 *
 *  Reglas de contenido (acordadas con el cliente):
 *   · No se inventan especificaciones técnicas, precios, testimonios ni
 *     condiciones de la promoción. Todo dato dudoso se marca como
 *     "por confirmar" y es configurable aquí.
 *   · Toda cifra mostrada al usuario debe poder rastrearse a una fuente
 *     oficial (ficha técnica / distribuidor autorizado).
 * ============================================================================
 */

/** Fotografía oficial recibida del cliente (recortada y optimizada en /assets). */
const IMG = "assets/vehiculos/silverado";

/** Colores de carrocería disponibles en el material fotográfico recibido. */
export const COLORES = [
  {
    id: "rojo-lava",
    nombre: "Rojo Lava",
    hex: "#B31217",
    hexSombra: "#7d0c10",
    disponible: true,
    descripcion: "Presencia fuerte para una camioneta que se hace notar en obra y en calle.",
  },
  {
    id: "negro",
    nombre: "Negro",
    hex: "#131417",
    hexSombra: "#000000",
    disponible: true,
    descripcion: "Acabado sobrio y ejecutivo; disimula polvo y uso diario de trabajo.",
  },
  {
    id: "blanco",
    nombre: "Blanco",
    hex: "#F2F3F4",
    hexSombra: "#c9ccd1",
    disponible: true,
    descripcion: "La opción más legible para rotular con el nombre de tu ferretería.",
  },
  {
    id: "gris-tiburon",
    nombre: "Gris Tiburón",
    hex: "#8C9095",
    hexSombra: "#5f6368",
    disponible: true,
    descripcion: "Neutro y resistente a la vista; combina con cualquier imagen corporativa.",
  },
  {
    id: "arena-lunar",
    nombre: "Arena Lunar",
    hex: "#C7B9A5",
    hexSombra: "#9c8f7c",
    disponible: true,
    descripcion: "Tono cálido y poco común, ideal si buscas distinguirte de la flota habitual.",
  },
];

export const SITE = {
  /* ------------------------------------------------------------------ METADATOS */
  meta: {
    idioma: "es-MX",
    titulo: "Chevrolet Silverado para ferreterías | Movilidad para tu negocio",
    descripcion:
      "Chevrolet Silverado, la camioneta de trabajo para ferreterías de la Ciudad de México. Mueve mercancía, conecta sucursales y recoge pedidos con un vehículo propio. Solicita tu cotización.",
    urlCanonica: "https://silverado-ferreterias.example.com/",
    imagenOg: "assets/og-silverado-ferreterias.jpg",
    themeColor: "#0b0f16",
    palabrasClave: [
      "Chevrolet Silverado",
      "camioneta de trabajo",
      "ferretería CDMX",
      "pickup para negocio",
      "cotizar Silverado",
    ],
  },

  /* ------------------------------------------------------------------- IDENTIDAD */
  marca: {
    nombre: "Chevrolet",
    modelo: "Silverado",
    anio: "2026",
    claim: "Together Let's Drive",
    /** Logotipo oficial extraído del material de campaña que proporcionó el
     *  cliente (bowtie + wordmark). Si el archivo no existe, se usa el respaldo
     *  tipográfico del encabezado. */
    logo: {
      local: "assets/marca/chevrolet-bowtie.png",
      remoto:
        "https://www.chevrolet.com.mx/content/dam/chevrolet/na/mx/es/primary-navigation-icons/01-images/bowtie-new-v1.svg",
      alt: "Chevrolet",
    },
  },

  /* -------------------------------------------------------------------- CAMPAÑA */
  campana: {
    id: "silverado-ferreterias-cdmx-2026",
    canal: "Meta Ads",
    ciudad: "Ciudad de México",
    publico: "Propietarios de ferreterías con 1 a 5 sucursales",
  },

  /* ------------------------------------------------------------- ENTORNO LOCAL */
  desarrollo: {
    /** true = muestra insignias de configuración pendiente (útil en revisión local). */
    mostrarMarcadores: true,
    /** true = imprime los eventos de seguimiento en consola. */
    logEventos: true,
  },

  /* ------------------------------------------------------------------ CONTACTO */
  contacto: {
    telefono: "", // ej. "+52 55 1234 5678"
    correo: "", // ej. "ventas@distribuidor.com.mx"
    distribuidor: "", // Nombre del distribuidor autorizado
    horario: "Lunes a sábado, 9:00 a 19:00 h",
  },

  /* ------------------------------------------------------------------ FOTOGRAFÍA */
  galeria: {
    colores: (id) => `${IMG}/color-${id}-1400.webp`,
    coloresMovil: (id) => `${IMG}/color-${id}-900.webp`,
    tablero: `${IMG}/interior-tablero-1700.webp`,
    tableroMovil: `${IMG}/interior-tablero-1000.webp`,
    asientos: `${IMG}/interior-asientos.webp`,
    caja: `${IMG}/caja-herramientas.webp`,
    trasera: `${IMG}/exterior-trasera-roja.webp`,
    hitch: `${IMG}/hitch-receptor.webp`,
    campanaRemolque: `${IMG}/campana-remolque-1122.webp`,
    campanaRemolqueAngosta: `${IMG}/campana-remolque-800.webp`,
    cierreCine: `${IMG}/cierre-cinematico-1122.webp`,
    cierreCineMovil: `${IMG}/cierre-cinematico-800.webp`,
  },

  /* ------------------------------------------------------- SECCIÓN 3: FICHA TÉCNICA
   *  `verificado: false` => el componente agrega la nota "por confirmar con
   *  ficha técnica oficial" y NO presenta los datos como definitivos.
   *  Los valores precargados provienen del material oficial del fabricante
   *  (versión Custom 4x4). Al confirmar la versión vendida, actualízalos aquí. */
  especificaciones: {
    verificado: false,
    versionReferencia: "Silverado Custom 4x4 (2026)",
    fuente: "Información oficial del fabricante",
    items: [
      { etiqueta: "Motor", valor: "V8 5.3 L", nota: "Ecotec3 con Dynamic Fuel Management" },
      { etiqueta: "Potencia", valor: "355 hp" },
      { etiqueta: "Torque", valor: "383 lb-pie" },
      { etiqueta: "Transmisión", valor: "Automática de 10 velocidades" },
      { etiqueta: "Tracción", valor: "4x4" },
      { etiqueta: "Volumen de caja", valor: "1,781 L" },
      { etiqueta: "Capacidad de carga", valor: "753 kg" },
      { etiqueta: "Capacidad de arrastre", valor: "4,218 kg" },
    ],
    nota:
      "Cifras de referencia de la versión indicada. La capacidad de carga y de arrastre varía según la versión, la configuración y el equipamiento. Confirma los datos de la unidad que te interesa con tu distribuidor autorizado y la ficha técnica oficial.",
  },

  /* --------------------------------------------------------- SECCIÓN 7: PROMOCIÓN */
  oferta: {
    activa: true,
    titulo: "ESTRENA TU CHEVROLET SILVERADO CON BENEFICIOS ESPECIALES",
    subtitulo:
      "Condiciones de lanzamiento para empresarios de ferretería que buscan su primera unidad de trabajo.",
    vigencia: "", // ej. "Del 1 al 30 de noviembre de 2026" — dejar vacío si no está definida
    beneficios: [
      {
        id: "seguro",
        etiqueta: "1 año",
        titulo: "de seguro gratis",
        detalle:
          "Cobertura de seguro por un año para tu Silverado, sujeta a la aseguradora participante y a las condiciones de la póliza.",
      },
      {
        id: "bono",
        etiqueta: "Hasta $198,000",
        titulo: "de bono",
        detalle:
          "Bono aplicable a la compra de tu unidad, sujeto a la versión, forma de pago y disponibilidad de inventario.",
      },
    ],
    cta: "QUIERO MI COTIZACIÓN",
    notaCorta: "Beneficios válidos con distribuidores participantes.",
    notaLegal:
      "Promoción sujeta a disponibilidad de inventario y a las condiciones vigentes del distribuidor autorizado. El bono de hasta $198,000 y el año de seguro gratis aplican únicamente a las versiones participantes, con aseguradora y forma de pago participantes. No es acumulable con otras promociones. Los montos y la vigencia pueden cambiar sin previo aviso; confirma las condiciones exactas con tu asesor al solicitar la cotización.",
  },

  /* ----------------------------------------------- SECCIÓN 8: TABLA COMPARATIVA */
  comparativa: {
    titulo: "¿Qué necesitas para el trabajo diario de tu ferretería?",
    columnas: [
      { id: "silverado", nombre: "Chevrolet Silverado", destacada: true },
      { id: "auto", nombre: "Automóvil convencional" },
      { id: "compacto", nombre: "Vehículo pequeño de capacidad limitada" },
    ],
    filas: [
      {
        criterio: "Espacio de caja para carga",
        valores: ["Caja de carga dedicada y separada de la cabina", "Cajuela cerrada, sin caja de carga", "Espacio de carga muy reducido"],
        evaluacion: ["alto", "bajo", "bajo"],
      },
      {
        criterio: "Transporte de mercancía voluminosa",
        valores: ["Diseñada para carga voluminosa y materiales", "Limitada por la cajuela y el peso admisible", "Muy limitada"],
        evaluacion: ["alto", "bajo", "bajo"],
      },
      {
        criterio: "Uso de remolque (si la versión lo permite)",
        valores: ["Sí, con enganche y capacidad de arrastre homologada", "Sujeto a que la versión esté homologada", "Generalmente no homologado"],
        evaluacion: ["alto", "medio", "bajo"],
      },
      {
        criterio: "Versatilidad para operación comercial",
        valores: ["Pensada para trabajo: carga, traslados y supervisión", "Uso principalmente personal o urbano", "Uso urbano y compras menores"],
        evaluacion: ["alto", "medio", "bajo"],
      },
      {
        criterio: "Robustez para jornadas de trabajo",
        valores: ["Chasis y suspensión orientados a carga", "Diseño orientado a confort y ciudad", "Diseño urbano ligero"],
        evaluacion: ["alto", "medio", "bajo"],
      },
      {
        criterio: "Supervisión de sucursales",
        valores: ["Traslados con mercancía entre sucursales", "Posible, sin capacidad para carga", "Posible, con limitaciones de espacio"],
        evaluacion: ["alto", "medio", "bajo"],
      },
    ],
    nota:
      "Comparación cualitativa de uso. Las capacidades reales de cada vehículo dependen de su versión, equipamiento y ficha técnica; no todos los automóviles tienen las mismas limitaciones. Consulta siempre la información oficial de cada modelo.",
  },

  /* ------------------------------------------- SECCIÓN 6: TRANSFORMACIÓN ANTES/DESPUÉS */
  transformacion: {
    antes: [
      "Contratación frecuente de fletes",
      "Esperar disponibilidad de transportistas",
      "Dificultad para organizar traslados",
      "Limitaciones de capacidad",
      "Menor flexibilidad operativa",
    ],
    despues: [
      "Vehículo propio disponible para el negocio",
      "Mayor autonomía de transporte",
      "Organización de movimientos entre sucursales",
      "Posibilidad de recoger pedidos",
      "Mayor flexibilidad para atender necesidades operativas",
    ],
    nota:
      "La compra de una camioneta no elimina por sí sola todos los gastos de transporte ni garantiza ahorros: forma parte de una decisión de inversión que debe evaluarse con tus números y tu operación.",
  },

  /* ------------------------------------------- SECCIÓN 9: TESTIMONIOS / CONFIANZA */
  testimonios: {
    titulo: "Empresarios que saben lo que significa mover un negocio",
    /** Estados:
     *   "pendiente" → espacio reservado, sin contenido
     *   "borrador"  → ejemplos visibles, marcados como editables (para revisión)
     *   "publicado" → solo items con autorizado: true (requiere consentimiento)
     */
    estado: "borrador",
    items: [
      {
        rol: "Propietario",
        zona: "Ferretería en Coyoacán",
        sucursales: "2 sucursales",
        comentario:
          "Antes dependíamos de la agenda de los fletes. Ahora programamos la salida a sucursal el mismo día que llega el pedido y resolvemos lo urgente sin esperar a un tercero.",
        ejemplo: true,
        autorizado: false,
      },
      {
        rol: "Encargada de operaciones",
        zona: "Ferretería en Iztapalapa",
        sucursales: "3 sucursales",
        comentario:
          "Lo que más nos ha servido es mover material voluminoso entre sucursales sin contratar un viaje extra cada semana.",
        ejemplo: true,
        autorizado: false,
      },
      {
        rol: "Dueño",
        zona: "Ferretería en Tlalpan",
        sucursales: "1 sucursal",
        comentario:
          "Recoger mercancía directo con el proveedor nos dio margen para aceptar pedidos que antes teníamos que rechazar.",
        ejemplo: true,
        autorizado: false,
      },
    ],
    notaEjemplos:
      "Textos de ejemplo para revisar el diseño, no testimonios reales. Sustitúyelos por declaraciones autorizadas por escrito antes de publicar: en la configuración, cambia estado a «publicado» y marca cada testimonio con autorizado: true.",
    notaPendiente:
      "Espacio reservado para testimonios de empresarios ferreteros. Se publicarán únicamente con autorización por escrito del cliente y verificación del distribuidor.",
    resenasVerificadas: {
      titulo: "Reseñas verificadas del distribuidor",
      fuente: "",
      estado: "pendiente",
      nota:
        "Aquí se integrarán las reseñas verificadas del distribuidor autorizado (Google, Facebook o portal oficial). No se muestran reseñas de ejemplo.",
    },
  },

  /* ------------------------------------------------- SECCIÓN 10: PREGUNTAS FRECUENTES */
  faq: {
    titulo: "Preguntas frecuentes",
    items: [
      {
        p: "¿La Chevrolet Silverado es adecuada para trabajar en una ferretería?",
        r: "Es una camioneta de trabajo con caja de carga dedicada, pensada para mover herramientas, materiales y mercancía. Su utilidad real depende de la versión que elijas y del volumen y peso de lo que transportes. En la cotización puedes revisar con tu asesor la versión que mejor se ajuste a tu operación.",
      },
      {
        p: "¿Puedo transportar herramientas y materiales?",
        r: "Sí. Su caja de carga permite trasladar herramientas, tornillería, pinturas, materiales de construcción y productos voluminosos, siempre respetando la capacidad de carga indicada en la ficha técnica de la versión y asegurando la mercancía correctamente.",
      },
      {
        p: "¿Puedo utilizar un remolque con la Silverado?",
        r: "Depende de la versión y de que cuente con la capacidad de arrastre y el equipamiento homologado (enganche, arnés y frenos de remolque, según corresponda). El remolque no está incluido en la compra. Verifica con tu distribuidor la capacidad de arrastre de la versión, el enganche requerido y la normativa aplicable antes de remolcar.",
      },
      {
        p: "¿Cuál es la capacidad de carga de la camioneta?",
        r: "La capacidad de carga varía según la versión, la configuración y el equipamiento. En esta página no publicamos una cifra definitiva: solicítala en la cotización y confírmala con la ficha técnica oficial de la unidad que te interesa, ya que la carga nunca debe exceder ese límite.",
      },
      {
        p: "¿Qué versiones y colores están disponibles?",
        r: "La disponibilidad de versiones, colores e inventario cambia por distribuidor. Los colores mostrados en esta página corresponden al material fotográfico oficial recibido (Rojo Lava, Negro, Blanco, Gris Tiburón y Arena Lunar). Confirma la disponibilidad exacta con tu asesor al solicitar la cotización.",
      },
      {
        p: "¿Qué incluye el año de seguro gratis?",
        r: "Incluye cobertura de seguro por un año con la aseguradora participante de la promoción, sujeta a las condiciones de la póliza, deducibles y requisitos de contratación. El alcance exacto de la cobertura se confirma al momento de la cotización; no todos los planes cubren lo mismo.",
      },
      {
        p: "¿Cómo funciona el bono de hasta $198,000?",
        r: "Es un bono aplicable a la compra de la unidad, sujeto a la versión participante, la forma de pago, la disponibilidad de inventario y la vigencia de la promoción. El monto puede variar; tu asesor te indicará el monto exacto que aplica a tu caso.",
      },
      {
        p: "¿Puedo solicitar una cotización de financiamiento?",
        r: "Sí. En el formulario puedes indicar que te interesa financiamiento y un asesor te presentará las opciones disponibles, incluyendo requisitos, mensualidades y plazos sujetos a aprobación de crédito. Las condiciones finales dependen de la institución financiera y de tu perfil.",
      },
      {
        p: "¿Dónde puedo conocer la camioneta?",
        r: "En el distribuidor autorizado de tu preferencia, donde podrás ver la unidad física, resolver dudas y solicitar una prueba de manejo sujeta a disponibilidad. Si lo deseas, tu asesor puede ayudarte a coordinar la visita.",
      },
      {
        p: "¿Cómo puedo contactar a un asesor?",
        r: "Completa el formulario de cotización de esta página o escríbenos por WhatsApp. Al enviar tus datos, un asesor se pondrá en contacto contigo para brindarte información sobre disponibilidad, versiones y opciones de compra.",
      },
    ],
    nota:
      "Respuestas editables desde la configuración central del sitio. La información de versiones, promociones, inventario y financiamiento debe verificarse con el distribuidor autorizado antes de publicarse.",
  },

  /* ------------------------------------------------ SECCIÓN 11: FORMULARIO */
  formulario: {
    endpoint: "/api/cotizacion",
    /** Destino directo cuando la página se abre como archivo (file://).
     *  Publicado en Netlify se usa el proxy /api/cotizacion. */
    endpointRemoto: "https://script.google.com/macros/s/AKfycbwj3hEDWUEcZa94a1ZThZHK4lWbJW7CsmGysRbXUayBrJcTV-MNWNHSd6BcZCZigBua/exec",
    titulo: "TU NEGOCIO ESTÁ LISTO PARA SEGUIR CRECIENDO. COTIZA TU SILVERADO",
    subtitulo:
      "Déjanos tus datos y un asesor se pondrá en contacto contigo para brindarte información sobre disponibilidad, versiones y opciones de compra.",
    boton: "SOLICITAR MI COTIZACIÓN",
    campos: {
      nombre: { etiqueta: "Nombre completo", requerido: true, placeholder: "Ej. Juan Pérez Ramírez" },
      whatsapp: {
        etiqueta: "Celular",
        requerido: true,
        placeholder: "55 1234 5678",
        ayuda: "10 dígitos. Te contactaremos por este medio.",
      },
      correo: { etiqueta: "Correo electrónico", requerido: true, placeholder: "nombre@correo.com" },
      plan: { etiqueta: "Plan", requerido: true },
      mensaje: { etiqueta: "Mensaje", requerido: false },
      ciudad: { etiqueta: "Ciudad o alcaldía", requerido: true },
      ferreteria: { etiqueta: "Nombre de la ferretería (opcional)", requerido: false, placeholder: "Ej. Ferretería El Tornillo" },
      sucursales: { etiqueta: "¿Cuántas sucursales tienes?", requerido: true },
      usoVehiculo: { etiqueta: "¿Actualmente utilizas un vehículo para transportar mercancía?", requerido: true },
      interes: { etiqueta: "¿Cómo te interesa adquirir tu Silverado?", requerido: true },
    },
    opciones: {
      plan: ["Contado", "Financiamiento", "Quiero conocer las opciones"],
      ciudad: [
        "Álvaro Obregón", "Azcapotzalco", "Benito Juárez", "Coyoacán", "Cuajimalpa de Morelos",
        "Cuauhtémoc", "Gustavo A. Madero", "Iztacalco", "Iztapalapa", "La Magdalena Contreras",
        "Miguel Hidalgo", "Milpa Alta", "Tláhuac", "Tlalpan", "Venustiano Carranza", "Xochimilco",
        "Área metropolitana / Otro",
      ],
      sucursales: ["1 sucursal", "2 sucursales", "3 sucursales", "4 sucursales", "5 o más sucursales"],
      usoVehiculo: ["Sí, vehículo propio", "Sí, pero de terceros o fletes", "No, todavía no", "A veces"],
      interes: ["Contado", "Financiamiento", "Quiero conocer las opciones"],
    },
    privacidad: {
      etiqueta: "Acepto el aviso de privacidad y el tratamiento de mis datos para ser contactado.",
      urlAviso: "#aviso-privacidad",
      textoAviso:
        "Los datos que compartes se utilizan únicamente para contactarte y brindarte información sobre la Chevrolet Silverado y opciones de compra. No se comparten con terceros ajenos a la atención de tu solicitud. Puedes solicitar la eliminación de tus datos en cualquier momento a través del medio de contacto indicado.",
    },
    /** Mensajes de confirmación. El sitio NUNCA simula un envío exitoso:
     *  el mensaje de éxito solo aparece cuando el servidor confirma el registro. */
    mensajes: {
      exitoTitulo: "Solicitud registrada",
      exitoCuerpo:
        "Recibimos tus datos y quedaron registrados con folio {folio}. Un asesor se pondrá en contacto contigo para brindarte información sobre disponibilidad, versiones y opciones de compra.",
      errorGeneral:
        "No pudimos registrar tu solicitud en este momento. Intenta de nuevo o escríbenos por WhatsApp; tus datos no se perdieron.",
      duplicado:
        "Ya tenemos una solicitud reciente con este número de WhatsApp. Un asesor te contactará; si necesitas algo urgente, escríbenos por WhatsApp.",
    },
  },

  /* ----------------------------------------------------- WHATSAPP FLOTANTE */
  whatsapp: {
    activo: true,
    /** Formato internacional sin signos: 521 + 10 dígitos para México.
     *  Si queda vacío, el botón permanece visible pero lleva al formulario. */
    numero: "",
    mensaje:
      "Hola, me interesa cotizar la Chevrolet Silverado para mi ferretería. ¿Me pueden dar informes?",
    etiqueta: "Cotiza por WhatsApp",
  },

  /* ---------------------------------------------------------------- ANALÍTICA */
  analitica: {
    /** Meta Pixel: colocar el ID para activar PageView, ViewContent, CTA y Lead.
     *  Con el ID vacío no se carga ningún script de terceros. */
    metaPixelId: "",
    /** Conversion API (server-side). Requiere token; se envía desde el backend. */
    conversionApi: {
      activo: false,
      endpoint: "", // p. ej. https://graph.facebook.com/v21.0/{pixel_id}/events
      token: "", // mantener en variables de entorno, nunca en el navegador
    },
    dataLayer: true,
    debug: false,
    eventos: {
      pageView: true,
      viewContent: true,
      ctaClick: true,
      lead: true,
      faqOpen: false,
      colorChange: false,
    },
  },

  /* -------------------------------------------------- INTEGRACIÓN DE PROSPECTOS */
  leads: {
    /** El endpoint /api/cotizacion valida, deduplica y guarda el prospecto.
     *  Puede reenviar a un CRM o webhook sin cambiar el frontend. */
    almacenamiento: "archivo-local", // archivo-local | webhook | crm
    webhookUrl: "",
    crm: { proveedor: "", endpoint: "", tokenEnv: "" },
    archivo: "data/prospectos.jsonl",
    dedupeMinutos: 30,
  },

  /* --------------------------------------------------------------- LEGALES */
  legales: {
    disclaimerGeneral:
      "Chevrolet y el logotipo de Chevrolet son marcas registradas de General Motors. Las imágenes del vehículo son material oficial del fabricante y pueden variar respecto a la unidad física. La disponibilidad de versiones, colores, equipamiento y promociones depende del distribuidor autorizado.",
    notaRemolque:
      "El remolque no está incluido en la compra. La capacidad de arrastre depende de la versión y su equipamiento. Antes de remolcar, verifica la capacidad de arrastre, la instalación del enganche, el sistema de frenos y la normativa aplicable en tu entidad.",
    notaPrivacidad:
      "Este sitio es una página de campaña para la generación de prospectos. Los datos se utilizan exclusivamente para dar seguimiento a tu solicitud de cotización.",
    avisoPrivacidadTitulo: "Aviso de privacidad",
  },
};

/** Datos derivados que usan varios componentes. */
export const NAVEGACION = [
  { id: "vehiculo", etiqueta: "La camioneta" },
  { id: "beneficios", etiqueta: "Beneficios" },
  { id: "remolque", etiqueta: "Carga y remolque" },
  { id: "comparativa", etiqueta: "Comparativa" },
  { id: "preguntas", etiqueta: "Preguntas" },
  { id: "cotizacion", etiqueta: "Cotizar" },
];

export const TRACK = {
  pageView: "PageView",
  viewContent: "ViewContent",
  ctaClick: "CtaClick",
  lead: "Lead",
};
