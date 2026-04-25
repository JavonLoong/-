from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "流体力学期末复习_AI_Learning_OS.html"


CHAPTERS = [
    ("01", "流体的物理性质", ["物性", "粘性", "单位"], "tau = mu du/dy", "非牛顿流体或速度梯度方向不清时不要硬套。"),
    ("02", "流体静力学", ["静水", "压强", "总压力"], "p = p0 + rho g h", "流体运动或不同密度分段时不要一条式子套到底。"),
    ("03", "流体运动学", ["速度场", "流线", "涡量"], "a = partial V/partial t + (V·nabla)V", "非定常时流线不等于迹线。"),
    ("04", "控制体与连续方程", ["控制体", "质量守恒", "通量"], "partial rho/partial t + div(rho V)=0", "变密度时不能直接写 A1v1=A2v2。"),
    ("05", "能量方程与伯努利方程", ["伯努利", "水头", "损失"], "z + p/(rho g) + v^2/(2g) = C", "有损失、泵/涡轮、高速可压或跨激波时不能用理想式。"),
    ("06", "动量方程与动量矩方程", ["控制体", "受力", "动量通量"], "sum F = out - in + storage", "不要把流体受力和固体受力方向混淆。"),
    ("07", "理想流体有旋与有势流动", ["环量", "势函数", "流函数"], "omega = curl V", "点涡奇点和多连通区域要单独说明。"),
    ("08", "量纲分析与相似原理", ["pi定理", "相似", "无量纲数"], "pi groups = n - r", "变量不独立或重复变量含待求量时会失真。"),
    ("09", "粘性不可压缩内部流动", ["层流", "Poiseuille", "Re"], "Q = pi R^4 Delta p / (8 mu L)", "紊流、入口段、非圆管、非牛顿流体不能直接套。"),
    ("10", "紊流与管路损失", ["紊流", "Moody", "局部损失"], "h_f = lambda (L/D) v^2/(2g)", "lambda 口径不清时先确认 Darcy/Fanning。"),
    ("11", "边界层与绕流阻力", ["边界层", "分离", "阻力"], "F_D = C_D rho V^2 A / 2", "阻力曲线临界 Re 不同资料可能有差异。"),
    ("12", "可压缩流体一维流动", ["Ma", "喷管", "堵塞"], "Ma = V/a", "等熵关系不能跨激波，面积-Ma 公式按老师要求使用。"),
    ("13", "可压缩超声速流动", ["激波", "膨胀波", "总压损失"], "斜激波先取 M_n", "膨胀扇和激波不能互套公式。"),
    ("14", "实验与综合题抢分", ["实验", "读数", "综合题"], "读数 -> 物理量 -> 方程 -> 误差", "专业拓展不进入期末主线。"),
]


GLOBAL_FORMULAS = [
    ("静水压强", "p = p0 + rho g h", "02/14", "同种静止液体"),
    ("连续方程", "rho A v = const", "04", "可压缩时保留 rho"),
    ("理想伯努利", "z+p/(rho g)+v^2/(2g)=C", "05", "定常、不可压、无粘、同流线"),
    ("实际能量", "H1 + Hp = H2 + hw + Ht", "05/10", "损失项必须展开"),
    ("控制体动量", "sum F = out - in + storage", "06", "力的对象和方向要写清"),
    ("雷诺数", "Re = vD/nu", "08/09/10", "尺度和速度要对应"),
    ("沿程损失", "hf = lambda(L/D)v^2/(2g)", "10", "lambda 默认 Darcy 口径"),
    ("局部损失", "hj = zeta v_ref^2/(2g)", "10/14", "参考速度必须说明"),
    ("声速/马赫数", "a=sqrt(kRT), Ma=V/a", "12/13", "用当地温度"),
    ("正/斜激波", "斜激波用 M_n", "13", "不能用整体 M 直接套正激波表"),
]


TYPE_PATHS = [
    ("静水/U形管", "定基准 -> 找等压面 -> 逐段 rho g h", "02, 14"),
    ("平面/曲面总压力", "画压强图 -> 求大小 -> 求作用线/分力", "02, 14"),
    ("流线/涡量判断", "看定常 -> 写速度场导数 -> 判 curl", "03, 07"),
    ("多入口流量", "画控制面 -> 进出通量守恒", "04"),
    ("文丘里/皮托管", "连续 + 伯努利；必要时加损失", "04, 05, 14"),
    ("喷嘴/弯管受力", "能量求速度压强 -> 动量求力", "05, 06"),
    ("管路损失", "能量账本 -> Re -> lambda/zeta", "05, 10, 14"),
    ("Poiseuille 层流", "压差 -> 速度剖面 -> Q/剪应力", "09"),
    ("喷管堵塞", "总参数 -> 临界压力比 -> Ma=1 -> 分段", "12"),
    ("激波/膨胀扇", "判压缩/膨胀 -> 选激波或 PM 入口", "13"),
]


