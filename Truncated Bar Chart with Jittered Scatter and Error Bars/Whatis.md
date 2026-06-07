### 🎯 模板标准命名

**带抖动散点与误差棒的截断柱状图 (Truncated Bar Chart with Jittered Scatter and Error Bars)**

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的高频专业术语作为标签保存，它们精准覆盖了该图表的所有核心组件和坐标系几何变换逻辑：

- **基础图形:** 分组柱状图, 抖动散点图, 误差棒, grouped bar chart, jittered scatter plot, error bars, bar plot with individual data points.
- **坐标轴处理:** Y轴截断, 截断坐标轴, 断层坐标轴, truncated y-axis, broken axis, split y-axis.
- **视觉修饰:** 显著性差异标注 (significance markers/asterisks), 对比短横线 (horizontal brackets), 半透明填充 (semi-transparent bar fill), 无边框柱体 (edge-less bars).
- **适用场景:** 小样本组间差异对比, 悬殊量级数据可视化 (如对照组与处理组数值跨度极大时).

### 📝 核心特征描述 (Prompt 提示词模板)

直接复制这段高度结构化的描述作为该模板的 AI 提示词（Prompt）。这段话精准剥离了具体的实验数据，提炼了复刻该图表所需的底层空间拓扑和渲染规则：

> “这是一个**带有 Y 轴截断功能（Broken Y-axis）的分组柱状图**。图表的核心视觉特征包括：1. 柱体采用无边框且带有一定透明度的面填充；2. 每个柱体上方叠加了与组别颜色相匹配、带有黑色描边的**抖动散点（Jittered Scatter）**，用于展示原始数据点的分布；3. 包含表示标准差或标准误的单向垂直**误差棒（Error Bars）**；4. 在特定对比组之间，使用水平线段结合星号进行了**显著性差异标注（Significance Markers）**；5. 针对 Y 轴进行了物理截断，隐藏了中间空白的数据区间，并在轴线的截断交界处使用了斜线（/）作为明显的视觉标识符。”
