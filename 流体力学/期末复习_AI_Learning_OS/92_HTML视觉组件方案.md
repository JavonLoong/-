# 92 HTML 视觉组件方案

角色：HTML Worker-B  
范围：为单文件 HTML 设计离线可内嵌的图文视觉组件，不依赖网络图片，不修改最终 HTML。  
只读依据：`00_期末复习总索引.md`、`01_HTML整合计划.md`、`05_能量方程与伯努利方程.md`、`06_动量方程与动量矩方程.md`、`10_紊流与管路损失.md`、`11_边界层与绕流阻力.md`、`12_可压缩流体一维流动.md`、`13_可压缩超声速流动.md`、`14_实验与综合题抢分.md`。

## 1. 页面视觉风格建议

### 1.1 总体布局

页面应像“考前决策面板”，不是教材插画集。首屏直接给出总索引、禁用条件和主线题型入口，视觉组件用于辅助判断模型、条件和方程分工。

- 桌面端采用三栏：左侧章节导航，中间主内容，右侧速查栏。视觉组件放在中间章节卡片或“视觉速查”区域，不单独抢成大封面。
- 中间主区建议使用模块化结构：`冲刺总览 -> 高风险条件 -> 公式/题型索引 -> 视觉组件 -> 章节全文折叠`。
- 右侧速查栏固定展示“何时不能用”“符号禁混”“专业拓展非主线”，并使用小尺寸标签，避免把补充内容抬成主线。
- 每个视觉组件以 `figure` 组织：上方 SVG，下面是 3 行信息：关联章节、表达的物理意义、条件/误导提示。
- 不做网络图片，不用外链字体，不依赖 MathJax。公式用纯文本、HTML 上标/下标和少量 SVG 文本即可。

### 1.2 色彩系统

建议用中性纸面 + 多物理量点色，避免单一蓝紫或单一米色主题。

```css
:root {
  --paper: #f7f9fb;
  --panel: #ffffff;
  --ink: #17202a;
  --muted: #5f6b75;
  --line: #d7e2ea;
  --water: #177ddc;
  --energy: #f6b73c;
  --momentum: #2f9e44;
  --loss: #d94841;
  --viscous: #8a6f3e;
  --compressible: #7b5cff;
  --experiment: #0f8b8d;
  --soft-blue: #e8f3ff;
  --soft-amber: #fff4d8;
  --soft-red: #ffe9e7;
  --soft-green: #e8f7ed;
  --soft-violet: #eeeafd;
}
```

语义约定：

- 蓝色：水流、流线、管路。
- 琥珀色：水头、能量线、账本。
- 绿色：动量通量、速度矢量、流量链。
- 红色：损失、禁用、激波总压下降。
- 紫色：可压缩、马赫数、斜激波/膨胀扇。
- 青色：实验读数和数据链。

### 1.3 字体与层级

- 正文：`system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", "Microsoft YaHei", sans-serif`。
- 数字/公式：`ui-monospace, "Cascadia Mono", "SFMono-Regular", Consolas, monospace`。
- 层级建议：
  - 页面标题：28 到 34 px，移动端 24 px。
  - 模块标题：18 到 22 px。
  - 卡片标题：15 到 17 px。
  - 公式/标签：12 到 14 px。
- SVG 内文字保持 11 到 13 px。窄屏时隐藏非关键长标签，保留图例。

### 1.4 移动端策略

- 三栏在 900 px 以下改为单列：顶部搜索和模式切换，章节导航变为横向滚动标签，右侧速查变成折叠块。
- SVG 全部使用 `viewBox` 与 `width:100%; height:auto;`，不要固定像素高度撑爆屏幕。
- 公式标签和图例允许换行，不在 SVG 内塞长句。长解释放在 `figcaption`。
- 交互不要依赖 hover。移动端使用展开按钮、可点击图例、短条件标签。
- 窄屏优先显示“条件判断”，复杂曲线或多标签图使用简化模式。

### 1.5 视觉权重与“必考”暗示规则

全站不使用“必考”徽章。建议统一使用：

- `主线`：基础方程和高频题型入口，如控制体、伯努利水头、管路损失、实验读数。
- `高风险`：容易误用的条件，如激波不能等熵跨越、动量方程要取反作用力。
- `高分/拓展`：边界层分离细节、面积-Ma 两支、Prandtl-Meyer 函数、斜激波弱/强解。
- `专业拓展/非主线`：第 14 章热泵、压气机等材料，只作为底部小注或折叠附录，不进入首屏路径。

不能做成“必考”暗示的视觉：

- 第 14 章热泵空调、压气机性能实验：资料明确为专业拓展附注，不能放入主线组件区。
- Prandtl-Meyer 函数完整公式、斜激波弱/强解细节、面积-Ma 定量两支：可作为高分入口，不做首屏大卡。
- Moody 图精确曲线：只能做读图流程和概念示意，不能画得像可直接查数的正式图表。
- 边界层分离和阻力危机：适合作概念图，不暗示每套期末都会定量考。

## 2. 组件通用骨架

所有组件使用同一 `figure` 结构，便于最终 HTML 统一样式和检索。