FORBIDDEN = [
    ("伯努利跨激波", "激波前后分段，跨激波用激波关系。"),
    ("两点不在同一流线仍套理想伯努利", "改用总流能量方程或控制体。"),
    ("A1v1=A2v2 不看密度", "可压缩流用 rho A v 守恒。"),
    ("64/Re 套紊流", "先判 Re，再查 Moody 或经验式。"),
    ("局部损失不写参考速度", "写明 hj = zeta v_ref^2/(2g)。"),
    ("斜激波直接用整体 M1", "先取法向马赫数。"),
    ("膨胀转角用激波关系", "膨胀扇用 PM 入口或方向判断。"),
    ("实验读数不转单位", "cm、mm、g、L/min 先转 SI。"),
]


def slug(text: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_\-\u4e00-\u9fff]+", "-", text).strip("-")


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\[([^\]]+)\]\(<([^>]+)>\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r"\1", text)
    text = text.replace("考试通用补充", '<span class="tag supplement">考试通用补充</span>')
    text = text.replace("专业拓展", '<span class="tag extension">专业拓展</span>')
    return text


def split_table_row(line: str) -> list[str]:
    raw = line.strip()
    if raw.startswith("|"):
        raw = raw[1:]
    if raw.endswith("|"):
        raw = raw[:-1]
    cells: list[str] = []
    buf: list[str] = []
    in_code = False
    in_math = False
    escaped = False
    for ch in raw:
        if escaped:
            buf.append(ch)
            escaped = False
            continue
        if ch == "\\":
            buf.append(ch)
            escaped = True
            continue
        if ch == "`" and not in_math:
            in_code = not in_code
            buf.append(ch)
            continue
        if ch == "$" and not in_code:
            in_math = not in_math
            buf.append(ch)
            continue
        if ch == "|" and not in_code and not in_math:
            cells.append("".join(buf).strip())
            buf = []
        else:
            buf.append(ch)
    cells.append("".join(buf).strip())
    return cells


