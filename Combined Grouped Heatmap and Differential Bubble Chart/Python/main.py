"""
图表：分组热图-差异气泡组合图 (Combined Grouped Heatmap and Differential Bubble Chart)
依赖：pandas, matplotlib, numpy
数据输入：data.csv，包含 gene(行名), 分组数据(用于热图), pvalue, log2fc
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.patches as patches
import os

# 读取数据
data_path = os.path.join(os.path.dirname(__file__), 'data.csv')
df = pd.read_csv(data_path)

rowName = df['gene'].values
colName = df.columns[1:7]
Data = df.iloc[:, 1:7].values
pValue = df['pvalue'].values
log2fc = df['log2fc'].values
negLog10pValue = -np.log10(pValue)

# 颜色配置
type_arr = [1, 1, 1, 2, 2, 2]
typeColor = {1: (105/255, 143/255, 45/255), 2: (157/255, 191/255, 61/255)}

from scipy.interpolate import PchipInterpolator

CM1_raw = np.array([
    [0.6471, 0, 0.1490], [0.7503, 0.0991, 0.1511], [0.8491, 0.2008, 0.1587],
    [0.9090, 0.3267, 0.2165], [0.9606, 0.4543, 0.2751], [0.9792, 0.5884, 0.3370],
    [0.9928, 0.7133, 0.4095], [0.9948, 0.8165, 0.5065], [0.9969, 0.9040, 0.6035],
    [0.9990, 0.9680, 0.7005], [0.9680, 0.9876, 0.8078], [0.9040, 0.9628, 0.9255],
    [0.8128, 0.9207, 0.9540], [0.7034, 0.8671, 0.9230], [0.5911, 0.7874, 0.8791],
    [0.4776, 0.6966, 0.8295], [0.3773, 0.5860, 0.7717], [0.2803, 0.4704, 0.7119],
    [0.2334, 0.3418, 0.6483], [0.1922, 0.2118, 0.5843]
])

CM2_raw = np.array([
    [1.0000, 0.9608, 0.9412], [0.9983, 0.9261, 0.8916], [0.9967, 0.8914, 0.8421],
    [0.9940, 0.8402, 0.7730], [0.9907, 0.7792, 0.6921], [0.9882, 0.7164, 0.6120],
    [0.9882, 0.6487, 0.5344], [0.9882, 0.5810, 0.4568], [0.9868, 0.5148, 0.3893],
    [0.9851, 0.4487, 0.3232], [0.9744, 0.3769, 0.2654], [0.9546, 0.2993, 0.2159],
    [0.9298, 0.2241, 0.1695], [0.8704, 0.1664, 0.1447], [0.8109, 0.1086, 0.1199],
    [0.7490, 0.0830, 0.1038], [0.6863, 0.0681, 0.0906], [0.6087, 0.0495, 0.0774],
    [0.5063, 0.0248, 0.0642], [0.4039, 0, 0.0510]
])

CMX1 = np.linspace(0, 1, CM1_raw.shape[0])
CMX2 = np.linspace(0, 1, CM2_raw.shape[0])
CMXX256 = np.linspace(0, 1, 256)

CM1_interp = np.column_stack([PchipInterpolator(CMX1, CM1_raw[:, i])(CMXX256) for i in range(3)])
CM2_interp = np.column_stack([PchipInterpolator(CMX2, CM2_raw[:, i])(CMXX256) for i in range(3)])

CM1_interp = np.clip(CM1_interp, 0, 1)
CM2_interp = np.clip(CM2_interp, 0, 1)

CM1_sliced = np.flipud(CM1_interp[36:220, :])
CM2_sliced = CM2_interp[29:200, :]

CM1 = LinearSegmentedColormap.from_list('CM1', CM1_sliced)
CM2 = LinearSegmentedColormap.from_list('CM2', CM2_sliced)

fig = plt.figure(figsize=(10, 8), facecolor='white')

# ==================== Left Panel (ax1) ====================
ax1 = fig.add_axes([0.05, 0.15, 0.25, 0.75])
ax1.set_xlim(0.5, Data.shape[1] + 0.5)
ax1.set_ylim(Data.shape[0] + 0.5, -1.25)
ax1.set_xticks([])
ax1.set_yticks(np.arange(1, Data.shape[0] + 1))
ax1.set_yticklabels(rowName, fontname='Cambria', fontsize=13)
ax1.yaxis.tick_right()
ax1.tick_params(axis='y', length=0)
for spine in ax1.spines.values():
    spine.set_visible(False)

# Annotations (Top blocks)
for j in range(Data.shape[1]):
    rect = patches.Rectangle((j + 0.5, -1.0), 1, 1, facecolor=typeColor[type_arr[j]], edgecolor='none')
    ax1.add_patch(rect)

# Draw heatmap cells
vmin, vmax = np.nanmin(Data), np.nanmax(Data)
nan_fc = (205/255, 205/255, 205/255)
nan_ec = (160/255, 160/255, 160/255)
for i in range(Data.shape[0]):
    for j in range(Data.shape[1]):
        val = Data[i, j]
        if pd.isna(val):
            # NaN cell
            rect = patches.Rectangle((j + 0.5, i + 0.5), 1, 1, facecolor=nan_fc, edgecolor=nan_ec, linewidth=1.2)
            ax1.add_patch(rect)
            # Draw X
            ax1.plot([j+0.5, j+1.5], [i+0.5, i+1.5], color=nan_ec, linewidth=1.2)
            ax1.plot([j+1.5, j+0.5], [i+0.5, i+1.5], color=nan_ec, linewidth=1.2)
        else:
            norm_val = (val - vmin) / (vmax - vmin) if vmax != vmin else 0.5
            fc = CM1(norm_val)
            rect = patches.Rectangle((j + 0.5, i + 0.5), 1, 1, facecolor=fc, edgecolor=nan_ec, linewidth=1.2)
            ax1.add_patch(rect)

# ax1 colorbar
sm1 = plt.cm.ScalarMappable(cmap=CM1, norm=plt.Normalize(vmin=vmin, vmax=vmax))
cax1 = fig.add_axes([0.05, 0.11, 0.25, 0.02])
cb1 = fig.colorbar(sm1, cax=cax1, orientation='horizontal')
cb1.outline.set_linewidth(0.8)

# ax1 NaN Custom Box (Same height as colorbar: 0.02, aspect ratio matches heatmap blocks)
ax_nan = fig.add_axes([0.31, 0.11, 0.0188, 0.02])
ax_nan.set_xlim(0, 1)
ax_nan.set_ylim(0, 1)
ax_nan.set_xticks([])
ax_nan.set_yticks([])
for spine in ax_nan.spines.values():
    spine.set_visible(False)
rect_nan = patches.Rectangle((0, 0), 1, 1, facecolor=nan_fc, edgecolor=nan_ec, linewidth=1.2)
ax_nan.add_patch(rect_nan)
ax_nan.plot([0, 1], [0, 1], color=nan_ec, linewidth=1.2)
ax_nan.plot([1, 0], [0, 1], color=nan_ec, linewidth=1.2)
fig.text(0.332, 0.12, 'NaN', va='center', fontname='Cambria', fontsize=12)

# ==================== Right Panel (ax2) ====================
# Closer to heatmap
ax2 = fig.add_axes([0.41, 0.15, 0.15, 0.75 * (Data.shape[0] / (Data.shape[0] + 1.75))])
ax2.set_xlim(-1.5, 1.5)
ax2.set_ylim(Data.shape[0] + 0.5, 0.5)
ax2.set_xticks([0])
ax2.set_xticklabels([])
ax2.set_yticks(np.arange(1, Data.shape[0] + 1))
ax2.set_yticklabels([])
for spine in ax2.spines.values():
    spine.set_visible(True)
    spine.set_linewidth(2)

ax2.tick_params(axis='y', which='major', width=2, length=6, direction='out', 
                left=True, right=False)
ax2.tick_params(axis='x', which='both', bottom=False, top=False)
ax2.grid(True, axis='y', linestyle='-', color='gray', alpha=0.5, zorder=0)
# Central vertical axis line
ax2.axvline(0, color='black', linewidth=1, zorder=1)

# Bubble sizes - Increased sizes for overlap
min_size, max_size = 200, 1200
log2fc_min, log2fc_max = np.min(log2fc), np.max(log2fc)
if log2fc_max > log2fc_min:
    sizes = min_size + (max_size - min_size) * (log2fc - log2fc_min) / (log2fc_max - log2fc_min)
else:
    sizes = np.full_like(log2fc, (min_size + max_size) / 2)

# Sort to plot small bubbles on top (descending size)
sort_idx = np.argsort(sizes)[::-1]
y_coords = np.arange(1, len(log2fc) + 1)
x_coords = np.zeros_like(log2fc)

scatter = ax2.scatter(x_coords[sort_idx], y_coords[sort_idx], s=sizes[sort_idx], 
                      c=negLog10pValue[sort_idx], cmap=CM2, edgecolors='black', linewidth=1, zorder=2)

# ==================== Colorbars and Legends ====================

# Precise Title Placements
fig.text(0.58, 0.81, "log2fc", va='top', ha='left', fontname='Cambria', fontsize=14, fontweight='bold')
fig.text(0.58, 0.55, "-log10(pvalue)", va='top', ha='left', fontname='Cambria', fontsize=14, fontweight='bold')

# 1. log2fc Size Legend (Top right)
ax_size = fig.add_axes([0.57, 0.60, 0.15, 0.18])
ax_size.set_xlim(-1, 3)
ax_size.set_ylim(0.5, 3.5)
ax_size.set_xticks([])
ax_size.set_yticks([])
for spine in ax_size.spines.values():
    spine.set_visible(False)

mid_val = (log2fc_min + log2fc_max) / 2
size_vals = [max_size, (min_size + max_size) / 2, min_size]
label_vals = [log2fc_max, mid_val, log2fc_min]

# Vertical main axis to the right of the bubbles, spanning from bottom bubble to top bubble
ax_size.plot([0.8, 0.8], [1, 3], color='black', linewidth=1.2, zorder=1)

for i, (sz, val) in enumerate(zip(size_vals, label_vals)):
    y_pos = 3 - i
    # Scatter bubble
    ax_size.scatter(0, y_pos, s=sz, facecolor='#666666', edgecolor='none', zorder=2)
    # Only draw tick and label for max and min
    if i != 1:
        # Horizontal tick pointing RIGHT (OUTWARDS)
        ax_size.plot([0.8, 1.1], [y_pos, y_pos], color='black', linewidth=1.2, zorder=1)
        # Label to the RIGHT of the tick
        ax_size.text(1.3, y_pos, f"{val:.5g}", va='center', ha='left', fontname='Cambria', fontsize=12)

# 2. -log10(pvalue) Colorbar (Bottom right)
cax2 = fig.add_axes([0.60, 0.15, 0.02, 0.37])
cb2 = fig.colorbar(scatter, cax=cax2)


plt.savefig(os.path.join(os.path.dirname(__file__), 'result.png'), dpi=300, bbox_inches='tight')
