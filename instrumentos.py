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
    {"mes": "Ago 2025", "lecap": "S29G5",  "vto": date(2025,  8, 29), "flujo": 157.700, "futuro": "DLRAGO"   },
    {"mes": "Sep 2025", "lecap": "S30S5",  "vto": date(2025,  9, 30), "flujo": 159.734, "futuro": "DLRSEP"   },
    {"mes": "Oct 2025", "lecap": "S31O5",  "vto": date(2025, 10, 31), "flujo": 132.821, "futuro": "DLROCT"   },
    {"mes": "Nov 2025", "lecap": "S28N5",  "vto": date(2025, 11, 28), "flujo": 123.561, "futuro": "DLRNOV"   },
    {"mes": "Dic 2025", "lecap": "T15D5",  "vto": date(2025, 12, 15), "flujo": 170.838, "futuro": "DLRDIC"   },
    {"mes": "Ene 2026", "lecap": "T30E6",  "vto": date(2026,  1, 31), "flujo": 142.222, "futuro": "DLRENE26" },
    {"mes": "Feb 2026", "lecap": "T13F6",  "vto": date(2026,  2, 13), "flujo": 144.960, "futuro": "DLRFEB26" },
    {"mes": "Mar 2026", "lecap": "TZXM6",  "vto": date(2026,  3, 31), "flujo": 212.570, "futuro": "DLRMAR26" },
    {"mes": "Abr 2026", "lecap": "S30A6",  "vto": date(2026,  4, 30), "flujo": 127.480, "futuro": "DLRABR26" },
    {"mes": "May 2026", "lecap": "S29Y6",  "vto": date(2026,  5, 29), "flujo": 127.480, "futuro": "DLRMAY26" },
    {"mes": "Jun 2026", "lecap": "T30J6",  "vto": date(2026,  6, 30), "flujo": 144.896, "futuro": "DLRJUN26" },
]
