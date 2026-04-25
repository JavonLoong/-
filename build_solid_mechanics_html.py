from __future__ import annotations

import html
import json
import re
from pathlib import Path


ROOT = Path(r"D:\虚拟C盘\学习")
SRC = ROOT / "固体力学" / "AI_Learning_OS_期末预编译"
OUT = SRC / "固体力学期末_AI_Learning_OS_图文版.html"
SOURCE_OUTLINE = SRC / "solid_mechanics_source_outline.json"


ORDER = [
    "00_期末总览.md",
    "第01章_材料力学导论.md",
    "第02章_内力分析与内力图.md",
    "第03章_轴向载荷杆件.md",
    "第04章_正应力分析.md",
    "第05章_剪应力分析.md",
    "第06章_应力状态与应变状态.md",
    "第07章_强度失效与强度设计.md",
    "第08章_梁的位移与刚度.md",
    "第09章_压杆稳定.md",
    "第10章_能量方法.md",
    "第11章_简单静不定问题.md",
    "第12章_动载荷与动应力.md",
    "第13章_疲劳强度与寿命估算.md",
    "第14章_复合材料与粘弹性.md",
    "REVIEW_审核记录.md",
]


THEMES = {
    "00": ("总览", "chain", "主链路"),
    "01": ("导论", "specimen", "基本假设"),
    "02": ("内力图", "cut", "截面法"),
    "03": ("轴向", "axial", "拉压变形"),
    "04": ("正应力", "bending", "弯曲应力"),
    "05": ("剪应力", "torsion", "扭转与剪切"),
    "06": ("应力应变", "mohr", "莫尔圆与应变花"),
    "07": ("强度", "failure", "失效准则"),
    "08": ("梁位移", "deflection", "挠曲线"),
    "09": ("稳定", "buckling", "压杆屈曲"),
    "10": ("能量", "energy", "单位载荷法"),
    "11": ("静不定", "indeterminate", "协调方程"),
    "12": ("动载", "impact", "冲击放大"),
    "13": ("疲劳", "fatigue", "S-N 曲线"),
    "14": ("复合/粘弹", "composite", "层合与模型"),
    "RV": ("审核", "review", "审核闭环"),
}

CHAPTER_ENRICHMENT = {
    "ch00": {
        "course": "课程总览：吴坚 14 章 + 殷雅俊 PPT/习题线",
        "weight": "总控",
        "ppt": ["吴坚第 1-14 章 PDF", "殷雅俊第 1-11 章 PPT/习题主题", "历年期末、模拟卷、2024 回忆版"],
        "sections": ["课程线：按课件章序查漏", "考试线：按题型权重刷题", "交叉线：每个 PPT 小节都要落到题型动作"],
        "exam": ["先用课程线补概念和公式来源", "再用考试线决定刷题顺序", "最后用错题线回到对应 PPT 小节复盘"],
    },
    "ch01": {
        "course": "材料力学对象、基本假设、杆件模型、强度/刚度/稳定任务",
        "weight": "低频基础",
        "ppt": ["吴坚第 1 章《材料力学导论》", "殷雅俊 {1}--第1章材料力学概论"],
        "sections": ["材料力学研究对象", "可变形固体基本假设", "内力、应力、应变、位移的层级", "强度、刚度、稳定的工程判据"],
        "exam": ["概念题和选择题常考基本假设", "计算题开头必须说明构件模型和校核目标", "作为所有题型的答题语言库"],
    },
    "ch02": {
        "course": "受力图、截面法、轴力/剪力/弯矩/扭矩、内力图",
        "weight": "高频入口",
        "ppt": ["吴坚第 2 章《内力分析与内力图》", "殷雅俊 {5}--梁的弯曲问题（1）剪力图与弯矩图"],
        "sections": ["约束反力与受力图", "截面法正负号", "N/V/M/T 内力方程", "载荷-剪力-弯矩微分关系", "内力图面积/斜率法"],
        "exam": ["几乎所有综合题第一步", "剪力图/弯矩图单独成题概率高", "错在支反力或符号会整题连锁失分"],
    },
    "ch03": {
        "course": "轴向拉压应力、变形、强度刚度、简单静不定雏形",
        "weight": "中高频",
        "ppt": ["吴坚第 3 章《轴向载荷作用下杆件》", "殷雅俊 {2}--拉伸与压缩杆件的应力变形分析与强度计算"],
        "sections": ["轴力图", "sigma=N/A", "Delta l=sum NL/EA", "许用应力与安全系数", "温度/装配引起的轴向静不定"],
        "exam": ["基础计算题常见", "可与静不定、温度应力组合", "注意分段面积和拉压符号"],
    },
    "ch04": {
        "course": "截面几何性质、弯曲正应力、梁强度设计",
        "weight": "高频核心",
        "ppt": ["吴坚第 4 章《横截面上正应力分析》", "殷雅俊 {6}--截面的几何性质", "殷雅俊 {7}--梁的弯曲应力与强度计算"],
        "sections": ["形心与惯性矩", "平行移轴公式", "纯弯曲假设", "sigma=My/I", "危险截面与危险点"],
        "exam": ["弯曲强度设计几乎必备", "常与剪弯图、截面选择结合", "几何量单位和 y 取值是高频坑"],
    },
    "ch05": {
        "course": "连接件剪切/挤压、圆轴扭转、梁横向剪应力",
        "weight": "中高频",
        "ppt": ["吴坚第 5 章《剪应力分析》", "殷雅俊 {3}--连接杆件工程假定计算", "殷雅俊 {4}--圆轴扭转强度与刚度"],
        "sections": ["剪切与挤压假定计算", "圆轴扭矩图", "tau=T rho/Ip", "phi=TL/GIp", "tau=VQ/(Ib)", "矩形/工字形剪应力分布"],
        "exam": ["扭转强度刚度题常见", "连接件小题常以剪切/挤压面积设陷阱", "梁剪应力常作为弯曲强度补充"],
    },
    "ch06": {
        "course": "平面应力、莫尔圆、广义胡克定律、应变花",
        "weight": "高频综合",
        "ppt": ["吴坚第 6 章《应力状态与应变状态分析》", "殷雅俊 {9}--应力状态与强度理论及其工程应用"],
        "sections": ["一点应力状态", "应力变换", "主应力与最大剪应力", "莫尔圆", "应变变换与应变花", "平面应力胡克定律"],
        "exam": ["弯扭组合和强度理论前置", "主应力/最大剪应力公式必须会", "应变花若出现通常是区分度题"],
    },
    "ch07": {
        "course": "强度失效理论、塑性/脆性材料准则、组合应力校核",
        "weight": "高频综合",
        "ppt": ["吴坚第 7 章《强度失效与强度设计》", "殷雅俊 {9}--应力状态与强度理论及其工程应用"],
        "sections": ["第一到第四强度理论定位", "最大拉应力理论", "Tresca 与 von Mises", "弯扭组合强度校核", "材料性质与准则选择"],
        "exam": ["综合题最后校核环节", "常与第 6 章主应力联动", "准则选错会导致结论全错"],
    },
    "ch08": {
        "course": "梁挠曲线、积分法、叠加法、刚度条件",
        "weight": "高频核心",
        "ppt": ["吴坚第 8 章《梁的位移分析与刚度设计》", "殷雅俊 {8}--梁的弯曲位移分析与刚度计算"],
        "sections": ["挠曲线近似微分方程", "积分法边界条件", "叠加法", "转角与挠度表", "刚度校核"],
        "exam": ["挠度/转角题常见", "可与静不定和能量法互相替代", "边界条件是第一失分点"],
    },
    "ch09": {
        "course": "压杆稳定、有效长度、欧拉公式、稳定安全系数",
        "weight": "中高频",
        "ppt": ["吴坚第 9 章《压杆稳定》", "殷雅俊 {10}--压杆稳定问题"],
        "sections": ["稳定与强度差异", "端部约束与长度系数", "Euler 临界力", "柔度与适用范围", "稳定校核"],
        "exam": ["常以独立小题出现", "弱轴和有效长度是核心", "先判 Euler 适用再算 Pcr"],
    },
    "ch10": {
        "course": "应变能、Castigliano 定理、单位载荷法",
        "weight": "高频方法",
        "ppt": ["吴坚第 10 章《材料力学中的能量方法》", "殷雅俊 {11}--材料力学中的能量法"],
        "sections": ["轴向/弯曲/扭转应变能", "外力功与互等定理", "Castigliano 定理", "单位载荷法", "分段积分"],
        "exam": ["位移计算高频替代路线", "静不定求多余约束力常用", "单位载荷方向和内力函数必须写清"],
    },
    "ch11": {
        "course": "轴向、扭转、梁的简单静不定系统",
        "weight": "高频综合",
        "ppt": ["吴坚第 11 章《简单的静不定问题》", "与殷雅俊第 2/4/8/11 章内容交叉"],
        "sections": ["静不定次数", "平衡方程", "变形协调", "本构关系", "力法基本结构", "温度/装配应力"],
        "exam": ["综合计算题常见", "不能只列平衡", "协调方程写错会整题失控"],
    },
    "ch12": {
        "course": "动载荷、动应力、冲击、动荷系数",
        "weight": "中低频",
        "ppt": ["吴坚第 12 章《动载荷与动应力概述》"],
        "sections": ["等加速度载荷", "突然加载", "冲击能量法", "动荷系数", "动应力强度校核"],
        "exam": ["多为小题或附加题", "冲击题必须先求静位移", "最后仍回到强度校核"],
    },
    "ch13": {
        "course": "循环应力、S-N 曲线、疲劳极限、寿命估算",
        "weight": "中低频",
        "ppt": ["吴坚第 13 章《疲劳强度与寿命估算》"],
        "sections": ["交变应力参数", "S-N 曲线", "疲劳极限修正", "Goodman/Soderberg 思路", "寿命与安全系数"],
        "exam": ["概念和小计算均可能", "不要用静强度代替疲劳强度", "平均应力和应力幅要先拆清"],
    },
    "ch14": {
        "course": "复合材料方向性、层合板、聚合物粘弹性模型",
        "weight": "低频拓展",
        "ppt": ["吴坚第 14 章《复合材料与粘弹性》"],
        "sections": ["纤维方向与横向模量", "规则混合法", "层合概念", "蠕变与松弛", "Maxwell/Kelvin 模型"],
        "exam": ["多为概念或简单代入", "核心是方向性和时间效应", "不能按各向同性材料盲算"],
    },
    "review": {
        "course": "生成材料的审核与纠偏记录",
        "weight": "质量控制",
        "ppt": ["不对应具体 PPT，是本 HTML 的质量追踪"],
        "sections": ["审核结论", "必须修正项", "建议增强项", "纠偏状态"],
        "exam": ["用于确认公式、章节和图示没有偏离课程/考试目标"],
    },
}

