from __future__ import annotations

import json
from pathlib import Path

from pypdf import PdfReader


ROOT = Path(r"D:\虚拟C盘\学习")
BASE = ROOT / "固体力学"
OUT = BASE / "AI_Learning_OS_期末预编译" / "solid_mechanics_source_outline.json"


def pdf_brief(path: Path, max_pages: int = 2) -> dict:
    item = {
        "name": path.name,
        "relative": str(path.relative_to(BASE)),
        "pages": None,
        "headings": [],
    }
    try:
        reader = PdfReader(str(path))
        item["pages"] = len(reader.pages)
        text = ""
        for page in reader.pages[:max_pages]:
            text += (page.extract_text() or "") + "\n"
        lines = []
        for raw in text.splitlines():
            line = " ".join(raw.strip().split())
            if line and line not in lines:
                lines.append(line)
        item["headings"] = lines[:10]
    except Exception as exc:
        item["error"] = f"{type(exc).__name__}: {exc}"
    return item


def collect() -> dict:
    wujian = [pdf_brief(p) for p in sorted((BASE / "课件" / "吴坚").glob("*.pdf"))]
    yin_dirs = []
    yin_root = BASE / "课件" / "殷雅俊"
    for d in sorted([p for p in yin_root.iterdir() if p.is_dir()], key=lambda p: p.name):
        files = []
        for p in sorted(d.iterdir(), key=lambda p: p.name):
            if p.suffix.lower() in {".pdf", ".ppt", ".pptx"}:
                files.append(
                    {
                        "name": p.name,
                        "relative": str(p.relative_to(BASE)),
                        "type": p.suffix.lower().lstrip("."),
                        "bytes": p.stat().st_size,
                        "pdf_brief": pdf_brief(p) if p.suffix.lower() == ".pdf" else None,
                    }
                )
        yin_dirs.append({"name": d.name, "files": files})
    exams = []
    for p in sorted((BASE / "考题").rglob("*")):
        if p.is_file():
            exams.append({"name": p.name, "relative": str(p.relative_to(BASE)), "bytes": p.stat().st_size})
    return {"wujian": wujian, "yin_yajun": yin_dirs, "exams": exams}


if __name__ == "__main__":
    data = collect()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(OUT)
