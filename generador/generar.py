"""Genera la pieza de feed (1080x1350) y la historia (1080x1920) de Aponwao Mantenimiento
a partir de un tema en JSON.  Uso: python3 generar.py temas/<tema>.json
Salida: out/<slug>_post.png, out/<slug>_historia.png (+ .jpg)"""
import json, sys, subprocess, pathlib, html
from PIL import Image

BASE = pathlib.Path(__file__).parent
ICONS = {
 "gota": '<path d="M12 3c-3 4.5-6 7.6-6 11a6 6 0 0 0 12 0c0-3.4-3-6.5-6-11z"/>',
 "tubo": '<path d="M4 7h7v6a3 3 0 0 0 3 3h6"/><path d="M4 4v6M20 13v6"/>',
 "llave": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4z"/>',
 "grifo": '<path d="M4 10h9a3 3 0 0 1 3 3v1"/><path d="M8 10V6h4"/><path d="M6 6h8"/><path d="M16 18v.5M16 21v.5"/>',
 "fuego": '<path d="M12 3c1 3 4 4.5 4 9a4 4 0 0 1-8 0c0-2 1-3 2-4 0 2 1 3 2 3 0-3-1-5 0-8z"/>',
 "rayo": '<path d="M13 2 4 14h7l-1 8 9-12h-7z"/>',
 "bateria": '<rect x="3" y="7" width="16" height="10" rx="2"/><path d="M21 11v2M8 10l-1 2h3l-1 2"/>',
 "rodillo": '<rect x="3" y="3" width="15" height="6" rx="1.5"/><path d="M18 6h2v5h-8v3"/><rect x="10.5" y="14" width="3" height="7" rx="1"/>',
 "puerta": '<rect x="5" y="3" width="14" height="18" rx="1"/><circle cx="15" cy="12" r="1"/>',
 "copo": '<path d="M12 2v20M3.3 7l17.4 10M20.7 7 3.3 17"/>',
 "olas": '<path d="M2 15c2 0 2-1.5 4-1.5S8 15 10 15s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M2 19c2 0 2-1.5 4-1.5S8 19 10 19s2-1.5 4-1.5 2 1.5 4 1.5 2-1.5 4-1.5"/><path d="M8 12V5a2 2 0 0 1 4 0M14 12V5a2 2 0 0 1 4 0"/>',
 "mas": '<path d="M12 5v14M5 12h14"/>',
 "reloj": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 "escudo": '<path d="M12 3 4 6v6c0 4.5 3.4 8 8 9 4.6-1 8-4.5 8-9V6z"/><path d="m8.5 12 2.5 2.5 4.5-5"/>',
 "persona": '<circle cx="12" cy="8" r="4"/><path d="M4 21c0-4 3.6-7 8-7s8 3 8 7"/>',
 "doc": '<path d="M6 3h9l4 4v14H6z"/><path d="M9 12h7M9 16h7M9 8h4"/>',
}
def icon(name, size, color="#fff", sw=2):
    return f'<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>'

HOUSE = '''<svg viewBox="0 0 120 120" fill="none" stroke="{c}" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 56 L60 16 L108 56"/><path d="M24 46 V104 H96 V46"/><path d="M42 96 L68 70"/><circle cx="74" cy="64" r="12" fill="{c}" stroke="none"/><rect x="73" y="47" width="9" height="16" rx="1.5" transform="rotate(45 77.5 55)" fill="{bg}" stroke="none"/><path d="M80 96 L62 78" stroke-width="5"/><path d="M60 76 L46 62" stroke-width="11"/></svg>'''
PHONE = '<svg width="{s}" height="{s}" viewBox="0 0 24 24" fill="#E8B023"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.6a1 1 0 0 1-.25 1z"/></svg>'
TEL = "829 373 5696"
SELLOS = [("escudo", "TRABAJO<br>GARANTIZADO"), ("persona", "PERSONAL<br>RESPONSABLE"), ("reloj", "SERVICIO<br>RÁPIDO")]

def e(s): return html.escape(s, quote=False)

def servicios_html(items, compact=False):
    out = []
    for it in items:
        out.append(f'''<div class="srv"><div class="srv-ic">{icon(it["icono"], 40 if not compact else 44)}</div>
        <div><div class="srv-t">{e(it["titulo"])}</div><div class="srv-d">{e(it["texto"])}</div></div></div>''')
    return "\n".join(out)

def sellos_html():
    return "".join(f'<div class="sello">{icon(i, 54, "#E8B023", 1.8)}<span>{t}</span></div>' for i, t in SELLOS)

def post(t):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../piezas.css"></head>
<body class="post"><div class="c">
 <div class="hero"><div class="photo" style="background-image:url(../{t["foto"]})"></div></div>
 <div class="top">
   <div class="wordmark">ΛPONWΛO</div>
   <div class="kicker">{e(t["etiqueta"])}</div>
   <div class="head h1">{e(t["titulo1"])}</div>
   <div class="head h2">{e(t["titulo2"])}</div>
   <div class="sub">{e(t["subtitulo"])}</div>
   <div class="pill">{t["pill"]}</div>
 </div>
 <div class="badge">{HOUSE.format(c="#fff", bg="#0C2340")}<div>{t["badge"]}</div></div>
 <div class="script">{t["script"]}</div>
 <div class="list">{servicios_html(t["servicios"])}</div>
 <div class="band">
   <div class="call"><div class="ic">{PHONE.format(s=44)}</div><div class="t"><small>¡LLAMA O ESCRIBE YA!</small><big>{TEL}</big></div></div>
   <div class="sellos">{sellos_html()}</div>
 </div>
 <div class="foot"><span>{icon("escudo", 30, "#E8B023", 2.2)}</span>{e(t["cierre"])}</div>
</div><script src="../fit.js"></script></body></html>'''

def historia(t):
    return f'''<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="../brand.css"><link rel="stylesheet" href="../piezas.css"></head>
<body class="story"><div class="c">
 <div class="top">
   <div class="wordmark">ΛPONWΛO</div>
   <div class="kicker">{e(t["etiqueta"])}</div>
   <div class="head h1">{e(t["titulo1"])}</div>
   <div class="head h2">{e(t["titulo2"])}</div>
   <div class="sub">{e(t["subtitulo"])}</div>
 </div>
 <div class="photo" style="background-image:url(../{t["foto"]})"><div class="badge">{HOUSE.format(c="#fff", bg="#0C2340")}<div>{t["badge"]}</div></div></div>
 <div class="pill">{t["pill"]}</div>
 <div class="list">{servicios_html(t["servicios"], True)}</div>
 <div class="script">{t["script"]}</div>
 <div class="call"><div class="ic">{PHONE.format(s=56)}</div><div class="t"><small>¡LLAMA O ESCRIBE YA!</small><big>{TEL}</big></div></div>
 <div class="sellos">{sellos_html()}</div>
</div><script src="../fit.js"></script></body></html>'''

def main():
    tema = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))
    slug = tema["slug"]
    (BASE / "build").mkdir(exist_ok=True); (BASE / "out").mkdir(exist_ok=True)
    for kind, fn, (w, h) in [("post", post, (1080, 1350)), ("historia", historia, (1080, 1920))]:
        src = BASE / "build" / f"{slug}_{kind}.html"
        src.write_text(fn(tema), encoding="utf-8")
        png = BASE / "out" / f"{slug}_{kind}.png"
        subprocess.run([sys.executable, str(BASE / "render.py"), str(src), str(png), str(w), str(h)], check=True)
        Image.open(png).convert("RGB").save(png.with_suffix(".jpg"), quality=92)

if __name__ == "__main__":
    main()
