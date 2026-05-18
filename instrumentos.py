# ─────────────────────────────────────────────────────────────────────────────
# instrumentos.py
# Base de datos de pares LECAP + Futuro para el sintético de dólar.
#
# CÓMO EDITAR:
#   • Agregar instrumento → nueva línea copiando el formato
#   • Sacar instrumento   → comentar la línea con #
#   • Actualizar flujo    → cambiar el número en el campo "flujo"
#
# CAMPOS:
#   mes    → etiqueta que aparece en el selector   (ej: "Jul 2026")
#   lecap  → ticker de la letra                    (ej: "S31J6")
#   vto    → fecha de vencimiento                  (ej: date(2026, 7, 31))
#   flujo  → pago al vencimiento por cada $100 VN  (ej: 148.50)
#   futuro → contrato ROFEX correspondiente        (ej: "DLRJUL26")
# ─────────────────────────────────────────────────────────────────────────────

from datetime import date

INSTRUMENTOS = [
    {"mes": "May 2026", "lecap": "S29Y6",  "vto": date(2026,  5, 29), "flujo": 132.0438, "futuro": "DLRMAY26"   },
    {"mes": "Jun 2025", "lecap": "T30J6",  "vto": date(2026,  6, 30), "flujo": 144.8957, "futuro": "DLRJUN26"   },
    {"mes": "Jul 2025", "lecap": "S31L6",  "vto": date(2026, 7, 31), "flujo": 117.6768, "futuro": "DLRJUL26"   },
    {"mes": "Ago 2025", "lecap": "S31G6",  "vto": date(2026, 8, 31), "flujo": 127.0637, "futuro": "DLRAGO26"   },
    {"mes": "Sep 2025", "lecap": "S30S6",  "vto": date(2026, 9, 30), "flujo": 117.5356, "futuro": "DLRSEP26"   },
    {"mes": "Oct 2026", "lecap": "S30O6",  "vto": date(2026,  10, 30), "flujo": 135.2782, "futuro": "DLROCT26" },
    {"mes": "Nov 2026", "lecap": "S30N6",  "vto": date(2026,  11, 30), "flujo": 129.8882, "futuro": "DLRNOV26" },
]
