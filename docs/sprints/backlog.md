# zmk-config (Kyria) — Sprint Backlog

**Última actualización:** 2026-11-13
**Sprint activo:** Sprint 3 (Sprints 1 y 2 cerrados; falta la prueba física)

Leyenda: 🟢 PENDIENTE · 🟡 EN CURSO · 🔴 BLOQUEADO · ✅ HECHO

## Contexto y supuestos

- Teclado: Kyria 50 teclas, 2× nice!nano v1, ZMK. Todo el mapa está en `config/kyria.keymap`.
- **El sistema operativo usa la distribución Español (alfabetización internacional).** ZMK envía
  códigos de posición US, así que cada tecla produce lo que imprime en esa posición un teclado
  español: `SEMI`→ñ, `SQT`→´ (tecla muerta), `MINUS`→', `EQUAL`→¡, `FSLH`→-, `LBKT`→` (muerta),
  `RBKT`→+, `BSLH`→ç, `GRAVE`→º, `NON_US_BSLH`→<. Los símbolos con AltGr van con `RA(...)`.
- Sistema operativo supuesto: **Windows** (por Win+Espacio). **Microsoft Teams** (confirmado) para reuniones, chats y archivos.
- Uso diario: reuniones, toma de notas, trabajo con `mma` (por aclarar) y `herdr`.
- Molestias: combinaciones complejas (Win+Espacio) y los símbolos.
- Verificación: no hay toolchain local, así que cada cambio se valida con el script de #4 y con la
  compilación de GitHub Actions. La prueba final siempre es flashear y teclear.

Posiciones de teclas usadas en este documento: fila 0 = 0–11, fila 1 = 12–23,
fila 2 = 24–39 (30–33 son las 4 teclas de pulgar superiores), pulgares = 40–49.

---

## Sprint 1 — Base fiable
**Objetivo:** que escribir texto normal no falle y que el firmware sea reproducible.
**Estado sprint:** 4/4 cerrados (pendientes de CI y prueba física)

### #1 Mayúsculas accidentales y espacios perdidos (Espacio/Shift)
- **Sprint:** 1
- **Estado:** ✅ HECHO (2026-11-12) — commit `edc6311`. Hold-tap `smt` (balanced, require-prior-idle 125 ms, sin quick-tap) en Espacio, + y º. **Falta probarlo en el teclado** (test plan). Si las mayúsculas tras «. » cuestan, se baja `require-prior-idle-ms`.
- **Valor:** alto · **Coste:** S
- **Descripción:** `&mt LSHFT SPACE` usa el modo por defecto `hold-preferred`. Al escribir rápido y
  pulsar la siguiente letra antes de soltar el espacio, ZMK lo toma como Shift: se pierde el espacio
  y la letra sale en mayúscula. Pasa en los mensajes reales del usuario («poderEscribir»,
  «diaA dia», «combinacionesDe»). Ya hubo un intento que se revirtió (commits `e101c11`/`8a749b1`).
- **Subtareas:**
  - [ ] Crear un hold-tap propio `spc_sft`: `flavor = "balanced"`, `tapping-term-ms = <200>`,
        `quick-tap-ms = <200>` (dos toques y mantener = repetir espacio),
        `require-prior-idle-ms = <150>` (si vienes tecleando, siempre es espacio)
  - [ ] Ponerlo en las posiciones 43 y 46
  - [ ] Aplicar el mismo criterio a `&mt LALT RBKT` y `&mt RALT GRAVE` (42, 47)
- **Test plan:** escribir un párrafo rápido sin que aparezcan mayúsculas pegadas; poner mayúsculas
  manteniendo espacio de forma deliberada; mantener espacio para que se repita.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #2 La capa NUMS saca otros operadores con la distribución española