def table_to_html(lines: list[str]) -> str:
    rows = []
    for line in lines:
        parts = split_table_row(line)
        if all(set(p) <= {"-", ":", " "} for p in parts):
            continue
        rows.append(parts)
    if not rows:
        return ""
    head = rows[0]
    body = rows[1:]
    out = ["<div class=\"table-wrap\"><table><thead><tr>"]
    out.extend(f"<th>{inline_md(c)}</th>" for c in head)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{inline_md(c)}</td>" for c in row)
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def md_to_html(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_code = False
    code_buf: list[str] = []
    list_open = False
    while i < len(lines):
        line = lines[i]
        if line.strip().startswith("```"):
            if not in_code:
                if list_open:
                    out.append("</ul>")
                    list_open = False
                in_code = True
                code_buf = []
            else:
                out.append("<pre><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue
        if line.strip().startswith("|") and i + 1 < len(lines) and lines[i + 1].strip().startswith("|"):
            if list_open:
                out.append("</ul>")
                list_open = False
            tbl = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                tbl.append(lines[i])
                i += 1
            out.append(table_to_html(tbl))
            continue
        m = re.match(r"^(#{1,4})\s+(.+)$", line)
        if m:
            if list_open:
                out.append("</ul>")
                list_open = False
            level = min(len(m.group(1)) + 1, 5)
            title = m.group(2).strip()
            out.append(f"<h{level} id=\"{slug(title)}\">{inline_md(title)}</h{level}>")
            i += 1
            continue
        if re.match(r"^\s*[-*]\s+", line) or re.match(r"^\s*\d+\.\s+", line):
            if not list_open:
                out.append("<ul>")
                list_open = True
            item = re.sub(r"^\s*(?:[-*]|\d+\.)\s+", "", line)
            out.append(f"<li>{inline_md(item)}</li>")
            i += 1
            continue
        if not line.strip():
            if list_open:
                out.append("</ul>")
                list_open = False
            i += 1
            continue
        if list_open:
            out.append("</ul>")
            list_open = False
        out.append(f"<p>{inline_md(line.strip())}</p>")
        i += 1
    if list_open:
        out.append("</ul>")
    return "\n".join(out)


def visual_gallery() -> str:
    return r"""
<section class="visual-band" id="visuals">
  <div class="section-head"><span>可视化速记</span><strong>把方程先看成图</strong></div>
  <div class="visual-grid">
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="控制体通量示意">
        <rect x="110" y="38" width="100" height="104" rx="6" fill="#e8f4f8" stroke="#26667f" stroke-width="3"/>
        <path d="M20 90 H110" stroke="#0f766e" stroke-width="8" marker-end="url(#arrow)"/>
        <path d="M210 70 H300" stroke="#0f766e" stroke-width="5" marker-end="url(#arrow)"/>
        <path d="M210 115 H300" stroke="#0f766e" stroke-width="7" marker-end="url(#arrow)"/>
        <text x="132" y="92">CV</text><text x="38" y="78">in</text><text x="242" y="58">out</text>
      </svg>
      <figcaption><b>控制体</b><span>进出口通量先画外法向，动量题别急着代数。</span></figcaption>
    </figure>
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="伯努利水头线示意">
        <polyline points="25,40 105,58 190,80 295,112" fill="none" stroke="#2563eb" stroke-width="4"/>
        <polyline points="25,76 105,88 190,112 295,138" fill="none" stroke="#f59e0b" stroke-width="4"/>
        <rect x="35" y="122" width="235" height="18" fill="#9ca3af"/>
        <circle cx="74" cy="78" r="8" fill="#2563eb"/><circle cx="225" cy="119" r="8" fill="#2563eb"/>
        <text x="30" y="32">EGL</text><text x="32" y="72">HGL</text><text x="198" y="158">h_w</text>
      </svg>
      <figcaption><b>能量账本</b><span>伯努利不是无损专属，实际题把损失项写进账本。</span></figcaption>
    </figure>
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="管路损失示意">
        <path d="M24 90 H108 C126 90 126 55 150 55 H202 C230 55 230 125 258 125 H300" fill="none" stroke="#334155" stroke-width="18" stroke-linecap="round"/>
        <path d="M24 90 H108 C126 90 126 55 150 55 H202 C230 55 230 125 258 125 H300" fill="none" stroke="#67e8f9" stroke-width="8" stroke-linecap="round"/>
        <text x="48" y="55">h_f</text><text x="182" y="42">ζ</text><text x="236" y="156">Σh_j</text>
      </svg>
      <figcaption><b>管损</b><span>沿程看长度，局部看构件；此处是概念图，不用于 Moody 查数。</span></figcaption>
    </figure>
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="动量方程受力示意">
        <rect x="82" y="52" width="156" height="76" rx="10" fill="#eef2ff" stroke="#4338ca" stroke-width="3"/>
        <path d="M24 90 H82" stroke="#0f766e" stroke-width="8" marker-end="url(#arrow)"/>
        <path d="M238 90 H300" stroke="#0f766e" stroke-width="5" marker-end="url(#arrow)"/>
        <path d="M160 52 V18" stroke="#dc2626" stroke-width="4" marker-end="url(#arrow)"/>
        <path d="M118 128 v34" stroke="#d97706" stroke-width="4" marker-end="url(#arrow)"/>
        <text x="34" y="78">ρQV in</text><text x="232" y="78">ρQV out</text>
        <text x="166" y="26">F</text><text x="124" y="160">W</text>
      </svg>
      <figcaption><b>动量方程</b><span>先列外力，再列动量通量；题问固体受力时别忘取反。</span></figcaption>
    </figure>
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="边界层分离示意">
        <path d="M12 132 C80 124 145 130 310 128" stroke="#475569" stroke-width="5" fill="none"/>
        <path d="M28 118 C80 72 150 54 286 46" stroke="#0f766e" stroke-width="3" fill="none"/>
        <path d="M125 126 C155 96 188 105 214 128 C234 145 260 144 286 130" stroke="#ef4444" stroke-width="4" fill="none"/>
        <text x="32" y="54">boundary layer</text><text x="178" y="154">separation</text>
      </svg>
      <figcaption><b>边界层</b><span>逆压梯度让边界层分离，压差阻力常成为主角。</span></figcaption>
    </figure>
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="喷管和激波示意">
        <path d="M30 50 C100 70 100 110 30 130 H285 C220 110 220 70 285 50 Z" fill="#e0f2fe" stroke="#0369a1" stroke-width="3"/>
        <path d="M155 50 L155 130" stroke="#f97316" stroke-width="4"/>
        <path d="M218 50 L238 130" stroke="#dc2626" stroke-width="5"/>
        <text x="140" y="42">M=1</text><text x="224" y="145">shock</text>
      </svg>
      <figcaption><b>可压缩分段</b><span>喷管等熵段和激波段必须分开，总压跨激波下降。</span></figcaption>
    </figure>
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="斜激波与膨胀扇示意">
        <path d="M24 90 H132" stroke="#0f766e" stroke-width="7" marker-end="url(#arrow)"/>
        <path d="M134 58 L206 90 L134 122 Z" fill="#e5e7eb" stroke="#64748b" stroke-width="2"/>
        <path d="M132 58 L240 24" stroke="#dc2626" stroke-width="4"/>
        <path d="M132 122 C170 128 202 142 242 160" stroke="#2563eb" stroke-width="3" fill="none"/>
        <path d="M132 122 C170 118 206 112 250 104" stroke="#2563eb" stroke-width="2" fill="none"/>
        <text x="42" y="76">M&gt;1</text><text x="204" y="36">shock</text><text x="206" y="150">expansion fan</text>
      </svg>
      <figcaption><b>斜激波 / 膨胀扇</b><span>压缩角走激波，膨胀角走 PM 入口；这不是同一套公式。</span></figcaption>
    </figure>
    <figure class="viz">
      <svg viewBox="0 0 320 180" role="img" aria-label="实验读数链示意">
        <rect x="20" y="34" width="74" height="38" rx="6" fill="#fef3c7" stroke="#d97706"/>
        <rect x="122" y="34" width="74" height="38" rx="6" fill="#dbeafe" stroke="#2563eb"/>
        <rect x="224" y="34" width="74" height="38" rx="6" fill="#dcfce7" stroke="#16a34a"/>
        <path d="M94 53 H122 M196 53 H224" stroke="#334155" stroke-width="3" marker-end="url(#arrow)"/>
        <text x="35" y="58">读数</text><text x="136" y="58">物理量</text><text x="240" y="58">方程</text>
        <path d="M57 95 C92 130 206 130 262 95" fill="none" stroke="#7c3aed" stroke-width="3"/>
        <text x="112" y="148">单位 / 误差 / 有效数字</text>
      </svg>
      <figcaption><b>实验链</b><span>液面、砝码、时间先翻译，再进方程。</span></figcaption>
    </figure>
  </div>
</section>
"""


def read_chapter(num: str) -> str:
    title = next(title for n, title, *_ in CHAPTERS if n == num)
    file = ROOT / f"{num}_{title}.md"
    if not file.exists():
        raise FileNotFoundError(f"Expected chapter file not found: {file}")
    return file.read_text(encoding="utf-8")


def build() -> str:
    index_md = (ROOT / "00_期末复习总索引.md").read_text(encoding="utf-8")
    chapters = []
    for num, title, tags, formula, forbidden in CHAPTERS:
        md = read_chapter(num)
        chapters.append({
            "num": num,
            "title": title,
            "tags": tags,
            "formula": formula,
            "forbidden": forbidden,
            "html": md_to_html(md),
        })
    data = json.dumps([{k: v for k, v in c.items() if k != "html"} for c in chapters], ensure_ascii=False)
    chapter_html = "\n".join(
        f"""<article class="chapter" id="chapter-{c['num']}" data-tags="{' '.join(c['tags'])}" data-title="{html.escape(c['title'])}">
        <div class="chapter-meta"><span class="num">{c['num']}</span><div><h2>{c['title']}</h2><p>{' / '.join(c['tags'])}</p></div><button class="done-btn" data-done="{c['num']}">标记完成</button></div>
        <div class="chapter-quick"><span><b>主线：</b>{inline_md(c['formula'])}</span><span><b>禁用：</b>{inline_md(c['forbidden'])}</span></div>
        <details><summary>展开完整章节</summary><div class="chapter-body">{c['html']}</div></details>
      </article>"""
        for c in chapters
    )
    formula_rows = "".join(f"<tr><td>{a}</td><td><code>{html.escape(b)}</code></td><td>{c}</td><td>{d}</td></tr>" for a, b, c, d in GLOBAL_FORMULAS)
    type_cards = "".join(f"<div class=\"path-card\"><b>{a}</b><span>{b}</span><em>{c}</em></div>" for a, b, c in TYPE_PATHS)
    forbid_cards = "".join(f"<li><b>{a}</b><span>{b}</span></li>" for a, b in FORBIDDEN)
    chapter_cards = "".join(
        f"""<button class="chapter-card" data-target="chapter-{num}" data-tags="{' '.join(tags)}">
        <span>{num}</span><strong>{title}</strong><small>{' · '.join(tags)}</small><code>{html.escape(formula)}</code>
      </button>"""
        for num, title, tags, formula, _ in CHAPTERS
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>流体力学期末复习 AI Learning OS</title>
  <style>
    :root {{
      --ink:#162033; --muted:#5b6475; --paper:#f7f8fb; --panel:#ffffff; --line:#d8dee9;
      --teal:#0f766e; --blue:#2563eb; --amber:#d97706; --red:#dc2626; --green:#16a34a; --violet:#7c3aed;
      --shadow:0 12px 32px rgba(22,32,51,.10);
    }}
    * {{ box-sizing:border-box; }}
    html {{ scroll-behavior:smooth; }}
    body {{ margin:0; font-family: "Microsoft YaHei", "Segoe UI", system-ui, sans-serif; color:var(--ink); background:var(--paper); line-height:1.65; }}
    button, input {{ font:inherit; }}
    .app {{ display:grid; grid-template-columns: 260px minmax(0,1fr) 310px; min-height:100vh; }}
    header {{ grid-column:1 / -1; background:#111827; color:white; padding:22px 28px; display:grid; grid-template-columns:1fr minmax(260px,520px); gap:22px; align-items:center; }}
    header h1 {{ margin:0; font-size:clamp(26px,4vw,46px); letter-spacing:0; }}
    header p {{ margin:8px 0 0; color:#cbd5e1; max-width:880px; }}
    .searchbar {{ display:flex; gap:8px; align-items:center; }}
    .searchbar input {{ width:100%; padding:12px 14px; border-radius:8px; border:1px solid #475569; background:#f8fafc; color:#111827; }}
    .tool-btn, .done-btn, .chapter-card {{ border:1px solid var(--line); background:var(--panel); color:var(--ink); border-radius:8px; cursor:pointer; transition:.18s ease; }}
    .tool-btn {{ padding:10px 12px; white-space:nowrap; }}
    .tool-btn:hover, .chapter-card:hover, .done-btn:hover {{ transform:translateY(-1px); box-shadow:var(--shadow); }}
    nav {{ position:sticky; top:0; height:100vh; overflow:auto; padding:18px; border-right:1px solid var(--line); background:#eef3f7; }}
    main {{ min-width:0; padding:24px; }}
    aside {{ position:sticky; top:0; height:100vh; overflow:auto; padding:18px; border-left:1px solid var(--line); background:#f4f1fb; }}
    .nav-title, .aside-title {{ font-weight:800; margin:4px 0 12px; }}
    .chapter-card {{ width:100%; text-align:left; padding:12px; margin:0 0 10px; display:grid; gap:4px; }}
    .chapter-card span {{ color:var(--teal); font-weight:900; }}
    .chapter-card strong {{ font-size:15px; }}
    .chapter-card small {{ color:var(--muted); }}
    .chapter-card code {{ font-size:12px; white-space:normal; color:#334155; background:#eef2ff; padding:4px; border-radius:4px; }}
    .filter-row {{ display:flex; flex-wrap:wrap; gap:8px; margin:12px 0 18px; }}
    .filter-row button.active {{ background:#111827; color:white; }}
    .hero {{ background:var(--panel); border-bottom:4px solid var(--teal); padding:24px; box-shadow:var(--shadow); margin-bottom:22px; }}
    .hero h2 {{ margin:0 0 8px; font-size:30px; }}
    .stats {{ display:grid; grid-template-columns:repeat(4,1fr); gap:12px; margin-top:18px; }}
    .stat {{ border:1px solid var(--line); padding:12px; background:#fbfdff; border-radius:8px; }}
    .stat b {{ display:block; font-size:24px; color:var(--blue); }}
    section, .chapter {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; margin:18px 0; padding:18px; box-shadow:0 4px 18px rgba(22,32,51,.05); }}
    .section-head {{ display:flex; justify-content:space-between; gap:14px; align-items:end; border-bottom:1px solid var(--line); padding-bottom:10px; margin-bottom:14px; }}
    .section-head span {{ color:var(--teal); font-weight:800; }}
    .section-head strong {{ font-size:22px; }}
    .formula-table {{ width:100%; border-collapse:collapse; }}
    th, td {{ border:1px solid var(--line); padding:9px 10px; vertical-align:top; }}
    th {{ background:#e8f0ff; text-align:left; }}
    code {{ background:#f1f5f9; padding:2px 4px; border-radius:4px; }}
    .table-wrap {{ overflow:auto; margin:12px 0; }}
    .path-grid {{ display:grid; grid-template-columns:repeat(2,minmax(0,1fr)); gap:12px; }}
    .path-card {{ border:1px solid var(--line); border-left:5px solid var(--amber); padding:12px; border-radius:8px; background:#fffaf0; display:grid; gap:6px; }}
    .path-card span {{ color:#334155; }}
    .path-card em {{ color:var(--muted); font-style:normal; }}
    .visual-band {{ background:#f8fafc; }}
    .visual-grid {{ display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }}
    .viz {{ margin:0; border:1px solid var(--line); border-radius:8px; background:white; overflow:hidden; }}
    .viz svg {{ width:100%; height:170px; display:block; background:#fbfdff; }}
    .viz figcaption {{ padding:12px; display:grid; gap:4px; }}
    .viz figcaption span {{ color:var(--muted); font-size:14px; }}
    .chapter-meta {{ display:flex; align-items:center; gap:14px; border-bottom:1px solid var(--line); padding-bottom:12px; }}
    .chapter-meta .num {{ width:48px; height:48px; border-radius:50%; display:grid; place-items:center; background:#111827; color:white; font-weight:900; }}
    .chapter-meta h2 {{ margin:0; }}
    .chapter-meta p {{ margin:2px 0 0; color:var(--muted); }}
    .done-btn {{ margin-left:auto; padding:8px 10px; }}
    .done-btn.done {{ background:#dcfce7; border-color:#86efac; color:#166534; }}
    .chapter-quick {{ display:grid; grid-template-columns:1fr 1fr; gap:10px; margin:12px 0; }}
    .chapter-quick span {{ background:#f8fafc; border:1px solid var(--line); padding:10px; border-radius:8px; }}
    details summary {{ cursor:pointer; font-weight:800; color:var(--blue); }}
    .chapter-body h2, .chapter-body h3, .chapter-body h4 {{ scroll-margin-top:20px; }}
    body.sprint .chapter details {{ display:none; }}
    body.sprint .chapter {{ border-left:5px solid var(--teal); }}
    .tag {{ display:inline-block; padding:1px 6px; border-radius:999px; font-size:12px; font-weight:700; }}
    .supplement {{ background:#fff7ed; color:#9a3412; }}
    .extension {{ background:#f3e8ff; color:#6b21a8; }}
    .sr-only {{ position:absolute; width:1px; height:1px; padding:0; margin:-1px; overflow:hidden; clip:rect(0,0,0,0); white-space:nowrap; border:0; }}
    body.hide-supplement .chapter-body .supplement, body.hide-supplement .chapter-body .extension,
    body.hide-supplement #index .supplement, body.hide-supplement #index .extension {{ opacity:.45; }}
    body.hide-supplement .chapter-body p:has(.supplement), body.hide-supplement .chapter-body li:has(.supplement), body.hide-supplement .chapter-body tr:has(.supplement),
    body.hide-supplement .chapter-body p:has(.extension), body.hide-supplement .chapter-body li:has(.extension), body.hide-supplement .chapter-body tr:has(.extension),
    body.hide-supplement #index p:has(.supplement), body.hide-supplement #index li:has(.supplement), body.hide-supplement #index tr:has(.supplement),
    body.hide-supplement #index p:has(.extension), body.hide-supplement #index li:has(.extension), body.hide-supplement #index tr:has(.extension) {{ opacity:.55; }}
    .risk-list {{ list-style:none; padding:0; margin:0; display:grid; gap:10px; }}
    .risk-list li {{ background:#fff1f2; border-left:5px solid var(--red); padding:10px; border-radius:8px; }}
    .risk-list span {{ display:block; color:#4b5563; }}
    .quiz-card {{ background:white; border:1px solid var(--line); border-radius:8px; padding:12px; margin:10px 0; }}
    .quiz-card button {{ margin-top:8px; }}
    .answer {{ display:none; color:#166534; margin-top:8px; }}
    .answer.show {{ display:block; }}
    .hidden {{ display:none !important; }}
    mark {{ background:#fef08a; padding:0 2px; }}
    @media (max-width:1100px) {{ .app {{ grid-template-columns:220px minmax(0,1fr); }} aside {{ grid-column:1 / -1; position:static; height:auto; border-left:0; border-top:1px solid var(--line); }} }}
    @media (max-width:760px) {{ header {{ grid-template-columns:1fr; padding:18px; }} .app {{ display:block; }} nav, aside {{ position:static; height:auto; border:0; }} main {{ padding:14px; }} .stats, .visual-grid, .path-grid, .chapter-quick {{ grid-template-columns:1fr; }} .chapter-meta {{ align-items:flex-start; }} .done-btn {{ margin-left:0; }} }}
  </style>
</head>
<body class="hide-supplement">
<svg width="0" height="0" aria-hidden="true"><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M 0 0 L 10 5 L 0 10 z" fill="currentColor"/></marker></defs></svg>
<header>
  <div><h1>流体力学期末复习 AI Learning OS</h1><p>一个离线 HTML：总索引、图解、公式、题型路径、章节全文、自测与进度记录都放在同一页。</p></div>
  <div class="searchbar"><label class="sr-only" for="search">搜索复习内容</label><input id="search" placeholder="搜索：伯努利 / Re / 激波 / 实验"><button class="tool-btn" id="sprintMode" aria-pressed="false">冲刺模式</button><button class="tool-btn" id="toggleSupplement" aria-pressed="true">显示补充</button></div>
</header>
<div class="app">
<nav>
  <div class="nav-title">章节导航</div>
  <div class="filter-row" id="filters">
    <button class="tool-btn active" data-filter="all" aria-pressed="true">全部</button>
    <button class="tool-btn" data-filter="静水" aria-pressed="false">静水</button>
    <button class="tool-btn" data-filter="控制体" aria-pressed="false">控制体</button>
    <button class="tool-btn" data-filter="损失" aria-pressed="false">损失</button>
    <button class="tool-btn" data-filter="Ma" aria-pressed="false">可压缩</button>
    <button class="tool-btn" data-filter="实验" aria-pressed="false">实验</button>
  </div>
  <div id="resultStatus" class="sr-only" aria-live="polite"></div>
  <div id="chapterCards">{chapter_cards}</div>
</nav>
<main>
  <section class="hero" id="top">
    <h2>考场第一问：这题该用哪本账？</h2>
    <p>静水看压强基准，流动先选流线或控制体，管路写损失，可压缩要分等熵段和激波段。不要急着背公式，先判条件。</p>
    <div class="stats"><div class="stat"><b>14</b>章节</div><div class="stat"><b>10</b>主线公式</div><div class="stat"><b>8</b>禁用条件</div><div class="stat"><b id="doneCount">0</b>已完成</div></div>
  </section>
  {visual_gallery()}
  <section id="formulas"><div class="section-head"><span>Formula Index</span><strong>公式速查</strong></div><div class="table-wrap"><table class="formula-table"><thead><tr><th>公式</th><th>表达</th><th>章节</th><th>条件</th></tr></thead><tbody>{formula_rows}</tbody></table></div></section>
  <section id="paths"><div class="section-head"><span>Problem Paths</span><strong>题型路径</strong></div><div class="path-grid">{type_cards}</div></section>
  <section id="index"><div class="section-head"><span>Master Index</span><strong>总索引原文</strong></div>{md_to_html(index_md)}</section>
  <section id="chapters"><div class="section-head"><span>Chapters</span><strong>章节全文</strong></div>{chapter_html}</section>
</main>
<aside>
  <div class="aside-title">禁用条件</div>
  <ul class="risk-list">{forbid_cards}</ul>
  <div class="aside-title" style="margin-top:18px;">自测卡片</div>
  <div class="quiz-card"><b>伯努利能跨激波吗？</b><br><button class="tool-btn quiz" aria-expanded="false" aria-controls="quiz-answer-1">显示答案</button><div class="answer" id="quiz-answer-1">不能。激波前后分段，跨激波用激波关系，总压下降。</div></div>
  <div class="quiz-card"><b>局部损失系数答案最少还要写什么？</b><br><button class="tool-btn quiz" aria-expanded="false" aria-controls="quiz-answer-2">显示答案</button><div class="answer" id="quiz-answer-2">写参考速度：hj = zeta v_ref^2/(2g)。</div></div>
  <div class="quiz-card"><b>动量方程最先画什么？</b><br><button class="tool-btn quiz" aria-expanded="false" aria-controls="quiz-answer-3">显示答案</button><div class="answer" id="quiz-answer-3">控制体、外法向、速度矢量和受力对象。</div></div>
</aside>
</div>
<script>
const CHAPTERS = {data};
const search = document.getElementById('search');
const body = document.body;
const doneKey = 'fluid-html-done';
function doneSet() {{ try {{ return new Set(JSON.parse(localStorage.getItem(doneKey) || '[]')); }} catch(e) {{ return new Set(); }} }}
function saveDone(s) {{ localStorage.setItem(doneKey, JSON.stringify([...s])); updateDone(); }}
function updateDone() {{
  const s = doneSet();
  document.getElementById('doneCount').textContent = s.size;
  document.querySelectorAll('.done-btn').forEach(btn => {{
    const on = s.has(btn.dataset.done);
    btn.classList.toggle('done', on);
    btn.textContent = on ? '已完成' : '标记完成';
  }});
}}
let currentFilter = 'all';
let searchTimer = null;
const searchableSelector = '.chapter, .chapter-card, .path-card, .formula-table tbody tr, .risk-list li, .quiz-card';
function cacheSearchText() {{
  document.querySelectorAll(searchableSelector).forEach(el => {{
    el.dataset.searchText = (el.textContent || '').toLowerCase();
  }});
}}
function hasFilter(el, f) {{
  if (f === 'all') return true;
  return ((el.dataset.tags || '') + ' ' + (el.dataset.title || '')).includes(f);
}}
function hasQuery(el, q) {{
  return !q || (el.dataset.searchText || '').includes(q);
}}
function applyFilters() {{
  const q = search.value.trim().toLowerCase();
  let visibleChapters = 0;
  document.querySelectorAll('.chapter-card').forEach(card => {{
    card.classList.toggle('hidden', !hasFilter(card, currentFilter) || !hasQuery(card, q));
  }});
  document.querySelectorAll('.chapter').forEach(ch => {{
    const visible = hasFilter(ch, currentFilter) && hasQuery(ch, q);
    ch.classList.toggle('hidden', !visible);
    if (visible) visibleChapters += 1;
  }});
  document.querySelectorAll('.path-card, .formula-table tbody tr, .risk-list li, .quiz-card').forEach(el => {{
    el.classList.toggle('hidden', !hasQuery(el, q));
  }});
  document.getElementById('resultStatus').textContent = `显示 ${{visibleChapters}} 个章节`;
}}
search.addEventListener('input', () => {{
  clearTimeout(searchTimer);
  searchTimer = setTimeout(applyFilters, 120);
}});
document.querySelectorAll('.chapter-card').forEach(card => card.addEventListener('click', () => {{
  document.getElementById(card.dataset.target).scrollIntoView({{behavior:'smooth', block:'start'}});
}}));
document.querySelectorAll('#filters button').forEach(btn => btn.addEventListener('click', () => {{
  document.querySelectorAll('#filters button').forEach(b => {{
    b.classList.remove('active');
    b.setAttribute('aria-pressed', 'false');
  }});
  btn.classList.add('active');
  btn.setAttribute('aria-pressed', 'true');
  currentFilter = btn.dataset.filter;
  applyFilters();
}}));
const supplementButton = document.getElementById('toggleSupplement');
function syncSupplementButton() {{
  const hidden = body.classList.contains('hide-supplement');
  supplementButton.textContent = hidden ? '显示补充' : '淡化补充';
  supplementButton.setAttribute('aria-pressed', String(!hidden));
}}
supplementButton.addEventListener('click', () => {{
  body.classList.toggle('hide-supplement');
  syncSupplementButton();
}});
document.getElementById('sprintMode').addEventListener('click', () => {{
  body.classList.toggle('sprint');
  const sprint = body.classList.contains('sprint');
  if (sprint) body.classList.add('hide-supplement');
  document.getElementById('sprintMode').textContent = sprint ? '完整模式' : '冲刺模式';
  document.getElementById('sprintMode').setAttribute('aria-pressed', String(sprint));
  syncSupplementButton();
}});
document.querySelectorAll('.done-btn').forEach(btn => btn.addEventListener('click', () => {{
  const s = doneSet();
  s.has(btn.dataset.done) ? s.delete(btn.dataset.done) : s.add(btn.dataset.done);
  saveDone(s);
}}));
document.querySelectorAll('.quiz').forEach(btn => btn.addEventListener('click', () => {{
  const answer = btn.nextElementSibling;
  const open = answer.classList.toggle('show');
  btn.textContent = open ? '收起答案' : '显示答案';
  btn.setAttribute('aria-expanded', String(open));
}}));
cacheSearchText();
updateDone();
syncSupplementButton();
applyFilters();
</script>
</body>
</html>"""


if __name__ == "__main__":
    OUT.write_text(build(), encoding="utf-8")
    print(f"Wrote {OUT}")