```html
<figure class="viz-card" data-chapters="05,10,14" data-weight="main">
  <div class="viz-head">
    <h3>伯努利水头线</h3>
    <span class="tag tag-main">主线</span>
    <span class="tag tag-risk">条件优先</span>
  </div>
  <svg class="viz-svg" viewBox="0 0 640 300" role="img" aria-labelledby="head-title head-desc">
    <title id="head-title">水头线示意</title>
    <desc id="head-desc">展示测压管水头线和总水头线在管路损失处下降。</desc>
  </svg>
  <figcaption>
    <p><strong>关联章节：</strong>05、10、14。</p>
    <p><strong>物理意义：</strong>把位置水头、压强水头、速度水头、损失水头放进同一账本。</p>
    <p><strong>条件提示：</strong>只在恒定总流和缓变断面上解释，不跨激波或高速可压缩段。</p>
  </figcaption>
</figure>
```

基础 CSS 建议：

```css
.viz-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 320px), 1fr));
  gap: 16px;
}
.viz-card {
  margin: 0;
  padding: 14px;
  border: 1px solid var(--line);
  border-radius: 8px;
  background: var(--panel);
}
.viz-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 8px;
}
.viz-head h3 {
  margin: 0;
  font-size: 16px;
}
.viz-svg {
  display: block;
  width: 100%;
  height: auto;
  min-height: 180px;
}
.tag {
  display: inline-flex;
  align-items: center;
  min-height: 22px;
  padding: 2px 8px;
  border-radius: 999px;
  font-size: 12px;
  line-height: 1.2;
  white-space: nowrap;
}
.tag-main { background: var(--soft-blue); color: #07569b; }
.tag-risk { background: var(--soft-red); color: #a3221d; }
.tag-high { background: var(--soft-violet); color: #4930a3; }
.tag-extra { background: #eef1f3; color: var(--muted); }
.formula-chip {
  font-family: ui-monospace, "Cascadia Mono", Consolas, monospace;
  background: #f2f5f8;
  border: 1px solid var(--line);
  border-radius: 6px;
  padding: 2px 6px;
}
```

SVG 通用符号：

```html
<defs>
  <marker id="arrow-water" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--water)"></path>
  </marker>
  <marker id="arrow-momentum" viewBox="0 0 10 10" refX="9" refY="5"
          markerWidth="7" markerHeight="7" orient="auto-start-reverse">
    <path d="M 0 0 L 10 5 L 0 10 z" fill="var(--momentum)"></path>
  </marker>
  <pattern id="loss-hatch" width="6" height="6" patternUnits="userSpaceOnUse">
    <path d="M0,6 L6,0" stroke="var(--loss)" stroke-width="1"></path>
  </pattern>
</defs>
```

## 3. 组件草案总表

| ID | 组件 | 关联章节 | 默认权重 | 核心用途 |
| --- | --- | --- | --- | --- |
| V01 | 控制体与通量边界 | 04、06、14 | 主线 | 先画边界、法向、入口出口，再判断连续/动量 |
| V02 | 伯努利水头线账本 | 05、10、14 | 主线 | 区分 HGL、EGL、损失、泵/涡轮项 |
| V03 | 动量控制体受力图 | 06、14 | 主线 | 表达外力、速度矢量和反作用力 |
| V04 | Moody/损失决策图 | 10、14 | 主线 | 表达 `Q -> v -> Re -> lambda/zeta -> h_w` |
| V05 | 边界层分离图 | 11 | 高分/拓展 | 表达无滑移、逆压梯度、分离和尾涡 |
| V06 | 喷管堵塞与质量流量平台 | 12、13 | 高风险 | 表达喉部 `M=1` 和背压降低后流量不再增大 |
| V07 | 斜激波/膨胀扇波系图 | 13 | 高分/拓展 | 区分压缩角与膨胀角、`beta` 与 `delta` |
| V08 | 实验读数链 | 14 | 主线 | 把原始读数翻译成 SI 物理量、方程和误差 |
| V09 | 可压缩分段与激波断点 | 12、13 | 高风险 | 提醒等熵关系只能分段用，不能跨激波 |
| V10 | 禁用条件矩阵 | 00、05、06、10、12、13、14 | 主线 | 快速排雷：何时不能套公式 |

## 4. 组件细案

### V01 控制体与通量边界

