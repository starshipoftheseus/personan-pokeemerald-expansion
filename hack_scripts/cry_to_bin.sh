#!/bin/sh
# Converts a cry .wav to the compressed .bin the game includes.
# Cries recorded above CRY_SAMPLE_RATE are resampled down first to save ROM space
# (see design/rom_budget.md). Called from audio_rules.mk:
#   cry_to_bin.sh <wav2agb> <rate, 0 = keep original> <in.wav> <out.bin>
set -e
WAV2AGB=$1
RATE=$2
IN=$3
OUT=$4

if [ "$RATE" -gt 0 ]; then
    if ! command -v sox >/dev/null 2>&1; then
        echo "error: sox is needed to resample cries (apt-get install sox), or set CRY_SAMPLE_RATE := 0 in audio_rules.mk" >&2
        exit 1
    fi
    SRC_RATE=$(sox --i -r "$IN")
    if [ "$SRC_RATE" -gt "$RATE" ]; then
        TMP="${OUT%.bin}.resampled.wav"
        # -D: no dither, so builds are reproducible. -G: lower gain only where resampling would clip.
        sox -D -G "$IN" -b 8 -e unsigned-integer -c 1 "$TMP" rate -v "$RATE"
        # NOTE: If using ipatix's High Quality Audio Mixer, remove "--no-pad" below.
        "$WAV2AGB" -b -c -l 1 --no-pad "$TMP" "$OUT"
        rm -f "$TMP"
        exit 0
    fi
fi

# NOTE: If using ipatix's High Quality Audio Mixer, remove "--no-pad" below.
"$WAV2AGB" -b -c -l 1 --no-pad "$IN" "$OUT"
