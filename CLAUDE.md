# zmk-config — Kyria del usuario

Firmware ZMK de un Kyria (50 teclas, nice!nano v1). Repositorio: github.com/mgbernal/zmk-config.

## Lo que hay que saber antes de tocar el keymap
- **Windows usa la distribución Español.** ZMK envía códigos US y Windows los traduce, así que los
  símbolos se escriben con las macros `ES_*` de `config/es_keys.h`, nunca con `&kp LPAR`, `&kp AT`, etc.
- **Capas:** 0 Base · 1 NUMS · 2 TEXT · 3 MOUSE · 4 SYM · 5 ACC (acentos). Si añades o quitas una
  capa, renumera los `#define` porque el número es el orden en el fichero.
- **Posiciones:** fila 0 = 0–11, fila 1 = 12–23, fila 2 = 24–39 (30–33 son los pulgares de arriba),
  pulgares = 40–49.
- **Behaviors propios:** `smt` (mod-tap seguro para espacios y pulgares), `acc` (pulgar º → capa de
  acentos), macros `es_grv`/`es_circ`/`es_tild` y `acc_*` (vocales con tilde).
- La versión de ZMK está fijada en `config/west.yml` y en `.github/workflows/build.yml` (el mismo
  commit en los dos). Solo se actualiza a propósito.

## Flujo de trabajo
1. Editar `config/kyria.keymap`.
2. `python3 scripts/check_keymap.py` (también lo ejecuta el hook pre-commit de `.githooks/` y el CI).
3. Commit con mensaje `tipo: descripción` en español, y stagear ficheros concretos.
4. Push solo si el usuario lo pide: `git push` (origin usa la deploy key SSH `github-zmk`, que solo
   tiene acceso a este repositorio).
5. GitHub Actions compila. El firmware es el artefacto `firmware` de la ejecución
   (https://github.com/mgbernal/zmk-config/actions); el usuario lo descarga y flashea las dos mitades.

## Documentación
- Backlog y estado: `docs/sprints/backlog.md` (skill project-sprints).
- Mapa visual de las capas: artefacto «Mapa del Kyria», https://claude.ai/artifact/Q3eK33p1P4ezNbGABvrzW9.
  Hay que actualizarlo cuando cambie el keymap.