关联章节：04 控制体与连续方程，06 动量方程，14 综合题。  
表达的物理意义：任何连续、能量、动量综合题都先圈研究对象。控制面决定入口/出口通量、外法线方向和外力清单。  
避免误导：控制体边界不是实体壁面本身；入口不总是“正”，严格符号由外法线 `n` 和 `V·n` 决定；可压缩流不能直接写 `A1v1=A2v2`。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 640 300" role="img">
  <title>控制体与通量边界</title>
  <desc>虚线控制体包围一段管流，入口和出口速度矢量穿过控制面，外法线指向控制体外。</desc>
  <defs><!-- arrow markers --></defs>
  <rect x="170" y="70" width="300" height="150" rx="8"
        fill="var(--soft-blue)" stroke="var(--water)" stroke-width="2"
        stroke-dasharray="8 6"></rect>
  <text x="320" y="92" text-anchor="middle" fill="var(--ink)" font-size="14">控制体 CV</text>
  <path d="M40 145 C100 120 135 120 170 145" fill="none" stroke="var(--water)" stroke-width="18" opacity=".18"></path>
  <path d="M40 145 L165 145" stroke="var(--water)" stroke-width="4" marker-end="url(#arrow-water)"></path>
  <text x="70" y="128" font-size="13">入口 ρ₁A₁V₁</text>
  <path d="M470 145 L600 120" stroke="var(--water)" stroke-width="4" marker-end="url(#arrow-water)"></path>
  <text x="500" y="104" font-size="13">出口 ρ₂A₂V₂</text>
  <path d="M170 145 L130 145" stroke="var(--momentum)" stroke-width="2" marker-end="url(#arrow-momentum)"></path>
  <path d="M470 145 L515 145" stroke="var(--momentum)" stroke-width="2" marker-end="url(#arrow-momentum)"></path>
  <text x="126" y="168" font-size="12" fill="var(--momentum)">n 向外</text>
  <text x="496" y="168" font-size="12" fill="var(--momentum)">n 向外</text>
  <rect x="210" y="230" width="220" height="34" rx="6" fill="#fff" stroke="var(--line)"></rect>
  <text x="320" y="252" text-anchor="middle" font-size="13">连续：Σṁ_in = Σṁ_out</text>
</svg>
```

视觉权重：主线，但标签写“控制体优先”，不写“必考”。  
条件提示：若题目求力或反力，必须把外力画出来并进入 V03；若只求流量，先做质量守恒即可。

### V02 伯努利水头线账本

关联章节：05 能量方程与伯努利方程，10 管路损失，14 实验读数。  
表达的物理意义：水头形式不是背公式，而是把 `z`、`p/(rho g)`、`v^2/(2g)`、`h_f`、`h_j`、`H_p` 放到同一本账里。  
避免误导：HGL/EGL 不是流线；急变流内部不解释断面平均；有泵可跃升，无泵无涡轮时总水头线不应上升；高速可压缩和激波不跨用低速水头图。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 680 320" role="img">
  <title>伯努利水头线账本</title>
  <desc>管路上方显示测压管水头线和总水头线，阀门处有局部跌落，泵处有水头跃升。</desc>
  <defs><!-- arrow markers and hatch --></defs>
  <path d="M60 210 H230 C260 210 260 160 290 160 H455 C485 160 485 205 515 205 H625"
        fill="none" stroke="var(--water)" stroke-width="28" stroke-linecap="round"></path>
  <rect x="330" y="145" width="30" height="30" fill="url(#loss-hatch)" stroke="var(--loss)"></rect>
  <circle cx="470" cy="182" r="23" fill="var(--soft-green)" stroke="var(--momentum)" stroke-width="2"></circle>
  <text x="470" y="187" text-anchor="middle" font-size="12">泵</text>
  <polyline points="70,95 210,105 320,132 420,139 470,96 620,118"
            fill="none" stroke="var(--energy)" stroke-width="4"></polyline>
  <polyline points="70,135 210,145 320,168 420,174 470,132 620,154"
            fill="none" stroke="var(--water)" stroke-width="4" stroke-dasharray="8 5"></polyline>
  <text x="80" y="82" font-size="13" fill="var(--energy)">EGL = HGL + αv²/2g</text>
  <text x="80" y="154" font-size="13" fill="var(--water)">HGL = z + p/ρg</text>
  <path d="M330 128 L330 168" stroke="var(--loss)" stroke-width="2" marker-end="url(#arrow-water)"></path>
  <text x="270" y="125" font-size="12" fill="var(--loss)">局部跌落 h_j</text>
  <text x="420" y="82" font-size="12" fill="var(--momentum)">泵水头 H_p</text>
  <text x="210" y="280" font-size="13">实际总流：H₁ + H_p = H₂ + h_f + Σh_j + H_t</text>
</svg>
```

视觉权重：主线。  
条件提示：只展示概念趋势，具体数值要回到断面编号、速度水头和损失清单。

### V03 动量控制体受力图

