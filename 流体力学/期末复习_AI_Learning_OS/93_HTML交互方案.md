# 流体力学期末复习 HTML 交互方案

更新时间：2026-04-25  
负责范围：HTML Worker-C，单文件 HTML 的交互结构方案  
目标文件：`流体力学期末复习_AI_Learning_OS.html`  
约束：单文件离线可用，不依赖外部库；本方案只提供交互结构，不修改最终 HTML 文件。

## 1. 交互目标

最终 HTML 应优先服务“考前定位、快速筛题、限时复测、错题回看”，而不是把整套材料做成百科式全文阅读器。默认首屏和默认筛选结果应突出：

- 总索引中的高风险条件、公式索引、题型索引、符号禁混表、何时不能用。
- 02、04、05、06、10、12、13、14 等冲刺高频入口。
- 章节正文中的核心公式、适用条件、禁用条件、题型动作、复测卡片。

“考试通用补充 / 专业拓展 / 非期末主线”只作为可查阅内容存在，默认不进入高亮、冲刺、推荐、自测优先队列。

## 2. 页面交互范围

### 2.1 搜索

搜索框放在顶部固定工具区，支持即时过滤和结果计数。

建议行为：

- 输入时对章节卡片、公式卡片、题型卡片、禁用条件、自测卡片进行统一过滤。
- 搜索字段匹配 `title`、`keywords`、`tags`、正文摘要、公式文本、禁用条件文本。
- 搜索结果只显示命中的模块；命中模块所在章节自动保留可见。
- 命中词用 `<mark>` 标记，但只在当前可见摘要中标记，避免重写大段 DOM。
- 支持清空按钮，`Esc` 清空搜索并恢复当前筛选状态。
- 搜索为空时回到章节/标签/模式筛选结果，而不是无条件展开全文。

实现建议：

```js
const normalized = text => text.toLowerCase().replace(/\s+/g, " ").trim();
```

为每个 `.content-card` 初始化一次 `data-search-text`，后续过滤只读该字段，避免每次输入都遍历复杂 DOM。

### 2.2 章节筛选

左侧或顶部横向章节导航使用按钮组，不使用跳转链接作为唯一入口。

建议章节分组：

- 全部
- 主线：02、04、05、06、10、14
- 高分：07、08、09、11、12、13
- 实验：14
- 单章：01 至 14

行为：

- 点击章节按钮只改变可见范围，不破坏搜索词和标签筛选。
- 当前章节按钮添加 `aria-pressed="true"`。
- 移动端改为横向滚动 segmented control 或 `<select>` 备用，不占据整屏。
- “主线 / 高分 / 实验”是筛选入口，不是内容评级；避免把专业拓展归入主线。

### 2.3 标签筛选

标签服务于考场动作，而不是知识分类堆砌。建议内置标签：

- `公式`
- `适用条件`
- `禁用条件`
- `题型`
- `易错`
- `符号`
- `实验`
- `可压缩`
- `管路损失`
- `控制体`
- `补充`
- `专业拓展`

行为：

- 支持多选标签，默认逻辑为“任一匹配”，并提供“全部匹配”切换。
- `补充`、`专业拓展` 默认不选中，也不在热门标签区置顶。
- 当启用冲刺模式时，自动排除 `补充`、`专业拓展`，除非用户手动点选。
- 标签筛选结果应显示数量，如 `题型 18`、`禁用条件 12`。

### 2.4 展开 / 折叠

默认不要全文铺开。建议三层展开结构：

- 页面级：全部展开 / 全部折叠。
- 章节级：展开本章核心摘要、题型、自测。
- 卡片级：展开公式细节、推导、例题、补充说明。

默认状态：

- 总索引、公式索引、题型索引、禁用条件展开。
- 章节正文只展开摘要与核心卡片。
- `data-kind="supplement"`、`data-kind="extension"` 默认折叠且淡化。

实现建议：

```html
<section class="chapter" data-chapter="05" data-title="能量方程与伯努利方程">
  <button class="chapter-toggle" aria-expanded="false" aria-controls="chapter-05-body">...</button>
  <div id="chapter-05-body" hidden>...</div>
</section>
```

使用 `hidden` 控制折叠内容，按钮同步 `aria-expanded`。

