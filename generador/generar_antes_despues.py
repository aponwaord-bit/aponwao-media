"""Pieza ANTES Y DESPUÉS (2 fotos). Uso: python3 generar_antes_despues.py temas/<tema>.json
JSON: slug, etiqueta, titulo, subtitulo, antes, despues, antes_pos, despues_pos, trabajos[]"""
import json, sys, subprocess, pathlib, html
from PIL import Image
from generar import PHONE, TEL
BASE = pathlib.Path(__file__).parent
e = lambda s: html.escape(s, quote=False)
ARROW = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="none" stroke="#0C2340" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v16M5 13l7 7 7-7"/></svg>'

def pieza(t, kind):
    ps = 44 if kind == "post" else 56
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../antes-despues.css"></head>
<body class="{kind}"><div class="ad">
 <div class="top"><div class="wordmark">ΛPONWΛO</div><div class="kicker">{e(t["etiqueta"])}</div>
  <div class="head">Antes <em>y después</em></div><div class="sub">{e(t["subtitulo"])}</div></div>
 <div class="fotos">
  <div class="foto antes" style="background-image:url(../{t["antes"]});background-position:{t.get("antes_pos","center")}"><span class="tag">ANTES</span></div>
  <div class="foto despues" style="background-image:url(../{t["despues"]});background-position:{t.get("despues_pos","center")}"><span class="tag">DESPUÉS</span></div>
 </div>
 <div class="flecha">{ARROW.format(s=44 if kind=="post" else 52)}</div>
 <div class="trabajos">{"".join(f"<span>{e(x)}</span>" for x in t["trabajos"])}</div>
 <div class="call"><div class="ic">{PHONE.format(s=ps)}</div><div class="t"><small>¡LLAMA O ESCRIBE YA!</small><big>{TEL}</big></div></div>
</div><script src="../fit.js"></script></body></html>'''

def main():
    t = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")); slug = t["slug"]
    (BASE/"build").mkdir(exist_ok=True); (BASE/"out").mkdir(exist_ok=True)
    for kind, (w, h) in [("post", (1080, 1350)), ("historia", (1080, 1920))]:
        src = BASE/"build"/f"{slug}_{kind}.html"
        src.write_text(pieza(t, "post" if kind == "post" else "story"), encoding="utf-8")
        png = BASE/"out"/f"{slug}_{kind}.png"
        subprocess.run([sys.executable, str(BASE/"render.py"), str(src), str(png), str(w), str(h)], check=True)
        Image.open(png).convert("RGB").save(png.with_suffix(".jpg"), quality=92)

if __name__ == "__main__":
    main()