关联章节：06 动量方程与动量矩方程，14 动量实验和综合题。  
表达的物理意义：动量方程是矢量账本，先画入口/出口速度分量和所有外力，再求“外界对流体”的合力，题问“流体对固体”时取反。  
避免误导：不能只画速度不画压力力；不要把 `R` 的方向当结果，假设方向可以错，方程会给负号；自由射流可用环境表压，弯管题不能随便忽略 `pA`。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 680 320" role="img">
  <title>动量控制体受力图</title>
  <desc>弯管控制体内水流从 x 方向转向 y 方向，标出速度矢量、压力力和壁面对流体的作用力。</desc>
  <defs><!-- arrow markers --></defs>
  <path d="M90 210 H310 Q390 210 390 130 V70" fill="none"
        stroke="var(--water)" stroke-width="34" stroke-linecap="round"></path>
  <path d="M130 210 H275" stroke="var(--momentum)" stroke-width="4" marker-end="url(#arrow-momentum)"></path>
  <path d="M390 170 V88" stroke="var(--momentum)" stroke-width="4" marker-end="url(#arrow-momentum)"></path>
  <text x="150" y="190" font-size="13">V₁x</text>
  <text x="405" y="120" font-size="13">V₂y</text>
  <rect x="70" y="170" width="355" height="85" rx="8"
        fill="none" stroke="var(--momentum)" stroke-width="2" stroke-dasharray="8 6"></rect>
  <path d="M90 235 L150 235" stroke="var(--loss)" stroke-width="3" marker-end="url(#arrow-water)"></path>
  <text x="95" y="256" font-size="12" fill="var(--loss)">p₁A₁</text>
  <path d="M420 70 L420 130" stroke="var(--loss)" stroke-width="3" marker-end="url(#arrow-water)"></path>
  <text x="428" y="98" font-size="12" fill="var(--loss)">p₂A₂</text>
  <path d="M330 250 L285 285" stroke="var(--compressible)" stroke-width="3" marker-end="url(#arrow-momentum)"></path>
  <text x="292" y="300" font-size="12" fill="var(--compressible)">R：管壁对水</text>
  <rect x="450" y="190" width="185" height="64" rx="6" fill="#fff" stroke="var(--line)"></rect>
  <text x="542" y="214" text-anchor="middle" font-size="13">ΣF = 出口动量通量</text>
  <text x="542" y="236" text-anchor="middle" font-size="13">- 入口动量通量</text>
</svg>
```

视觉权重：主线。  
条件提示：组件标题建议叫“动量控制体”，不要叫“受力公式模板”，避免用户跳过受力分析直接套 `rho QV`。

### V04 Moody/损失决策图

关联章节：10 紊流与管路损失，14 沿程/局部损失实验。  
表达的物理意义：损失计算不是先找公式，而是固定链条：`Q -> A -> v -> Re -> lambda/zeta -> h_f/h_j -> 能量方程`。Moody 图概念表达 `lambda=f(Re,k_s/D)`，不是精确读数图。  
避免误导：图中曲线不能承担查数功能；必须标明 Darcy/Fanning 口径；过渡区不稳定，不能把 `64/Re` 套到紊流。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 700 340" role="img">
  <title>Moody 与损失决策图</title>
  <desc>左侧为损失计算流程，右侧为定性 Moody 曲线示意，显示层流线、紊流曲线族和粗糙区。</desc>
  <defs><!-- arrow markers --></defs>
  <g transform="translate(28,38)">
    <rect width="270" height="245" rx="8" fill="#fff" stroke="var(--line)"></rect>
    <text x="135" y="28" text-anchor="middle" font-size="15">损失计算链</text>
    <g font-size="13">
      <rect x="35" y="50" width="200" height="28" rx="6" fill="var(--soft-blue)"></rect>
      <text x="135" y="69" text-anchor="middle">Q -> A -> v</text>
      <rect x="35" y="92" width="200" height="28" rx="6" fill="var(--soft-green)"></rect>
      <text x="135" y="111" text-anchor="middle">Re = vD/ν</text>
      <rect x="35" y="134" width="200" height="28" rx="6" fill="var(--soft-violet)"></rect>
      <text x="135" y="153" text-anchor="middle">λ = f(Re, kₛ/D)</text>
      <rect x="35" y="176" width="200" height="28" rx="6" fill="var(--soft-red)"></rect>
      <text x="135" y="195" text-anchor="middle">h_f + Σh_j</text>
      <text x="135" y="232" text-anchor="middle" fill="var(--loss)">先判 Re，再选 λ</text>
    </g>
  </g>
  <g transform="translate(350,50)">
    <rect width="300" height="230" rx="8" fill="#fff" stroke="var(--line)"></rect>
    <line x1="45" y1="190" x2="270" y2="190" stroke="var(--ink)"></line>
    <line x1="45" y1="190" x2="45" y2="24" stroke="var(--ink)"></line>
    <text x="155" y="218" text-anchor="middle" font-size="12">Re，对数轴</text>
    <text x="18" y="105" text-anchor="middle" font-size="12" transform="rotate(-90 18 105)">Darcy λ</text>
    <path d="M55 55 C85 86 112 118 142 155" fill="none" stroke="var(--momentum)" stroke-width="3"></path>
    <text x="72" y="48" font-size="11" fill="var(--momentum)">层流 64/Re</text>
    <path d="M120 90 C160 78 215 68 265 68" fill="none" stroke="var(--water)" stroke-width="3"></path>
    <path d="M120 120 C165 105 220 94 265 94" fill="none" stroke="var(--water)" stroke-width="2"></path>
    <path d="M120 150 C170 132 225 122 265 122" fill="none" stroke="var(--water)" stroke-width="2" stroke-dasharray="5 4"></path>
    <text x="190" y="54" font-size="11" fill="var(--water)">kₛ/D 增大</text>
    <rect x="105" y="168" width="68" height="16" fill="var(--soft-amber)" stroke="var(--energy)"></rect>
    <text x="139" y="180" text-anchor="middle" font-size="10">过渡区</text>
  </g>
</svg>
```

