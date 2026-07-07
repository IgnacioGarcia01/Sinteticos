import math
from datetime import date

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

# Valores genéricos de mercado (placeholder — sin API conectada)
MERCADO_LETRA_VAL  = 114.800
MERCADO_FUTURO_VAL = 1547.00
MERCADO_SPOT_VAL   = 1465.00

# ─────────────────────────────────────────────────────────────────────────────
# CSS — Gama de azules, recuadros con fondo blanco
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;500;600;700;900&display=swap');

.stApp { background-color: #fafafa; }

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    border-bottom: 2px solid #5b96d4;
    background: transparent;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #334155;
    border: none;
    font-weight: 600;
    padding: 10px 20px;
    font-size: 14px;
}
.stTabs [aria-selected="true"] {
    background: rgba(29,78,216,0.12) !important;
    color: #1d4ed8 !important;
    border-bottom: 3px solid #1d4ed8 !important;
    border-radius: 6px 6px 0 0;
}

/* Inputs */
input, select, textarea {
    font-family: 'IBM Plex Mono', monospace !important;
    background-color: #ffffff !important;
    color: #0f172a !important;
    border: 1.5px solid #3b82f6 !important;
    border-radius: 8px !important;
    font-size: 17px !important;
    padding: 14px 16px !important;
}
label { color: #1e3a5f !important; font-size: 15px !important; font-weight: 600 !important; }

/* Número hero */
.tasa-hero {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 64px;
    font-weight: 600;
    line-height: 1;
    text-align: center;
    margin: 8px 0;
}
.tasa-positive { color: #1e3a8a; }
.tasa-negative { color: #b91c1c; }

/* Card resultado principal */
.result-hero {
    background: linear-gradient(135deg, #dbeafe 0%, #93c5fd 100%);
    border: 2px solid #3b82f6;
    border-radius: 16px;
    padding: 32px 24px;
    text-align: center;
    margin-bottom: 16px;
}
.result-label {
    font-size: 11px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #1e3a8a;
    font-weight: 700;
    margin-bottom: 8px;
}
.result-sub { font-size: 13px; color: #334155; margin-top: 8px; }
.result-sub span { color: #0f172a; font-weight: 600; }

/* Metric cards secundarias */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-bottom: 16px;
}
.metric-card {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border: 2px solid #3b82f6;
    border-radius: 10px;
    padding: 22px 22px;
}
.metric-card .m-label {
    font-size: 13px;
    color: #1e4080;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    font-weight: 700;
    margin-bottom: 8px;
}
.metric-card .m-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 25px;
    font-weight: 600;
    color: #0f172a;
}

/* Cards de nominales */
.nominales-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 12px;
    margin: 16px 0;
}
.nominal-card {
    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
    border: 3px solid #1d4ed8;
    border-radius: 12px;
    padding: 26px 28px;
}
.nominal-card .n-label {
    font-size: 13px;
    color: #1d4ed8;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    font-weight: 700;
    margin-bottom: 10px;
}
.nominal-card .n-value {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 34px;
    font-weight: 600;
    color: #0f172a;
}

/* Chips */
.chip-row { display: flex; gap: 8px; flex-wrap: wrap; margin-top: 10px; }
.chip {
    display: inline-flex; align-items: center; gap: 6px;
    padding: 4px 10px;
    background: #dbeafe;
    border: 1.5px solid #60a5fa;
    border-radius: 6px;
    font-size: 12px;
    color: #0f172a;
}
.chip .chip-lbl {
    font-size: 9px; color: #1e4080;
    text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;
}

/* Títulos de sección */
.step-title {
    font-size: 23px;
    font-weight: 700;
    color: #0f172a;
    margin: 28px 0 12px;
    padding-left: 14px;
    border-left: 4px solid #1d4ed8;
}
.step-num {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 11px;
    color: #1d4ed8;
    letter-spacing: 0.12em;
    font-weight: 700;
    display: block;
    margin-bottom: 2px;
    padding-left: 14px;
}

.badge-expired {
    display: inline-block;
    background: rgba(220,38,38,0.1);
    color: #dc2626;
    font-size: 11px;
    font-weight: 700;
    padding: 2px 10px;
    border-radius: 4px;
}

#MainMenu, header, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
for _k, _v in [
    ("mercado_activo", False),
    ("mercado_letra",  True),
    ("mercado_futuro", True),
    ("mercado_spot",   True),
    ("com_fut", 0.0),
    ("com_lec", 0.0),
]:
    if _k not in st.session_state:
        st.session_state[_k] = _v


def _toggle_mercado():
    st.session_state.mercado_activo = not st.session_state.mercado_activo
    if st.session_state.mercado_activo:
        st.session_state.mercado_letra  = True
        st.session_state.mercado_futuro = True
        st.session_state.mercado_spot   = True


def _manual_letra():  st.session_state.mercado_letra  = False
def _manual_futuro(): st.session_state.mercado_futuro = False
def _manual_spot():   st.session_state.mercado_spot   = False


def _set_com_default():
    st.session_state.com_fut = 0.2
    st.session_state.com_lec = 0.2


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
    return "$ " + f"{n:,.0f}".replace(",", ".")


def fmt_usd(n: float) -> str:
    if n is None or not math.isfinite(n):
        return "—"
    return f"USD {n:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def fmt_n(n: float, decimals: int = 2) -> str:
    if n is None or not math.isfinite(n):
        return "—"
    return f"{n:,.{decimals}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def numero_a_palabras(n: int) -> str:
    if n == 0:
        return "cero"
    if n < 0:
        return "menos " + numero_a_palabras(-n)

    _uni = [
        "", "un", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve",
        "diez", "once", "doce", "trece", "catorce", "quince", "dieciséis",
        "diecisiete", "dieciocho", "diecinueve",
    ]
    _dec = ["", "", "veinte", "treinta", "cuarenta", "cincuenta",
            "sesenta", "setenta", "ochenta", "noventa"]
    _cen = ["", "cien", "doscientos", "trescientos", "cuatrocientos", "quinientos",
            "seiscientos", "setecientos", "ochocientos", "novecientos"]

    def _bloque(x: int) -> str:
        if x == 0:
            return ""
        if x < 20:
            return _uni[x]
        if x < 100:
            d, u = divmod(x, 10)
            if u == 0:
                return _dec[d]
            if d == 2:
                return "veinti" + _uni[u]
            return f"{_dec[d]} y {_uni[u]}"
        c, r = divmod(x, 100)
        if r == 0:
            return _cen[c]
        prefijo = "ciento" if c == 1 else _cen[c]
        return f"{prefijo} {_bloque(r)}"

    partes = []
    if n >= 1_000_000_000:
        b, n = divmod(n, 1_000_000_000)
        partes.append("mil millones" if b == 1 else f"{_bloque(b)} mil millones")
    if n >= 1_000_000:
        m, n = divmod(n, 1_000_000)
        partes.append("un millón" if m == 1 else f"{_bloque(m)} millones")
    if n >= 1_000:
        k, n = divmod(n, 1_000)
        partes.append("mil" if k == 1 else f"{_bloque(k)} mil")
    if n > 0:
        partes.append(_bloque(n))
    return " ".join(partes)


# ─────────────────────────────────────────────────────────────────────────────
# CÁLCULO CENTRAL
# ─────────────────────────────────────────────────────────────────────────────
def calcular_sintetico_dolar(monto, precio_letra, precio_futuro, spot,
                              com_fut_pct, com_lec_pct, instrumento):
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
# TABS
# ─────────────────────────────────────────────────────────────────────────────
tab_dolar, tab_pesos = st.tabs(["💵  Sintético de Dólar", "🏦  Sintético de Pesos"])


# ═════════════════════════════════════════════════════════════════════════════
# TAB 1 — SINTÉTICO DE DÓLAR
# ═════════════════════════════════════════════════════════════════════════════
with tab_dolar:

    st.markdown("""
    <div style="padding: 40px 0 20px;">
        <h1 style="font-size:38px; font-weight:900; line-height:1.1; color:#0f172a; margin-bottom:14px;">
            Sintético de dólar
        </h1>
        <p style="color:#334155; font-size:15px; line-height:1.75; max-width:580px;">
            Un <strong style="color:#0f172a;">sintético de dólar</strong> es una estrategia de cobertura cambiaria
            que permite asegurar una tasa de interés en dólares a través de instrumentos en pesos.
            Combina la compra de una <strong style="color:#0f172a;">LECAP</strong> con la compra de contratos de
            <strong style="color:#0f172a;">futuros de dólar</strong>, garantizando un rendimiento predecible
            con independencia del tipo de cambio.
        </p>
        <p style="color:#64748b; font-size:12.5px; line-height:1.6; max-width:580px; font-style:italic; margin-top:10px;">
            *El rendimiento puede presentar desvíos con respecto al cálculo por las diferencias diarias a integrar
            por las variaciones en los futuros, lo cual también puede resultar favorable.
        </p>
    </div>
    <hr style="border:none; border-top:2px solid #5b96d4; margin-bottom:8px;">
    """, unsafe_allow_html=True)

    # ── PASO 1 — Plazo ────────────────────────────────────────────────────
    st.markdown('<span class="step-num">01</span><div class="step-title">Plazo</div>', unsafe_allow_html=True)

    today = date.today()
    opciones = {}
    for inst in INSTRUMENTOS:
        label = inst["mes"]
        if inst["vto"] < today:
            label += "  (vencido)"
        opciones[label] = inst
    opciones["Otro (ingreso manual)"] = None

    plazo_sel   = st.selectbox("Mes de vencimiento", list(opciones.keys()), label_visibility="collapsed")
    instrumento = opciones[plazo_sel]

    if instrumento is None:
        st.markdown("""
        <div style="background:#eff6ff;border:1px solid #93c5fd;
                    border-radius:10px;padding:16px 18px;margin-top:12px;">
            <p style="font-size:13px;color:#1e40af;font-weight:500;margin-bottom:0;">
                ⚠ No hay par preconfigurado. Ingresá los datos manualmente.
            </p>
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: m_lecap  = st.text_input("Nombre LECAP",        placeholder="Ej: S31J6")
        with c2: m_futuro = st.text_input("Contrato futuro",      placeholder="Ej: DLRJUL26")
        with c3: m_vto    = st.date_input("Fecha vencimiento",    value=today)
        with c4: m_flujo  = st.number_input("Flujo a cobrar ($)", value=0.0, format="%.3f")
        if m_lecap and m_futuro and m_flujo > 0:
            instrumento = {"mes": plazo_sel, "lecap": m_lecap, "futuro": m_futuro,
                           "vto": m_vto, "flujo": m_flujo}
    else:
        expired = instrumento["vto"] < today
        st.markdown(f"""
        <div class="chip-row">
            <span class="chip"><span class="chip-lbl">LECAP</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#1d4ed8;font-weight:700;">{instrumento['lecap']}</span></span>
            <span class="chip"><span class="chip-lbl">Futuro</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#1d4ed8;font-weight:700;">{instrumento['futuro']}</span></span>
            <span class="chip"><span class="chip-lbl">Vencimiento</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#334155;font-weight:600;">{instrumento['vto']}</span></span>
            <span class="chip"><span class="chip-lbl">Flujo × $100VN</span>
                <span style="font-family:'IBM Plex Mono',monospace;color:#0369a1;font-weight:700;">${instrumento['flujo']}</span></span>
            {"<span class='badge-expired'>Vencido</span>" if expired else ""}
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PASO 2 — Monto ───────────────────────────────────────────────────
    st.markdown('<span class="step-num">02</span><div class="step-title">Monto inicial</div>', unsafe_allow_html=True)

    monto = st.number_input(
        "Pesos a invertir ($)",
        min_value=0.0, value=0.0, step=100_000.0, format="%.0f",
        label_visibility="collapsed", placeholder="Ej: 10000000",
        key="monto_input",
    )
    if monto > 0:
        monto_fmt   = "$ " + f"{int(monto):,}".replace(",", ".")
        monto_words = numero_a_palabras(int(monto))
        st.markdown(
            f'<div style="font-size:12px;color:#1d4ed8;font-weight:600;margin-top:3px;">'
            f'{monto_fmt} &nbsp;·&nbsp; <em>{monto_words}</em></div>',
            unsafe_allow_html=True,
        )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PASO 3 — Condiciones de mercado ──────────────────────────────────
    st.markdown('<span class="step-num">03</span><div class="step-title">Condiciones actuales de mercado</div>', unsafe_allow_html=True)

    _btn_lbl = "✅ Mercado actual (activo)" if st.session_state.mercado_activo else "📊 Mercado actual"
    st.button(_btn_lbl, on_click=_toggle_mercado, key="btn_mercado")

    c1, c2, c3 = st.columns(3)

    with c1:
        _mkt = st.session_state.mercado_activo and st.session_state.mercado_letra
        if _mkt:
            precio_letra = st.number_input(
                "Precio de la letra", value=MERCADO_LETRA_VAL,
                disabled=True, format="%.3f", key="pl_mkt",
            )
            st.button("↩ Manual", key="btn_pl_manual", on_click=_manual_letra)
        else:
            precio_letra = st.number_input(
                "Precio de la letra", min_value=0.0, value=0.0,
                format="%.3f", placeholder="Ej: 114.800", key="pl_input",
            )

    with c2:
        _mkt = st.session_state.mercado_activo and st.session_state.mercado_futuro
        if _mkt:
            precio_futuro = st.number_input(
                "Precio del futuro ($/USD)", value=MERCADO_FUTURO_VAL,
                disabled=True, format="%.2f", key="pf_mkt",
            )
            st.button("↩ Manual", key="btn_pf_manual", on_click=_manual_futuro)
        else:
            precio_futuro = st.number_input(
                "Precio del futuro ($/USD)", min_value=0.0, value=0.0,
                format="%.2f", placeholder="Ej: 1547.00", key="pf_input",
            )

    with c3:
        _mkt = st.session_state.mercado_activo and st.session_state.mercado_spot
        if _mkt:
            spot = st.number_input(
                "Tipo de cambio spot ($/USD)", value=MERCADO_SPOT_VAL,
                disabled=True, format="%.2f", key="spot_mkt",
            )
            st.button("↩ Manual", key="btn_spot_manual", on_click=_manual_spot)
        else:
            spot = st.number_input(
                "Tipo de cambio spot ($/USD)", min_value=0.0, value=0.0,
                format="%.2f", placeholder="Ej: 1465.00", key="spot_input",
            )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── PASO 4 — Comisiones ───────────────────────────────────────────────
    st.markdown('<span class="step-num">04</span><div class="step-title">Comisiones</div>', unsafe_allow_html=True)

    st.button("Comisiones predeterminadas (0,2% c/u)", on_click=_set_com_default, key="btn_com_default")

    c1, c2 = st.columns(2)
    with c1:
        com_fut = st.number_input("Comisión futuro (%)", min_value=0.0, step=0.01, format="%.2f", key="com_fut")
    with c2:
        com_lec = st.number_input("Comisión LECAP (%)",  min_value=0.0, step=0.01, format="%.2f", key="com_lec")

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
        r = calcular_sintetico_dolar(
            monto, precio_letra, precio_futuro, spot, com_fut, com_lec, instrumento
        )

        st.markdown('<hr style="border:none;border-top:2px solid #5b96d4;margin:8px 0 24px;">', unsafe_allow_html=True)
        st.markdown("""
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:20px;">
            <div style="width:4px;height:22px;background:#1d4ed8;border-radius:2px;"></div>
            <h2 style="font-size:20px;font-weight:700;color:#0f172a;margin:0;">Resultados</h2>
        </div>
        """, unsafe_allow_html=True)

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

        st.markdown(f"""
        <div class="metric-grid">
            <div class="metric-card">
                <div class="m-label">Rendimiento directo</div>
                <div class="m-value">{fmt_pct(r['rend_dir'])}</div>
            </div>
            <div class="metric-card">
                <div class="m-label">USD inicial equivalente</div>
                <div class="m-value">{fmt_usd(r['usd_inicial'])}</div>
            </div>
            <div class="metric-card">
                <div class="m-label">USD al vencimiento</div>
                <div class="m-value">{fmt_usd(r['usd_final'])}</div>
            </div>
            <div class="metric-card">
                <div class="m-label">Rendimiento en USD</div>
                <div class="m-value">{fmt_usd(r['usd_final'] - r['usd_inicial'])}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="nominales-grid">
            <div class="nominal-card">
                <div class="n-label">Nominales Lecaps</div>
                <div class="n-value">{fmt_n(r['cant_lecap'], 0)}</div>
            </div>
            <div class="nominal-card">
                <div class="n-label">Nominales Futuros</div>
                <div class="n-value">{fmt_n(r['cant_futuros'], 4)}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    elif plazo_sel and plazo_sel != "Otro (ingreso manual)":
        st.markdown("""
        <div style="margin-top:32px;padding:36px;text-align:center;
                    border:2px dashed #60a5fa;border-radius:14px;background:#dbeafe;">
            <p style="font-size:14px;color:#334155;font-weight:500;">
                Completá todos los campos para ver los resultados.
            </p>
        </div>
        """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# TAB 2 — SINTÉTICO DE PESOS
# ═════════════════════════════════════════════════════════════════════════════
with tab_pesos:
    pass
