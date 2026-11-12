#!/usr/bin/env python3
"""Validación rápida de config/kyria.keymap sin toolchain de ZMK.

Comprueba:
  - que cada capa tenga exactamente KEYS bindings (Kyria = 50 teclas),
  - que las referencias a capas (&mo, &tog, &to, &lt, &sl) existan,
  - que las macros ES_* usadas estén definidas,
  - que los comportamientos propios usados (&xxx) estén declarados o sean de ZMK.

Uso: python3 scripts/check_keymap.py [ruta_keymap]
"""
import re
import sys
from pathlib import Path

KEYS = 50
ROOT = Path(__file__).resolve().parent.parent
KEYMAP = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "config" / "kyria.keymap"

# Comportamientos que trae ZMK (los que usamos o podríamos usar).
ZMK_BEHAVIORS = {
    "kp", "mt", "lt", "mo", "to", "tog", "sl", "sk", "trans", "none", "gresc",
    "bt", "out", "ext_power", "rgb_ug", "bl", "mkp", "mmv", "msc", "caps_word",
    "key_repeat", "sys_reset", "bootloader", "studio_unlock", "soft_off",
}


def strip_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    return re.sub(r"//[^\n]*", "", text)


def main() -> int:
    raw = KEYMAP.read_text(encoding="utf-8")
    errors: list[str] = []

    # #define NOMBRE valor  (se leen antes de quitar comentarios para no perder ninguno)
    defines = dict(re.findall(r"^\s*#define\s+(\w+)\s+(.+?)\s*$", raw, flags=re.M))
    # incluir cabeceras locales (p. ej. es_keys.h)
    for inc in re.findall(r'^\s*#include\s+"([^"]+)"', raw, flags=re.M):
        path = KEYMAP.parent / inc
        if path.exists():
            defines.update(re.findall(r"^\s*#define\s+(\w+)\s+(.+?)\s*$",
                                      path.read_text(encoding="utf-8"), flags=re.M))
        else:
            errors.append(f"#include \"{inc}\" no existe")

    text = strip_comments(raw)

    # Comportamientos propios: etiqueta: nombre { compatible = ...
    custom = set(re.findall(r"\b(\w+)\s*:\s*[\w-]+\s*\{", text))

    km = re.search(r"\bkeymap\s*\{(.*)\};\s*\};?\s*$", text, flags=re.S)
    if not km:
        print("ERROR: no encuentro el nodo keymap")
        return 1
    layers = re.findall(r"(\w+)\s*\{[^{}]*?bindings\s*=\s*<(.*?)>\s*;", km.group(1), flags=re.S)
    n_layers = len(layers)

    def resolve(tok: str) -> str:
        seen = 0
        while tok in defines and seen < 10:
            tok = defines[tok].split("//")[0].strip()
            seen += 1
        return tok

    for idx, (name, body) in enumerate(layers):
        bindings = re.findall(r"&\w+(?:\s+(?!&)[^\s&]+)*", body)
        if len(bindings) != KEYS:
            errors.append(f"capa {idx} '{name}': {len(bindings)} bindings (esperados {KEYS})")
        for b in bindings:
            parts = b.split()
            beh = parts[0][1:]
            if beh not in ZMK_BEHAVIORS and beh not in custom:
                errors.append(f"capa '{name}': comportamiento desconocido &{beh}")
            if beh in {"mo", "tog", "to", "sl", "lt"} and len(parts) > 1:
                val = resolve(parts[1])
                if not val.isdigit() or int(val) >= n_layers:
                    errors.append(f"capa '{name}': &{beh} {parts[1]} -> capa inexistente ({val})")
            for p in parts[1:]:
                for m in re.findall(r"\bES_\w+", p):
                    if m not in defines:
                        errors.append(f"capa '{name}': {m} no está definido")

    # macros ES_* usadas fuera de las capas (macros, combos...)
    for m in set(re.findall(r"\bES_\w+", text)):
        if m not in defines:
            errors.append(f"{m} usado pero no definido")

    print(f"{KEYMAP.name}: {n_layers} capas")
    for idx, (name, body) in enumerate(layers):
        n = len(re.findall(r"&\w+(?:\s+(?!&)[^\s&]+)*", body))
        print(f"  {idx} {name:<14} {n} bindings")
    if errors:
        print("\nERRORES:")
        for e in sorted(set(errors)):
            print(f"  - {e}")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
