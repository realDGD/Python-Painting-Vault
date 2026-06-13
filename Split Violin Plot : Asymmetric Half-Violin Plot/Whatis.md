### 🎯 模板标准命名

分裂小提琴图 / 双边半小提琴对比图 (Split Violin Plot / Asymmetric Half-Violin Plot)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语作为标签保存，精准覆盖它的视觉元素与统计学特征：

- **基础图形** : 分裂小提琴图 (Split violin plot), 半小提琴图 (Half violin plot), 不对称小提琴图 (Asymmetric violin plot), 密度分布图 (Density plot).
- **布局与拓扑** : 左右/背靠背对称布局 (Back-to-back layout / side-by-side split), 正负向多边形填充 (Positive/negative mirrored polygon fill).
- **视觉细节** : 核密度估计曲线 (KDE curve), 嵌套四分位数线段 (Nested quartile lines), 中位数点 (Median scatter point), 显著性检验标注 (Significance/p-value text labels), 半透明填充 (Translucent fill/Alpha).
- **适用场景** : 同一类别下双分组（如 A/B 测试、对照/实验组）数据分布形状、集中趋势与离散程度的直观对比。

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段描述作为该模板的 AI 提示词（Prompt）。这段话精准剔除了具体的测试数据，提取了复刻该图表所需的全部底层几何构建逻辑：

“这是一个用于直观对比两组数据分布的 **分裂小提琴图 (Split Violin Plot)**。在每一个X轴分类节点上，图表利用核密度估计（KDE）分别向左和向右绘制半个平滑的分布轮廓，并使用不同的半透明颜色进行面填充（背靠背布局）。在每个半小提琴的内部，通过黑色实线段标注了25%到75%的四分位区间（Q1-Q3），并用黑色实心散点标记了中位数位置。图表顶部包含用于展示两组数据统计差异的显著性文本标签（如 ns, *, ），图表外部附有双色矩形图例。”