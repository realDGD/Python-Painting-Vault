"""
图表：Grouped Correlation Heatmap / Block-Diagonal Correlation Matrix
依赖：matplotlib, pandas, numpy, scikit-learn
数据输入：data.csv
"""
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from mpl_toolkits.axes_grid1 import make_axes_locatable

# 获取当前脚本的绝对路径的目录
script_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(script_dir, 'data.csv')
result_path = os.path.join(script_dir, 'result.png')

# 取消暗黑风格，使用默认背景
# plt.style.use('dark_background')

# 设置字体，防止找不到报错
try:
    plt.rcParams['font.family'] = 'Times New Roman'
except:
    pass

# 读取数据
data = pd.read_csv(data_path).values

# K-means 分组数
K = 8
CName = [f'Class-{i}' for i in range(1, K+1)]

# 运行 KMeans 进行聚类
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
labels = kmeans.fit_predict(data)

# 将相同组数据放在一起，排序
Ind = np.argsort(labels)
Class = labels[Ind]
data_sorted = data[Ind]

# 计算相关矩阵
# corrcoef 默认计算行之间的相关性
HMat = np.corrcoef(data_sorted)

# 找到分组边界
change_indices = np.where(np.diff(Class) != 0)[0] + 1
TickPos = np.concatenate(([0], change_indices, [len(Class)]))

# 绘图部分
fig, ax = plt.subplots(figsize=(8, 8))

# pcolor 绘制热图
N = data.shape[0]
X = np.arange(N + 1)

pc = ax.pcolormesh(X, X, HMat, cmap='turbo_r', vmin=-1, vmax=1, edgecolors=(0.3, 0.3, 0.3), linewidth=0.5)

# 坐标区域修饰
ax.set_aspect('equal')
ax.invert_yaxis()

# 设置刻度字体并隐藏凸出的刻度线
ax.tick_params(labelsize=14, length=0)

# 计算 Tick 位置（每个类的中点）
XTicks = (TickPos[:-1] + TickPos[1:]) / 2

ax.set_xticks(XTicks)
ax.set_yticks(XTicks)
ax.set_xticklabels(CName, rotation=30, fontsize=14, ha='right', rotation_mode='anchor')
ax.set_yticklabels(CName, fontsize=14)

# 修改标题
ax.set_title('XXXXXX K-means Centroid', fontsize=24, loc='center', pad=10)

# 绘制分组线
for i in range(1, len(TickPos)-1):
    pos = TickPos[i]
    ax.plot([pos, pos], [0, N], color='k', linewidth=2)
    ax.plot([0, N], [pos, pos], color='k', linewidth=2)

# 使用 make_axes_locatable 保证 colorbar 完美贴合并等高
# size 控制粗细，pad 控制距离（比原来更近）
divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="3%", pad=0.08)
cbar = fig.colorbar(pc, cax=cax)
cbar.ax.tick_params(direction='in')

# 保存
fig.tight_layout()
fig.savefig(result_path, dpi=300, bbox_inches='tight', facecolor=fig.get_facecolor())