视觉权重：主线，但标注“概念示意，不能查数”。  
条件提示：若最终 HTML 有交互筛选，可在该组件旁显示小卡：Darcy `lambda=64/Re`，Fanning `f=16/Re`，两者差 4 倍。

### V05 边界层分离图

关联章节：11 边界层与绕流阻力。  
表达的物理意义：高 Re 外流不是全场无粘，粘性集中在贴壁边界层；逆压梯度 + 近壁动能亏损导致 `tau_w=0` 和回流，形成尾涡和压差阻力。  
避免误导：边界层外缘不是真实流线；0.99 `U_e` 是工程约定；顺压梯度通常不分离；湍流边界层摩擦更大，但可能推迟钝体分离。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 700 330" role="img">
  <title>边界层分离</title>
  <desc>外流经过钝体，上游边界层附着，逆压梯度后发生分离，后方形成回流和尾涡低压区。</desc>
  <defs><!-- arrow markers --></defs>
  <path d="M80 170 C160 95 310 90 430 165 C510 215 390 260 250 242 C160 232 105 210 80 170"
        fill="#eef3f7" stroke="var(--ink)" stroke-width="2"></path>
  <path d="M60 85 H620" stroke="var(--water)" stroke-width="2" marker-end="url(#arrow-water)" opacity=".75"></path>
  <path d="M60 125 H620" stroke="var(--water)" stroke-width="2" marker-end="url(#arrow-water)" opacity=".75"></path>
  <text x="65" y="70" font-size="12">U∞</text>
  <path d="M120 178 C180 145 270 135 360 150" fill="none" stroke="var(--viscous)" stroke-width="4"></path>
  <path d="M360 150 C420 156 440 180 450 205" fill="none" stroke="var(--loss)" stroke-width="4"></path>
  <circle cx="360" cy="150" r="5" fill="var(--loss)"></circle>
  <text x="315" y="136" font-size="12" fill="var(--loss)">分离点 τw=0</text>
  <path d="M455 205 C520 165 590 175 630 215" fill="none" stroke="var(--loss)" stroke-width="3" stroke-dasharray="6 5"></path>
  <path d="M455 235 C525 285 600 265 640 225" fill="none" stroke="var(--loss)" stroke-width="3" stroke-dasharray="6 5"></path>
  <path d="M585 220 C560 200 545 225 565 240 C590 258 612 236 585 220"
        fill="none" stroke="var(--loss)" stroke-width="2"></path>
  <text x="515" y="295" font-size="12" fill="var(--loss)">尾涡低压区 -> 压差阻力</text>
  <text x="128" y="222" font-size="12" fill="var(--viscous)">无滑移 + 速度梯度</text>
  <text x="390" y="118" font-size="12" fill="var(--loss)">逆压梯度 dp/dx &gt; 0</text>
</svg>
```

视觉权重：高分/拓展。  
条件提示：不能做成首屏“必考”大图。它应在第 11 章卡片内或高分模块中出现，作为概念判断图。

### V06 喷管堵塞与质量流量平台

关联章节：12 可压缩一维流动，13 喷管非设计工况接口。  
表达的物理意义：上游总参数和喉部面积固定时，背压降低到临界后喉部 `M=1`，质量流量达到最大并保持平台；继续降背压只改变下游/管外波系。  
避免误导：堵塞后出口静压不一定等于背压；收缩喷管管内最多到 `M=1`；缩放喷管要先喉部临界，扩张段才可超声速；有激波时进入第 13 章分段。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 700 340" role="img">
  <title>喷管堵塞与质量流量平台</title>
  <desc>左侧为收缩喷管喉部 Ma=1，右侧为背压降低时质量流量先增大后达到平台。</desc>
  <defs><!-- arrow markers --></defs>
  <g transform="translate(40,50)">
    <path d="M20 90 C100 40 180 55 250 85 C180 115 100 130 20 90"
          fill="var(--soft-violet)" stroke="var(--compressible)" stroke-width="2"></path>
    <path d="M35 90 H245" stroke="var(--compressible)" stroke-width="4" marker-end="url(#arrow-water)"></path>
    <line x1="185" y1="62" x2="185" y2="118" stroke="var(--loss)" stroke-width="2" stroke-dasharray="5 4"></line>
    <text x="156" y="52" font-size="12" fill="var(--loss)">喉部 M=1</text>
    <text x="30" y="145" font-size="12">p₀,T₀</text>
    <text x="195" y="145" font-size="12">p_b 降低</text>
  </g>
  <g transform="translate(360,48)">
    <rect width="285" height="225" rx="8" fill="#fff" stroke="var(--line)"></rect>
    <line x1="42" y1="180" x2="255" y2="180" stroke="var(--ink)"></line>
    <line x1="42" y1="180" x2="42" y2="32" stroke="var(--ink)"></line>
    <text x="148" y="210" text-anchor="middle" font-size="12">p_b / p₀ 下降</text>
    <text x="18" y="100" text-anchor="middle" font-size="12" transform="rotate(-90 18 100)">ṁ</text>
    <path d="M52 162 C85 135 112 96 145 68 H245" fill="none" stroke="var(--compressible)" stroke-width="4"></path>
    <line x1="145" y1="42" x2="145" y2="182" stroke="var(--loss)" stroke-width="2" stroke-dasharray="6 5"></line>
    <text x="152" y="55" font-size="11" fill="var(--loss)">临界压比</text>
    <text x="174" y="82" font-size="12" fill="var(--compressible)">堵塞平台</text>
  </g>
  <text x="105" y="302" font-size="13">条件：理想气体、一维、定常、等熵到喉部；激波或摩擦需重新分段。</text>
</svg>
```

