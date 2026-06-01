"""
图表：Circular Clustered Heatmap
依赖：matplotlib, pandas, numpy, scipy
数据输入：data.csv，包含80行(slan1-slan80)和8列(var1-var8)的相关系数矩阵
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
import matplotlib.colors as mcolors
import matplotlib.cm as cm

# 1. 加载数据
import os
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data.csv')
df = pd.read_csv(data_path, index_col=0)
data = df.values
row_names = df.index.values
col_names = df.columns.values

# 2. 计算层次聚类
row_linkage = linkage(data, method='average')
row_dendro = dendrogram(row_linkage, no_plot=True)
order1 = row_dendro['leaves']

col_linkage = linkage(data.T, method='average')
col_dendro = dendrogram(col_linkage, no_plot=True)
order2 = col_dendro['leaves']

# Reorder data and names
data = data[order1, :]
data = data[:, order2]
row_names = row_names[order1]
col_names = col_names[order2]

# 3. 设置绘图参数
theta1 = np.pi / 4
theta2 = -3 * np.pi / 2

R1 = 1
R2 = 2

n_rows = data.shape[0]
n_cols = data.shape[1]

theta3 = (theta2 - theta1) / n_rows
theta4 = theta1 + theta3 / 2
theta5 = theta2 - theta3 / 2
theta6 = 2.7 * np.pi / 8

R3 = (R2 - R1) / n_cols
R4 = R1 + R3 / 2
R5 = R2 - R3 / 2

# 创建画布
fig = plt.figure(figsize=(11, 10))
fig.patch.set_facecolor('white')
# 为给 Colorbar 留出空间，将主图收缩至 0.85
ax = fig.add_axes([0, 0, 0.85, 1])
ax.set_aspect('equal')
ax.axis('off')
ax.set_xlim(-2.5, 2.5)
ax.set_ylim(-2.5, 2.5)

# 4. 绘制中心极坐标树状图 (Tree 1)
def draw_central_dendrogram():
    icoord = np.array(row_dendro['icoord'])
    dcoord = np.array(row_dendro['dcoord'])
    max_y = np.max(dcoord)
    
    for xs, ys in zip(icoord, dcoord):
        tX = (xs - 5) / (10 * (n_rows - 1))
        tT = theta4 + (theta5 - theta4) * tX
        tR = (max_y - ys) / max_y
        
        # Line 1
        ax.plot([tR[0]*np.cos(tT[0]), tR[1]*np.cos(tT[1])],
                [tR[0]*np.sin(tT[0]), tR[1]*np.sin(tT[1])], color='k', lw=0.7)
        # Line 2 (arc)
        tS = np.linspace(tT[1], tT[2], 50)
        ax.plot(tR[1]*np.cos(tS), tR[1]*np.sin(tS), color='k', lw=0.7)
        # Line 3
        ax.plot([tR[2]*np.cos(tT[2]), tR[3]*np.cos(tT[3])],
                [tR[2]*np.sin(tT[2]), tR[3]*np.sin(tT[3])], color='k', lw=0.7)

draw_central_dendrogram()

# 5. 绘制侧面树状图 (Tree 2)
def draw_side_dendrogram():
    icoord = np.array(col_dendro['icoord'])
    dcoord = np.array(col_dendro['dcoord'])
    max_y = np.max(dcoord)
    
    for xs, ys in zip(icoord, dcoord):
        tX = (xs - 5) / (10 * (n_cols - 1))
        tR = R4 + (R5 - R4) * tX
        tT = theta6 + (theta1 - theta6) * (max_y - ys) / max_y
        
        # Line 1 (arc)
        tS1 = np.linspace(tT[0], tT[1], 20)
        ax.plot(tR[0]*np.cos(tS1), tR[0]*np.sin(tS1), color='k', lw=0.7)
        # Line 2 (radial link)
        ax.plot([tR[1]*np.cos(tT[1]), tR[2]*np.cos(tT[2])],
                [tR[1]*np.sin(tT[1]), tR[2]*np.sin(tT[2])], color='k', lw=0.7)
        # Line 3 (arc)
        tS2 = np.linspace(tT[3], tT[2], 20)
        ax.plot(tR[3]*np.cos(tS2), tR[3]*np.sin(tS2), color='k', lw=0.7)

draw_side_dendrogram()

# 6. 绘制环形热力图
# Using coolwarm which matches -1 to 1 correlation range intuitively
try:
    cmap = cm.get_cmap('coolwarm')
except AttributeError:
    import matplotlib as mpl
    cmap = mpl.colormaps['coolwarm']
norm = mcolors.Normalize(vmin=-1, vmax=1)

for i in range(n_cols):
    for j in range(n_rows):
        tX = np.array([i, i+1]) / n_cols
        tY = np.array([j, j+1]) / n_rows
        
        tX = tX + 1
        tY = theta1 + (theta2 - theta1) * tY
        
        tS = np.linspace(tY[0], tY[1], 50)
        r_inner = tX[0]
        r_outer = tX[1]
        
        r_poly = np.concatenate([r_inner * np.ones(50), r_outer * np.ones(50)])
        t_poly = np.concatenate([tS, tS[::-1]])
        
        val = data[j, i]
        color = cmap(norm(val))
        
        ax.fill(r_poly * np.cos(t_poly), r_poly * np.sin(t_poly), 
                facecolor=color, edgecolor='white', lw=0.7)

# 7. 添加文本1
for i in range(n_rows):
    tT = theta4 + (theta5 - theta4) * i / (n_rows - 1)
    
    rot = np.degrees(tT)
    if tT > -np.pi/2:
        ha = 'left'
    else:
        ha = 'right'
        rot += 180
        
    ax.text((2 + 1/30) * np.cos(tT), (2 + 1/30) * np.sin(tT), 
            row_names[i], fontsize=7, fontname='sans-serif', 
            rotation=rot, rotation_mode='anchor', ha=ha, va='center')

# 8. 添加文本2
for i in range(n_cols):
    r = R4 + (R5 - R4) * i / (n_cols - 1)
    ax.text(1/30, r, col_names[i], fontsize=10, fontname='sans-serif', va='center')

# 9. 添加colorbar
sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
sm.set_array([])
cbaxes = fig.add_axes([0.83, 0.4, 0.015, 0.2]) 
cb = plt.colorbar(sm, cax=cbaxes)
cb.outline.set_visible(False)
cb.ax.tick_params(labelsize=10)

out_path = os.path.join(script_dir, 'result.png')
plt.savefig(out_path, dpi=300, bbox_inches='tight')
