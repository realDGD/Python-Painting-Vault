🎯 **模板标准命名**

地理栅格映射图 / 带自定义缺失值颜色映射的投影地图 (Geospatial Raster Map / Projected Map with Custom NaN Colormap)

🏷️ **AI 检索高频关键词 (Tags)**

建议将这些涵盖其空间信息特征和特殊数值处理技巧的中英双语术语作为标签：

- **基础图形**: 地理栅格图 (Raster map), 地理信息可视化 (Geospatial visualization), 地表网格投影 (Surface mesh plot), topograhpic map.
- **坐标与拓扑**: 经纬度网格 (Latitude-longitude limits), 地理空间投影 (Map projection/usamap), GeoTIFF 读写映射.
- **视觉细节**: 自定义缺失值灰度映射 (NaN/threshold gray mapping), 颜色条矩阵拼接 (Colormap matrix concatenation), 不等长颜色映射比例压缩 (Pivot-shifted colormap / Non-linear color mapping), 颜色条刻度文本重写 (Colorbar tick labels manipulation).
- **适用场景**: 气象/海洋/地质环境数据可视化, 带有无效区或陆地/海洋掩膜（Mask）的空间连续数据展示.

📝 **核心特征描述 (Prompt 提示词模板)**

你可以直接复制以下这段描述作为该模板的 AI 提示词（Prompt）。这段话剥离了具体的经纬度或高程数据，向 AI 精准传达了坐标系属性和颜色条魔改的底层逻辑：

“这是一个 **基于地理空间投影的栅格数据渲染地图 (Geospatial Raster Map)**。图表构建在一个受限的经纬度地图坐标系上。该模板的核心视觉和代码特征在于其 **处理特定数据（如极值或 NaN 缺失值）的颜色映射法则**：它通过向基础渐变 Colormap 矩阵的顶端（或底端）拼接自定义颜色（如单色灰色），利用非等分的阈值锚点（Pivot）压缩正常数据的颜色映射区间，并在 Colorbar 上重写刻度标签（TickLabels），从而在同一个连续颜色条中，清晰地将无效遮罩区域与有效连续数据区分开来。”