视觉权重：高风险。  
条件提示：应放在第 12 章和第 13 章接口处，强调“堵塞是条件判断”，不是所有喷管题都直接平台。

### V07 斜激波/膨胀扇波系图

关联章节：13 可压缩超声速流动。  
表达的物理意义：超声速遇压缩转角形成斜激波，遇膨胀转角形成膨胀扇。斜激波先看 `M1n=M1 sin beta`，膨胀扇用 Prandtl-Meyer 入口，趋势完全相反。  
避免误导：只在 `Ma>1` 时画；`beta` 是激波角，`delta` 是气流偏转角；斜激波后整体 `M2` 不一定亚声速；膨胀波近似等熵，激波一定熵增、总压下降。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 720 340" role="img">
  <title>斜激波与膨胀扇</title>
  <desc>左侧楔形压缩角产生斜激波，右侧凸角膨胀产生扇形膨胀波。</desc>
  <defs><!-- arrow markers --></defs>
  <g transform="translate(35,40)">
    <text x="150" y="0" text-anchor="middle" font-size="15">压缩转角：斜激波</text>
    <path d="M20 125 H270" stroke="var(--compressible)" stroke-width="4" marker-end="url(#arrow-water)"></path>
    <text x="28" y="106" font-size="12">M₁ &gt; 1</text>
    <path d="M165 125 L285 185 L165 185 Z" fill="#eef3f7" stroke="var(--ink)" stroke-width="2"></path>
    <line x1="160" y1="125" x2="250" y2="45" stroke="var(--loss)" stroke-width="4"></line>
    <path d="M175 130 Q202 113 224 91" fill="none" stroke="var(--loss)" stroke-width="1.5"></path>
    <text x="205" y="95" font-size="12" fill="var(--loss)">β</text>
    <path d="M178 132 Q202 143 222 153" fill="none" stroke="var(--momentum)" stroke-width="1.5"></path>
    <text x="217" y="150" font-size="12" fill="var(--momentum)">δ</text>
    <text x="70" y="235" font-size="13" fill="var(--loss)">先算 M₁n = M₁ sin β</text>
  </g>
  <g transform="translate(390,40)">
    <text x="150" y="0" text-anchor="middle" font-size="15">膨胀转角：PM 扇</text>
    <path d="M20 135 H245" stroke="var(--compressible)" stroke-width="4" marker-end="url(#arrow-water)"></path>
    <path d="M165 135 L285 88 L285 190 Z" fill="#eef3f7" stroke="var(--ink)" stroke-width="2"></path>
    <path d="M165 135 L255 68" stroke="var(--compressible)" stroke-width="2"></path>
    <path d="M165 135 L278 92" stroke="var(--compressible)" stroke-width="2"></path>
    <path d="M165 135 L280 126" stroke="var(--compressible)" stroke-width="2"></path>
    <path d="M165 135 L278 162" stroke="var(--compressible)" stroke-width="2"></path>
    <text x="210" y="70" font-size="12" fill="var(--compressible)">膨胀扇</text>
    <text x="64" y="235" font-size="13" fill="var(--compressible)">δ = ν(M₂) - ν(M₁)</text>
  </g>
  <rect x="205" y="285" width="310" height="34" rx="6" fill="var(--soft-red)" stroke="var(--loss)"></rect>
  <text x="360" y="307" text-anchor="middle" font-size="13">激波不等熵，膨胀扇才近似等熵</text>
