## 🎯 模板标准命名

多层对齐桑基图 / 复杂流动分配图 (Multi-layer Aligned Sankey Diagram / Complex Flow Alluvial Diagram)

## 🏷️ AI 检索高频关键词 (Tags)

建议使用这些中英双语的高频术语作为标签，它们精准覆盖了该图表的几何联动和排版特征：

- **基础图形:** 桑基图, 冲击图, 数据流向图, sankey diagram, alluvial diagram, flow chart, energy/resource distribution.
- **版式布局:** 多层级结构 (multi-layer topology), 跨层映射 (cross-layer links), 单向流动 (unidirectional flow), 反向/末端对齐 (reverse/terminal alignment).
- **视觉细节:** 自定义节点间隙 (custom layer separation), 节点比例映射 (block scaling), 起点颜色继承渲染 (left-rendered links), 矩形白描边修饰 (white-edged blocks).
- **适用场景:** 复杂的投入产出分析 (input-outcome analysis), 多阶段能量/资源留存跟踪 (multi-stage resource tracking), 碳足迹或物质转移转化网络.

## 📝 核心特征描述 (Prompt 提示词模板)

直接复制这段描述作为该图表的核心 AI 提示词（Prompt）。这段话剥离了具体的计算代码和随机数据，向 AI 明确传递了复刻该图表所需的底层拓扑规则与渲染策略：

> “这是一个具有高度自定义排版对齐逻辑的**多层桑基图 (Multi-layer Sankey Diagram)**。主体视觉由位于不同层级的矩形数据节点（Blocks）以及表示数值流向的半透明连线带（Links/Ribbons）组成。其核心特征在于其**空间拓扑策略**：为了应对不对等数据流入流出造成的视觉混乱，整个图形网络的节点强制采用反向（右侧）对齐逻辑；同时，每一层的垂直节点物理间隙（Separation）支持基于独立的比例数组进行个性化调整，从而使得两端能够保持平齐。所有数据流向带的颜色均强制渲染为继承其起点端（左侧）节点的颜色。主体图形边界的空白处带有独立定位的悬浮文本标签，用于标记全局输入（Input）与全局产出（OutCome）状态。”
