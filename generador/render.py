"""Renderiza un HTML a PNG con el tamaño exacto. Uso: python3 render.py entrada.html salida.png ancho alto"""
import sys, pathlib
from playwright.sync_api import sync_playwright

src, out, w, h = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
url = pathlib.Path(src).resolve().as_uri()
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": w, "height": h}, device_scale_factor=1)
    pg.goto(url)
    pg.wait_for_load_state("networkidle")
    pg.evaluate("document.fonts.ready")
    pg.wait_for_function("document.body.dataset.fit=='1' || !document.querySelector('.head')", timeout=5000)
    pg.wait_for_timeout(200)
    pg.screenshot(path=out, clip={"x": 0, "y": 0, "width": w, "height": h})
    b.close()
print(out)
