#!/usr/bin/env bash
# Gerekli paketleri ve Türkçe ses modelini kurar (her yeni oturumda bir kez çalıştırılır).
set -e
pip install --break-system-packages -q piper-tts skia-python soundfile scipy numpy pillow 2>&1 | grep -v -E "WARNING|dependency|requires" || true
C="$HOME/.cache/nedenboyle"; mkdir -p "$C"
if [ ! -f "$C/vits-piper-tr_TR-fahrettin-medium/tr_TR-fahrettin-medium.onnx" ]; then
  curl -sSL -o "$C/v.tar.bz2" https://github.com/k2-fsa/sherpa-onnx/releases/download/tts-models/vits-piper-tr_TR-fahrettin-medium.tar.bz2
  tar xjf "$C/v.tar.bz2" -C "$C" && rm "$C/v.tar.bz2"
fi
echo "kurulum tamam"