- **Sprint:** 1
- **Estado:** ✅ HECHO (2026-11-12) — commit `5c747ef`. `KP_DIVIDE/MULTIPLY/PLUS/MINUS` y `=` como `LS(N0)`. La coma se queda (en Excel español es el separador decimal).
- **Valor:** alto · **Coste:** S
- **Descripción:** el teclado numérico de la capa 1 usa códigos US, y con la distribución española
  salen otros caracteres: `SLASH`→«-», `ASTERISK`→«(», `PLUS`→«¿», `MINUS`→«'», `EQUAL`→«¡».
- **Subtareas:**
  - [ ] Cambiarlos por `KP_DIVIDE`, `KP_MULTIPLY`, `KP_PLUS`, `KP_MINUS` (no dependen de la
        distribución) y «=» por `LS(N0)`
  - [ ] Revisar `COMMA` en el teclado numérico: en Excel español puede interesar `KP_DOT`
        (separador decimal)
- **Test plan:** abrir el Bloc de notas y Excel y escribir `12/3*4+5-6=`.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #3 Fijar la versión de ZMK
- **Sprint:** 1
- **Estado:** ✅ HECHO (2026-11-12) — commit `d558b1c`. Fijado a `ff09f2d0` (main del 2026-06-07), el ZMK con el que compiló el último firmware bueno (16-jun). Queda pendiente que CI pase tras el push.
- **Valor:** medio · **Coste:** S
- **Descripción:** `west.yml` y el workflow apuntan a `main`, así que un cambio en ZMK puede romper la
  compilación sin tocar nada aquí. La v0.3.0 es anterior a la nomenclatura `nice_nano@1//zmk` que
  usa `build.yaml`, por eso se fija un commit concreto de `main` (hoy `4dd95d7840`).
- **Subtareas:**
  - [ ] `config/west.yml`: `revision: <sha>`
  - [ ] `.github/workflows/build.yml`: `build-user-config.yml@<sha>`
  - [ ] Confirmar que CI compila las tres imágenes (left, right, settings_reset)
- **Test plan:** compilación de GitHub Actions en verde.
- **Ficheros:** `config/west.yml`, `.github/workflows/build.yml`
- **Añadido:** 2026-11-12

### #4 Validación local del keymap
- **Sprint:** 1
- **Estado:** ✅ HECHO (2026-11-12) — commits `f9055c5`, `8954b51`, `d558b1c`. `scripts/check_keymap.py` (50 bindings por capa, capas referenciadas, comportamientos, `ES_*`, llaves) y job `check` en CI antes de compilar.
- **Valor:** medio · **Coste:** S
- **Descripción:** script que compruebe que cada capa tiene exactamente 50 bindings, que las capas
  referenciadas existen y que las macros `ES_*` están definidas. Así se detectan errores antes de
  esperar a CI.
- **Subtareas:**
  - [ ] `scripts/check_keymap.py` (Python, sin dependencias)
  - [ ] Paso en el workflow antes de compilar (opcional)
- **Test plan:** el script pasa con el keymap actual y falla si se borra un binding.
- **Ficheros:** `scripts/check_keymap.py`
- **Añadido:** 2026-11-12

---

## Sprint 2 — Símbolos y acentos sin esfuerzo
**Objetivo:** escribir cualquier símbolo con una capa y una tecla, sin AltGr ni teclas muertas.
**Estado sprint:** ✅ CERRADO 2026-11-13 (#5 #6 #7 #16; #8 pasa al Sprint 3)

### #5 Definiciones para la distribución española (`es_keys.h`)
- **Sprint:** 2
- **Estado:** ✅ HECHO (2026-11-12) — commit `c7118b5`. `config/es_keys.h`.
- **Valor:** alto · **Coste:** S
- **Descripción:** cabecera con nombres legibles que encapsulan la traducción US→ES, por ejemplo
  `ES_AT = RA(N2)`, `ES_LBRC = RA(LBKT)`, `ES_LCBR = RA(SQT)`, `ES_PIPE = RA(N1)`,
  `ES_BSLH = RA(GRAVE)`, `ES_EURO = RA(E)`, `ES_LT = NON_US_BSLH`, `ES_QUES = LS(MINUS)`,
  `ES_IQUE = LS(EQUAL)`…
- **Ficheros:** `config/es_keys.h`, `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #6 Capa SYM accesible con el pulgar
- **Sprint:** 2
- **Estado:** ✅ HECHO (2026-11-12) — commit `c7118b5`. Disposición revisada por ergonomía (ver diagrama en `kyria.keymap`): lo que abre va en la izquierda y lo que cierra en la tecla espejo de la derecha; ¿? ( ) ¡! en la fila central con índice, medio y anular; @ y # en los índices. Falta la prueba física.
- **Valor:** alto · **Coste:** M
- **Descripción:** capa nueva de símbolos que se activa manteniendo el pulgar izquierdo interior
  (posición 41, ahora la tecla muerta «`», que pasa a esta capa). Propuesta inicial, a validar con
  el usuario:
  ```
  `  !  "  #  $  %        &  /  (  )  =  ?
  ~  @  €  {  }  |        ¿  [  ]  <  >  ¡
  \  ^  '  *  +  ·        -  _  ;  :  º  ª
  ```
  Los pares de apertura y cierre van juntos bajo los dedos fuertes y la fila de arriba sigue el
  orden de Shift+números del teclado español.
- **Subtareas:**
  - [ ] Validar la disposición con el usuario
  - [ ] Implementar la capa con macros `ES_*`
- **Test plan:** escribir `user@mail.com`, `{ "a": [1, 2] }`, `<b>` y `¿Qué? ¡Sí! 10 €`.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #7 Teclas muertas que se escriben de un toque
- **Sprint:** 2
- **Estado:** ✅ HECHO (2026-11-12) — commit `c7118b5`. Macros `es_grv`, `es_circ`, `es_tild`. Hay que comprobar en Windows que «~» (AltGr+4) es tecla muerta; si no lo es, saldría «~ » y se quita el espacio.
- **Valor:** medio · **Coste:** S
- **Descripción:** en español, «`», «^», «~» y «¨» son teclas muertas: hay que pulsar espacio después.
  Se crean macros (tecla + espacio) para que salgan de un toque desde la capa SYM. La tilde «´» se
  queda muerta en la tecla `SQT` de la capa base, porque así es como se escriben los acentos.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #8 Arreglar la tecla de copiar/pegar
- **Sprint:** 3 (movido desde el 2 el 2026-11-13)
- **Estado:** ✅ HECHO (2026-11-13). Hold-tap propio `cpy` (`tap-preferred`, 250 ms) en la posición 31: tocar = Ctrl+V; solo copia si se mantiene ¼ s, aunque se pulse otra tecla antes. Cortar y deshacer no se añaden aquí: Ctrl+X/Ctrl+Z ya salen con el Ctrl de la esquina, y TEXT+X/V están reservadas para #9. **Falta la prueba física.**
- **Valor:** medio · **Coste:** S
- **Descripción:** `&mt LC(C) LC(V)` en modo `hold-preferred` copia por error si se pulsa otra tecla
  durante el toque. Se cambia por un hold-tap `tap-preferred` (toque = pegar, mantener = copiar).
  Valorar también añadir cortar y deshacer.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

---

## Sprint 3 — Atajos de trabajo (reuniones, notas, herdr)
**Objetivo:** que cualquier atajo de varias teclas se haga con la capa TEXT y una sola tecla.
**Estado sprint:** 2/6 cerrados (#8, #11; #17 en curso)

### #9 Atajos de Windows de una tecla en la capa TEXT
- **Sprint:** 3
- **Estado:** 🟢 PENDIENTE
- **Valor:** alto · **Coste:** M
- **Descripción:** se usan los huecos libres de la capa TEXT, con letras fáciles de recordar:
  - TEXT + Espacio (43/46) → **Win+Espacio**
  - TEXT + V (28) → Win+V (historial del portapapeles)
  - TEXT + R (4) → Win+Shift+S (recorte de pantalla)
  - TEXT + X (26) → Win+H (dictado por voz, útil para notas)
  - TEXT + G (17) → Win+. (emojis)
  - Pulgares de TEXT → Alt+Tab, Win+Tab y Win+L (bloquear), por definir
- **Test plan:** probar cada atajo en Windows.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #10 Atajos de Microsoft Teams (reuniones, chats y archivos)
- **Sprint:** 3
- **Estado:** 🟢 PENDIENTE
- **Valor:** alto · **Coste:** M
- **Descripción:** Teams es la herramienta corporativa principal: reuniones, chats y archivos. Se
  agrupan sus atajos en la mano izquierda de la capa TEXT:
  - **Micro global → Win+Alt+K** en la posición 29, la que ahora ocupa **F20, que no hace nada** (el
    usuario lo confirmó el 2026-11-12). Es el silencio de llamada nativo de Windows 11: funciona con
    Teams aunque su ventana no esté activa. No hace falta PowerToys; además, su utilidad «Video
    Conference Mute» ya no existe en versiones recientes.
  - **Reunión (con Teams activo):** cámara Ctrl+Shift+O · levantar la mano Ctrl+Shift+K ·
    compartir pantalla Ctrl+Shift+E · colgar Ctrl+Shift+H · aceptar llamada Ctrl+Shift+A ·
    rechazarla Ctrl+Shift+D
  - **Navegación:** buscar Ctrl+E · chat nuevo Ctrl+N. Orden de la barra lateral según la captura
    del usuario: **Ctrl+1 Actividad · Ctrl+2 Calendario · Ctrl+3 Chat · Ctrl+4 Equipos ·
    Ctrl+5 Llamadas · Ctrl+6 OneDrive/Archivos** (falta comprobar Ctrl+1 y Ctrl+3 en vivo)
  - **Escribir:** abrir el cuadro de redacción grande Ctrl+Shift+X (útil para notas largas en un
    chat)
- **Subtareas:**
  - [x] Comprobar el orden de la barra lateral (captura del 2026-11-12)
  - [x] Confirmar qué hace F20 hoy → nada; se sustituye por Win+Alt+K
  - [x] 2026-11-12: Win+Alt+K también va en la capa base, en la tecla de arriba a la derecha (antes ç, que el usuario no usa)
  - [ ] El usuario comprueba en una llamada que Win+Alt+K silencia el micro
  - [ ] Proponer la colocación y validarla con el usuario
  - [ ] Implementar
- **Test plan:** en una reunión de prueba, cada tecla hace su acción; en el chat, buscar y crear
  chat nuevo.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #11 Capa HERDR: cada acción de herdr-app con una sola tecla
- **Sprint:** 3
- **Estado:** ✅ HECHO (2026-11-13). Capa 6 `herdr_layer` con la propuesta tal cual; se activa con `ls_herdr` en la posición 49 (sustituye a Win derecho, avisa con F18 si `SENAL_CAPAS` = 1). Hoja 05 del PDF y `kyria-layout.json` actualizados. **Falta probarla en herdr-app** y ajustar lo que no guste.
- **Valor:** alto · **Coste:** M
- **Datos:** `keys.json` del portátil (`C:\Users\mgbernal\.config\herdr-app\keys.json`), pegado
  por el usuario. **herdr-app no usa prefijo**: todo son acordes directos (Ctrl+Shift+…, Alt+…).
  El prefijo Ctrl+B solo existe en el herdr clásico (TUI) del VPS, que es lo antiguo y no va en la
  capa.
- **Activación:** mantener el pulgar exterior derecho (posición 49, ahora RGUI y casi sin uso).
- **Propuesta de capa (letra → acción):**
  ```
  ·  F1cab F2muro F3equ F5met  L·layout      tab←  tab→  agente↑ agente↓  paleta  barra
  ·  A·acc  S·split→ D·split↓ F·frentes G·nav    foco←  foco↓  foco↑  foco→   ·      ·
  ✕tab Z·zoom X·✕panel C·+tab V·renombrar B·+space  ··  ··    mover← mover↓ mover↑ mover→ ·  ·
  ```
  | Tecla | Acordes que manda | Acción |
  |---|---|---|
  | Q W E R | Alt+F1 / F2 / F3 / F5 | cabina / muro / equipo / métricas |
  | T | Ctrl+Shift+L | alternar layout |
  | A · F · G | Alt+Shift+A / C / N | barra de acciones / barra de frentes / navegar frentes |
  | S · D | Ctrl+Shift+O / E | dividir a la derecha / abajo |
  | Z · X | Ctrl+Shift+Z / X | zoom / cerrar panel |
  | C · V · B | Ctrl+Shift+T / F2 / Ctrl+Shift+N | pestaña nueva / renombrar / espacio nuevo |
  | posición 24 (esquina) | Ctrl+Shift+W | cerrar pestaña (en la esquina para no darle sin querer) |
  | H J K L | Alt+H/J/K/L | foco entre paneles |
  | N M , . | Alt+Shift+H/J/K/L | intercambiar paneles |
  | Y U | Ctrl+Shift+Tab / Ctrl+Tab | pestaña anterior / siguiente |
  | I O | Alt+↑ / Alt+↓ | agente anterior / siguiente |
  | P · posición 11 | Ctrl+Shift+P / Ctrl+Shift+B | paleta / barra lateral |
- **Con la distribución española:** `alt-[` y `alt-]` no se pueden usar (en español [ ] van con
  AltGr), así que se usa Ctrl+Tab. Para la ayuda va la paleta en lugar de `ctrl-?`. El zoom de la app
  `ctrl--` usa la tecla física `FSLH`.
- **Sin conflicto con Teams:** herdr-app y Teams comparten algunos acordes (Ctrl+Shift+O/E/K…), pero
  cada uno solo responde con su ventana activa.
- **Espacios y pestañas por número:** Alt+1…9 (espacios) y Ctrl+1…9 (pestañas) ya salen con los
  modificadores del pulgar y la capa NUMS. Si se quiere un acceso más directo, queda para una
  segunda iteración.
- **Subtareas:**
  - [x] Validar la disposición con el usuario (2026-11-13: «me interesa mucho capa herdr», se implementa la propuesta y se ajusta tras probar)
  - [x] Implementar la capa
  - [x] README, kyria-layout.json y PDF
  - [x] 2026-11-13: un toque a la tecla HERDR envía Win+1 y pone delante herdr-app (anclada la 1ª en la barra de tareas). Si ya está delante, Windows podría minimizarla: comprobarlo. Lo ideal es que la lanzadera active la ventana al recibir F18 (#17).
  - [ ] Prueba en herdr-app
- **Test plan:** en herdr-app, cada tecla de la capa hace su acción.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #15 Macros de texto para mma
- **Sprint:** 3
- **Estado:** 🟢 PENDIENTE
- **Valor:** medio · **Coste:** S
- **Descripción:** `mma` (`~/mma`) es el espacio del asistente personal de gestión (Claude Code o
  Copilot sobre un vault de Obsidian en el VPS). Macros que escriben los comandos más repetidos:
  - `cd ~/mma && claude` + Enter (lo que más se repite). Ojo: «~» es una tecla muerta en español y
    «&» es Shift+6, así que la macro tiene que usar las definiciones `ES_*` de #5.
  - `frente ` (deja el cursor para escribir el número y la acción), `hc ls` + Enter
  - `herdr-app do layout.switch --name mma-indra` + Enter (la variante Indra no tiene atajo)
- **Dónde:** en la capa HERDR, en posiciones de la mano izquierda que no use herdr.
- **Depende de:** #5
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

---

## Sprint 4 — Ratón, orden y documentación
**Objetivo:** que lo que ya está a medias funcione y que el teclado se entienda sin abrir el código.
**Estado sprint:** 0/3 cerrados

### #12 Capa MOUSE que funcione
- **Sprint:** 4
- **Estado:** 🟢 PENDIENTE
- **Valor:** medio · **Coste:** M
- **Descripción:** ahora mismo no hay ninguna tecla que active la capa MOUSE (ahora la 3). Además usa
  `&kp K_SCROLL_*` (no hace scroll de ratón) y le falta el movimiento del cursor.
- **Subtareas:**
  - [ ] Activarla desde TEXT (por ejemplo TEXT + O → `&tog MOUSE`)
  - [ ] Movimiento con `&mmv` en I/J/K/L, scroll con `&msc` y clics en la mano izquierda
  - [ ] Salir con Esc o Q (`&to DEFAULT`, ya existe)
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #13 Limpieza del keymap y la configuración
- **Sprint:** 4
- **Estado:** 🟢 PENDIENTE
- **Valor:** bajo · **Coste:** S
- **Descripción:** borrar `hm` (definido y sin usar), poner los nombres de propiedades al estilo
  actual (`tapping-term-ms`), corregir los dibujos ASCII de cada capa (no coinciden con la
  configuración real) y quitar de `kyria.conf` los comentarios que ya no aplican.
- **Ficheros:** `config/kyria.keymap`, `config/kyria.conf`
- **Añadido:** 2026-11-12

### #14 README con mapa visual (keymap-drawer)
- **Sprint:** 4
- **Estado:** 🟡 EN CURSO. 2026-11-13: README.md, docs/procedimientos.md y docs/kyria-layout.json (datos de las capas para la lanzadera de mma). Falta: keymap-drawer
- **Valor:** medio · **Coste:** M
- **Descripción:** README que explique cómo flashear y cada capa, más un SVG del mapa generado
  automáticamente con keymap-drawer en un GitHub Action. Debe mostrar los caracteres en español.
- **Ficheros:** `README.md`, `.github/workflows/draw.yml`, `keymap-drawer/config.yaml`
- **Añadido:** 2026-11-12

---

### #16 Capa de acentos con AltGr ✅ HECHO (2026-11-12)
- **Sprint:** 2 · **Valor:** alto · **Coste:** S
- **Descripción:** el usuario prefiere poner los acentos con AltGr, como en EE. UU.-Internacional, pero sin cambiar Windows. Al mantener el pulgar º se abre la capa ACC (5): A E I O U dan á é í ó ú (macro ´ + vocal; con Shift salen Á É Í Ó Ú gracias a un mod-morph que quita el Shift de la ´), Y da ü, N da ñ y la tecla de - da ¿. Si se pulsa sin mantener, sale º. El pulgar deja de ser AltGr, pero los símbolos que lo necesitaban ya están en SYM.
- **Prueba física:** «Canción, pingüino, ¿Ómnibus? Él añadió más.»
- **Ficheros:** config/kyria.keymap

### #17 Avisar al PC de la capa activa (para la chuleta de la lanzadera mma)
- **Sprint:** 3 · **Estado:** 🟡 EN CURSO. Firmware hecho el 2026-11-13; falta activarlo cuando la lanzadera escuche
- **Valor:** alto · **Coste:** M
- **Descripción:** ZMK no le dice al PC qué capa está activa. Ahora las teclas de capa son macros
  (`ls_sym`, `ls_nums`, `ls_text`, `ls_acc`): `&mo` y, si `SENAL_CAPAS` = 1, un toque de F13 (SYM),
  F14 (NUMS), F15 (TEXT), F16 (ACC) o F18 (HERDR, `ls_herdr`) al entrar y de F19 al salir. F17 (MOUSE)
  queda reservada. F20 no se usa porque ya está en TEXT.
- **Por qué está en 0:** sin un programa que se coma esas teclas, una terminal (herdr-app) podría
  recibir F13–F19 como secuencias de escape y escribir basura.
- **Subtareas:**
  - [x] Macros de capa para SYM, NUMS y TEXT
  - [x] ACC: el hold-tap `acc` usa `ls_acc` como binding de hold
  - [x] Comprobar con cpp que las dos variantes (0 y 1) expanden bien
  - [ ] Flashear con 0 y comprobar que las capas funcionan igual que antes
  - [ ] Cuando la lanzadera escuche y bloquee F13–F19: poner 1, compilar y probar en Teams, herdr-app y el navegador
- **Ficheros:** config/kyria.keymap · **Depende de:** lanzadera mma
- **Añadido:** 2026-11-13

## 📅 Diferido

- **Home row mods** (Ctrl, Alt, Win y Shift en la fila central): reducen las combinaciones, pero
  necesitan ajuste fino. Se valora cuando el Sprint 1 esté estable.
- **Combos** (por ejemplo J+K = Esc, o pulsar dos teclas a la vez para un atajo).
- **Encoders, OLED o RGB:** solo si el hardware los tiene (`kyria.conf` los trae comentados).
- ~~Repasar el modo juego~~: capa GAME eliminada el 2026-11-12 (el usuario no la usa). MOUSE pasa a ser la capa 3 y SYM la 4.
- **Trackball PMW3610 (futuro):** el teclado aún no lo lleva. La rama `origin/PWM3610Add` (jun-2024) fue
  solo una prueba y queda de referencia. La capa MOUSE (#12) se diseña sin él, pero dejando sitio
  para clics y scroll cuando llegue.
- **Recolocar º** (la ç ya se quitó el 2026-11-12: el usuario no la usa; su sitio es ahora el botón del micro) (`BSLH` y `GRAVE` ocupan sitios buenos y se usan poco).

---

## ✅ Historial de sprints cerrados

- **Sprint 1 — Base fiable** (cerrado 2026-11-12): #1 `edc6311`, #2 `5c747ef`, #3 `d558b1c`, #4 `f9055c5`/`8954b51`.
- **Sprint 2 — Símbolos y acentos** (cerrado 2026-11-13): #5 #6 #7 `c7118b5`, #16 (ACC). #8 pasa al Sprint 3.
  Lección: con la distribución española casi todo símbolo necesita una macro `ES_*`; el mod-morph
  resuelve las mayúsculas acentuadas sin tocar Windows.

---

## 📝 Historial de replanificaciones

- 2026-11-12 — Backlog inicial, creado a partir de la revisión del repo y de la conversación con el
  usuario.
- 2026-11-12 — Teams confirmado: #10 pasa de BLOQUEADO a PENDIENTE y se amplía a chats y archivos.
  #11 sigue bloqueado; se han pedido los datos de herdr y mma a la sesión `mma-e0`.
- 2026-11-12 — `mma-e0` responde con los atajos de herdr y herdr-app. #11 se rediseña como capa
  HERDR y deja de estar bloqueado (solo falta confirmar `keys.json`). Nuevo #15 para las macros de
  texto de mma.
- 2026-11-12 — El `keys.json` real de herdr-app no tiene prefijo: #11 se rehace con acordes directos.
- 2026-11-13 — Se cierra el Sprint 2. #8 (copiar/pegar) pasa al Sprint 3, a petición del usuario, y se hace junto con #11 (capa HERDR).
