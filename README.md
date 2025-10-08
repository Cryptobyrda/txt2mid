# seq_to_midi - Text to midi tool

A minimal Python tool that converts a **step-sequencer-style text sequence** into a **MIDI file**, ideal for quick idea generation, prototyping, or use with language models.

The new thing here, is creating a structure that a LM can use to create melodies.

This script supports:
- Monophonic and **block chords**
- **Sustains** (`-`) and **rests** (`.`)
- Custom **tempo**, **velocity**, and **channel**
- Integration with LLMs for automatic MIDI sequence creation *(not really, this is like the back-end a LLM could use)*

---

## Side Note

This is the best way i found to turn any LLM into a sort of MIDI generator. You can easily convert that into a tool for any LLM so it can generate a MIDI file. And yeah, it works quite well !

This could be used to make an actual VST which would do that directly in your DAW, `*cough*` (paid vsts out there are quite expensive for what they do) `*cough*`. 

Well that's an idea i have, and i probably will do in a near future. 

Stay tuned. 

*Oh and by the way, if you're interested in generating some melodies for inspiration, check out this site i'm not affiliated with  : https://midigen.app/melody-generator/*

*(just found it, if i did earlier, maybe i wouldn't have done this, or maybe I would have anyways, doesn't matter)*

---

## Installation

You can use either **conda** or **pip**.  
Below is the recommended setup using **conda** for isolation.

### 1. Create a new environment

conda create -n seq2midi python=3.10 -y  
conda activate seq2midi

### 2. Install dependencies

pip install midiutil

### 3. Clone this repository

git clone https://github.com/yourusername/seq_to_midi.git
cd seq_to_midi

### 4. Testing

You can verify that everything works by running this minimal test sequence:
```
python seq_to_midi.py --sequence "[[\"C4\",\"-\",\"E4\",\"-\"],[\"G4\",\"-\",\"C5\",\"-\"]]" --output test.mid --bpm 100 --steps-per-bar 4
```
This will generate a `test.mid` file in the current directory.  
Open it in any DAW (FL Studio, Ableton, Logic, etc.) to confirm playback.

---
## Usage

### Example: Generating a Simple Melody
```
python seq_to_midi.py --sequence "[[\"A#3\",\"-\",\"D#4\",\"-\"],[\"F4\",\"-\",\".\",\"G#3\"],[\"C#4\",\"-\",\"D#4\",\"-\"],[\"G#3\",\".\",\"A#3\",\"-\"]]" --output melody.mid --bpm 120 --steps-per-bar 4
```
### Example: Block Chords
```
python seq_to_midi.py --sequence "[[[\"C3\",\"E3\",\"G3\"],\"-\",\"-\",\"-\"],[[\"F3\",\"A3\",\"C4\"],\"-\",\"-\",\"-\"],[[\"G3\",\"B3\",\"D4\"],\"-\",\"-\",\"-\"],[[\"C3\",\"E3\",\"G3\"],\"-\",\"-\",\"-\"]]" --output basic_chords.mid --bpm 100 --steps-per-bar 4 --velocity 100 
```
### Example: Complex melody using every features 
```
python seq_to_midi.py --sequence "[[[\"A#3\",\"D#4\",\"F4\"],\"-\",\"-\",\"-\",\"-\",\"-\",\"-\",\"-\"],[\"A#3\",\"-\",\"C#4\",\".\",\"D#4\",\"-\",\"F4\",\".\"],[[\"G#3\",\"C#4\",\"D#4\"],\"-\",\"-\",\"-\",[\"F3\",\"A#3\",\"C#4\"],\"-\",\"-\",\"-\"],[\"G#3\",\"-\",\"-\",\".\",\"A#3\",\"C#4\",\"-\",\"D#4\"],[[\"B2\",\"F#3\",\"D#4\"],\"-\",\"A#3\",\"C#4\",\"-\",\"D#4\",\"-\",\".\"],[\".\",\".\",\"A#2\",\"-\",\"-\",\".\",\"G#2\",\"-\"],[\"A#3\",\"C#4\",\"D#4\",\"F4\",\"G#4\",\"F4\",\"D#4\",\"C#4\"],[[\"A#3\",\"D#4\",\"F4\",\"A#4\"],\"-\",\"-\",\"-\",\"-\",\"-\",\"-\",\"-\"]]" --output complex_demo.mid --bpm 128 --steps-per-bar 8 --velocity 108 --channel 0
```
Each inner list represents a **bar**, and each bar has a number of **steps** (`--steps-per-bar`).  
A step can contain:
- A note (e.g., "A#3")
- A chord (e.g., ["A#3","D#4","F4"])
- A sustain ("-")
- A rest (".")

---


## Prompt Template for LLMs

You can use the following prompt to instruct any LLM (e.g., ChatGPT, Claude, Gemini) to generate valid sequences for this script:
```
You are a music assistant that generates step-sequencer MIDI patterns.

Your task:
- Produce a single shell command that can be directly pasted into a terminal and will run the tool `seq_to_midi.py`.
- The command must include the full `python seq_to_midi.py --sequence ...` structure.
- Escape all double quotes (`"`) as `\"` so it works in a standard bash or zsh shell.
- Use valid JSON for the `--sequence` argument:
  • The sequence must be an array of 8 bars.
  • Each bar must contain 4 or 8 steps.
  • Notes are strings like `"A#3"`, `"C#4"`, etc.
  • Sustains use `"-"`, rests use `"."`.
  • Chords are arrays of notes like `["A#3","D#4","F4"]`.
- Also include example flags like `--output`, `--bpm`, `--steps-per-bar`, and `--velocity`.
- Do not include code blocks, explanations, or any text before or after the command.

Expected output format:

python seq_to_midi.py --sequence "[[[\"C3\",\"E3\",\"G3\"],\"-\",\"-\",\"-\"],[[\"F3\",\"A3\",\"C4\"],\"-\",\"-\",\"-\"],[[\"G3\",\"B3\",\"D4\"],\"-\",\"-\",\"-\"],[[\"C3\",\"E3\",\"G3\"],\"-\",\"-\",\"-\"]]" --output my_song.mid --bpm 120 --steps-per-bar 4 --velocity 100 --channel 0
```
Then run it directly what the LLM gives you, for instance :
```
python seq_to_midi.py --sequence "[[[\"C3\",\"E3\",\"G3\"],\"-\",\"-\",\"-\"],[[\"F3\",\"A3\",\"C4\"],\"-\",\"-\",\"-\"],[[\"G3\",\"B3\",\"D4\"],\"-\",\"-\",\"-\"],[[\"C3\",\"E3\",\"G3\"],\"-\",\"-\",\"-\"]]" --output my_song.mid --bpm 120 --steps-per-bar 4 --velocity 100 --channel 0
```
---
## Enjoy

This is much better than all those AI tools making a whole song for you 🤢, aaaaaand much better than what i tried to do here https://github.com/DirtyBeastAfterTheToad/AiVstPlugin 

---
## License

MIT License © 2025 DirtyBeastAfterTheToad
