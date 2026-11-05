# Asistente de imágenes de mantenimiento – Aponwao

Cada ejecución (un día sí y otro no) produce una pieza nueva, la audita, la envía por correo y la programa en Metricool.

## Datos fijos
- Marca: Aponwao Mantenimiento Las Terrenas · Tel/WhatsApp 829 373 5696
- Público: villas, hoteles y hospedajes de Las Terrenas (Samaná, RD)
- Correo: para mariemiliapuigbo@gmail.com y mpuigbo@aponwaord.com, con copia a lepage.armando@gmail.com
- Metricool: blogId 7518515, zona America/Caracas
  - Facebook: página Aponwao Mantenimiento Las Terrenas → post (facebookData.type POST) con texto
  - Instagram aponwao_rd → SOLO historia (instagramData.type STORY), nunca en el feed, sin texto
- Imágenes públicas: https://raw.githubusercontent.com/aponwaord-bit/aponwao-media/main/AAAA-MM/<archivo>.jpg

## Alcance de los servicios (no prometer más)
- Plomería: solo aguas limpias y desagües: cambio de duchas, llaves/grifería, destapes, fugas de agua limpia.
- Electricidad: mantenimiento: tomacorrientes, interruptores, sócates y bombillos, lámparas y abanicos. Nada de "¿se fue la luz?" ni inversores.
- Pintura, carpintería y otros mantenimientos menores de villas y hoteles.

## Calendario (orden pedido por el cliente)
1. 2026-11-05 pintura (publicado)
2. 2026-11-07 carpinteria
3. 2026-11-09 plomeria
4. 2026-11-11 electricidad
Después: temas nuevos según las necesidades que se repitan en los grupos de Facebook de Las Terrenas
(Amigos de Las Terrenas, Everything Expats Las Terrenas, DE INTERÉS LAS TERRENAS, Las terrenas).
Ideas dentro del alcance: mantenimiento preventivo entre huéspedes, cerraduras y puertas, abanicos de techo,
retoques de pintura exterior por salitre, revisión antes de temporada alta, jardinería/limpieza de áreas comunes.
Nunca copiar nombres ni datos de quienes publican en los grupos.

## Pasos
1. `git clone` este repo; `cd generador`.
2. Si existe `temas/<tema>.json` con el slug de hoy, úsalo. Si no, crea uno nuevo (mismo formato) con slug `AAAA-MM-DD_<tema>`
   y una foto de `assets/` (o recorte de `assets/referencia.jpg`). Títulos cortos (2 líneas, ≤ 9 letras por línea idealmente).
3. `python3 generar.py temas/<tema>.json` → `out/<slug>_post.jpg` (1080×1350) y `out/<slug>_historia.jpg` (1080×1920).
   Requiere Playwright/Chromium y las fuentes Poppins e Inter del sistema (Oswald y Dancing Script van en `fonts/`).
4. AUDITORÍA (mirar ambas imágenes): ortografía y acentos, teléfono 829 373 5696, ningún texto cortado ni tapado,
   títulos dentro del margen, servicios dentro del alcance. Corregir y regenerar si algo falla.
5. Copiar los .jpg a `../AAAA-MM/`, commit y push. Verificar que la URL raw responde 200.
6. Enviar el correo (Gmail) con enlaces a ambas imágenes, tema y próximo tema.
7. Programar en Metricool para las 11:30 del mismo día: post Facebook con texto + historia Instagram.
8. Recordar en el correo que la historia se agrega a Destacadas → "Mantenimiento" desde la app de Instagram.
