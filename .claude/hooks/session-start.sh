#!/bin/bash
# Installs the build tools in Claude Code cloud sessions so `make hns` works:
# the GBA toolchain, plus sox for resampling cries (see audio_rules.mk).
set -euo pipefail
[ "${CLAUDE_CODE_REMOTE:-}" = "true" ] || exit 0
command -v arm-none-eabi-gcc >/dev/null && command -v sox >/dev/null && exit 0
export DEBIAN_FRONTEND=noninteractive
apt-get update -q >/dev/null
apt-get install -y -q gcc-arm-none-eabi binutils-arm-none-eabi libnewlib-arm-none-eabi libpng-dev sox >/dev/null
