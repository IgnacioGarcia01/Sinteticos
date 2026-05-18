# Sintético de Dólar — Calculadora

Calculadora de sintéticos de dólar usando LECAP + Futuros ROFEX.

## Archivos

| Archivo | Para qué sirve |
|---|---|
| `app.py` | Aplicación principal (no editar) |
| `instrumentos.py` | **Base de datos de instrumentos — editar acá** |
| `requirements.txt` | Dependencias de Python |

## Cómo editar instrumentos

Abrí `instrumentos.py` y modificá el array `INSTRUMENTOS`:

```python
# Agregar una letra nueva → nueva línea
{"mes": "Jul 2026", "lecap": "S31J6",  "vto": date(2026, 7, 31), "flujo": 148.50, "futuro": "DLRJUL26"},

# Sacar una letra → comentar con #
# {"mes": "Ago 2025", "lecap": "S29G5", ...},

# Actualizar un flujo → cambiar el número
{"mes": "Jun 2026", "lecap": "T30J6",  "vto": date(2026, 6, 30), "flujo": 146.20, "futuro": "DLRJUN26"},
```

## Correr localmente

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy en Streamlit Cloud (gratis)

1. Subir este repositorio a GitHub
2. Ir a [share.streamlit.io](https://share.streamlit.io)
3. Conectar la cuenta de GitHub
4. Elegir el repo → `app.py` como archivo principal
5. Click en **Deploy**

Cada vez que hacés `git push`, la app se actualiza automáticamente.