EXAM_TRACKS = [
    ("T1", "内力图、剪力图、弯矩图", "16 / A级", "第02章；殷雅俊第5专题", "受力图 -> 支反力 -> 分段截面 -> V/M 图 -> 端点与跳跃校核"),
    ("T2", "梁弯曲应力、截面性质、强度校核", "18 / A级", "第04、05章；殷雅俊第6/7专题", "剪弯图 -> Mmax/Vmax -> I/W/Q -> sigma/tau -> 危险点校核"),
    ("T3", "梁位移、刚度、能量法", "15 / A级", "第08、10章；殷雅俊第8/11专题", "M(x) 或单位载荷 -> 积分/叠加/能量法 -> 边界条件 -> 刚度结论"),
    ("T4", "应力状态、莫尔圆、强度理论、组合变形", "16 / A级", "第06、07章；殷雅俊第9专题", "危险点应力 -> 主应力/最大剪应力 -> 强度准则 -> 安全结论"),
    ("T5", "轴向拉压、变形、静不定、温度应力", "12 / B+级", "第03、11章；殷雅俊第2专题", "轴力图 -> sigma/Delta l -> 平衡 + 协调 + 本构 -> 反力或应力"),
    ("T6", "扭转、连接件剪切/挤压", "10 / B级", "第05章；殷雅俊第3/4专题", "扭矩图/剪切面 -> tau/挤压应力/phi -> 强度与刚度双校核"),
    ("T7", "压杆稳定", "8 / B级", "第09章；殷雅俊第10专题", "端部约束 -> 有效长度 -> Euler/柔度 -> 稳定安全系数"),
    ("T8", "动载荷、疲劳、复合材料、粘弹性", "3 / C级", "第12-14章", "识别类型 -> 专用公式或概念卡 -> 回到强度、寿命或时间效应结论"),
    ("T9", "基本概念、单位、假设、边界条件", "2 / C级", "第01章及全章散点", "判断模型 -> 写单位 -> 明确边界条件 -> 避免低级扣分"),
]

