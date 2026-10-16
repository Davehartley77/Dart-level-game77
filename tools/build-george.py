# Builds the George caller voice: every clip key the Serena set has, plus any new TOKEN_TEXT phrase, spoken by the free
# Kokoro voice "bm_george", brisk and dry, breaths gated out (the owner found echo and slow
# delivery awful). The 180 is two slow natural takes joined with a pause: "One hundred ... and eighty!" (no pitch tricks: they warble). Existing clips are kept, so re-running only adds new ones.
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
        jobs.append((k, "One hundred... and eighty!" if n == 180 else "No score." if n == 0 else words(n) + ".", None if n == 180 else 1.35))
    elif k in TEXT:
        t = TEXT[k]; jobs.append((k, t, 1.25 if t.endswith("!") else 1.35))
    else:
        print("no text for", k)
for nm in names:
    jobs.append(("name-" + nm, pretty.get(nm, nm.capitalize()) + ".", 1.3))
# Whole sentences flow far better than words glued together, so the commonest lines get their own clips:
# "you require N", "checkout N" and every checkout route (index.html uses them when present).
def part(t):
    if t == "Bull": return "bull"
    if t == "25": return "outer bull"
    return {"T": "treble ", "D": "double "}.get(t[0], "single ") + words(int(t.lstrip("TD")))
routes = sorted(set(re.findall(r'\d+:"([^"]+)"', re.search(r"const CHECKOUTS = \{(.*?)\};", src, re.S).group(1))))
for n in range(2, 171):
    jobs += [(f"req-{n}", f"you require {words(n)}.", 1.3), (f"chk-{n}", f"checkout {words(n)}.", 1.3)]
for r in routes:
    jobs.append(("route-" + r.lower().replace(" ", "-"), ", ".join(part(t) for t in r.split()) + ".", 1.3))
keys += [j[0] for j in jobs if j[0].split("-")[0] in ("req", "chk", "route") and j[0] not in keys]
GATE = "agate=threshold=0.03:ratio=6:attack=2:release=60"
FX = ("silenceremove=start_periods=1:start_threshold=-35dB:stop_periods=-1:stop_duration=0.08:stop_threshold=-35dB," + GATE +
      ",acompressor=threshold=-20dB:ratio=3:attack=5:release=80,apad=pad_dur=0.04,loudnorm=I=-14:TP=-1.5")
ENDS = "silenceremove=start_periods=1:start_threshold=-35dB,areverse,silenceremove=start_periods=1:start_threshold=-35dB,areverse," + GATE
def say180(dst, tmp):
    parts = []
    for i, (text, spd) in enumerate([("One hundred", 0.75), ("and eighty!", 0.8)]):
        a, sr = k.create(text, voice="bm_george", speed=spd, lang="en-gb"); w = os.path.join(tmp, f"p{i}.wav"); sf.write(w, a, sr); parts.append(w)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", parts[0], "-i", parts[1], "-filter_complex",
                    f"[0]{ENDS},apad=pad_dur=0.25[a];[1]{ENDS}[b];[a][b]concat=n=2:v=0:a=1,acompressor=threshold=-20dB:ratio=3,loudnorm=I=-12:TP=-1",
                    "-ar", "44100", "-c:a", "aac", "-b:a", "56k", dst + f".{os.getpid()}.part.m4a"], check=True)
    os.replace(dst + f".{os.getpid()}.part.m4a", dst)
k = Kokoro(TTS + "/kokoro.onnx", TTS + "/voices.bin")
tmp = tempfile.mkdtemp()
for i, (key, text, spd) in enumerate(jobs):
    dst = os.path.join(OUT, key + ".m4a")
    if os.path.exists(dst): continue
    if spd is None: say180(dst, tmp); continue
    a, sr = k.create(text, voice="bm_george", speed=spd, lang="en-gb")
    wav = os.path.join(tmp, "x.wav"); sf.write(wav, a, sr)
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", wav, "-af", FX, "-ar", "44100", "-c:a", "aac", "-b:a", "56k", dst + f".{os.getpid()}.part.m4a"], check=True)
    os.replace(dst + f".{os.getpid()}.part.m4a", dst)
    if i % 50 == 0: print(i, "/", len(jobs), key, flush=True)
open(os.path.join(OUT, "manifest.txt"), "w").write("\n".join(keys + ["name-" + n for n in names if "name-" + n not in keys]) + "\n")
open(os.path.join(OUT, "names.txt"), "w").write("\n".join(names) + "\n")
print("done", len(jobs))
