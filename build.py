"""Build the profile card: ASCII portrait + info panel, in light and dark."""
from xml.sax.saxutils import escape

W, H = 985, 610
ART_FS, INFO_FS = 16, 15
CW, LH = ART_FS * 0.6, ART_FS * 1.25
INFO_X, INFO_COLS, ROW = 490, 52, 20

INFO = [
    ("head", "srikar@desemsetti"),
    ("kv", "OS", "Engineer, Trumpeter, Philosopher"),
    ("kv", "Host", "NC State University, Class of 2027"),
    ("kv", "Kernel", "B.S. Computer Science (AI)"),
    ("kv", "Shell", "B.S. Philosophy"),
    ("kv", "Minors", "Music, Cognitive Science, Mathematics"),
    ("kv", "Location", "Raleigh, NC"),
    ("gap",),
    ("kv", "Languages.Programming", "Python, TypeScript, SQL"),
    ("kv", "Languages.Web", "JavaScript, HTML, CSS"),
    ("kv", "Languages.Tools", "Next.js, AWS, OpenCV, NumPy"),
    ("gap",),
    ("kv", "Hobbies.Music", "Trumpet (wind ensemble, sextet)"),
    ("kv", "Hobbies.Court", "Pickleball, Tennis, Table Tennis"),
    ("kv", "Hobbies.Other", "Hiking, Reading"),
    ("blank",),
    ("head", "- Projects"),
    ("kv", "NASA.Lunar", "Rover agent, 50 mm map accuracy"),
    ("kv", "Drone.Planner", "A* search + Q-learning dispatch"),
    ("kv", "Robots.Study", "robots.txt rules vs. AI crawlers"),
    ("blank",),
    ("head", "- Writing"),
    ("kv", "Metaphysics", "Humean laws and causation"),
    ("kv", "Epistemology", "A defense of externalism"),
    ("blank",),
    ("head", "- Contact"),
    ("kv", "Email", "spdesems@ncsu.edu"),
    ("kv", "LinkedIn", "srikar-desemsetti"),
    ("kv", "GitHub", "SrikarD123"),
]

THEMES = {
    "dark":  dict(bg="#161b22", fg="#c9d1d9", key="#ffa657", value="#a5d6ff", cc="#616e7f", art="art_dark.txt"),
    "light": dict(bg="#f6f8fa", fg="#24292f", key="#953800", value="#0a3069", cc="#c2cfde", art="art_light.txt"),
}

def keyspans(key):
    return ".".join(f'<tspan class="key">{escape(p)}</tspan>' for p in key.split("."))

def build(theme):
    t = THEMES[theme]
    art = open(t["art"]).read().rstrip("\n").split("\n")
    top = (H - len(art) * LH) / 2 + ART_FS
    out = [f'''<?xml version='1.0' encoding='UTF-8'?>
<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback,Consolas,Menlo,monospace" width="{W}px" height="{H}px" font-size="{INFO_FS}px" role="img" aria-label="Srikar Desemsetti: ASCII portrait and profile">
<style>
@font-face {{ src: local('Consolas'), local('Consolas Bold'); font-family: 'ConsolasFallback'; font-display: swap; size-adjust: 109%; }}
.key {{fill: {t["key"]};}} .value {{fill: {t["value"]};}} .cc {{fill: {t["cc"]};}}
text, tspan {{white-space: pre;}}
</style>
<rect width="{W}px" height="{H}px" fill="{t["bg"]}" rx="15"/>
<text fill="{t["fg"]}" font-size="{ART_FS}px" xml:space="preserve">''']
    for i, line in enumerate(art):
        body = line.lstrip(" ")
        if not body: continue
        x = 15 + (len(line) - len(body)) * CW
        out.append(f'<tspan x="{x:.2f}" y="{top + i * LH:.2f}" textLength="{len(body) * CW:.2f}" lengthAdjust="spacing">{escape(body)}</tspan>')
    out.append(f'</text>\n<text x="{INFO_X}" y="30" fill="{t["fg"]}" xml:space="preserve">')
    y = 30
    for item in INFO:
        if item[0] == "head":
            rule = "-" + "—" * (INFO_COLS - len(item[1]) - 5) + "-—-"
            out.append(f'<tspan x="{INFO_X}" y="{y}">{escape(item[1])}</tspan> {rule}')
        elif item[0] == "gap":
            out.append(f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>')
        elif item[0] == "kv":
            _, key, value = item
            dots = INFO_COLS - len(". ") - len(key) - len(":") - len(value) - 2
            assert dots >= 2, (key, value, dots)
            out.append(f'<tspan x="{INFO_X}" y="{y}" class="cc">. </tspan>{keyspans(key)}:<tspan class="cc"> {"." * dots} </tspan><tspan class="value">{escape(value)}</tspan>')
        y += ROW
    out.append("</text>\n</svg>\n")
    assert y - ROW + 15 <= H, y
    return "\n".join(out)

for theme in THEMES:
    open(f"{theme}_mode.svg", "w").write(build(theme))
    print(theme, "ok")
