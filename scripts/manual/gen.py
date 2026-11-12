#!/usr/bin/env python3
"""Genera el manual imprimible del Kyria (HTML -> PDF con chrome headless)."""
import json, html, sys, pathlib

SRC = pathlib.Path(sys.argv[1])
OUT = pathlib.Path(sys.argv[2])
D = json.loads(SRC.read_text(encoding="utf-8"))
GEO = {k["pos"]: k for k in D["geometry"]["keys"]}
L = {l["id"]: l for l in D["layers"]}
BASE = {k["pos"]: k for k in L["base"]["keys"]}

# Ajustes de impresión (los datos del JSON llevan notas de pantalla o de planes).
OVR = {
    ("base", 11): ("MIC", "Win+Alt+K"),
    ("base", 31): ("Pegar", "mant.: copiar"),
    ("text", 29): ("F20", "sin uso"),
}

CAT = {  # relleno, borde, texto
    "letter": ("#FFFFFF", "#72D3D3", "#004254"),
    "mod":    ("#EFEEE8", "#9DB8BC", "#004859"),
    "layer":  ("#B1EFE8", "#006F77", "#004254"),
    "sym":    ("#E3F8F5", "#00B0BD", "#002B36"),
    "num":    ("#EEEBFA", "#8661F5", "#3B2D7A"),
    "nav":    ("#E4F2EB", "#246B4E", "#0A382A"),
    "media":  ("#F8EAE4", "#C0623F", "#84270B"),
    "sys":    ("#F8EAE4", "#C0623F", "#84270B"),
    "herdr":  ("#EAF4F6", "#004859", "#004254"),
}
U = 100   # unidad SVG por tecla
GAP = 7
W = D["geometry"]["width"]


def fsize(text, maxs, width=U - GAP - 16, k=0.6):
    n = max(1, len(text))
    return min(maxs, width / (k * n))


