# Kyria · firmware ZMK

Configuración del teclado partido **Kyria** (50 teclas, controladores **nice!nano v1**, Bluetooth) con
[ZMK](https://zmk.dev). Está pensado para trabajar en Windows con la distribución **Español**:
reuniones y chats en Teams, notas, mma y herdr.

Mapa visual de todas las capas: [Mapa del Kyria](https://claude.ai/artifact/Q3eK33p1P4ezNbGABvrzW9).

## Capas

| Nº | Capa | Cómo se activa | Para qué |
|---|---|---|---|
| 0 | Base | siempre | QWERTY con ñ y ´; arriba a la derecha, micro de Teams (Win+Alt+K) |
| 1 | NUMS | mantener el pulgar NUMS (derecho) | números, F1–F12, teclado numérico |
| 2 | TEXT | mantener una de las teclas TEXT (pulgares de arriba) | flechas, páginas, multimedia, Bluetooth |
| 3 | MOUSE | ninguna, de momento (ticket #12) | clics de ratón |
| 4 | SYM | mantener el pulgar SYM (izquierdo, junto a Win) | todos los símbolos a una tecla |
| 5 | ACC | mantener el pulgar º (derecho) | á é í ó ú ü ñ ¿, como AltGr en EE. UU.-Internacional |

Los espacios hacen de Shift si se mantienen, pero solo cuando no se viene tecleando. Así, al escribir
rápido no salen mayúsculas pegadas.

## Estructura

```
config/kyria.keymap      keymap: capas, behaviors y macros
config/es_keys.h         macros ES_* (símbolo → tecla física con la distribución Español)
config/kyria.conf        opciones de ZMK (Kconfig)
config/west.yml          versión de ZMK (fijada a un commit)
build.yaml               qué se compila: mitad izquierda, derecha y settings_reset
scripts/check_keymap.py  validación rápida del keymap, sin compilar
.github/workflows/       CI: validar → compilar → (con etiqueta fw-*) publicar Release
.githooks/pre-commit     ejecuta check_keymap.py antes de cada commit
docs/sprints/backlog.md  backlog de cambios y su estado
docs/procedimientos.md   cómo trabajar con GitHub, flashear y volver atrás
docs/manual-kyria.pdf    manual imprimible (A4 apaisado); se regenera con scripts/manual/generar.sh
```

## Uso rápido

1. Cambia `config/kyria.keymap`. Escribe los símbolos con `ES_*`, nunca con `&kp AT` ni similares.
2. `python3 scripts/check_keymap.py`
3. Haz commit y push. GitHub Actions compila en unos 5 minutos.
4. Descarga el artefacto `firmware` de la ejecución y flashea las dos mitades.

El detalle de cada paso, cómo probar cambios grandes en una rama y cómo volver a un firmware
anterior está en [docs/procedimientos.md](docs/procedimientos.md).

## Primera vez en un equipo nuevo

```sh
git clone git@github.com:mgbernal/zmk-config.git
cd zmk-config
git config core.hooksPath .githooks   # activa la validación antes de cada commit
```
