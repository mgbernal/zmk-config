# zmk-config (Kyria) — Sprint Backlog

**Última actualización:** 2026-11-12
**Sprint activo:** Sprint 1

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
**Estado sprint:** 0/4 cerrados

### #1 Mayúsculas accidentales y espacios perdidos (Espacio/Shift)
- **Sprint:** 1
- **Estado:** 🟢 PENDIENTE
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
- **Estado:** 🟢 PENDIENTE
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
- **Estado:** 🟢 PENDIENTE
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
- **Estado:** 🟢 PENDIENTE
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
**Estado sprint:** 0/4 cerrados

### #5 Definiciones para la distribución española (`es_keys.h`)
- **Sprint:** 2
- **Estado:** 🟢 PENDIENTE
- **Valor:** alto · **Coste:** S
- **Descripción:** cabecera con nombres legibles que encapsulan la traducción US→ES, por ejemplo
  `ES_AT = RA(N2)`, `ES_LBRC = RA(LBKT)`, `ES_LCBR = RA(SQT)`, `ES_PIPE = RA(N1)`,
  `ES_BSLH = RA(GRAVE)`, `ES_EURO = RA(E)`, `ES_LT = NON_US_BSLH`, `ES_QUES = LS(MINUS)`,
  `ES_IQUE = LS(EQUAL)`…
- **Ficheros:** `config/es_keys.h`, `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #6 Capa SYM accesible con el pulgar
- **Sprint:** 2
- **Estado:** 🟢 PENDIENTE
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
- **Estado:** 🟢 PENDIENTE
- **Valor:** medio · **Coste:** S
- **Descripción:** en español, «`», «^», «~» y «¨» son teclas muertas: hay que pulsar espacio después.
  Se crean macros (tecla + espacio) para que salgan de un toque desde la capa SYM. La tilde «´» se
  queda muerta en la tecla `SQT` de la capa base, porque así es como se escriben los acentos.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #8 Arreglar la tecla de copiar/pegar
- **Sprint:** 2
- **Estado:** 🟢 PENDIENTE
- **Valor:** medio · **Coste:** S
- **Descripción:** `&mt LC(C) LC(V)` en modo `hold-preferred` copia por error si se pulsa otra tecla
  durante el toque. Se cambia por un hold-tap `tap-preferred` (toque = pegar, mantener = copiar).
  Valorar también añadir cortar y deshacer.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

---

## Sprint 3 — Atajos de trabajo (reuniones, notas, herdr)
**Objetivo:** que cualquier atajo de varias teclas se haga con la capa TEXT y una sola tecla.
**Estado sprint:** 0/4 cerrados

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
- **Estado:** 🟢 PENDIENTE — Teams confirmado el 2026-11-12; falta saber cómo funciona hoy F20
- **Valor:** alto · **Coste:** M
- **Descripción:** Teams es la herramienta corporativa principal: reuniones, chats y archivos. Se
  agrupan sus atajos en la mano izquierda de la capa TEXT, junto a F20 (posición 29):
  - **Reunión:** micro Ctrl+Shift+M · cámara Ctrl+Shift+O · levantar la mano Ctrl+Shift+K ·
    compartir pantalla Ctrl+Shift+E · colgar Ctrl+Shift+H · aceptar llamada Ctrl+Shift+A ·
    rechazarla Ctrl+Shift+D
  - **Navegación:** buscar Ctrl+E · chat nuevo Ctrl+N · Ctrl+1…6 para Actividad, Chat, Teams,
    Calendario, Llamadas y Archivos (el orden depende de cómo esté anclada la barra lateral, hay que
    comprobarlo)
  - **Escribir:** abrir el cuadro de redacción grande Ctrl+Shift+X (útil para notas largas en un
    chat)
- **Nota:** los atajos Ctrl+Shift+… solo funcionan con la ventana de Teams activa. El micro global
  queda en F20; hay que confirmar qué lo gestiona (¿PowerToys u otra herramienta?) para no duplicar.
- **Subtareas:**
  - [ ] Comprobar el orden de Ctrl+1…6 en el Teams del usuario
  - [ ] Confirmar qué hace F20 hoy
  - [ ] Proponer la colocación y validarla con el usuario
  - [ ] Implementar
- **Test plan:** en una reunión de prueba, cada tecla hace su acción; en el chat, buscar y crear
  chat nuevo.
- **Ficheros:** `config/kyria.keymap`
- **Añadido:** 2026-11-12

### #11 Capa HERDR: cada acción con una sola tecla
- **Sprint:** 3
- **Estado:** 🟢 PENDIENTE — falta confirmar `keys.json` de herdr-app en el portátil (¿el prefijo
  sigue siendo Ctrl+B?)
- **Valor:** alto · **Coste:** M
- **Datos (de la sesión `mma-e0`, 2026-11-12):** el uso diario es **herdr-app**, una ventana nativa
  en Windows (la «cabina MMA») conectada a los agentes del VPS. El prefijo por defecto es
  **Ctrl+B**: se pulsa, se suelta y luego va la tecla de la acción.
