# Builds the George caller voice: every clip key the Serena set has, plus any new TOKEN_TEXT phrase, spoken by the free
# Kokoro voice "bm_george" with a deeper pitch and arena echo (ffmpeg). Existing clips are kept, so re-running only adds new ones.
# Runs on Linux (cloud sessions) as well as a Mac. Setup, once:
#   python3 -m venv /tmp/tts && /tmp/tts/bin/pip install kokoro-onnx soundfile
#   curl -L -o /tmp/tts/kokoro.onnx https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx
#   curl -L -o /tmp/tts/voices.bin  https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin
# usage: /tmp/tts/bin/python tools/build-george.py /tmp/tts .
import re, sys, os, subprocess, tempfile, soundfile as sf
from kokoro_onnx import Kokoro
TTS, REPO = sys.argv[1], sys.argv[2]
OUT = os.path.join(REPO, "sounds/voice/george"); os.makedirs(OUT, exist_ok=True)
src = open(os.path.join(REPO, "index.html")).read()
tt = re.search(r"const TOKEN_TEXT = \{(.*?)\};", src).group(1)
TEXT = {k.strip('"'): v for k, v in re.findall(r'("[\w-]+"|[\w-]+)\s*:\s*"((?:[^"\\]|\\.)*)"', tt)}
ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()
def words(n):
    if n < 20: return ONES[n]
    if n < 100: return TENS[n // 10] + ("-" + ONES[n % 10] if n % 10 else "")
    return "one hundred" + (" and " + words(n - 100) if n > 100 else "")
pretty = {w.lower(): w for line in open(os.path.join(REPO, "sounds/names.txt")) for w in line.split()}
keys = open(os.path.join(REPO, "sounds/voice/serena/manifest.txt")).read().split()
keys += [t for t in TEXT if t not in keys]
TEXT.setdefault("player", "Player.")
names = open(os.path.join(REPO, "sounds/voice/serena/names.txt")).read().split()
jobs = []
for k in keys:
    if k.startswith("name-"): continue  # names come from names.txt below
    if k.startswith("n-"):
        n = int(k[2:])
        jobs.append((k, "One hundred... and eighty!" if n == 180 else "No score." if n == 0 else words(n) + ".", 0.82 if n == 180 else 0.95))
    elif k in TEXT:
        t = TEXT[k]; jobs.append((k, t, 0.9 if t.endswith("!") else 1.0))
    else:
        print("no text for", k)
for nm in names:
    jobs.append(("name-" + nm, pretty.get(nm, nm.capitalize()) + ".", 1.0))
FX = ("silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.15:stop_threshold=-45dB,"
      "asetrate=24000*0.93,aresample=24000,atempo=1.075,acompressor=threshold=-20dB:ratio=4:attack=5:release=80,"
      "apad=pad_dur=0.35,aecho=0.85:0.7:90|180|290:0.38|0.24|0.12,loudnorm=I=-14:TP=-1.5")
k = Kokoro(TTS + "/kokoro.onnx", TTS + "/voices.bin")
tmp = tempfile.mkdtemp()
for i, (key, text, spd) in enumerate(jobs):
    dst = os.path.join(OUT, key + ".m4a")
    if os.path.exists(dst): continue
    a, sr = k.create(text, voice="bm_george", speed=spd, lang="en-gb")
    wav = os.path.join(tmp, "x.wav"); sf.write(wav, a, sr)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", FX, "-ar", "44100", "-c:a", "aac", "-b:a", "56k", dst + ".part.m4a"], check=True)
    os.replace(dst + ".part.m4a", dst)
    if i % 50 == 0: print(i, "/", len(jobs), key, flush=True)
open(os.path.join(OUT, "manifest.txt"), "w").write("\n".join(keys + ["name-" + n for n in names if "name-" + n not in keys]) + "\n")
open(os.path.join(OUT, "names.txt"), "w").write("\n".join(names) + "\n")
print("done", len(jobs))
