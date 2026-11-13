import json, sys, re

nb = json.load(open(sys.argv[1], encoding="utf-8"))
out = [
    "import subprocess as _sp, sys as _sys",
    "def _sh(c):",
    "    print('$', c, flush=True)",
    "    r = _sp.run(c, shell=True, text=True, capture_output=True)",
    "    print(r.stdout[-3000:], r.stderr[-3000:], flush=True)",
    "    return r",
    "display = lambda x: print(x.to_string() if hasattr(x, 'to_string') else x, flush=True)",
    "",
]
n = 0
for i, c in enumerate(nb["cells"]):
    if c["cell_type"] != "code":
        continue
    out.append(f"# ===== cell {i} =====")
    out.append(f"print('===== cell {i} =====', flush=True)")
    for line in "".join(c["source"]).split("\n"):
        m = re.match(r"^(\s*)!(.*)$", line)
        if m:
            line = f"{m.group(1)}_sh(f{m.group(2)!r})".replace("f'", "f'", 1)
            n += 1
        out.append(line)
src = "\n".join(out)
compile(src, "a8_run.py", "exec")
open(sys.argv[2], "w", encoding="utf-8").write(src)
print("converted", n, "shell lines; compiles OK")
