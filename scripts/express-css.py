"""Estilos del formulario express y ajustes finales del modo Apple."""

from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
css = RAIZ / "src/styles/apple.css"
texto = css.read_text(encoding="utf-8")

bloque = """
/* ==========================================================================
   FORMULARIO EXPRESS · banda oscura con captura en un minuto
   ==========================================================================*/

.express {
  position: relative;
  overflow: hidden;
  padding-block: clamp(3.5rem, 8vw, 6rem);
  background: radial-gradient(ellipse 70% 80% at 82% 12%, rgba(199, 162, 76, 0.16), transparent 60%),
    radial-gradient(ellipse 80% 70% at 8% 100%, rgba(28, 70, 126, 0.28), transparent 66%),
    linear-gradient(170deg, #070a11 0%, #0a1019 60%, #070b12 100%);
  color: #eef1f5;
}

.express__inner {
  display: grid;
  gap: clamp(1.75rem, 4vw, 3.5rem);
  align-items: center;
}

.express__texto {
  display: grid;
  gap: 0.75rem;
}

.express__texto .eyebrow {
  color: var(--gold-bright);
}

.express__titulo {
  font-size: clamp(2rem, 4.4vw, 3.4rem);
  line-height: 1;
  letter-spacing: -0.04em;
  color: #ffffff;
}

.express__bajada {
  max-width: 44ch;
  font-size: clamp(0.98rem, 1.3vw, 1.08rem);
  line-height: 1.6;
  color: #a4aebc;
}

.express__puntos {
  display: grid;
  gap: 0.4rem;
  margin-top: 0.35rem;
  font-size: 0.84rem;
  color: #8b95a3;
}

.express__puntos li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.express__puntos li::before {
  content: "";
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--gold);
  flex: none;
}

/* Panel con el formulario */
.express__panel {
  padding: clamp(1.25rem, 2.6vw, 2rem);
  border-radius: var(--r-lg);
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(18px) saturate(140%);
  -webkit-backdrop-filter: blur(18px) saturate(140%);
  box-shadow: 0 40px 70px -50px rgba(0, 0, 0, 0.9);
}

.express__form {
  display: grid;
  gap: 0.9rem;
}

.express__campo {
  display: grid;
  gap: 0.3rem;
}

.express__label {
  font-family: var(--font-display);
  font-size: 0.66rem;
  font-weight: 700;
  letter-spacing: 0.14em;
  text-transform: uppercase;
  color: #9aa4b2;
}

.express__input {
  width: 100%;
  min-height: 48px;
  padding: 0.7rem 0.9rem;
  border-radius: var(--r-sm);
  border: 1px solid rgba(255, 255, 255, 0.16);
  background: rgba(255, 255, 255, 0.06);
  color: #ffffff;
  font-size: 0.95rem;
  transition: border-color var(--dur) var(--ease-out), box-shadow var(--dur) var(--ease-out),
    background-color var(--dur) var(--ease-out);
}

.express__input::placeholder {
  color: rgba(255, 255, 255, 0.38);
}

.express__input:focus {
  outline: none;
  border-color: var(--gold);
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 0 0 3px rgba(199, 162, 76, 0.2);
}

.express__select {
  appearance: none;
  padding-right: 2.4rem;
  cursor: pointer;
}

.express__select option {
  color: #101317;
}

.express__campo.has-error .express__input {
  border-color: #e0726a;
}

.express__check {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(255, 255, 255, 0.12);
}

.express__check .form__check-label {
  color: #a7b1bf;
}

.express__check .form__link {
  color: #ffffff;
}

.express__form .form__error {
  color: #f0a49e;
}

.express__estado {
  display: none;
}

.express__estado.is-visible {
  display: block;
  padding: 0.65rem 0.8rem;
  border-radius: var(--r-sm);
  background: rgba(224, 114, 106, 0.14);
  border: 1px solid rgba(224, 114, 106, 0.35);
  color: #f3b8b3;
  font-size: 0.8rem;
}

.express__enviar {
  margin-top: 0.2rem;
  text-transform: none;
  letter-spacing: 0.02em;
  font-size: 0.92rem;
  min-height: 50px;
}

.express__exito {
  display: grid;
  gap: 0.6rem;
  justify-items: center;
  text-align: center;
  padding: 1rem 0.5rem;
}

.express__exito[hidden] {
  display: none;
}

.express__exito h3 {
  font-size: 1.25rem;
  color: #ffffff;
}

.express__exito p {
  max-width: 40ch;
  font-size: 0.86rem;
  line-height: 1.55;
  color: #a7b1bf;
}

.express__folio {
  padding: 0.35rem 0.75rem;
  border-radius: var(--r-pill);
  background: rgba(255, 255, 255, 0.08);
  font-size: 0.78rem;
  color: #ffffff;
}

@media (min-width: 900px) {
  .express__inner {
    grid-template-columns: minmax(0, 1fr) minmax(0, 460px);
  }

  .express__form {
    gap: 1rem;
  }
}
"""

if "FORMULARIO EXPRESS" not in texto:
    css.write_text(texto.rstrip() + "\n" + bloque, encoding="utf-8", newline="\n")
    print("  estilos express añadidos")
else:
    print("  ya aplicado")
