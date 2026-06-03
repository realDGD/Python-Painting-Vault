### 🎯 模板标准命名

**分组热图-差异气泡组合图 (Combined Grouped Heatmap and Differential Bubble Chart)**

### 🏷️ AI 检索高频关键词 (Tags)

建议使用这些中英双语的结构性术语作为标签，以便 AI 能够准确捕捉图表的各个组件：

- **基础图形**：组合图表 (composite chart), 分组热图 (grouped heatmap), 一维气泡图 (1D bubble chart).
- **版式布局**：左右并排双坐标系 (side-by-side subplots), 垂直对齐 (vertical alignment), 共享Y轴标签 (shared Y-axis).
- **视觉细节**：顶部类别注释色块 (top annotation bar), 缺失值交叉线标记 (missing value cross marks / NaN 'X' marks), 气泡大小与颜色双重映射 (bubble size and color mapping).
- **适用场景**：多组学特征展示 (multi-omics profiling), 基因表达与差异显著性联合可视化 (expression and differential significance visualization).

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段简短的描述作为该模板的 AI 提示词。这段话剔除了具体的生物学数据背景，精准提取了复刻该图表所需的几何结构和渲染逻辑：

> “这是一个左右并排布局的**复合型数据可视化图表**。**左侧主体**是一个带有顶部类别分组指示色块的矩阵热图（Heatmap），单元格具有灰色描边，且针对缺失值（NaN）有特殊的视觉设计（绘制交叉线 'X' 标记），其底部配有一个水平的连续型颜色条。**右侧主体**是一个沿垂直方向与热图行严格对齐的一维气泡图（Bubble Chart），所有气泡在X轴居中，气泡的面积大小和颜色深浅分别独立映射两个不同的连续型变量。图表最右侧外部悬浮着独立的**气泡大小图例**和**垂直连续型颜色条**。”

### 🗂️ 结构化特征解析 (模板属性卡片)

| **核心组件**               | **绘图类型与视觉特征**                                       |
| -------------------------- | ------------------------------------------------------------ |
| **整体版式 (Layout)**      | **左右双坐标系共享Y轴**。利用绝对定位（Position）精准控制两个子图的间距与高度，确保左侧热图的行与右侧气泡图的Y轴坐标点在视觉上水平完全对齐。 |
| **左侧视觉 (Left Panel)**  | **带顶部注释的网格热图**。利用 `fill` 函数循环绘制带边框的方形网格映射数值；顶部附加额外的矩形色块表示列的分组（Group Annotation）；对空值/无效值位置使用 `plot` 绘制 'X' 形交叉线进行占位标记。 |
| **右侧视觉 (Right Panel)** | **一维气泡图 (1D Bubble Plot)**。所有气泡固定在相同的X轴坐标上呈单列垂直排列；使用 `bubblechart` 实现，气泡散点的面积（Size）和内部填充色（Color）分别映射不同的数据维度。 |
| **图例设计 (Legends)**     | **三组独立图例**。热图配有底部居中的水平 Colorbar 和 NaN 的文本图例；右侧气泡图外部独立配置了气泡尺寸参照图例（Bubble legend）以及专属的垂直 Colorbar，并通过 `annotation` 叠加了自定义的指标文本标题。 |