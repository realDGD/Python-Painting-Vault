"""
图表：Geospatial Raster Map : Projected Map with Custom NaN Colormap
依赖：matplotlib, cartopy, numpy, pandas
数据输入：data.csv (网格高程数据矩阵), cmap.csv (颜色映射矩阵)
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.patches as mpatches

def main():
    # 1. 加载数据
    data = pd.read_csv('Python/data.csv', header=None).values
    cmap_data = pd.read_csv('Python/cmap.csv').values
    
    lats = np.linspace(40, 39, data.shape[0])
    lons = np.linspace(-106, -105, data.shape[1])
    lon_grid, lat_grid = np.meshgrid(lons, lats)
    
    # 准备基础渐变 Colormap
    base_cmap = LinearSegmentedColormap.from_list('base_map', cmap_data)
    grey_color = [240/255, 240/255, 240/255]
    
    # 2. 数据处理：找出有效范围
    data_valid = data.copy()
    data_valid[data_valid < 2100] = np.nan
    min_val = np.nanmin(data_valid)
    max_val = np.nanmax(data_valid)
    
    # 画布设置
    fig = plt.figure(figsize=(18, 8))
    proj = ccrs.Mercator()
    
    # 设置统一的刻度位置
    xticks = [-106.0, -105.5, -105.0]
    yticks = [39.0, 39.5, 40.0]
    
    # ==========================================
    # 画法 1 (Demo 1): 独立 NaN 图例 + 正常渐变 Colorbar
    # ==========================================
    ax1 = fig.add_subplot(1, 2, 1, projection=proj)
    ax1.set_extent([-106, -105, 39, 40], crs=ccrs.PlateCarree())
    ax1.set_facecolor(grey_color)
    
    mesh1 = ax1.pcolormesh(lon_grid, lat_grid, data_valid, cmap=base_cmap,
                           vmin=min_val, vmax=max_val, shading='auto',
                           transform=ccrs.PlateCarree())
    
    ax1.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax1.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax1.xaxis.set_major_formatter(LongitudeFormatter())
    ax1.yaxis.set_major_formatter(LatitudeFormatter())
    ax1.set_title("Demo 1: Independent Legend for NaN")
    
    # ==========================================
    # 画法 2 (Demo 2): 拼接 Colormap + 刻度重写
    # ==========================================
    ax2 = fig.add_subplot(1, 2, 2, projection=proj)
    ax2.set_extent([-106, -105, 39, 40], crs=ccrs.PlateCarree())
    
    range_val = max_val - min_val
    nan_plot_val = min_val - range_val / 10
    
    Z_plot = data.copy()
    Z_plot[Z_plot < 2100] = nan_plot_val
    
    color_list = [(0.0, grey_color), (1/11, grey_color)]
    for i, c in enumerate(cmap_data):
        pos = 1/11 + (10/11) * (i / (len(cmap_data) - 1))
        color_list.append((pos, list(c)))
        
    custom_cmap = LinearSegmentedColormap.from_list('custom_nan_map', color_list)
    
    mesh2 = ax2.pcolormesh(lon_grid, lat_grid, Z_plot, cmap=custom_cmap,
                           vmin=nan_plot_val, vmax=max_val, shading='auto',
                           transform=ccrs.PlateCarree())
    
    ax2.set_xticks(xticks, crs=ccrs.PlateCarree())
    ax2.set_yticks(yticks, crs=ccrs.PlateCarree())
    ax2.xaxis.set_major_formatter(LongitudeFormatter())
    ax2.yaxis.set_major_formatter(LatitudeFormatter())
    ax2.set_title("Demo 2: Concatenated Colormap & Custom Ticks")
    
    # ==========================================
    # 绝对定位后处理：严格对齐 Colorbar 与主图的上下边界
    # ==========================================
    fig.canvas.draw() # 强制渲染以获取准确的主图 bounding box
    pos1 = ax1.get_position()
    pos2 = ax2.get_position()
    
    # 定义统一的宽度和间距
    cbar_width = 0.020
    pad_cbar = 0.01
    
    # Demo 1 颜色条与 NaN 框定位
    # 要求：顶部与主图平齐，底部与主图平齐，NaN 厚度与之前一致，gap 与之前一致
    gap = 0.015
    nan_height = pos1.height * 0.026 # 等同于之前 shrinkage 下的绝对厚度，保持形状不变
    cbar1_height = pos1.height - gap - nan_height
    
    # 创建 Demo 1 的两个精确 Axes
    cax1 = fig.add_axes([pos1.x1 + pad_cbar, pos1.y0 + gap + nan_height, cbar_width, cbar1_height])
    nan_ax = fig.add_axes([pos1.x1 + pad_cbar, pos1.y0, cbar_width, nan_height])
    
    cbar1 = plt.colorbar(mesh1, cax=cax1, orientation='vertical')
    cbar1.ax.tick_params(direction='in')
    
    # 绘制 Demo 1 的 NaN 框
    nan_ax.set_facecolor(grey_color)
    nan_ax.set_xticks([])
    for spine in nan_ax.spines.values():
        spine.set_edgecolor([162/255, 162/255, 162/255])
        spine.set_linewidth(cbar1.outline.get_linewidth() * 2.0)
    nan_ax.yaxis.tick_right()
    nan_ax.set_yticks([0.5])
    nan_ax.set_yticklabels(['NaN'])
    nan_ax.tick_params(left=False, right=False)
    
    # Demo 2 颜色条定位
    # 要求：顶部与主图平齐，底部与主图平齐
    cax2 = fig.add_axes([pos2.x1 + pad_cbar, pos2.y0, cbar_width, pos2.height])
    cbar2 = plt.colorbar(mesh2, cax=cax2, orientation='vertical')
    cbar2.ax.tick_params(direction='in')
    
    # 重写 Demo 2 的刻度
    ticks_orig = cbar2.get_ticks()
    mid_nan = (nan_plot_val + min_val) / 2
    tick_locs = [mid_nan] + [t for t in ticks_orig if t >= min_val and t <= max_val]
    cbar2.set_ticks(tick_locs)
    new_labels = ['NaN'] + [f'{t:g}' for t in tick_locs[1:]]
    cbar2.set_ticklabels(new_labels)
    
    # 保存结果前不做 tight_layout，以维持精准的绝对定位
    plt.savefig('Python/result.png', dpi=300, bbox_inches='tight')
    print("Plot saved to Python/result.png")

if __name__ == "__main__":
    main()