</svg>
```

视觉权重：高分/拓展。  
条件提示：不要做成“第 13 章必考公式全图”。默认展示趋势和入口公式，完整 PM 函数和弱/强解放入折叠详情。

### V08 实验读数链

关联章节：14 实验与综合题抢分，连接 02、05、06、10。  
表达的物理意义：实验题先把仪器读数转换成方程能使用的物理量，再列静水、连续、能量、动量和误差/图表。  
避免误导：不是所有实验都走同一条直线；测压管高程不是压强本身；砝码质量不是力；`zeta` 必须说明参考速度；热泵/压气机是专业拓展非主线。

HTML/SVG 草案：

```html
<div class="viz-chain" role="group" aria-labelledby="exp-title">
  <h3 id="exp-title">实验读数链</h3>
  <svg class="viz-svg" viewBox="0 0 720 260" role="img">
    <title>实验读数到结果链条</title>
    <desc>液面高、量水箱、砝码、尺寸和温度先转成 SI 物理量，再进入方程和误差分析。</desc>
    <defs><!-- arrow markers --></defs>
    <g font-size="13">
      <rect x="24" y="70" width="145" height="92" rx="8" fill="var(--soft-blue)" stroke="var(--water)"></rect>
      <text x="96" y="98" text-anchor="middle">原始读数</text>
      <text x="96" y="124" text-anchor="middle">h, ΔH, t, m</text>
      <text x="96" y="146" text-anchor="middle">d, T, 压力表</text>
      <path d="M178 116 H250" stroke="var(--experiment)" stroke-width="3" marker-end="url(#arrow-water)"></path>
      <rect x="260" y="70" width="145" height="92" rx="8" fill="#eefafa" stroke="var(--experiment)"></rect>
      <text x="332" y="98" text-anchor="middle">SI 物理量</text>
      <text x="332" y="124" text-anchor="middle">Δp, Q, v</text>
      <text x="332" y="146" text-anchor="middle">Re, R, h_w</text>
      <path d="M414 116 H486" stroke="var(--experiment)" stroke-width="3" marker-end="url(#arrow-water)"></path>
      <rect x="496" y="70" width="180" height="92" rx="8" fill="var(--soft-amber)" stroke="var(--energy)"></rect>
      <text x="586" y="98" text-anchor="middle">方程/结论</text>
      <text x="586" y="124" text-anchor="middle">静水/连续/能量/动量</text>
      <text x="586" y="146" text-anchor="middle">误差、图表、有效数字</text>
    </g>
    <text x="360" y="218" text-anchor="middle" font-size="13" fill="var(--loss)">
      先单位换算，再列方程；专业拓展只按通用读数链处理
    </text>
  </svg>
</div>
```

视觉权重：主线。  
条件提示：第 14 章专业拓展内容只在该组件底部用灰色小注出现，不放在主流程箭头中。

### V09 可压缩分段与激波断点

关联章节：12 等熵喷管，13 激波。  
表达的物理意义：可压缩流中“等熵关系”只能在无摩擦、无激波的段内用。遇到激波，前后分段，激波处用质量、动量、能量守恒和熵增/总压下降判断。  
避免误导：总温可跨绝热无功激波保持，总压不能保持；不要把低速伯努利水头图跨到高 Ma 喷管；面积-Ma 有亚声速和超声速两支，须由状态选支。

SVG 草案：

```html
<svg class="viz-svg" viewBox="0 0 720 240" role="img">
  <title>可压缩分段与激波断点</title>
  <desc>喷管流程被激波断开，激波前后各自可以等熵处理，跨激波总压下降。</desc>
  <defs><!-- arrow markers --></defs>
  <line x1="60" y1="115" x2="650" y2="115" stroke="var(--compressible)" stroke-width="4" marker-end="url(#arrow-water)"></line>
  <rect x="80" y="70" width="170" height="84" rx="8" fill="var(--soft-violet)" stroke="var(--compressible)"></rect>
  <text x="165" y="102" text-anchor="middle" font-size="13">等熵段 1</text>
  <text x="165" y="128" text-anchor="middle" font-size="12">T₀,p₀ 可保持</text>
  <polygon points="322,48 358,115 322,182 294,115" fill="var(--soft-red)" stroke="var(--loss)" stroke-width="2"></polygon>
  <text x="326" y="109" text-anchor="middle" font-size="12" fill="var(--loss)">激波</text>
  <text x="326" y="129" text-anchor="middle" font-size="12" fill="var(--loss)">p₀↓</text>
  <rect x="430" y="70" width="170" height="84" rx="8" fill="var(--soft-violet)" stroke="var(--compressible)"></rect>
  <text x="515" y="102" text-anchor="middle" font-size="13">等熵段 2</text>
  <text x="515" y="128" text-anchor="middle" font-size="12">用新的 p₀₂</text>
  <text x="360" y="215" text-anchor="middle" font-size="13" fill="var(--loss)">禁止一条等熵公式从入口套到出口</text>
</svg>
```

视觉权重：高风险。  
条件提示：应与 V06/V07 相邻，作为“激波是等熵链条断点”的补充组件。

### V10 禁用条件矩阵

关联章节：00 总索引中的高风险条件、公式索引、何时不能用；连接 05、06、10、12、13、14。  
表达的物理意义：用小矩阵提醒用户先判模型再套公式，尤其是伯努利、动量、损失、可压缩和实验单位。  
避免误导：矩阵不是知识点排序，不代表每个格子都是同等考频；用“禁用/改用”表达，不用“必考”。

HTML/CSS 草案：

```html
<section class="risk-matrix" aria-labelledby="risk-title">
  <h3 id="risk-title">何时不能这样用</h3>
  <div class="risk-row">
    <span class="formula-chip">伯努利</span>
    <span>跨激波/高 Ma/明显损失</span>
    <strong>改用：</strong>
    <span>分段能量或第 13 章激波</span>
  </div>
  <div class="risk-row">
    <span class="formula-chip">A₁v₁=A₂v₂</span>
    <span>密度变化显著</span>
    <strong>改用：</strong>
    <span>ρAv 守恒</span>
  </div>
  <div class="risk-row">
    <span class="formula-chip">λ=64/Re</span>
    <span>紊流/过渡区</span>
    <strong>改用：</strong>
    <span>Moody 图或题给经验式</span>
  </div>
  <div class="risk-row">
    <span class="formula-chip">斜激波</span>
    <span>直接套整体 M₁</span>
    <strong>改用：</strong>
    <span>M₁n = M₁ sin β</span>
  </div>
  <div class="risk-row extra">
    <span class="formula-chip">专业拓展</span>
    <span>热泵/压气机</span>
    <strong>权重：</strong>
    <span>非期末主线，只保留通用数据处理入口</span>
  </div>
