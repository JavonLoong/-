from __future__ import annotations

import html
import re
from html.parser import HTMLParser
from pathlib import Path


HTML_PATH = Path(r"D:\虚拟C盘\大学物理\00_导航与计划\期末复习全套资料\大学物理（2）期末复习全景讲义.html")


MATH_TOKENS = re.compile(
    r"[=<>≈≤≥±∑√^_()|/]|"
    r"\b(Delta|delta|lambda|theta|phi|pi|sigma|nu|hbar|sin|cos|tan|exp|sqrt|psi|Psi)\b"
)


def looks_like_filename(text: str) -> bool:
    s = text.strip()
    return bool(
        re.search(r"(\.pdf|\.md|\.html|\.tex|\.svg|\.png|\.jpg|\.jpeg|\.doc|\.docx)$", s, re.I)
        or re.search(r"^[A-Za-z]:[\\/]", s)
        or ("\\" in s)
    )


def looks_like_math(text: str) -> bool:
    s = text.strip()
    if not s or looks_like_filename(s):
        return False
    if MATH_TOKENS.search(s):
        return True
    if re.fullmatch(r"[A-Za-z](?:_[A-Za-z0-9]+)?", s):
        return True
    if re.fullmatch(r"\d+[A-Za-z_]+", s):
        return True
    if re.fullmatch(r"[A-Za-z][A-Za-z0-9_ ]{0,16}", s) and re.search(r"\d", s):
        return True
    return False


def latexify(expr: str) -> str:
    s = " ".join(expr.strip().split())
    replacements: list[tuple[str, str]] = [
        (r"<=", r"\le "),
        (r">=", r"\ge "),
        (r"->", r"\to "),
        (r"≈", r"\approx "),
        (r"≤", r"\le "),
        (r"≥", r"\ge "),
        (r"±", r"\pm "),
        (r"·", r"\cdot "),
        (r"\bDelta\b", r"\Delta"),
        (r"\bdelta\b", r"\delta"),
        (r"\blambdaC\b", r"\lambda_C"),
        (r"\blambda_m\b", r"\lambda_m"),
        (r"\blambda0\b", r"\lambda_0"),
        (r"\blambda\b", r"\lambda"),
        (r"\btheta\b", r"\theta"),
        (r"\bphi\b", r"\phi"),
        (r"\bpi\b", r"\pi"),
        (r"\bsigma\b", r"\sigma"),
        (r"\bnu0\b", r"\nu_0"),
        (r"\bnu\b", r"\nu"),
        (r"\bhbar\b", r"\hbar"),
        (r"\bPsi\b", r"\Psi"),
        (r"\bpsi\b", r"\psi"),
        (r"\bsin\b", r"\sin"),
        (r"\bcos\b", r"\cos"),
        (r"\btan\b", r"\tan"),
        (r"\bexp\b", r"\exp"),
        (r"\bsum\b", r"\sum"),
        (r"\bmax\b", r"\max"),
        (r"\bmin\b", r"\min"),
        (r"\bavg\b", r"\mathrm{avg}"),
        (r"\bIin\b", r"I_{\mathrm{in}}"),
        (r"\beUs\b", r"eU_s"),
        (r"\bb_max\b", r"b_{\max}"),
        (r"\btheta_min\b", r"\theta_{\min}"),
        (r"\bNmax\b", r"N_{\max}"),
        (r"\bDelta x_shift\b", r"\Delta x_{\mathrm{shift}}"),
        (r"\bDelta x_center\b", r"\Delta x_{\mathrm{center}}"),
        (r"\bEavg\b", r"E_{\mathrm{avg}}"),
        (r"\bpsi1\b", r"\psi_1"),
        (r"\bpsi2\b", r"\psi_2"),
        (r"\bE1\b", r"E_1"),
        (r"\bE2\b", r"E_2"),
        (r"\bx1\b", r"x_1"),
        (r"\bx2\b", r"x_2"),
        (r"\bml\b", r"m_l"),
    ]
    for pattern, repl in replacements:
        s = re.sub(pattern, lambda _m, repl=repl: repl, s)

    prev = None
    while s != prev:
        prev = s
        s = re.sub(r"sqrt\(([^()]+)\)", r"\\sqrt{\1}", s)

    s = re.sub(r"\|\s*([^|]+?)\s*\|", r"| \1 |", s)
    return s


def convert_backticks(text: str) -> str:
    parts = re.split(r"(`[^`]+`)", text)
    if len(parts) == 1:
        return html.escape(text, quote=False)

    out: list[str] = []
    for part in parts:
        if not part:
            continue
        m = re.fullmatch(r"`([^`]+)`", part)
        if not m:
            out.append(html.escape(part, quote=False))
            continue
        content = m.group(1)
        if looks_like_math(content):
            out.append(f'<span class="inline-math">\\({latexify(content)}\\)</span>')
        else:
            out.append(f'<code class="inline-code">{html.escape(content, quote=False)}</code>')
    return "".join(out)


class Transformer(HTMLParser):
    RAW_TAGS = {"script", "style", "pre", "code"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=False)
        self.output: list[str] = []
        self.no_transform_stack: list[bool] = []

    def current_no_transform(self) -> bool:
        return any(self.no_transform_stack)

    def handle_starttag(self, tag: str, attrs) -> None:
        classes = {item for key, val in attrs if key == "class" and val for item in val.split()}
        no_transform = (
            tag in self.RAW_TAGS
            or "formula-sheet" in classes
            or "formula-eq" in classes
            or "mjx-container" in classes
            or "inline-math" in classes
            or "inline-code" in classes
        )
        self.no_transform_stack.append(no_transform)
        self.output.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        if self.no_transform_stack:
            self.no_transform_stack.pop()
        self.output.append(f"</{tag}>")

    def handle_startendtag(self, tag: str, attrs) -> None:
        self.output.append(self.get_starttag_text())

    def handle_data(self, data: str) -> None:
        if self.current_no_transform():
            self.output.append(data)
        else:
            self.output.append(convert_backticks(data))

    def handle_entityref(self, name: str) -> None:
        self.output.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self.output.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self.output.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self.output.append(f"<!{decl}>")

    def handle_pi(self, data: str) -> None:
        self.output.append(f"<?{data}>")

    def get_html(self) -> str:
        return "".join(self.output)


def main() -> None:
    raw = HTML_PATH.read_text(encoding="utf-8")
    parser = Transformer()
    parser.feed(raw)
    parser.close()
    transformed = parser.get_html()

    def upgrade_inline_code(match: re.Match[str]) -> str:
        content = html.unescape(match.group(1))
        if looks_like_math(content):
            return f'<span class="inline-math">\\({latexify(content)}\\)</span>'
        return match.group(0)

    def normalize_inline_math(match: re.Match[str]) -> str:
        inner = match.group(1).replace("\\\\", "\\")
        return f'<span class="inline-math">\\({inner}\\)</span>'

    transformed = re.sub(
        r'<code class="inline-code">([^<]+)</code>',
        upgrade_inline_code,
        transformed,
    )

    transformed = re.sub(
        r'<span class="inline-math">\\\((.*?)\\\)</span>',
        normalize_inline_math,
        transformed,
        flags=re.S,
    )
    HTML_PATH.write_text(transformed, encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