### 2.5 冲刺模式

冲刺模式是强约束视图，不只是换颜色。

开启后：

- 只显示总索引、公式索引、题型索引、何时不能用、高风险条件、错题、自测入口。
- 章节正文只保留 `data-priority="core"` 或 `data-exam="true"` 的卡片。
- 自动折叠长推导、背景知识、拓展内容。
- 自测卡片按错题优先、禁用条件优先、主线章节优先排序。
- 页面顶部显示“冲刺中”的紧凑状态条：剩余复测数、错题数、当前筛选数。

关闭后：

- 恢复用户进入冲刺模式前的搜索词、章节、标签和展开状态。
- 不应把冲刺模式产生的临时排序永久写回 DOM。

### 2.6 补充内容淡化开关

必须提供“淡化补充内容”开关，并且默认开启。

默认规则：

- `data-kind="supplement"`、`data-kind="extension"`、`data-exam-weight="low"` 统一加淡化样式。
- 淡化内容可见但不抢视觉焦点：降低透明度、弱边框、弱标签，不使用醒目色。
- 搜索命中补充内容时可以显示，但结果中标注“补充”，排序低于核心内容。
- 冲刺模式下补充内容默认隐藏，而不是仅淡化。

开关文案建议：

- 开：`淡化补充`
- 关：`显示补充`

不要使用“解锁高阶”“重点拓展”等会提高补充内容权重的文案。

## 3. 自测与本地交互

### 3.1 自测卡片

每张自测卡片建议使用统一结构：

```html
<article class="quiz-card"
  data-card-id="q-05-energy-loss-01"
  data-chapter="05"
  data-tags="公式,适用条件,易错"
  data-priority="core">
  <h3>...</h3>
  <div class="quiz-prompt">...</div>
  <button data-action="show-answer" aria-expanded="false">看答案</button>
  <div class="quiz-answer" hidden>...</div>
  <div class="quiz-actions">
    <button data-action="mark-correct">掌握</button>
    <button data-action="mark-wrong">错题</button>
    <button data-action="mark-later">稍后</button>
  </div>
</article>
```

卡片行为：

- 点击“看答案”展开答案，同时记录 `lastReviewedAt`。
- 点击“掌握”增加正确次数，若之前是错题，可从错题队列移除。
- 点击“错题”写入错题记录，保留章节、标签、题干摘要、最近错误时间。
- 点击“稍后”加入轻量复测队列，不等同于错题。

### 3.2 限时复测

限时复测使用纯前端计时器，不需要后台。

建议模式：

- 5 分钟：只抽 8 至 10 张核心卡。
- 10 分钟：抽 15 至 20 张，错题优先。
- 30 分钟：章节混合复测，包含禁用条件和符号禁混。

抽题优先级：

1. 本地错题。
2. `禁用条件`、`易错`、`符号` 标签。
3. 主线章节核心卡。
4. 用户当前章节/标签筛选命中的卡。
5. 其他核心卡。

补充内容规则：

- 限时复测默认不抽 `补充`、`专业拓展`。
- 只有当用户明确选择“包含补充”时才加入，并且数量不超过本轮 15%。

计时行为：

- 开始后生成固定队列，避免中途筛选变化导致题目跳动。
- 暂停只暂停倒计时，不清空当前题。
- 时间到后展示结果：完成数、错题数、未答数、需要回看的章节。
- 结果可写入 localStorage，但不要记录过长答案全文。

### 3.3 错题记录

允许使用 localStorage。错题记录应轻量、可清除、可导出文本。

建议存储键：

```js
const STORAGE_KEYS = {
  state: "fluid-final-html:state:v1",
  progress: "fluid-final-html:progress:v1",
  wrong: "fluid-final-html:wrong:v1",
  sessions: "fluid-final-html:sessions:v1"
};
```

错题记录结构：

```js
{
  "q-05-energy-loss-01": {
    "cardId": "q-05-energy-loss-01",
    "chapter": "05",
    "tags": ["公式", "适用条件", "易错"],
    "title": "实际总流能量方程的损失项",
    "wrongCount": 2,
    "correctCount": 1,
    "lastWrongAt": "2026-04-25T10:30:00+08:00",
    "lastReviewedAt": "2026-04-25T10:35:00+08:00",
    "status": "wrong"
  }
}
```