PPT_TOPICS = [
    ("P1", "殷雅俊第1专题：材料力学概论", "ch01", "T9", "基本假设、研究对象、强度/刚度/稳定语言"),
    ("P2", "殷雅俊第2专题：拉伸与压缩", "ch03", "T5", "轴力图、拉压应力、变形、轴向静不定"),
    ("P3", "殷雅俊第3专题：连接件工程假定", "ch05", "T6", "剪切面、挤压面、连接件许用应力校核"),
    ("P4", "殷雅俊第4专题：圆轴扭转", "ch05", "T6", "扭矩图、扭转剪应力、扭转角、刚度校核"),
    ("P5", "殷雅俊第5专题：剪力图与弯矩图", "ch02", "T1", "支反力、截面法、q-V-M 关系和跳跃规则"),
    ("P6", "殷雅俊第6专题：截面几何性质", "ch04", "T2", "形心、惯性矩、平行移轴、抗弯截面系数"),
    ("P7", "殷雅俊第7专题：梁应力与强度", "ch04", "T2", "弯曲正应力、梁剪应力、危险截面与危险点"),
    ("P8", "殷雅俊第8专题：梁位移与刚度", "ch08", "T3", "挠曲线、积分法、叠加法、刚度校核"),
    ("P9", "殷雅俊第9专题：应力状态与强度理论", "ch06", "T4", "莫尔圆、主应力、强度理论、组合变形"),
    ("P10", "殷雅俊第10专题：压杆稳定", "ch09", "T7", "有效长度、Euler 临界力、柔度和稳定设计"),
    ("P11", "殷雅俊第11专题：能量法", "ch10", "T3", "应变能、卡氏定理、单位载荷法、静不定辅助"),
]


def slug_for(name: str) -> str:
    if name.startswith("00"):
        return "ch00"
    if name.startswith("REVIEW"):
        return "review"
    m = re.search(r"第(\d+)章", name)
    return f"ch{m.group(1)}" if m else "section"


def theme_key(name: str) -> str:
    if name.startswith("00"):
        return "00"
    if name.startswith("REVIEW"):
        return "RV"
    m = re.search(r"第(\d+)章", name)
    return m.group(1) if m else "00"


def chapter_id_from_number(num: str | int) -> str:
    return f"ch{int(num):02d}" if str(num).isdigit() else str(num)


def load_source_outline() -> dict:
    if not SOURCE_OUTLINE.exists():
        return {"wujian": [], "yin_yajun": [], "exams": []}
    return json.loads(SOURCE_OUTLINE.read_text(encoding="utf-8"))


def wujian_pages(outline: dict) -> dict[str, str]:
    grouped: dict[str, list[dict]] = {}
    for item in outline.get("wujian", []):
        m = re.search(r"第(\d+)章", item.get("name", ""))
        if m:
            grouped.setdefault(chapter_id_from_number(m.group(1)), []).append(item)
    pages: dict[str, str] = {}
    for chapter_id, items in grouped.items():
        preferred = sorted(
            items,
            key=lambda x: (
                "新" not in x.get("name", ""),
                x.get("name", ""),
            ),
        )[0]
        suffix = "（新）" if "新" in preferred.get("name", "") and len(items) > 1 else ""
        pages[chapter_id] = f"{preferred.get('pages') or '未抽取'}{suffix}"
    return pages


def numeric_pages(value: str) -> int:
    m = re.match(r"(\d+)", value or "")
    return int(m.group(1)) if m else 0


def pill(text: str) -> str:
    return f"<span class=\"pill\">{html.escape(text)}</span>"


def render_bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{inline_md(item)}</li>" for item in items) + "</ul>"


def render_enrichment(card: dict[str, str]) -> str:
    info = CHAPTER_ENRICHMENT.get(card["id"], {})
    if not info:
        return ""
    page_note = f"吴坚课件页数：{card.get('wujian_pages', '未对应')}" if card["id"].startswith("ch") and card["id"] != "ch00" else "来源：课程总览与审核记录"
    ppt_tags = "".join(pill(x) for x in info.get("ppt", []))
    course_sections = render_bullets(info.get("sections", []))
    exam_items = render_bullets(info.get("exam", []))
    return f"""
      <section class="enrichment">
        <div class="meta-grid">
          <div><strong>课程/PPT定位</strong><p>{inline_md(info.get("course", ""))}</p></div>
          <div><strong>考试权重</strong><p><span class="weight">{html.escape(info.get("weight", ""))}</span></p></div>
          <div><strong>源材料依据</strong><p>{html.escape(page_note)}</p><div class="pill-row">{ppt_tags}</div></div>
        </div>
        <div class="dual-block">
          <div>
            <h3>课程/PPT小节展开</h3>
            {course_sections}
          </div>
          <div>
            <h3>考试可能性与题型入口</h3>
            {exam_items}
          </div>
        </div>
      </section>
    """


def render_course_index(cards: list[dict[str, str]]) -> str:
    rows = []
    for c in cards:
        if not c["id"].startswith("ch") or c["id"] == "ch00":
            continue
        info = CHAPTER_ENRICHMENT.get(c["id"], {})
        rows.append(
            "<tr>"
            f"<td><a href=\"#{c['id']}\">{html.escape(c['short'])}</a></td>"
            f"<td>{inline_md(info.get('course', c['title']))}</td>"
            f"<td>{', '.join(html.escape(x) for x in info.get('ppt', []))}</td>"
            f"<td>{html.escape(c.get('wujian_pages', ''))}</td>"
            "</tr>"
        )
    return f"""
      <section class="index-section" id="course-map">
        <div class="section-title">
          <p class="eyebrow">Course / PPT</p>
          <h2>课程/PPT目录线</h2>
          <p>这条线按课件走，解决“有没有按 PPT 讲过的内容覆盖到”的问题。吴坚 PDF 是 14 章主线，殷雅俊 PPT 细分了拉压、连接件、扭转、梁的四段、应力强度、压杆和能量法。</p>
        </div>
        <div class="table-wrap"><table>
          <thead><tr><th>入口</th><th>课程小节覆盖</th><th>PPT/课件依据</th><th>吴坚页数</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table></div>
      </section>
    """


def render_ppt_topic_index(outline: dict) -> str:
    topic_count = len(outline.get("yin_yajun", []))
    exam_count = len(outline.get("exams", []))
    rows = []
    for code, topic, chapter, track, action in PPT_TOPICS:
        rows.append(
            "<tr>"
            f"<td id=\"ppt-{code.lower()}\">{html.escape(code)}</td>"
            f"<td>{html.escape(topic)}</td>"
            f"<td><a href=\"#{chapter}\">{html.escape(chapter.upper())}</a></td>"
            f"<td>{html.escape(track)}</td>"
            f"<td>{inline_md(action)}</td>"
            "</tr>"
        )
    return f"""
      <section class="index-section" id="ppt-topic-map">
        <div class="section-title">
          <p class="eyebrow">PPT Topics</p>
          <h2>殷雅俊 PPT 专题级目录</h2>
          <p>这里把殷雅俊的 {topic_count} 个 PPT/习题专题直接映射到章节和 T1-T9 考试线；考题库当前索引到 {exam_count} 个文件，用作考试线索来源，不把未逐题统计的内容伪装成精确频率。</p>
        </div>
        <div class="table-wrap"><table>
          <thead><tr><th>专题</th><th>PPT 主题</th><th>回到章节</th><th>考试线</th><th>复习动作</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table></div>
      </section>
    """


