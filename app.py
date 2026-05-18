import math
from datetime import date

import pandas as pd
import streamlit as st

from instrumentos import INSTRUMENTOS

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sintético de Dólar",
    page_icon="💵",
    layout="centered",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS PERSONALIZADO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap');

/* Fondo general */
.stApp { background-color: #0b0b12; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 1px solid rgba(255,255,255,0.08);
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #7e7a8f;
    border: none;
    font-weight: 500;
    padding: 10px 20px;
    font-size: 14px;
}
.stTabs [aria-selected="true"] {
    background: rgba(201,168,76,0.08) !important;
    color: #c9a84c !important;
    border-bottom: 2px solid #c9a84c !important;
    border-radius: 6px 6px 0 0;
}

/* Inputs */
input, select, textarea {
    font-family: 'IBM Plex Mono', monospace !important;
    background-color: #0e0e17 !important;
    color: #ede9e0 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
}

/* Labels de inputs */
label { color: #7e7a8f !important; font-size: 12px !important; }

/* Número grande de resultado */
.tasa-hero {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 64px;
    font-weight: 600;
    line-height: 1;
    text-align: center;
    margin: 8px 0;
}
.tasa-positive { color: #22d87a; text-shadow: 0 0 40px rgba(34,216,122,0.3); }
.tasa-negative { color: #f04e4e; text-shadow: 0 0 40px rgba(240,78,78,0.3); }

/* Card de resultado principal */
.result-hero {
    background: linear-gradient(135deg, #0d201a 0%, #091510 100%);
    border: 1px solid rgba(34,216,122,0.2);
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    margin-bottom: 16px;
}
.result-label {
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #22d87a;
    font-weight: 700;
    margin-bottom: 8px;
}
.result-sub {
    font-size: 13px;
    color: #7e7a8f;
    margin-top: 8px;
}
.result-sub span { color: #ede9e0; }

/* Metric cards secundarias */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}
.metric-card {
    background: #111119;
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 10px;
    padding: 16px 18px;
}
.metric-card .m-label {
    font-size: 10px;
    color: #7e7a8f;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 700;
    margin-bottom: 6px;
}
.metric-card .m-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 17px;
    font-weight: 600;
    color: #ede9e0;
}
.metric-card .m-sub {
    font-size: 11px;
    color: #7e7a8f;
    margin-top: 4px;
}

/* Chips de instrumento seleccionado */
.chip-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 10px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 6px;
    font-size: 12px;
}
.chip .chip-lbl { font-size: 9px; color: #7e7a8f; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; }

/* Separador de sección */
.step-title {
    font-size: 18px;
    font-weight: 700;
    color: #ede9e0;
    margin: 28px 0 12px;
    padding-left: 14px;
    border-left: 3px solid #c9a84c;
}
.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 10px;
    color: #c9a84c;
    letter-spacing: 0.12em;
    font-weight: 600;
    display: block;
    margin-bottom: 2px;
    padding-left: 14px;
}

/* Dataframe / tabla */
.stDataFrame { border-radius: 12px; overflow: hidden; }

/* Advertencia vencido */
.badge-expired {
    display: inline-block;
    background: rgba(240,78,78,0.1);
    color: #f04e4e;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 4px;
}

/* Ocultar header de Streamlit */
#MainMenu, header, footer { visibility: hidden; }

/* Próximamente card */
.coming-soon {
    background: #111119;
    border: 1px dashed rgba(255,255,255,0.1);
    border-radius: 14px;
    padding: 60px 24px;
    text-align: center;
    color: #7e7a8f;
    font-size: 15px;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────────────────────────────────────
def fmt_pct(n: float) -> str:
    if n is None or not math.isfinite(n):
        return "—"
    return f"{n * 100:.2f}%"

def fmt_ars(n: float) -> str:
    if n is None or not math.isfinite(n):
        return "—"
    return f"$ {n:,.0f}".replace(",", ".")

def fmt_usd(n: float) -> str:
    if n is None or not math.isfinite(n):
        return "—"
    return f"USD {n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def fmt_n(n: float, decimals: int = 2) -> str:
    if n is None or not math.isfinite(n):
        return "—"
    return f"{n:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULO CENTRAL
# ─────────────────────────────────────────────────────────────────────────────
def calcular_sintetico_dolar(monto, precio_letra, precio_futuro, spot, com_fut_pct, com_lec_pct, instrumento):
    """
    Fórmulas del modelo:
      Cant. LECAP   = monto × (1 − com_lec) × 100 / precio_letra
      Flujo ARS     = cant_lecap × flujo_letra / 100
      Cant. Futuros = flujo_ars / (precio_futuro × 1.000)
      USD inicial   = monto / spot
      USD final     = (flujo_ars / precio_futuro) × (1 − com_fut)
      Rend. directo = USD_final / USD_inicial − 1
      Tasa cub. TNA = (1 + rend_dir)^(365/días) − 1
    """
    from datetime import timedelta
    today = date.today() + timedelta(days=1)
    dias  = (instrumento["vto"] - today).days

    com_fut = com_fut_pct / 100
    com_lec = com_lec_pct / 100

    cant_lecap   = monto * (1 - com_lec) * 100 / precio_letra
    flujo_ars    = cant_lecap * instrumento["flujo"] / 100
    cant_futuros = flujo_ars / (precio_futuro * 1_000)
    usd_inicial  = monto / spot
    usd_final    = (flujo_ars / precio_futuro) * (1 - com_fut)
    rend_dir     = usd_final / usd_inicial - 1
    tasa_cub     = (1 + rend_dir) ** (365 / dias) - 1 if dias > 0 else None

    return {
        "dias":         dias,
        "cant_lecap":   cant_lecap,
        "flujo_ars":    flujo_ars,
        "cant_futuros": cant_futuros,
        "usd_inicial":  usd_inicial,
        "usd_final":    usd_final,
        "rend_dir":     rend_dir,
        "tasa_cub":     tasa_cub,
    }


# ─────────────────────────────────────────────────────────────────────────────
# TABS PRINCIPALES
# ─────────────────────────────────────────────────────────────────────────────
tab_dolar, tab_pesos = st.tabs(["💵  Sintético de Dólar", "🏦  Sintético de Pesos"])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — SINTÉTICO DE DÓLAR
# ═════════════════════════════════════════════════════════════════════════════
with tab_dolar:

    # HEADER
    st.markdown("""
    <div style="padding: 40px 0 20px;">
        <h1 style="font-size:38px; font-weight:900; line-height:1.1; color:#ede9e0; margin-bottom:14px;">
            Armá tu sintético<br>de dólar
        </h1>
        <p style="color:#7e7a8f; font-size:15px; line-height:1.75; max-width:580px;">
            Un <strong style="color:#ede9e0;">sintético de dólar</strong> es una estrategia de cobertura cambiaria
            que permite asegurar una tasa de interés en dólares a través de instrumentos en pesos.
            Combina la compra de una <strong style="color:#ede9e0;">LECAP</strong> con la compra de contratos de
            <strong style="color:#ede9e0;">futuros de dólar</strong>, garantizando un rendimiento predecible
            con independencia del tipo de cambio.
        </p>
    </div>
    <hr style="border:none; border-top:1px solid rgba(255,255,255,0.07); margin-bottom:8px;">
    """, unsafe_allow_html=True)

    # ── PASO 1 — Plazo ────────────────────────────────────────────────────
    st.markdown('<span class="step-num">01</span><div class="step-title">¿Qué plazo?</div>', unsafe_allow_html=True)

    today = date.today()
    opciones = {}
    for inst in INSTRUMENTOS:
        label = inst["mes"]
        if inst["vto"] < today:
            label += "  (vencido)"
        opciones[label] = inst
    opciones["Otro (ingreso manual)"] = None

    plazo_sel = st.selectbox("Mes de vencimiento", list(opciones.keys()), label_visibility="collapsed")
    instrumento = opciones[plazo_sel]

    # Ingreso manual si no hay par preconfigurado
    if instrumento is None:
        st.markdown("""
        <div style="background:rgba(201,168,76,0.04);border:1px solid rgba(201,168,76,0.18);
                    border-radius:10px;padding:16px 18px;margin-top:12px;">
            <p style="font-size:13px;color:#c9a84c;font-weight:500;margin-bottom:12px;">
                ⚠ No hay par preconfigurado. Ingresá los datos manualmente.
            </p>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            m_lecap  = st.text_input("Nombre LECAP",           placeholder="Ej: S31J6")
        with c2:
            m_futuro = st.text_input("Contrato futuro",         placeholder="Ej: DLRJUL26")
        with c3:
            m_vto    = st.date_input("Fecha vencimiento",       value=today)
        with c4:
            m_flujo  = st.number_input("Flujo a cobrar ($)",    value=0.0, format="%.3f")

        if m_lecap and m_futuro and m_flujo > 0:
            instrumento = {"mes": plazo_sel, "lecap": m_lecap, "futuro": m_futuro, "vto": m_vto, "flujo": m_flujo}
    else:
        # Chips informativos
        expired = instrumento["vto"] < today
        st.markdown(f"""
        <div class="chip-row">
            <span class="chip"><span class="chip-lbl">LECAP</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#c9a84c;font-weight:500;">{instrumento['lecap']}</span></span>
            <span class="chip"><span class="chip-lbl">Futuro</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#6bb8f5;font-weight:500;">{instrumento['futuro']}</span></span>
            <span class="chip"><span class="chip-lbl">Vencimiento</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#7e7a8f;">{instrumento['vto']}</span></span>
            <span class="chip"><span class="chip-lbl">Flujo × $100VN</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#22d87a;">${instrumento['flujo']}</span></span>
            {"<span class='badge-expired'>Vencido</span>" if expired else ""}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PASO 2 — Monto ───────────────────────────────────────────────────
    st.markdown('<span class="step-num">02</span><div class="step-title">Monto inicial</div>', unsafe_allow_html=True)

    monto = st.number_input("Pesos a invertir ($)", min_value=0.0, value=0.0, step=100_000.0, format="%.0f", label_visibility="collapsed", placeholder="Ej: 10.000.000")

    # ── PASO 3 — Condiciones de mercado ──────────────────────────────────
    st.markdown('<span class="step-num">03</span><div class="step-title">Condiciones actuales de mercado</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        precio_letra   = st.number_input("Precio de la letra",         min_value=0.0, value=0.0, format="%.3f", placeholder="Ej: 114.800")
    with c2:
        precio_futuro  = st.number_input("Precio del futuro ($/USD)",   min_value=0.0, value=0.0, format="%.2f", placeholder="Ej: 1547.00")
    with c3:
        spot           = st.number_input("Tipo de cambio spot ($/USD)", min_value=0.0, value=0.0, format="%.2f", placeholder="Ej: 1465.00")

    # Chips de referencia rápida
    if precio_letra > 0 and precio_futuro > 0 and spot > 0:
        prima_fwd  = (precio_futuro - spot) / spot
        rend_letra = (instrumento["flujo"] / precio_letra - 1) if instrumento else None
        st.markdown(f"""
        <div class="chip-row" style="margin-top:8px;">
            <span class="chip"><span class="chip-lbl">Prima fwd.</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#7e7a8f;">{fmt_pct(prima_fwd)}</span></span>
            {"" if rend_letra is None else f'''<span class="chip"><span class="chip-lbl">Rend. letra</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#7e7a8f;">{fmt_pct(rend_letra)}</span></span>'''}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PASO 4 — Comisiones ───────────────────────────────────────────────
    st.markdown('<span class="step-num">04</span><div class="step-title">Comisiones</div>', unsafe_allow_html=True)

    c1, c2 = st.columns([1, 1])
    with c1:
        com_fut = st.number_input("Comisión futuro (%)", min_value=0.0, value=0.0, step=0.01, format="%.2f")
    with c2:
        com_lec = st.number_input("Comisión LECAP (%)",  min_value=0.0, value=0.0, step=0.01, format="%.2f")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── RESULTADOS ───────────────────────────────────────────────────────
    inputs_ok = (
        instrumento is not None
        and monto > 0
        and precio_letra > 0
        and precio_futuro > 0
        and spot > 0
    )

    if inputs_ok:
        r = calcular_sintetico_dolar(monto, precio_letra, precio_futuro, spot, com_fut, com_lec, instrumento)

        st.markdown('<hr style="border:none;border-top:1px solid rgba(255,255,255,0.07);margin:8px 0 24px;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
            <div style="width:3px;height:22px;background:#22d87a;border-radius:2px;"></div>
            <h2 style="font-size:20px;font-weight:700;color:#ede9e0;margin:0;">Resultados</h2>
        </div>
        """, unsafe_allow_html=True)

        # Hero — Tasa Cubierta
        tasa_str   = fmt_pct(r["tasa_cub"]) if r["tasa_cub"] is not None else ("vencido" if r["dias"] <= 0 else "—")
        tasa_class = "tasa-positive" if (r["tasa_cub"] or 0) >= 0 else "tasa-negative"
        st.markdown(f"""
        <div class="result-hero">
            <div class="result-label">Tasa Cubierta (TNA)</div>
            <div class="tasa-hero {tasa_class}">{tasa_str}</div>
            <div class="result-sub">
                Anualizada &nbsp;·&nbsp; {r['dias']} días hasta vencimiento
                &nbsp;·&nbsp; <span>{instrumento['lecap']}</span> + <span>{instrumento['futuro']}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Cards secundarias
        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="m-label">Rendimiento directo</div>
                <div class="m-value">{fmt_pct(r['rend_dir'])}</div>
                <div class="m-sub">en el período (no anualizado)</div>
            </div>
            <div class="metric-card">
                <div class="m-label">USD inicial equivalente</div>
                <div class="m-value">{fmt_usd(r['usd_inicial'])}</div>
                <div class="m-sub">pesos ÷ spot</div>
            </div>
            <div class="metric-card">
                <div class="m-label">USD al vencimiento</div>
                <div class="m-value">{fmt_usd(r['usd_final'])}</div>
                <div class="m-sub">post comisiones</div>
            </div>
            <div class="metric-card">
                <div class="m-label">Rendimiento en USD</div>
                <div class="m-value">{fmt_usd(r['usd_final'] - r['usd_inicial'])}</div>
                <div class="m-sub">absoluto en el período</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tabla de detalle
        df = pd.DataFrame([{
            "Instrumento":        f"{instrumento['lecap']} · {instrumento['futuro']}",
            "Vencimiento":        str(instrumento["vto"]),
            "Días":               r["dias"],
            "Cant. LECAP (VN)":   f"{r['cant_lecap']:,.0f}",
            "Cant. Futuros":      f"{r['cant_futuros']:,.4f}",
            "Flujo ARS":          fmt_ars(r["flujo_ars"]),
            "Rend. Directo":      fmt_pct(r["rend_dir"]),
            "Tasa Cub. TNA ★":   fmt_pct(r["tasa_cub"]),
            "Monto final USD":    fmt_usd(r["usd_final"]),
        }])

        st.dataframe(df, hide_index=True, use_container_width=True)

        # Nota metodológica
        st.markdown("""
        <p style="font-size:12px;color:#55516a;line-height:1.65;margin-top:12px;">
            <strong style="color:rgba(255,255,255,0.25);">Metodología:</strong>
            Cant. LECAP = Pesos × (1 − com.LECAP) × 100 / Precio letra ·
            Flujo ARS = Cant. × Flujo / 100 ·
            Cant. Futuros = Flujo ARS / (Precio futuro × 1.000) ·
            USD final = (Flujo ARS / Precio futuro) × (1 − com.futuro) ·
            Tasa cubierta TNA = (1 + Rend.)^(365/días) − 1
        </p>
        """, unsafe_allow_html=True)

    elif plazo_sel and plazo_sel != "Otro (ingreso manual)":
        st.markdown("""
        <div style="margin-top:32px;padding:36px;text-align:center;
                    border:1px dashed rgba(255,255,255,0.08);border-radius:14px;">
            <p style="font-size:14px;color:#7e7a8f;">
                Completá todos los campos para ver los resultados.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — SINTÉTICO DE PESOS  (próximamente)
# ═════════════════════════════════════════════════════════════════════════════
with tab_pesos:
    st.markdown("""
    <div style="padding:40px 0 20px;">
        <h1 style="font-size:38px;font-weight:900;color:#ede9e0;margin-bottom:14px;">
            Sintético de Pesos
        </h1>
        <p style="color:#7e7a8f;font-size:15px;line-height:1.75;max-width:580px;">
            Esta sección está en desarrollo.
        </p>
    </div>
    <div class="coming-soon">
        🏗️&nbsp; Próximamente<br>
        <span style="font-size:13px;margin-top:8px;display:block;">
            La mecánica del sintético de pesos se agregará aquí.
        </span>
    </div>
    """, unsafe_allow_html=True)
