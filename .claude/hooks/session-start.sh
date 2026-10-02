#!/bin/bash
# Installs the GBA toolchain in Claude Code cloud sessions so `make` works.
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
command -v arm-none-eabi-gcc >/dev/null && exit 0
export DEBIAN_FRONTEND=noninteractive
apt-get update -q >/dev/null
apt-get install -y -q gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-arm-none-eabi libpng-dev >/dev/null
