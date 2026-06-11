### 🎯 模板标准命名

环形聚类树图 / 带分类背景的极坐标树状图 (Circular Dendrogram / Radial Dendrogram with Category Sectors)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的专业术语作为标签保存，涵盖了该图表的几何特征和视觉结构：

- **基础图形**: 环形树状图, 极坐标聚类树, 系统发育树, circular dendrogram, radial dendrogram, polar hierarchical clustering tree, phylogenetic tree.
- **布局与拓扑**: 极坐标转换 (polar transformation), 层次聚类 (hierarchical clustering), 树节点与分支 (tree nodes and branches).
- **视觉细节**: 扇形分类背景 (sector/wedge colored backgrounds), 内外双环高亮 (inner and outer ring highlighting), 半透明填充 (translucent face alpha), 径向旋转文本 (radial text alignment/rotation).
- **适用场景**: 样本聚类分群分析 (sample clustering), 物种进化关系可视化, 多类别高维特征分型展示。

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段描述作为该模板的 AI 提示词（Prompt）。这段话精准提取了复刻该图表所需的底层几何变换逻辑和拓扑结构指令：

> “这是一个**带分类扇形背景的环形聚类树图 (Circular Dendrogram)**。图表的主体是一个在极坐标系下展开的层次聚类树，用于展示样本间的层级距离关系。树的边缘带有随角度径向旋转的样本名称标签。整个圆形画布根据设定的最大聚类数（如 5 类）划分为了若干个区块：内部树枝区域垫有不同颜色的半透明扇形色块作为背景；最外围环绕着一圈不透明的同色弧带，并在此区域标注了对应的类别标签（Class A, B...）。整体视觉用于直观区分不同聚类簇的层级与归属。”
