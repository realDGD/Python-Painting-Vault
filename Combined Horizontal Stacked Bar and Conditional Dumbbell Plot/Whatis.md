### 🎯 模板标准命名

**水平堆叠柱状图 - 条件着色哑铃图组合图** (Combined Horizontal Stacked Bar and Conditional Dumbbell Plot)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语作为标签保存，涵盖该图表的布局和核心视觉元素：

- **基础图形**: 双面板组合图 (Dual-panel composite chart), 水平堆叠柱状图 (Horizontal stacked bar chart), 哑铃图 (Dumbbell plot), 范围点图 (Range dot plot).
- **版式布局**: 左右并排布局 (Side-by-side layout), 共享 Y 轴 (Shared Y-axis), 垂直对齐 (Vertical alignment).
- **视觉细节**: 圆角矩形区间 (Rounded rectangle range intervals), 连线 (Connecting lines), 条件着色散点 (Conditionally colored scatter points), 无边框柱体 (Edge-less bars).
- **适用场景**: 多类别组分占比与期望/实际观测值差异联合分析 (Composition mapping combined with expected vs. observed variance).

### 📝 核心特征描述 (Prompt 提示词模板)

直接复制这段描述作为你的 AI 提示词（Prompt）。这段话精准剥离了具体数据，提取了复刻该图表所需的所有拓扑结构和逻辑规则：

> “这是一个**左右并排布局、共享分类 Y 轴的复合型图表**。 **左侧面板**是一个水平堆叠柱状图 (Horizontal Stacked Bar)，用于展示各类别（行）内部不同组分的占比，柱体无描边。 **右侧面板**是一个变体哑铃图 (Dumbbell Plot)。该面板以水平方向的圆角矩形色块表示数据的置信/期望区间；每行使用线段连接中位数和实际观测值两个数据点；代表中位数的散点颜色固定，代表实际观测值的散点基于其与期望区间的关系（高于、低于、位于区间内）进行**条件逻辑着色**。 **全局特征**：左侧隐藏 X 轴刻度线，右侧隐藏 Y 轴标签与刻度线以实现视觉贯通；两个面板拥有各自独立的图例。”

### 🗂️ 结构化特征解析 (模板属性卡片)

| **核心组件**               | **绘图类型与视觉特征**                                       |
| -------------------------- | ------------------------------------------------------------ |
| **整体版式 (Layout)**      | **左右双坐标系共享 Y 轴**。通过绝对位置（Position）控制两个子图的间距，左侧保留 Y 轴分类标签文本，右侧去除 Y 轴文本和颜色，使视线能够自然从左侧平移到右侧。 |
| **左侧视觉 (Left Panel)**  | **水平堆叠柱状图**。使用 `barh` 函数配合 `stacked` 属性绘制，去除了柱体的边框（EdgeColor='none'）以呈现扁平化现代感。 |
| **右侧视觉 (Right Panel)** | **带区间的条件哑铃图**。底层使用 `rectangle` 绘制圆角矩形作为区间底色；中层使用 `plot` 绘制连接中点与实际点的线段；顶层使用多次 `scatter` 叠加圆点。其中实际值圆点通过逻辑索引（如 `< Low`, `> High`）被强行分成了三组进行**条件着色**。 |
| **图例设计 (Legends)**     | **双独立图例**。左侧图例标注堆叠柱状图的组分，放置在左侧底部；右侧图例标注哑铃图散点的条件含义，放置在右侧图表内部的右下角，互不干扰。 |

