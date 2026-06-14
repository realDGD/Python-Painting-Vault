### 🎯 模板标准命名

带分隔线的聚类分组热图 / 分块相关性矩阵图 (Grouped Correlation Heatmap with Separation Lines / Block-Diagonal Correlation Matrix)

### 🏷️ AI 检索高频关键词 (Tags)

建议将这些中英双语的高频专业术语作为标签保存，精准覆盖它的底层绘制技巧与视觉特征：

- **基础图形**: 分组热图 (Grouped heatmap), 聚类热图 (Clustered heatmap), 相关性矩阵图 (Correlation matrix plot), 伪彩色图 (Pseudocolor plot / pcolor).
- **布局与拓扑**: 块状对角结构 (Block-diagonal structure), K-means 聚类排序 (K-means clustered sorting), 类别网格划分 (Category grid partitioning).
- **视觉细节**: 贯穿式分组边界线 (Intersecting boundary lines), 倾斜坐标轴分类标签 (Rotated categorical tick labels), 无边框色块叠加 (Edgeless colored cells overlay), 自定义发散型/连续型配色 (Custom continuous colormap).
- **适用场景**: 机器学习聚类结果评估可视化 (Clustering evaluation visualization), 多变量/多组学模块化相关性分析 (Modular correlation analysis), 特征共线性分组展示。

### 📝 核心特征描述 (Prompt 提示词模板)

你可以直接复制这段描述作为该模板的 AI 提示词（Prompt）。这段话精准剥离了具体的分类数据，向 AI 下达了复刻该图表所需的底层重构逻辑和图层叠加指令：

> “这是一个**带自定义边界线的聚类分组热图 (Grouped Heatmap)**。为了支持多图层叠加（hold on），底层的颜色矩阵放弃了常规的热图函数，而是采用伪彩色网格图（pcolor）配合行列维度补偿（填充 NaN）来进行数值渲染。热图的行列数据经过聚类算法（如 K-means）重新排序，使组内高度相关的变量在对角线上聚集形成色块。在颜色矩阵之上，**精准叠加了多条贯穿全局的水平和垂直黑色实线**，将整个热图切割成与聚类类别一一对应的独立矩形区块。坐标刻度居中对齐于每个类别区块，并配合连续型颜色条（Colorbar）展示相关性系数梯度。”