</section>
```

```css
.risk-matrix {
  display: grid;
  gap: 8px;
}
.risk-row {
  display: grid;
  grid-template-columns: minmax(88px, auto) 1fr auto 1.2fr;
  gap: 8px;
  align-items: center;
  padding: 8px 10px;
  border: 1px solid var(--line);
  border-left: 4px solid var(--loss);
  border-radius: 8px;
  background: #fff;
}
.risk-row.extra {
  border-left-color: var(--muted);
  color: var(--muted);
  background: #f6f7f8;
}
@media (max-width: 640px) {
  .risk-row {
    grid-template-columns: 1fr;
  }
}
```

视觉权重：主线排雷。  
条件提示：作为右侧速查栏或章节顶部小组件使用，不做大幅红色警告墙，避免造成焦虑或误判考频。

## 5. 组件摆放建议

| 页面区域 | 推荐组件 | 理由 |
| --- | --- | --- |
| 冲刺总览 | V10、V01、V02、V08 | 对应总索引的高风险条件、方程分工和实验链 |
| 公式索引附近 | V02、V04、V09 | 公式旁边必须看到适用条件和断点 |
| 题型索引附近 | V03、V04、V06、V08 | 从题眼直接连到解题动作 |
| 第 05 章卡片 | V02 | 伯努利与实际总流能量方程 |
| 第 06 章卡片 | V03 | 动量方程方向、外力和反作用力 |
| 第 10 章卡片 | V04 | `Re -> lambda -> 损失` |
| 第 11 章卡片 | V05 | 概念判断和高分解释 |
| 第 12 章卡片 | V06、V09 | 堵塞、等熵段、激波接口 |
| 第 13 章卡片 | V07、V09 | 斜激波、膨胀扇、跨激波禁用 |
| 第 14 章卡片 | V08、V10 | 读数链、单位、误差、非主线拓展 |

## 6. 离线内嵌实现注意

- 所有图形使用内联 SVG、CSS shape、HTML 卡片完成，不引用网络图片、CDN 图标或外链字体。
- SVG 图中文字只放短标签，长解释放到 `figcaption`，便于移动端换行和搜索。
- 每个 SVG 加 `<title>` 和 `<desc>`，颜色之外还用线型、虚线、纹理区分含义，避免色弱用户失去信息。
- 公式不要依赖 MathJax。最终 HTML 可用纯文本：`HGL=z+p/(rho g)`、`M1n=M1 sin beta`。
- 如果需要动画，只做可关闭的轻量 CSS 动画，例如流向虚线移动。默认静态也必须完整可读。
- 打印模式中保留 SVG 和图注，隐藏交互控件。
- 不把组件做成可精确查数工具。Moody、斜激波图、PM 函数都用“入口/流程/趋势”表达。

## 7. 主要风险点

1. 视觉误把“条件图”变成“必考图”。解决：使用 `主线/高风险/高分/拓展/非主线` 标签，不使用“必考”。
2. 低速水头线误导到可压缩题。解决：V02 明确写“不可跨高 Ma/激波”，V09 作为可压缩断点补充。
3. Moody 图被当作查数图。解决：V04 标注“概念示意，不能查数”，只画定性曲线。
4. 动量图方向误导。解决：V03 固定写“R 为管壁对水，题问水对管需取反”，并展示压力力。
5. 边界层外缘误画成实体边界。解决：V05 用虚线/半透明线，并在图注写“0.99 约定，不是真实界面”。
6. 喷管堵塞误导为“背压永远不影响下游”。解决：V06 只说质量流量平台，V09/V07 补充管外膨胀波、斜激波或管内正激波。
7. 专业拓展被抬高。解决：热泵、压气机只在 V08 或 V10 的灰色小注中出现，不进入主流程、不用醒目色。

## 8. 最小可交付视觉范围

若主 HTML 时间紧，优先实现 8 个组件：

1. V01 控制体与通量边界。
2. V02 伯努利水头线账本。
3. V03 动量控制体受力图。
4. V04 Moody/损失决策图。
5. V05 边界层分离图。
6. V06 喷管堵塞与质量流量平台。
7. V07 斜激波/膨胀扇波系图。
8. V08 实验读数链。

V09 和 V10 建议作为风险增强组件：V09 放在可压缩章节接口，V10 放在右侧速查栏或总览区。