错题视图：

- 顶部提供“只看错题”筛选。
- 支持按章节、标签、最近错误时间排序。
- 支持单题移除、清空全部错题。
- 清空前使用原生 `confirm()` 即可，不需要复杂弹窗。
- 导出错题可生成纯文本到 `<textarea>` 或下载 `.txt`，仍保持单文件离线。

## 4. 页面状态建议

页面运行态统一放入一个对象，避免多个组件各自维护状态。

```js
const AppState = {
  query: "",
  chapterFilter: "all",
  tagFilters: [],
  tagMatchMode: "any",
  expandedIds: new Set(),
  sprintMode: false,
  dimSupplement: true,
  includeSupplementInQuiz: false,
  wrongOnly: false,
  activeQuizSession: null,
  sortMode: "default"
};
```

可持久化状态：

- `query` 可保存，但页面首次打开可以为空。
- `chapterFilter`、`tagFilters`、`tagMatchMode` 可保存。
- `dimSupplement` 必须默认 `true`；若用户关闭，可保存。
- `wrongOnly` 不建议跨会话保存，避免用户下次打开误以为内容缺失。
- `sprintMode` 不建议默认恢复为开启；可保存上次状态提示，但首次渲染仍默认关闭。

状态更新流程：

1. 用户触发事件。
2. 更新 `AppState`。
3. 写入必要 localStorage。
4. 调用 `applyFilters()`。
5. 调用 `renderCounters()` 和 `renderQuizPanel()`。

不要在每个按钮事件中直接散落 DOM 显隐逻辑，后期很难排查筛选叠加问题。

## 5. DOM 数据结构建议

### 5.1 顶层布局

建议结构：

```html
<body>
  <header id="topbar">搜索、模式、计数</header>
  <main id="app">
    <nav id="chapterNav" aria-label="章节筛选"></nav>
    <section id="content" aria-live="polite"></section>
    <aside id="reviewPanel" aria-label="复测与错题"></aside>
  </main>
</body>
```

移动端可将 `reviewPanel` 放到内容下方，或用非遮挡式底部入口打开。

### 5.2 内容卡片属性

所有可筛选单元统一使用 `.content-card`：

```html
<article class="content-card"
  id="card-10-darcy-fanning"
  data-chapter="10"
  data-section="公式血缘表"
  data-kind="core"
  data-priority="core"
  data-tags="公式,易错,管路损失"
  data-search-text="">
</article>
```

字段建议：

- `data-chapter`：`00` 至 `14`。
- `data-kind`：`core`、`summary`、`formula`、`quiz`、`supplement`、`extension`。
- `data-priority`：`core`、`normal`、`low`。
- `data-tags`：中文逗号或英文逗号均可，初始化时统一拆分。
- `data-exam-weight`：`high`、`medium`、`low`。

补充/拓展内容必须显式标注：

```html
<article class="content-card is-supplement"
  data-kind="extension"
  data-exam-weight="low"
  data-tags="专业拓展,补充">
</article>
```

不要只靠标题文本识别补充内容。

### 5.3 数据源方式

单文件 HTML 中有两种可选实现：

- 直接写静态 HTML 卡片，再由 JS 扫描 DOM 建索引。
- 使用内嵌 JSON 数据渲染卡片。

推荐第一种：静态 HTML 卡片更利于离线打开、无 JS 时仍可阅读；JS 只增强搜索、筛选、自测和状态。

如果使用 JSON，放在：

```html
<script type="application/json" id="app-data">...</script>
```

不要从外部 `.json` 加载。

## 6. 事件设计

统一使用事件委托：

```js
document.addEventListener("click", event => {
  const button = event.target.closest("[data-action]");
  if (!button) return;
  handleAction(button.dataset.action, button);
});
```

推荐 `data-action`：

- `clear-search`
- `toggle-chapter`
- `toggle-tag`
- `set-tag-mode`
- `toggle-section`
- `expand-all`
- `collapse-all`
- `toggle-sprint`
- `toggle-dim-supplement`
- `start-quiz`
- `pause-quiz`
- `show-answer`
- `mark-correct`
- `mark-wrong`
- `mark-later`
- `show-wrong-only`
- `clear-wrong`
- `export-wrong`

