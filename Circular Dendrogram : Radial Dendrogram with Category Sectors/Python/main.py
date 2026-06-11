"""
图表：环形聚类树图 (Circular Dendrogram)
依赖：matplotlib, pandas, numpy, scipy
数据输入：data.csv，包含三列数值特征（F1, F2, F3），用于计算样本间的距离和层次聚类
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import os

script_dir = os.path.dirname(__file__)
data_path = os.path.join(script_dir, 'data.csv')
data = pd.read_csv(data_path).values
num_samples = data.shape[0]

# 样本名称 (slan1 到 slan75)
sample_names = [f"slan{i+1}" for i in range(num_samples)]

# 分类数
N = 5

# 分类名
class_names = [f"Class-{chr(65+i)}" for i in range(N)]

# 设置半径参数 (样本文本，类弧形内侧，类弧形外侧，类文本)
RSet = [1 + 1/30, 1.22, 1.27, 1.35]

# 颜色列表
colors = [
    (0, 0.4470, 0.7410),
    (0.8500, 0.3250, 0.0980),
    (0.9290, 0.6940, 0.1250),
    (0.4940, 0.1840, 0.5560),
    (0.4660, 0.6740, 0.1880)
]

# 层次聚类 (平均距离法)
Z = linkage(data, method='average')
T = fcluster(Z, N, criterion='maxclust')

# 获取树状图结构以提取坐标和顺序，但不显示图像
fig = plt.figure()
dendro = dendrogram(Z, no_plot=True)
plt.close(fig)

order = dendro['leaves']
ordered_TT = T[order]

# 角度设置
theta1 = 0
theta2 = 2 * np.pi
theta3 = (theta2 - theta1) / num_samples
theta4 = theta1 + theta3 / 2
theta5 = theta2 - theta3 / 2

# 获取节点坐标
icoord = np.array(dendro['icoord'])
dcoord = np.array(dendro['dcoord'])
maxY = np.max(dcoord)

# 计算分支截止高度
cutoff = np.median([Z[-(N-1), 2], Z[-(N-2), 2]])

# 找到每个聚类族的节点高度 (对应背景颜色深度)
HSet_dict = {}
for ic, dc in zip(icoord, dcoord):
    if (dc[0] - cutoff) * (dc[1] - cutoff) < 0:
        h = (dc[0] + dc[1]) / 2
        idx = int(round((ic[0] - 5) / 10))
        c = ordered_TT[idx]
        HSet_dict[c] = h
    if (dc[3] - cutoff) * (dc[2] - cutoff) < 0:
        h = (dc[3] + dc[2]) / 2
        idx = int(round((ic[3] - 5) / 10))
        c = ordered_TT[idx]
        HSet_dict[c] = h

# 开始绘制主图
fig, ax = plt.subplots(figsize=(10, 10))
ax.set_aspect('equal')
ax.axis('off')

# 坐标映射函数
def x_to_theta(x):
    x_min = 5
    x_max = 5 + 10 * (num_samples - 1)
    return theta4 + (theta5 - theta4) * (x - x_min) / (x_max - x_min)

def idx_to_theta(idx):
    return theta4 + (theta5 - theta4) * idx / (num_samples - 1)

# 绘制环形树状图线条
for ic, dc in zip(icoord, dcoord):
    r = maxY - np.array(dc)
    theta = x_to_theta(np.array(ic))
    
    arc_theta = np.linspace(theta[1], theta[2], 50)
    arc_r = np.full(50, r[1])
    
    plot_theta = np.concatenate(([theta[0]], arc_theta, [theta[3]]))
    plot_r = np.concatenate(([r[0]], arc_r, [r[3]]))
    
    plot_x = plot_r * np.cos(plot_theta)
    plot_y = plot_r * np.sin(plot_theta)
    
    ax.plot(plot_x, plot_y, color='k', linewidth=0.7)

# 绘制样本名称标签
for i, leaf_idx in enumerate(order):
    tT = idx_to_theta(i)
    r = maxY * RSet[0]
    
    x = r * np.cos(tT)
    y = r * np.sin(tT)
    
    rot = np.degrees(tT)
    if tT < np.pi/2 or tT > 3*np.pi/2:
        align = 'left'
    else:
        rot += 180
        align = 'right'
        
    ax.text(x, y, sample_names[leaf_idx], rotation=rot, 
            ha=align, va='center', fontsize=12, fontname='Times New Roman',
            rotation_mode='anchor')

# 获取唯一的分类类别 (按数据中出现的顺序)
classNum = pd.unique(T)

# 绘制分类背景信息和类标签
for i, c in enumerate(classNum):
    indices = np.where(ordered_TT == c)[0]
    start_idx = indices[0]
    end_idx = indices[-1]
    
    h = HSet_dict.get(c, cutoff)
    inner_r = maxY - h
    outer_r = maxY
    
    tX_start = start_idx - 0.5
    tX_end = end_idx + 0.5
    
    theta_start = idx_to_theta(tX_start)
    theta_end = idx_to_theta(tX_end)
    
    tS = np.linspace(0, 1, 50)
    arc_theta1 = theta_start + tS * (theta_end - theta_start)
    arc_theta2 = theta_end + tS * (theta_start - theta_end)
    
    # 绘制内部分类扇形
    poly_theta = np.concatenate((arc_theta1, arc_theta2))
    poly_r = np.concatenate((np.full(50, outer_r), np.full(50, inner_r)))
    
    poly_x = poly_r * np.cos(poly_theta)
    poly_y = poly_r * np.sin(poly_theta)
    
    ax.fill(poly_x, poly_y, color=colors[i], alpha=0.25, edgecolor='none')
    
    # 绘制外部分类扇形
    tX_start_outer = start_idx - 0.2
    tX_end_outer = end_idx + 0.2
    
    theta_start_outer = idx_to_theta(tX_start_outer)
    theta_end_outer = idx_to_theta(tX_end_outer)
    
    arc_theta1_o = theta_start_outer + tS * (theta_end_outer - theta_start_outer)
    arc_theta2_o = theta_end_outer + tS * (theta_start_outer - theta_end_outer)
    
    r_inner_o = maxY * RSet[1]
    r_outer_o = maxY * RSet[2]
    
    poly_theta_o = np.concatenate((arc_theta1_o, arc_theta2_o))
    poly_r_o = np.concatenate((np.full(50, r_outer_o), np.full(50, r_inner_o)))
    
    poly_x_o = poly_r_o * np.cos(poly_theta_o)
    poly_y_o = poly_r_o * np.sin(poly_theta_o)
    
    ax.fill(poly_x_o, poly_y_o, color=colors[i], alpha=0.9, edgecolor='none')
    
    # 绘制分类信息标签
    text_theta = (theta_start_outer + theta_end_outer) / 2
    r_text = maxY * RSet[3]
    
    tx = r_text * np.cos(text_theta)
    ty = r_text * np.sin(text_theta)
    
    rot = np.degrees(text_theta)
    if text_theta < np.pi:
        rot -= 90
    else:
        rot += 90
        
    ax.text(tx, ty, class_names[i], color=colors[i],
            fontsize=18, fontname='Times New Roman', fontweight='bold',
            rotation=rot, ha='center', va='center', rotation_mode='anchor')

result_path = os.path.join(script_dir, 'result.png')
plt.savefig(result_path, bbox_inches='tight', dpi=300)
