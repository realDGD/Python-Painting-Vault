### 🎯 模板标准命名

有向弦图-桑基组合图 / 复杂关系流向串联复合图 (Directed Chord-Sankey Composite Plot / Serial Flow Composite Chart)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语作为标签保存，它们精准覆盖了该图表的几何联动和视觉特征：

- **基础图形** : 弦图 (Chord diagram), 有向弦图 (Directed chord diagram), 桑基图 (Sankey diagram/Alluvial diagram), 复合图表 (Composite chart/plot).
- **版式布局** : 左右并排布局 (Side-by-side layout), 跨图连线串联 (Cross-axes annotation/connecting lines), 异构图表联动 (Heterogeneous chart linkage).
- **视觉细节** : 箭头流向指示 (Arrow directed flow), 外部致密线性刻度 (Compact linear ticks), 桑基图渐变色渲染 (Gradient/interp rendering), 刻度标签旋转 (Label rotation), 坐标区域相对定位 (Normalized axes positioning).
- **适用场景** : 多维数据流向与成分追踪 (Multi-dimensional flow tracking), 生态学/宏基因组学/病毒组来源分析 (Microbiome/virome source tracking), 复杂网络多级拓扑拆解.

### 📝 核心特征描述 (Prompt 提示词模板)

直接复制这段描述作为你的 AI 提示词（Prompt）。这段话精准剥离了具体的测序或区域数据，提取了复刻该图表所需的所有拓扑结构和空间逻辑：

> “这是一个**左右并排布局、跨子图逻辑串联的异构复合型图表 (Chord-Sankey Composite Plot)**。**左侧面板**是一个带有外部致密线性刻度与次级刻度线的**有向弦图 (Directed Chord Diagram)**，弦带末端带有箭头以指示数据的明确流向；**右侧面板**是一个具有**渐变色填充带 (Gradient/interp links)\**的\**桑基图 (Sankey Diagram)**，用于对弦图中的某一个或多个核心节点的流出数据进行次级成分拆解。在两个独立坐标系之间，使用**跨图虚线 (Annotation line)**将左侧弦图的特定节点与右侧桑基图的起始节点进行物理连线，从而在视觉上实现数据流向的完美接力与过渡。”