键盘快捷键可选，但不要作为唯一操作方式：

- `/` 聚焦搜索。
- `Esc` 清空搜索或关闭当前展开浮层。
- `Enter` 激活当前焦点按钮。

## 7. 可访问性注意事项

- 所有可点击控件使用 `<button>`，不要用 `<div>` 模拟按钮。
- 筛选按钮使用 `aria-pressed` 表示选中状态。
- 展开按钮使用 `aria-expanded` 和 `aria-controls`。
- 搜索结果计数放入 `aria-live="polite"` 区域。
- 计时器每秒视觉更新即可，读屏提示不应每秒打断；只在开始、暂停、结束时更新 live region。
- 色彩不能作为唯一状态提示；错题、掌握、补充都要有文字标签。
- 保证键盘 Tab 顺序：搜索 -> 模式 -> 章节 -> 标签 -> 内容 -> 复测面板。
- 折叠内容使用 `hidden`，避免读屏读到不可见长内容。
- `prefers-reduced-motion: reduce` 下关闭滚动动画、卡片翻转、倒计时闪烁。

## 8. 移动端注意事项

- 顶部搜索和模式开关保持紧凑，避免固定头部超过屏幕高度的 20%。
- 章节筛选在窄屏使用横向滚动按钮条或 `<select>`，不要使用永久左侧栏。
- 复测面板在移动端放到内容下方，或通过底部按钮进入；不要遮挡题干和答案。
- 卡片按钮最小点击区域建议 44px。
- 长公式允许横向滚动，不能压缩到不可读。
- 标签区默认折叠为一行加“更多”，防止标签把核心内容挤出首屏。
- 限时复测状态条固定在底部时，需要给正文加 `padding-bottom`，避免遮住最后一题按钮。
- 文本不要依赖 hover；答案、提示、标签说明必须点击或聚焦也能显示。

## 9. 风险与控制

### 9.1 补充内容被默认突出

风险：`考试通用补充 / 专业拓展` 如果进入热门标签、冲刺卡、限时复测默认队列，会削弱期末主线。

控制：

- 默认开启 `dimSupplement`。
- 冲刺模式默认隐藏补充/拓展。
- 限时复测默认不抽补充/拓展。
- 搜索结果中补充内容排序靠后。
- 补充标签不使用高亮色，不放在推荐标签第一屏。

### 9.2 多筛选叠加导致“内容消失”

风险：搜索、章节、标签、错题、冲刺模式同时生效时，用户可能误以为页面坏了。

控制：

- 始终显示当前筛选摘要：`搜索：xxx / 章节：05 / 标签：易错 / 结果：6`。
- 零结果时显示清除按钮：清搜索、清标签、退出冲刺。
- `wrongOnly` 不跨会话默认恢复。

### 9.3 localStorage 数据过期

风险：卡片 ID 改动后，旧错题记录找不到对应 DOM。

控制：

- 每条记录保留 `cardId` 和 `title`。
- 渲染错题时若找不到卡片，显示为“旧记录”，允许删除。
- 存储键带版本号 `v1`，后续结构变化可迁移或清空。

### 9.4 单文件性能

风险：全文很长，搜索时频繁读 `textContent` 会卡顿。

控制：

- 初始化时建立 `data-search-text`。
- 输入搜索使用 100 至 150ms debounce。
- 过滤只切换 `hidden` 或 class，不重建整页 DOM。
- 大量展开/折叠使用父容器 class 控制，少做逐节点样式写入。

## 10. 验收清单

- 离线打开 HTML 后，无网络请求、无外部库依赖。
- 搜索、章节筛选、标签筛选可以叠加，并能一键清除。
- 展开/折叠状态和 `aria-expanded` 同步。
- 冲刺模式能显著压缩视图，只保留核心复习入口。
- 补充内容默认淡化；冲刺和限时复测默认不突出补充内容。
- 自测卡片可看答案、标掌握、标错题、稍后复测。
- 错题记录写入 localStorage，可查看、删除、清空、导出。
- 移动端无横向页面溢出，长公式仅公式区域横向滚动。
- 键盘可完成搜索、筛选、展开、复测主要操作。