def render_exam_index() -> str:
    cards = []
    for code, name, weight, chapters, action in EXAM_TRACKS:
        cards.append(
            f"<article class=\"exam-card\"><div><span class=\"exam-code\">{code}</span><h3>{html.escape(name)}</h3></div>"
            f"<p><strong>权重：</strong>{html.escape(weight)}</p>"
            f"<p><strong>关联：</strong>{html.escape(chapters)}</p>"
            f"<p><strong>答题动作：</strong>{inline_md(action)}</p></article>"
        )
    return f"""
      <section class="index-section" id="exam-map">
        <div class="section-title">
          <p class="eyebrow">Exam Priority</p>
          <h2>考试可能性目录线</h2>
          <p>这条线按“最可能拿分的题型动作”走。先刷极高/高频，再补中低频章节；但每个题型都能回到对应 PPT 小节。</p>
        </div>
        <div class="exam-grid">{''.join(cards)}</div>
      </section>
    """


def render_cross_index() -> str:
    rows = []
    for code, topic, chapter, track, action in PPT_TOPICS:
        rows.append(
            "<tr>"
            f"<td><a href=\"#ppt-{code.lower()}\">{html.escape(code)} {html.escape(topic)}</a></td>"
            f"<td><a href=\"#{chapter}\">{html.escape(chapter.upper())}</a></td>"
            f"<td>{html.escape(track)}</td>"
            f"<td>{inline_md(action)}</td>"
            "</tr>"
        )
    return f"""
      <section class="index-section" id="cross-map">
        <div class="section-title">
          <p class="eyebrow">Cross Index</p>
          <h2>PPT-考试交叉索引</h2>
          <p>每个课程小节都要落到一个考试动作；每个考试动作都能回到课件源头复盘。这样既不漏课，也不被低频内容拖慢。</p>
        </div>
        <div class="table-wrap"><table>
          <thead><tr><th>PPT 专题</th><th>回看章节</th><th>对应考试线</th><th>标准动作</th></tr></thead>
          <tbody>{''.join(rows)}</tbody>
        </table></div>
      </section>
    """


def render_sprint_index() -> str:
    return """
      <section class="index-section" id="sprint-map">
        <div class="section-title">
          <p class="eyebrow">Final Sprint</p>
          <h2>考前冲刺查漏清单</h2>
          <p>用这张表安排最后一轮：先保 A 级大题，再稳 B 级小综合，最后扫 C 级概念。它不是兜底，而是把有限时间投到最可能得分的位置。</p>
        </div>
        <div class="exam-grid">
          <article class="exam-card"><div><span class="exam-code">A</span><h3>必刷大题线</h3></div><p>内力图、弯曲强度、梁位移/能量法、应力状态与强度理论。</p><p><strong>动作：</strong>每条至少做 2 道限时题，写完整校核结论。</p></article>
          <article class="exam-card"><div><span class="exam-code">B</span><h3>稳分综合线</h3></div><p>轴向拉压静不定、扭转与连接件、压杆稳定。</p><p><strong>动作：</strong>整理公式适用条件和典型面积/长度系数。</p></article>
          <article class="exam-card"><div><span class="exam-code">C</span><h3>概念速查线</h3></div><p>动载、疲劳、复合材料、粘弹性、基本假设和单位。</p><p><strong>动作：</strong>用复习卡片扫定义、曲线、模型和常见判断题。</p></article>
        </div>
      </section>
    """


def inline_md(text: str) -> str:
    text = html.escape(text)
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    return text