def key_svg(layer_id, pos, k, held):
    g = GEO[pos]
    x, y, rot = g["x"] * U, g["y"] * U, g["rot"]
    s = U - GAP
    cx, cy = x + U / 2, y + U / 2
    label, hint, cat = k["label"], k["hint"], k["category"]
    if (layer_id, pos) in OVR:
        label, hint = OVR[(layer_id, pos)]
    c = 14  # chaflán
    pts = f"{x+GAP/2},{y+GAP/2} {x+GAP/2+s-c},{y+GAP/2} {x+GAP/2+s},{y+GAP/2+c} {x+GAP/2+s},{y+GAP/2+s} {x+GAP/2+c},{y+GAP/2+s} {x+GAP/2},{y+GAP/2+s-c}"
    out = [f'<g transform="rotate({rot} {cx} {cy})">']
    if label is None:  # transparente: deja ver la base
        b = BASE[pos]
        bl = OVR.get(("base", pos), (b["label"], None))[0]
        out.append(f'<polygon points="{pts}" fill="none" stroke="#C9C8BF" stroke-width="1.6" stroke-dasharray="5 4"/>')
        out.append(f'<text x="{cx}" y="{cy+6}" class="ghost" font-size="{fsize(bl, 20):.1f}">{html.escape(bl)}</text>')
        out.append("</g>")
        return "".join(out)
    if pos in held:
        fill, stroke, ink = "#004254", "#004254", "#FFFFFF"
    else:
        fill, stroke, ink = CAT.get(cat, CAT["letter"])
    big = cat in ("sym", "letter", "num") and len(label) <= 2
    ls = fsize(label, 44 if big else 26, k=0.62)
    ly = cy + (ls * 0.36) - (10 if hint else 0)
    out.append(f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="2.2"/>')
    if pos in held:
        out.append(f'<polygon points="{pts}" fill="none" stroke="#00B0BD" stroke-width="2" transform="translate(0 0)" stroke-dasharray="2 6"/>')
    if " " in label and len(label) > 6 and pos not in held:
        a, b = label.split(" ", 1)
        ls = min(fsize(a, 22, k=0.62), fsize(b, 22, k=0.62))
        top = cy - (12 if hint else 2)
        out.append(f'<text x="{cx}" y="{top:.1f}" class="lbl" fill="{ink}" font-size="{ls:.1f}">{html.escape(a)}</text>')
        out.append(f'<text x="{cx}" y="{top+ls*1.02:.1f}" class="lbl" fill="{ink}" font-size="{ls:.1f}">{html.escape(b)}</text>')
    else:
        out.append(f'<text x="{cx}" y="{ly:.1f}" class="lbl" fill="{ink}" font-size="{ls:.1f}">{html.escape(label)}</text>')
    if hint:
        hs = fsize(hint, 12.5, k=0.62)
        out.append(f'<text x="{cx}" y="{y+U-GAP/2-11}" class="hint" fill="{ink}" font-size="{hs:.1f}">{html.escape(hint.upper())}</text>')
    out.append("</g>")
    return "".join(out)


def board(layer_id):
    l = L[layer_id]
    held = set(l["held_positions"])
    keys = "".join(key_svg(layer_id, k["pos"], k, held) for k in l["keys"])
    return (f'<svg class="board" viewBox="-4 -4 {W*U+8} 570" preserveAspectRatio="xMidYMid meet" xmlns="http://www.w3.org/2000/svg">'
            f'{keys}</svg>')


def panel(layer_id, code, title, how, desc, extra=""):
    return f"""
<section class="panel">
  <header class="ph">
    <span class="code">{code}</span>
    <h2>{title}</h2>
    <span class="how">▶ {how}</span>
  </header>
  {board(layer_id)}
  <div class="callout">{desc}{(" &nbsp;·&nbsp; " + extra) if extra else ""}</div>
</section>"""


def page(num, total, body, section):
    return f"""
<div class="page">
  <div class="topbar">
    <span class="brand">KYRIA<b>//</b>MANUAL DE CAMPO</span>
    <span class="sec">{section}</span>
    <span class="ref">REF KY-50 · ZMK · ES-WIN · FW 2026-11-13</span>
  </div>
  <div class="body">{body}</div>
  <div class="foot">
    <span>CLASIFICACIÓN: USO PERSONAL</span>
    <span class="stripe"></span>
    <span>HOJA {num:02d}/{total:02d}</span>
  </div>
  <i class="br tl"></i><i class="br tr"></i><i class="br bl"></i><i class="br brr"></i>
</div>"""


LEGEND = """
<div class="legend">
  <span><i style="background:#004254"></i>Tecla que mantienes</span>
  <span><i style="background:#E3F8F5;border-color:#00B0BD"></i>Símbolo</span>
  <span><i style="background:#B1EFE8;border-color:#006F77"></i>Capa</span>
  <span><i style="background:#EFEEE8;border-color:#9DB8BC"></i>Modificador</span>
  <span><i style="background:#EEEBFA;border-color:#8661F5"></i>Número / F</span>
  <span><i style="background:#E4F2EB;border-color:#246B4E"></i>Navegación</span>
  <span><i style="background:#F8EAE4;border-color:#C0623F"></i>Multimedia / sistema</span>
  <span><i class="dash"></i>Igual que la base</span>
</div>"""

p1 = f"""
<div class="hero">
  <div>
    <div class="kicker">PROTOCOLO 00 · OPERACIÓN DIARIA</div>
    <h1>Kyria<span>.</span></h1>
    <p class="lede">Teclado partido de 50 teclas. Las letras están donde siempre; todo lo demás está en
    <b>capas</b> que se activan manteniendo una tecla con el pulgar. Suelta y vuelves a la base.</p>
  </div>
  <div class="rules">
    <div class="rule"><span class="n">01</span><div><b>Tocar o mantener.</b> Las teclas con texto pequeño debajo hacen dos cosas:
      tocada, lo de arriba; mantenida mientras pulsas otra tecla, lo de abajo.</div></div>
    <div class="rule"><span class="n">02</span><div><b>Mayúsculas.</b> Mantén un <b>espacio</b> y toca la letra. Si vienes escribiendo
      seguido, el espacio siempre es espacio: haz una pausa mínima antes.</div></div>
    <div class="rule"><span class="n">03</span><div><b>Micro de Teams.</b> La tecla <b>MIC</b> (arriba a la derecha) silencia y activa el
      micro en cualquier llamada, aunque Teams no esté delante.</div></div>
  </div>
</div>
{panel("base", "CAPA 00", "Base", "siempre activa", "QWERTY con ñ y la tilde ´. Para los acentos, mejor la capa ACENTOS (mantén º).")}
<div class="thumbs">
  <div class="tcol"><div class="th">PULGAR IZQUIERDO</div>
    <table><tr><td>Win</td><td><b>SYM</b><small>mantener</small></td><td>+<small>mant.: Alt</small></td><td>Espacio<small>mant.: Shift</small></td><td>Enter</td></tr></table></div>
  <div class="tcol"><div class="th">PULGAR DERECHO</div>
    <table><tr><td>Borrar</td><td>Espacio<small>mant.: Shift</small></td><td>º<small>mant.: ACENTOS</small></td><td><b>NUMS</b><small>mantener</small></td><td><b>HERDR</b><small>toque: Win+1</small></td></tr></table></div>
  <div class="tcol"><div class="th">FILA SUPERIOR DE PULGARES</div>
    <table><tr><td><b>TEXT</b><small>mantener</small></td><td>Pegar<small>mant. ¼ s: copiar</small></td><td>Supr</td><td><b>TEXT</b><small>mantener</small></td></tr></table></div>
</div>
{LEGEND}
"""

acc_extra = """<b>Mayúsculas:</b> mantén además un espacio → Á É Í Ó Ú Ñ Ü.
  &nbsp;·&nbsp; <b>Prueba:</b> <code>Canción, pingüino, ¿Ómnibus? Él añadió más.</code>"""
sym_extra = """<b>Regla:</b> lo que abre, mano izquierda; lo que cierra, la tecla espejo de la derecha.
  &nbsp;·&nbsp; <b>Prueba:</b> <code>¿Qué tal? ¡Bien! (nota) user@mail.com # Título</code>"""
p2 = (panel("sym", "CAPA 04", "SYM · Símbolos", "mantén el pulgar izquierdo junto a Win",
            "Todos los símbolos a una tecla, sin AltGr ni teclas muertas.", sym_extra)
      + panel("acc", "CAPA 05", "ACENTOS", "mantén el pulgar º (derecho)",
              "Como AltGr en EE. UU.-Internacional: una pulsación por letra. Tocada sin mantener, la tecla da º.", acc_extra))

nums_extra = """<b>Operadores</b> del teclado numérico: salen bien en cualquier programa.
  La coma es el separador decimal de Excel. &nbsp;·&nbsp; <b>Prueba:</b> <code>12/3*4+5-6=</code>"""
text_extra = """<b>Bluetooth:</b> TEXT + Tab = perfil 0 · TEXT + A = perfil 1 · TEXT + Z = USB ↔ Bluetooth ·
  TEXT + Ctrl izq. = borrar emparejamiento del perfil activo."""
p3 = (panel("nums", "CAPA 01", "NUMS · Números", "mantén el pulgar NUMS (derecho)",
            "Números arriba, F1–F12 a la izquierda y teclado numérico a la derecha (0 en el pulgar exterior).", nums_extra)
      + panel("text", "CAPA 02", "TEXT · Navegación", "mantén una tecla TEXT (pulgares de arriba)",
              "Flechas y páginas a la derecha; multimedia, Bluetooth y clics de ratón.", text_extra))

herdr_extra = """<b>Paneles:</b> S / D dividen, H J K L mueven el foco, N M , . mueven el panel, Z zoom, X cierra.
  &nbsp;·&nbsp; <b>Pestañas:</b> C nueva, Y / U anterior / siguiente, esquina Ctrl = cerrar.
  &nbsp;·&nbsp; <b>Primero</b> un toque a HERDR: Win+1 pone delante herdr-app (anclada la 1ª en la barra de tareas)."""
p5 = panel("herdr", "CAPA 06", "HERDR · herdr-app", "toca HERDR (trae la app) y luego mantenla",
           "Cada acción de herdr-app con una tecla, con los mismos atajos de tu keys.json.", herdr_extra)

p4 = """
<div class="grid4">
  <section class="box"><div class="bh"><span class="code">PROC 01</span><h3>Flashear el firmware</h3></div>
    <ol>
      <li>GitHub → <code>mgbernal/zmk-config</code> → <b>Actions</b> → última ejecución en verde → descarga <b>firmware</b> y descomprime.</li>
      <li>Conecta la <b>mitad izquierda</b> por USB y pulsa <b>dos veces</b> el botón de reset: aparece la unidad <code>NICENANO</code>.</li>
      <li>Copia <code>kyria_left…uf2</code>. Se reinicia sola.</li>
      <li>Repite con la <b>derecha</b> y <code>kyria_right…uf2</code>. Flashea siempre las dos.</li>
    </ol></section>
  <section class="box"><div class="bh"><span class="code">PROC 02</span><h3>Si algo no conecta</h3></div>
    <ol>
      <li>Flashea <code>settings_reset…uf2</code> en las dos mitades.</li>
      <li>Vuelve a flashear <code>kyria_left</code> y <code>kyria_right</code>.</li>
      <li>Windows → Configuración → Bluetooth: quita el Kyria y vuelve a emparejarlo.</li>
    </ol>
    <p class="note">Firmware bueno guardado: pestaña <b>Releases</b> del repositorio (etiquetas <code>fw-…</code>).</p></section>
  <section class="box"><div class="bh"><span class="code">PROC 03</span><h3>Comprobación tras flashear</h3></div>
    <ul class="check">
      <li>Escribir rápido: sin mayúsculas pegadas.</li>
      <li>«. » + mantener espacio + letra → mayúscula.</li>
      <li>SYM: <code>¿Qué tal? ¡Bien! (nota) user@mail.com</code></li>
      <li>ACENTOS: <code>Canción, pingüino, Él añadió más.</code></li>
      <li>MIC silencia en una llamada de Teams.</li>
      <li><code>~</code> sale solo, sin espacio detrás.</li>
      <li>Pegar rápido no copia; mantener ¼ s copia.</li>
      <li>Toque HERDR trae herdr-app; HERDR + S divide el panel.</li>
    </ul></section>
  <section class="box"><div class="bh"><span class="code">PROC 04</span><h3>Atajos de bolsillo</h3></div>
    <table class="combo">
      <tr><td>Copiar / pegar</td><td>mantener ¼ s / tocar <b>Pegar</b></td></tr>
      <tr><td>Deshacer</td><td>Ctrl + Z (Ctrl en la esquina izq.)</td></tr>
      <tr><td>Esc</td><td>esquina superior izquierda, o TEXT + SYM</td></tr>
      <tr><td>Captura</td><td>TEXT + T (Impr Pant)</td></tr>
      <tr><td>Volumen</td><td>TEXT + E / C · ⏯ TEXT + F</td></tr>
      <tr><td>Micro Teams</td><td><b>MIC</b> (Win+Alt+K)</td></tr>
    </table></section>
</div>
<div class="status">
  <div class="sh">ESTADO DE SISTEMAS</div>
  <span class="ok">● BASE</span><span class="ok">● SYM</span><span class="ok">● ACENTOS</span><span class="ok">● NUMS</span><span class="ok">● TEXT</span><span class="ok">● HERDR</span>
  <span class="dev">○ MOUSE · en desarrollo</span><span class="dev">○ Chuleta en pantalla (lanzadera mma)</span>
  <div class="links">Mapa interactivo: claude.ai/artifact/Q3eK33p1P4ezNbGABvrzW9 &nbsp;·&nbsp; Código: github.com/mgbernal/zmk-config</div>
</div>
"""

pages = [(p1, "SECTOR 00 · BASE Y REGLAS"), (p2, "SECTOR 04–05 · SÍMBOLOS Y ACENTOS"),
         (p3, "SECTOR 01–02 · NÚMEROS Y NAVEGACIÓN"), (p5, "SECTOR 06 · HERDR-APP"),
         (p4, "SECTOR 99 · PROCEDIMIENTOS")]
body = "".join(page(i + 1, len(pages), b, s) for i, (b, s) in enumerate(pages))
css = (OUT.parent / "style.css").read_text(encoding="utf-8")
OUT.write_text(f"""<!doctype html><html lang="es"><head><meta charset="utf-8">
<title>Kyria · Manual de campo</title><style>{css}</style></head><body>{body}</body></html>""", encoding="utf-8")
print("ok", OUT)