- **Diseño:** capa nueva **HERDR** que se activa manteniendo el pulgar exterior derecho (posición
  49, ahora RGUI y casi sin uso). La regla es sencilla: **HERDR + tecla = Ctrl+B y luego esa tecla**,
  de modo que lo que ya sabes de herdr sigue valiendo, pero en un solo gesto. Cada tecla es una macro
  `Ctrl+B, <tecla>`.
  - Letras directas: `a` tablero · `c` nueva pestaña · `n`/`p` pestaña siguiente/anterior ·
    `v` split vertical · `x` cerrar panel · `z` zoom · `h j k l` mover el foco entre paneles ·
    `r` redimensionar · `w` workspaces · `g` goto · `b` barra lateral · `o` notificación ·
    `e` scrollback · `s` ajustes · `q` detach · Tab/Shift+Tab panel siguiente/anterior
  - Números 1…9 → pestaña N (en la fila de arriba de la capa)
  - Con Shift (HERDR + Shift + letra): `T` renombrar pestaña · `X` cerrar pestaña · `N` nuevo
    workspace · `W` renombrar workspace · `D` cerrar workspace · `G` nuevo worktree · `R` recargar
    config · `P` renombrar panel. Hay que decidir si se hace con mod-morph o con teclas aparte.
  - Split horizontal «-»: la macro manda la tecla **física** `FSLH`, porque con la distribución
    española `MINUS` saca «'». Ayuda «?»: se manda `LS(MINUS)`.
- **Cabina MMA (atajos propios de herdr-app, en la fila de arriba o en los pulgares de la capa):**
  Alt+F1 cabina · Alt+F2 muro de agentes · Alt+F3 equipo · Alt+F5 métricas · Alt+Shift+C barra de
  frentes · Alt+Shift+A barra de acciones · Alt+Shift+N navegar frentes · Ctrl+Shift+L alternar
  muro/cabina. Ctrl+Alt+Shift+Esc (escape de emergencia) va en una posición difícil de pulsar sin
  querer.
- **Restricciones:**
  - No usar acordes Ctrl+Alt+letra propios: en Windows AltGr = Ctrl+Alt y chocan con @ # € [ ] { }.
  - Nunca generar Alt+F4 (cierra la ventana).
  - herdr-bar (`herdr-bar.open`) no tiene atajo, y `prefix+k` choca con mover el foco arriba. Si se
    quiere, hay que asignarlo antes en `keys.json` (propuesta: `prefix+space`) y después mapearlo.
- **Subtareas:**
  - [ ] El usuario confirma en el portátil el prefijo de `keys.json` de herdr-app
  - [ ] Decidir el atajo de herdr-bar en `keys.json` (opcional)
  - [ ] Implementar la capa HERDR con macros
  - [ ] Añadirla al README y al dibujo del keymap (#14)
- **Test plan:** en herdr-app, cada tecla de la capa hace su acción: split, cambiar de pestaña,
  zoom, tablero, cabina con Alt+F1…
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
- **Descripción:** ahora mismo no hay ninguna tecla que active la capa 4. Además usa
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
- **Estado:** 🟢 PENDIENTE
- **Valor:** medio · **Coste:** M
- **Descripción:** README que explique cómo flashear y cada capa, más un SVG del mapa generado
  automáticamente con keymap-drawer en un GitHub Action. Debe mostrar los caracteres en español.
- **Ficheros:** `README.md`, `.github/workflows/draw.yml`, `keymap-drawer/config.yaml`
- **Añadido:** 2026-11-12

---

## 📅 Diferido

- **Home row mods** (Ctrl, Alt, Win y Shift en la fila central): reducen las combinaciones, pero
  necesitan ajuste fino. Se valora cuando el Sprint 1 esté estable.
- **Combos** (por ejemplo J+K = Esc, o pulsar dos teclas a la vez para un atajo).
- **Encoders, OLED o RGB:** solo si el hardware los tiene (`kyria.conf` los trae comentados).
- **Repasar el modo juego** (capa 3).
- **Recolocar ç y º** (`BSLH` y `GRAVE` ocupan sitios buenos y se usan poco).

---

## ✅ Historial de sprints cerrados

_(vacío)_

---

## 📝 Historial de replanificaciones

- 2026-11-12 — Backlog inicial, creado a partir de la revisión del repo y de la conversación con el
  usuario.
- 2026-11-12 — Teams confirmado: #10 pasa de BLOQUEADO a PENDIENTE y se amplía a chats y archivos.
  #11 sigue bloqueado; se han pedido los datos de herdr y mma a la sesión `mma-e0`.
- 2026-11-12 — `mma-e0` responde con los atajos de herdr y herdr-app. #11 se rediseña como capa
  HERDR y deja de estar bloqueado (solo falta confirmar `keys.json`). Nuevo #15 para las macros de
  texto de mma.