def is_table_block(lines: list[str], i: int) -> bool:
    return i + 1 < len(lines) and "|" in lines[i] and re.match(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?\s*$", lines[i + 1])


def render_table(block: list[str]) -> str:
    rows: list[list[str]] = []
    for line in block:
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows.append(cells)
    if len(rows) < 2:
        return ""
    head = rows[0]
    body = rows[2:]
    out = ["<div class=\"table-wrap\"><table>", "<thead><tr>"]
    out.extend(f"<th>{inline_md(c)}</th>" for c in head)
    out.append("</tr></thead><tbody>")
    for row in body:
        out.append("<tr>")
        out.extend(f"<td>{inline_md(c)}</td>" for c in row)
        out.append("</tr>")
    out.append("</tbody></table></div>")
    return "".join(out)


def render_markdown(md: str) -> str:
    lines = md.splitlines()
    out: list[str] = []
    i = 0
    in_ul = False
    in_ol = False
    in_code = False
    code_buf: list[str] = []

    def close_lists() -> None:
        nonlocal in_ul, in_ol
        if in_ul:
            out.append("</ul>")
            in_ul = False
        if in_ol:
            out.append("</ol>")
            in_ol = False

    while i < len(lines):
        line = lines[i]
        stripped = line.strip()

        if stripped.startswith("```"):
            if not in_code:
                close_lists()
                in_code = True
                code_buf = []
            else:
                out.append("<pre class=\"diagram-text\"><code>" + html.escape("\n".join(code_buf)) + "</code></pre>")
                in_code = False
            i += 1
            continue
        if in_code:
            code_buf.append(line)
            i += 1
            continue

        if not stripped:
            close_lists()
            i += 1
            continue

        if is_table_block(lines, i):
            close_lists()
            block = [lines[i], lines[i + 1]]
            i += 2
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                block.append(lines[i])
                i += 1
            out.append(render_table(block))
            continue

        h = re.match(r"^(#{1,4})\s+(.+)$", stripped)
        if h:
            close_lists()
            level = min(len(h.group(1)) + 1, 5)
            title = inline_md(h.group(2))
            out.append(f"<h{level}>{title}</h{level}>")
            i += 1
            continue

        ordered = re.match(r"^\d+\.\s+(.+)$", stripped)
        if ordered:
            if in_ul:
                out.append("</ul>")
                in_ul = False
            if not in_ol:
                out.append("<ol>")
                in_ol = True
            out.append(f"<li>{inline_md(ordered.group(1))}</li>")
            i += 1
            continue

        unordered = re.match(r"^[-*]\s+(.+)$", stripped)
        if unordered:
            if in_ol:
                out.append("</ol>")
                in_ol = False
            if not in_ul:
                out.append("<ul>")
                in_ul = True
            out.append(f"<li>{inline_md(unordered.group(1))}</li>")
            i += 1
            continue

        close_lists()
        out.append(f"<p>{inline_md(stripped)}</p>")
        i += 1

    close_lists()
    return "\n".join(out)


def svg(kind: str) -> str:
    common = "viewBox=\"0 0 520 220\" role=\"img\" aria-hidden=\"true\""
    if kind == "chain":
        labels = ["受力图", "截面法", "平衡", "内力", "应力/变形", "校核"]
        parts = [f"<svg {common}>"]
        for idx, lab in enumerate(labels):
            x = 18 + idx * 82
            parts.append(f"<rect x=\"{x}\" y=\"76\" width=\"72\" height=\"48\" rx=\"8\"/><text x=\"{x+36}\" y=\"105\">{lab}</text>")
            if idx < len(labels) - 1:
                parts.append(f"<path d=\"M{x+74} 100 H{x+96}\"/><path d=\"M{x+90} 94 l8 6 -8 6\"/>")
        parts.append("</svg>")
        return "".join(parts)
    if kind == "specimen":
        return f"""<svg {common}><rect x="78" y="86" width="360" height="48" rx="24"/><rect x="196" y="74" width="128" height="72" rx="10"/><path d="M64 110 H20"/><path d="M456 110 h44"/><path d="M28 102 l-12 8 12 8"/><path d="M492 102 l12 8 -12 8"/><text x="260" y="42">连续、均匀、各向同性、小变形</text><text x="260" y="118">试件</text></svg>"""
    if kind == "cut":
        return f"""<svg {common}><rect x="54" y="82" width="320" height="56" rx="4"/><line x1="216" y1="62" x2="216" y2="158"/><path d="M390 110 h82"/><path d="M462 102 l14 8 -14 8"/><text x="214" y="48">截面</text><text x="108" y="116">外载</text><text x="430" y="92">N,V,M,T</text><path d="M90 70 v-42"/><path d="M82 34 l8-12 8 12"/></svg>"""
    if kind == "axial":
        return f"""<svg {common}><rect x="90" y="88" width="320" height="44" rx="6"/><path d="M80 110 H24"/><path d="M440 110 h56"/><path d="M32 102 l-12 8 12 8"/><path d="M488 102 l12 8 -12 8"/><line x1="90" y1="154" x2="410" y2="154"/><path d="M90 148 v12M410 148 v12"/><text x="250" y="178">Delta l = NL/EA</text><text x="250" y="74">sigma = N/A</text></svg>"""
    if kind == "bending":
        return f"""<svg {common}><rect x="70" y="94" width="350" height="32" rx="4"/><path d="M100 150 q150 36 290 0"/><path d="M118 64 q130 -34 260 0"/><line x1="255" y1="60" x2="255" y2="160"/><polygon points="276,70 352,94 276,118"/><polygon points="276,126 352,126 276,154"/><text x="260" y="42">弯曲正应力 sigma = My/I</text><text x="354" y="110">拉/压线性分布</text></svg>"""
    if kind == "torsion":
        return f"""<svg {common}><rect x="118" y="82" width="284" height="56" rx="28"/><ellipse cx="118" cy="110" rx="24" ry="28"/><ellipse cx="402" cy="110" rx="24" ry="28"/><path d="M84 82 q-34 28 0 56"/><path d="M438 82 q34 28 0 56"/><path d="M70 98 l-10 -14M70 122 l-10 14M450 98 l10 -14M450 122 l10 14"/><text x="260" y="54">tau = T rho / Ip</text><text x="260" y="170">phi = TL / GIp</text></svg>"""
    if kind == "mohr":
        return f"""<svg {common}><rect x="78" y="72" width="84" height="84"/><path d="M120 72 v-34M120 156 v34M78 114 h-34M162 114 h34"/><path d="M92 60 h54M92 168 h54"/><circle cx="344" cy="112" r="68"/><line x1="250" y1="112" x2="448" y2="112"/><line x1="344" y1="34" x2="344" y2="190"/><circle cx="344" cy="112" r="4"/><text x="120" y="40">应力单元</text><text x="344" y="34">莫尔圆</text><text x="434" y="104">sigma</text><text x="356" y="50">tau</text></svg>"""
    if kind == "failure":
        return f"""<svg {common}><line x1="92" y1="176" x2="432" y2="176"/><line x1="112" y1="194" x2="112" y2="34"/><path d="M132 154 C184 74, 304 58, 402 114"/><path d="M150 154 L230 74 L366 126 L288 176 Z"/><text x="252" y="42">强度理论选择</text><text x="410" y="170">sigma1</text><text x="92" y="42">sigma2</text></svg>"""
    if kind == "deflection":
        return f"""<svg {common}><rect x="60" y="76" width="34" height="86"/><line x1="94" y1="104" x2="438" y2="104"/><path d="M94 104 C190 120, 300 154, 438 166"/><path d="M310 70 v50"/><path d="M302 112 l8 12 8-12"/><text x="268" y="52">EI v'' = M(x)</text><text x="274" y="184">边界条件 + 连续条件</text></svg>"""
    if kind == "buckling":
        return f"""<svg {common}><line x1="160" y1="42" x2="160" y2="180"/><path d="M160 42 C236 78, 84 142, 160 180"/><rect x="122" y="28" width="76" height="14"/><rect x="122" y="180" width="76" height="14"/><path d="M160 20 v26M160 202 v-26"/><text x="314" y="86">Pcr = pi^2 EI/(mu L)^2</text><text x="314" y="126">弱轴 + 有效长度</text></svg>"""
    if kind == "energy":
        return f"""<svg {common}><path d="M78 154 C160 94, 236 90, 316 142 S432 170 470 96"/><path d="M260 60 v84"/><path d="M252 136 l8 12 8-12"/><circle cx="260" cy="60" r="16"/><text x="260" y="40">单位载荷 1</text><text x="260" y="186">delta = ∫ M m / EI dx</text></svg>"""
    if kind == "indeterminate":
        return f"""<svg {common}><rect x="72" y="74" width="22" height="88"/><rect x="426" y="74" width="22" height="88"/><rect x="94" y="100" width="332" height="36"/><path d="M260 70 v60"/><path d="M252 122 l8 12 8-12"/><text x="260" y="52">平衡 + 协调 + 本构</text><text x="260" y="168">多余约束力</text></svg>"""
    if kind == "impact":
        return f"""<svg {common}><line x1="92" y1="36" x2="428" y2="36"/><path d="M260 36 v28 l-24 12 48 20 -48 20 48 20 -24 12 v20"/><rect x="222" y="168" width="76" height="34" rx="4"/><path d="M182 68 v62"/><path d="M174 122 l8 12 8-12"/><text x="146" y="60">h</text><text x="352" y="106">Kd = 1 + sqrt(1+2h/delta_st)</text></svg>"""
    if kind == "fatigue":
        return f"""<svg {common}><line x1="84" y1="178" x2="444" y2="178"/><line x1="108" y1="190" x2="108" y2="34"/><path d="M120 58 C190 88, 236 118, 412 158"/><path d="M134 128 q34 -52 68 0 t68 0"/><text x="268" y="50">S-N 曲线</text><text x="424" y="170">log N</text><text x="76" y="46">sigma_a</text></svg>"""
    if kind == "composite":
        return f"""<svg {common}><rect x="70" y="62" width="188" height="96" rx="6"/><path d="M70 86 H258M70 110 H258M70 134 H258"/><text x="164" y="178">0/90/±45 层合</text><rect x="318" y="58" width="68" height="34" rx="4"/><path d="M386 75 h44"/><path d="M430 58 v34"/><path d="M430 75 h48"/><rect x="478" y="58" width="18" height="34"/><text x="410" y="128">Maxwell / Kelvin</text></svg>"""
    if kind == "review":
        labels = ["生成", "审核", "纠偏", "验证"]
        parts = [f"<svg {common}>"]
        for idx, lab in enumerate(labels):
            x = 70 + idx * 108
            parts.append(f"<rect x=\"{x}\" y=\"78\" width=\"78\" height=\"48\" rx=\"8\"/><text x=\"{x+39}\" y=\"103\">{lab}</text>")
            if idx < len(labels) - 1:
                parts.append(f"<path d=\"M{x+82} 102 H{x+106}\"/><path d=\"M{x+100} 96 l9 6 -9 6\"/>")
        parts.append("<text x=\"260\" y=\"154\">公式血缘、图示、交互、打印闭环</text></svg>")
        return "".join(parts)
    return f"""<svg {common}><rect x="86" y="62" width="348" height="96" rx="12"/><text x="260" y="116">审核闭环</text></svg>"""


def build_card(file_name: str, md: str) -> dict[str, str]:
    first = next((ln.strip("# ").strip() for ln in md.splitlines() if ln.startswith("# ")), file_name)
    key = theme_key(file_name)
    short, kind, tag = THEMES.get(key, THEMES["00"])
    rendered = render_markdown(md)
    plain = re.sub(r"\s+", " ", re.sub(r"[#`|*\-]", " ", md))
    return {
        "id": slug_for(file_name),
        "file": file_name,
        "title": first,
        "short": short,
        "tag": tag,
        "svg": svg(kind),
        "html": rendered,
        "plain": html.escape(plain[:2000]),
    }


def html_doc(cards: list[dict[str, str]], outline: dict) -> str:
    nav = "\n".join(
        f"<a href=\"#{c['id']}\" data-target=\"{c['id']}\"><span>{c['short']}</span><small>{html.escape(c['tag'])}</small></a>"
        for c in cards
    )
    stat_chapters = len([c for c in cards if c["id"].startswith("ch") and c["id"] != "ch00"])
    total_pages = sum(numeric_pages(c.get("wujian_pages", "")) for c in cards)
    course_index = render_course_index(cards)
    ppt_topic_index = render_ppt_topic_index(outline)
    exam_index = render_exam_index()
    cross_index = render_cross_index()
    sprint_index = render_sprint_index()
    articles = "\n".join(
        f"""
        <article class="chapter" id="{c['id']}" data-title="{html.escape(c['title'])}" data-text="{c['plain']}">
          <header class="chapter-head">
            <div>
              <p class="eyebrow">{html.escape(c['file'])}</p>
              <h2>{html.escape(c['title'])}</h2>
              <p class="chapter-tag">{html.escape(c['tag'])}</p>
            </div>
            <figure class="visual">{c['svg']}</figure>
          </header>
          {render_enrichment(c)}
          <details open class="chapter-body">
            <summary>展开 / 收起本章内容</summary>
            <div class="content">{c['html']}</div>
          </details>
        </article>
        """
        for c in cards
    )
    return f"""<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>固体力学期末 AI Learning OS 图文版</title>
  <style>
    :root {{
      --bg: #f6f7f3;
      --paper: #fffdf8;
      --ink: #202321;
      --muted: #5e665f;
      --line: #d9ddd4;
      --accent: #0f766e;
      --accent-2: #b45309;
      --accent-3: #2563eb;
      --danger: #b91c1c;
      --shadow: 0 18px 48px rgba(31, 41, 35, .12);
      --radius: 8px;
    }}
    * {{ box-sizing: border-box; }}
    html {{ scroll-behavior: smooth; }}
    body {{
      margin: 0;
      font-family: "Microsoft YaHei", "PingFang SC", "Segoe UI", Arial, sans-serif;
      color: var(--ink);
      background: var(--bg);
      line-height: 1.65;
    }}
    .app {{
      display: grid;
      grid-template-columns: 292px minmax(0, 1fr);
      min-height: 100vh;
    }}
    aside {{
      position: sticky;
      top: 0;
      height: 100vh;
      overflow: auto;
      border-right: 1px solid var(--line);
      background: #f1f4ee;
      padding: 18px 14px;
    }}
    .brand h1 {{
      margin: 0 0 6px;
      font-size: 22px;
      line-height: 1.2;
      letter-spacing: 0;
    }}
    .brand p {{ margin: 0 0 14px; color: var(--muted); font-size: 13px; }}
    .controls {{ display: grid; gap: 10px; margin: 14px 0; }}
    input[type="search"] {{
      width: 100%;
      height: 40px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 0 12px;
      background: var(--paper);
      font-size: 14px;
    }}
    .button-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }}
    button {{
      height: 36px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--paper);
      color: var(--ink);
      cursor: pointer;
      font-size: 13px;
    }}
    button:hover, nav a:hover {{ border-color: var(--accent); }}
    .nav-block {{
      display: grid;
      gap: 6px;
      margin-top: 14px;
      padding-top: 12px;
      border-top: 1px solid var(--line);
    }}
    .nav-label {{
      margin: 0 0 4px;
      color: var(--muted);
      font-size: 12px;
      font-weight: 700;
    }}
    nav {{ display: grid; gap: 6px; margin-top: 14px; }}
    nav a {{
      display: grid;
      grid-template-columns: 1fr auto;
      align-items: center;
      gap: 10px;
      min-height: 38px;
      padding: 8px 10px;
      color: var(--ink);
      text-decoration: none;
      border: 1px solid transparent;
      border-radius: var(--radius);
    }}
    nav a.active {{ background: var(--paper); border-color: var(--accent); box-shadow: 0 4px 16px rgba(15,118,110,.12); }}
    nav small {{ color: var(--muted); font-size: 12px; }}
    main {{ padding: 26px clamp(18px, 4vw, 56px) 70px; }}
    .hero {{
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(320px, .8fr);
      gap: 24px;
      align-items: center;
      padding-bottom: 24px;
      border-bottom: 1px solid var(--line);
    }}
    .hero h2 {{
      margin: 0;
      font-size: clamp(30px, 5vw, 54px);
      line-height: 1.05;
      letter-spacing: 0;
    }}
    .hero p {{ max-width: 760px; color: var(--muted); font-size: 16px; }}
    .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 18px; }}
    .stat {{
      border-top: 3px solid var(--accent);
      background: var(--paper);
      padding: 12px;
      border-radius: var(--radius);
      box-shadow: 0 8px 28px rgba(31,41,35,.06);
    }}
    .stat strong {{ display: block; font-size: 24px; }}
    .stat span {{ color: var(--muted); font-size: 13px; }}
    .index-section {{
      margin-top: 24px;
      padding: 22px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: 0 12px 34px rgba(31,41,35,.08);
    }}
    .section-title h2 {{
      margin: 0 0 8px;
      font-size: 24px;
      letter-spacing: 0;
    }}
    .section-title p {{ color: var(--muted); margin: 0 0 14px; }}
    .exam-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
    }}
    .exam-card {{
      border: 1px solid var(--line);
      border-radius: var(--radius);
      padding: 14px;
      background: #ffffff;
    }}
    .exam-card h3 {{
      margin: 4px 0 8px;
      font-size: 18px;
      letter-spacing: 0;
    }}
    .exam-card p {{ margin: 6px 0; color: var(--muted); }}
    .exam-code {{
      display: inline-grid;
      place-items: center;
      min-width: 28px;
      height: 28px;
      border-radius: 50%;
      color: white;
      background: var(--accent);
      font-weight: 700;
    }}
    .overview-visual svg, .visual svg {{
      width: 100%;
      height: auto;
      display: block;
    }}
    svg rect, svg ellipse, svg circle, svg polygon {{
      fill: #fffaf0;
      stroke: #334155;
      stroke-width: 2;
    }}
    svg path, svg line {{
      fill: none;
      stroke: #0f766e;
      stroke-width: 3;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}
    svg text {{
      font-size: 15px;
      text-anchor: middle;
      dominant-baseline: middle;
      fill: #1f2937;
      font-weight: 700;
    }}
    .chapter {{
      margin-top: 26px;
      background: var(--paper);
      border: 1px solid var(--line);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow: hidden;
    }}
    .chapter.hidden {{ display: none; }}
    .chapter-head {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) minmax(260px, 420px);
      gap: 22px;
      padding: 22px;
      background: linear-gradient(180deg, #fffdf8, #f8faf5);
      border-bottom: 1px solid var(--line);
    }}
    .eyebrow {{ margin: 0 0 6px; color: var(--accent-2); font-size: 12px; font-weight: 700; }}
    .chapter h2 {{ margin: 0; font-size: 26px; line-height: 1.25; letter-spacing: 0; }}
    .chapter-tag {{ color: var(--muted); margin: 8px 0 0; }}
    .enrichment {{
      padding: 18px 22px;
      border-bottom: 1px solid var(--line);
      background: #fbfcf8;
    }}
    .meta-grid {{
      display: grid;
      grid-template-columns: minmax(0, 1.2fr) minmax(120px, .4fr) minmax(0, 1.4fr);
      gap: 12px;
    }}
    .meta-grid > div {{
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #fff;
      padding: 12px;
    }}
    .meta-grid strong {{ display: block; margin-bottom: 6px; color: #134e4a; }}
    .meta-grid p {{ margin: 0; color: var(--muted); }}
    .weight {{
      display: inline-block;
      color: #fff;
      background: var(--accent-2);
      border-radius: 999px;
      padding: 3px 10px;
      font-weight: 700;
    }}
    .pill-row {{ display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }}
    .pill {{
      display: inline-block;
      border: 1px solid #cdd8d2;
      border-radius: 999px;
      padding: 3px 8px;
      color: #2f3b35;
      background: #f5f7f2;
      font-size: 12px;
    }}
    .dual-block {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
      margin-top: 14px;
    }}
    .dual-block > div {{
      border-left: 4px solid var(--accent);
      background: #fff;
      padding: 12px 14px;
      border-radius: var(--radius);
    }}
    .dual-block h3 {{ margin: 0 0 8px; font-size: 17px; letter-spacing: 0; }}
    .visual {{
      margin: 0;
      min-height: 160px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #ffffff;
      display: grid;
      place-items: center;
      padding: 8px;
    }}
    details > summary {{
      cursor: pointer;
      padding: 14px 22px;
      font-weight: 700;
      color: var(--accent);
      border-bottom: 1px solid var(--line);
    }}
    .content {{ padding: 2px 22px 26px; }}
    .content h2, .content h3, .content h4, .content h5 {{
      margin: 22px 0 10px;
      line-height: 1.3;
      letter-spacing: 0;
    }}
    .content h2 {{ font-size: 22px; }}
    .content h3 {{ font-size: 18px; border-left: 4px solid var(--accent); padding-left: 10px; }}
    .content p {{ margin: 10px 0; }}
    .content code {{
      background: #edf2f7;
      color: #0f172a;
      border: 1px solid #d8dee9;
      border-radius: 5px;
      padding: 1px 5px;
      font-family: Consolas, "Cascadia Mono", monospace;
      font-size: .92em;
    }}
    .diagram-text {{
      overflow: auto;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: #0f172a;
      color: #e5e7eb;
      padding: 14px;
      font-family: Consolas, "Cascadia Mono", monospace;
    }}
    .diagram-text code {{ background: transparent; color: inherit; border: 0; padding: 0; }}
    .table-wrap {{ overflow-x: auto; margin: 12px 0 18px; border: 1px solid var(--line); border-radius: var(--radius); }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; min-width: 680px; }}
    th, td {{ border-bottom: 1px solid var(--line); padding: 10px 12px; vertical-align: top; text-align: left; }}
    th {{ background: #eef6f4; color: #134e4a; white-space: nowrap; }}
    tr:last-child td {{ border-bottom: 0; }}
    ul, ol {{ padding-left: 24px; }}
    .no-results {{
      display: none;
      margin-top: 24px;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: var(--radius);
      background: var(--paper);
      color: var(--muted);
    }}
    .top-link {{
      position: fixed;
      right: 18px;
      bottom: 18px;
      width: 44px;
      height: 44px;
      border-radius: 50%;
      border: 1px solid var(--line);
      background: var(--accent);
      color: white;
      display: grid;
      place-items: center;
      text-decoration: none;
      box-shadow: var(--shadow);
    }}
    mark {{ background: #fde68a; color: inherit; padding: 0 2px; }}
    @media (max-width: 980px) {{
      .app {{ grid-template-columns: 1fr; }}
      aside {{ position: relative; height: auto; }}
      main {{ padding: 18px; }}
      .hero, .chapter-head, .meta-grid, .dual-block {{ grid-template-columns: 1fr; }}
      .stats {{ grid-template-columns: 1fr; }}
      nav {{ grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)); }}
    }}
    @media print {{
      aside, .top-link, .controls, details > summary {{ display: none; }}
      .app {{ display: block; }}
      main {{ padding: 0; }}
      .chapter {{ break-inside: avoid; box-shadow: none; border-color: #bbb; }}
      .chapter-body {{ display: block; }}
      .index-section, .enrichment {{ box-shadow: none; break-inside: avoid; }}
      .content {{ padding: 0 12px 12px; }}
      a {{ color: inherit; }}
    }}
  </style>
</head>
<body>
  <div class="app" id="top">
    <aside>
      <div class="brand">
        <h1>固体力学期末 OS</h1>
        <p>PPT课程线 + 考试高频线 · 图文复习工作台</p>
      </div>
      <div class="controls">
        <input id="search" type="search" placeholder="搜索：弯矩、扭转、应变花、Euler..." aria-label="搜索章节内容">
        <div class="button-row">
          <button id="expandAll" type="button">全部展开</button>
          <button id="collapseAll" type="button">全部收起</button>
        </div>
        <div class="button-row">
          <button id="clearSearch" type="button">清空搜索</button>
          <button id="printPage" type="button">打印</button>
        </div>
      </div>
      <div class="nav-block">
        <p class="nav-label">双线索引</p>
        <nav>
          <a href="#course-map"><span>课程/PPT目录</span><small>按课件查漏</small></a>
          <a href="#ppt-topic-map"><span>殷雅俊PPT专题</span><small>专题级锚点</small></a>
          <a href="#exam-map"><span>考试高频目录</span><small>按题型刷题</small></a>
          <a href="#cross-map"><span>PPT-考试交叉</span><small>双线对照</small></a>
          <a href="#sprint-map"><span>考前冲刺查漏</span><small>A/B/C 优先级</small></a>
        </nav>
      </div>
      <div class="nav-block">
        <p class="nav-label">章节目录</p>
        <nav id="toc">{nav}</nav>
      </div>
    </aside>
    <main>
      <section class="hero">
        <div>
          <h2>按 PPT 查漏，按考试得分</h2>
          <p>这版不是只按考试动作压缩，也不是只照搬课件目录。它把吴坚 14 章 PDF、殷雅俊 PPT/习题主题和历年考题线索并到一页：课程线保证不漏讲义，考试线决定刷题优先级。</p>
          <div class="stats">
            <div class="stat"><strong>{stat_chapters}</strong><span>章核心内容</span></div>
            <div class="stat"><strong>{total_pages}</strong><span>页吴坚课件映射</span></div>
            <div class="stat"><strong>100</strong><span>分考试权重矩阵</span></div>
          </div>
        </div>
        <figure class="overview-visual">{svg("chain")}</figure>
      </section>
      {course_index}
      {ppt_topic_index}
      {exam_index}
      {cross_index}
      {sprint_index}
      <div id="noResults" class="no-results">没有匹配的章节。换一个关键词试试，比如“剪力”“疲劳”“应变花”。</div>
      {articles}
    </main>
  </div>
  <a class="top-link" href="#top" aria-label="返回顶部">↑</a>
  <script>
    const search = document.getElementById('search');
    const chapters = Array.from(document.querySelectorAll('.chapter'));
    const navLinks = Array.from(document.querySelectorAll('nav a'));
    const noResults = document.getElementById('noResults');
    const normalize = (s) => (s || '').toLowerCase();

    function applySearch() {{
      const q = normalize(search.value.trim());
      let shown = 0;
      chapters.forEach(ch => {{
        const hay = normalize(ch.dataset.title + ' ' + ch.textContent);
        const ok = !q || hay.includes(q);
        ch.classList.toggle('hidden', !ok);
        if (ok) shown++;
      }});
      navLinks.forEach(a => {{
        const target = document.getElementById(a.dataset.target);
        a.style.display = target && target.classList.contains('hidden') ? 'none' : '';
      }});
      noResults.style.display = shown ? 'none' : 'block';
    }}

    search.addEventListener('input', applySearch);
    document.getElementById('clearSearch').addEventListener('click', () => {{ search.value = ''; applySearch(); search.focus(); }});
    document.getElementById('expandAll').addEventListener('click', () => document.querySelectorAll('details').forEach(d => d.open = true));
    document.getElementById('collapseAll').addEventListener('click', () => document.querySelectorAll('details').forEach(d => d.open = false));
    const detailsList = Array.from(document.querySelectorAll('details'));
    let printState = [];
    function openForPrint() {{
      printState = detailsList.map(d => d.open);
      detailsList.forEach(d => d.open = true);
    }}
    function restoreAfterPrint() {{
      if (!printState.length) return;
      detailsList.forEach((d, i) => d.open = printState[i]);
      printState = [];
    }}
    window.addEventListener('beforeprint', openForPrint);
    window.addEventListener('afterprint', restoreAfterPrint);
    document.getElementById('printPage').addEventListener('click', () => {{
      openForPrint();
      window.print();
      setTimeout(restoreAfterPrint, 800);
    }});

    const observer = new IntersectionObserver((entries) => {{
      entries.forEach(entry => {{
        if (entry.isIntersecting) {{
          navLinks.forEach(a => a.classList.toggle('active', a.dataset.target === entry.target.id));
        }}
      }});
    }}, {{ rootMargin: '-30% 0px -55% 0px', threshold: 0.01 }});
    chapters.forEach(ch => observer.observe(ch));
  </script>
</body>
</html>"""


def main() -> None:
    cards = []
    missing = []
    outline = load_source_outline()
    pages = wujian_pages(outline)
    for name in ORDER:
        path = SRC / name
        if not path.exists():
            missing.append(name)
            continue
        card = build_card(name, path.read_text(encoding="utf-8"))
        card["wujian_pages"] = pages.get(card["id"], "")
        cards.append(card)
    if missing:
        raise FileNotFoundError("Missing source files: " + ", ".join(missing))
    OUT.write_text(html_doc(cards, outline), encoding="utf-8")
    print(OUT)


if __name__ == "__main__":
    main()
