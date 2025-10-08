'''
seq_to_midi.py

A simple Python tool to convert a step-sequencer style melody or chords into a MIDI file.

Usage:
    1. Install dependencies:
         pip install midiutil
    2. Run with your sequence argument (supports notes, rests, sustains, and **block chords**):
         python seq_to_midi.py \
           --sequence '[ ["A#3","-","D#4","-"], ... ]' \
           --output my_melody.mid \
           [--bpm 120] [--steps-per-bar 4] [--velocity 100] [--channel 0]

    • **Values per step**:
        - "A#3"  → single note
        - ["A#3","D#4","F#4"] → block chord (all notes start together)
        - "-"    → sustain previous step (extends last note *or chord*)
        - "."    → rest

It will generate the specified MIDI file in the current directory.
'''
import argparse
import json
import re
from typing import List, Union
from midiutil import MIDIFile

# Mapping for note names to semitones
NOTE_BASE = {
    'C': 0, 'C#': 1, 'Db': 1, 'D': 2, 'D#': 3, 'Eb': 3,
    'E': 4, 'F': 5, 'F#': 6, 'Gb': 6, 'G': 7, 'G#': 8,
    'Ab': 8, 'A': 9, 'A#': 10, 'Bb': 10, 'B': 11
}


def note_to_midi(note_str: str) -> int:
    """Convert note name (e.g. 'A#3') to MIDI note number."""
    m = re.match(r"^([A-G][#b]?)(-?\d+)$", note_str)
    if not m:
        raise ValueError(f"Invalid note: {note_str}")
    name, octave = m.groups()
    semitone = NOTE_BASE[name]
    octave = int(octave)
    # MIDI: C-1 = 0, C0 = 12, C4 = 60
    return 12 * (octave + 1) + semitone


StepValue = Union[str, List[str]]


def main():
    parser = argparse.ArgumentParser(
        description="Convert a step-sequencer style melody/chords into a MIDI file."
    )
    parser.add_argument(
        '--sequence', '-s', required=True,
        help=(
            "JSON list of bars; each bar is a list of steps. Steps can be 'note' strings, "
            "lists of note strings (block chords), '-' for sustain, or '.' for rest."
        )
    )
    parser.add_argument(
        '--output', '-o', default='output.mid',
        help="Output MIDI filename (default: output.mid)."
    )
    parser.add_argument(
        '--bpm', type=int, default=120,
        help="Tempo in BPM (default: 120)."
    )
    parser.add_argument(
        '--steps-per-bar', type=int, default=4,
        help="Number of steps per bar (default: 4)."
    )
    parser.add_argument(
        '--velocity', type=int, default=100,
        help="MIDI velocity for notes 1–127 (default: 100)."
    )
    parser.add_argument(
        '--channel', type=int, default=0,
        help="MIDI channel 0–15 (default: 0)."
    )
    args = parser.parse_args()

    try:
        sequence: List[List[StepValue]] = json.loads(args.sequence)
    except json.JSONDecodeError as e:
        raise SystemExit(f"Error parsing sequence JSON: {e}")

    beats_per_bar = 4
    midi = MIDIFile(1)
    midi.addTempo(track=0, time=0, tempo=args.bpm)

    flat: List[tuple] = []
    for bar_idx, bar in enumerate(sequence):
        if len(bar) != args.steps_per_bar:
            raise SystemExit(f"Bar {bar_idx+1} has {len(bar)} steps; expected {args.steps_per_bar}.")
        for step_idx, val in enumerate(bar):
            flat.append((bar_idx, step_idx, val))

    # Iterate through flattened steps
    i = 0
    while i < len(flat):
        bar_idx, step_idx, val = flat[i]

        if val == '.' or val == '-':
            i += 1
            continue
        if isinstance(val, str):
            notes_this_step = [val]
        elif isinstance(val, list):
            if not val:
                i += 1
                continue
            notes_this_step = val
        else:
            raise SystemExit(f"Unsupported step value at bar {bar_idx+1}, step {step_idx+1}: {val}")

        start_time = bar_idx * beats_per_bar + step_idx * (beats_per_bar / args.steps_per_bar)

        duration = 1  # one step = one beat
        j = i + 1
        while j < len(flat) and flat[j][2] == '-':
            duration += 1
            j += 1

        for note_name in notes_this_step:
            pitch = note_to_midi(note_name)
            midi.addNote(
                track=0,
                channel=args.channel,
                pitch=pitch,
                time=start_time,
                duration=duration,
                volume=max(1, min(args.velocity, 127))
            )
        i = j

    with open(args.output, 'wb') as outf:
        midi.writeFile(outf)

    print(f"MIDI file written to {args.output}")


if __name__ == '__main__':
    main()