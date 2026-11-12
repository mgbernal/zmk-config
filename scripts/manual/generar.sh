#!/bin/sh
# Regenera docs/manual-kyria.pdf a partir de docs/kyria-layout.json.
# Necesita python3 y chrome-headless-shell (o chromium). Las fuentes (OFL) se descargan la primera vez.
set -e
cd "$(dirname "$0")"
mkdir -p fonts
G=https://github.com/google/fonts/raw/main/ofl
for f in ChakraPetch-Medium ChakraPetch-SemiBold ChakraPetch-Bold; do
  [ -f fonts/$f.ttf ] || curl -sfL -o fonts/$f.ttf "$G/chakrapetch/$f.ttf"
done
[ -f fonts/JetBrainsMono.ttf ] || curl -sfL -o fonts/JetBrainsMono.ttf "$G/jetbrainsmono/JetBrainsMono%5Bwght%5D.ttf"
python3 gen.py ../../docs/kyria-layout.json manual.html
CHROME=${CHROME:-$(ls ~/.cache/ms-playwright/chromium_headless_shell-*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | tail -1)}
"$CHROME" --no-sandbox --disable-gpu --no-pdf-header-footer --print-to-pdf=../../docs/manual-kyria.pdf "file://$PWD/manual.html"
rm manual.html
