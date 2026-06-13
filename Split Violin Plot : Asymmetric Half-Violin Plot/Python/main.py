"""
图表：Split Violin Plot : Asymmetric Half-Violin Plot
依赖：matplotlib, pandas, numpy, scipy
数据输入：data.csv，包含 L_AAA, L_BBB, L_CCC, R_AAA, R_BBB, R_CCC 六列数据
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.stats import gaussian_kde
from matplotlib.patches import Patch

def plot():
    # 读取数据
    import os
    script_dir = os.path.dirname(os.path.abspath(__file__))
    df = pd.read_csv(os.path.join(script_dir, 'data.csv'))
    
    Name = ['AAA', 'BBB', 'CCC']
    ClassName = ['Ambient', 'WarNing']
    Condition = ['ns', '*', '**']
    
    # 配色
    color_L = (153/255, 153/255, 253/255)
    color_R = (255/255, 153/255, 154/255)
    
    # 此参数用于调整小提琴图宽度
    width = 0.36
    
    fig, ax = plt.subplots(figsize=(6, 5))
    ax.set_facecolor('white')
    ax.grid(True, linestyle='-', linewidth=0.5, color='lightgray', axis='both', alpha=0.7)
    # 使grid在底下
    ax.set_axisbelow(True)
    
    for i in range(len(Name)):
        data_L = df[f'L_{Name[i]}'].dropna().values
        data_R = df[f'R_{Name[i]}'].dropna().values
        
        # 使用和 MATLAB ksdensity 类似的自动带宽高斯核带宽延伸算法
        kde_L = gaussian_kde(data_L)
        bw_L = np.sqrt(kde_L.covariance[0, 0])
        yiL = np.linspace(data_L.min() - 3 * bw_L, data_L.max() + 3 * bw_L, 100)
        fL = kde_L(yiL)
        fL[0], fL[-1] = 0, 0
        
        kde_R = gaussian_kde(data_R)
        bw_R = np.sqrt(kde_R.covariance[0, 0])
        yiR = np.linspace(data_R.min() - 3 * bw_R, data_R.max() + 3 * bw_R, 100)
        fR = kde_R(yiR)
        fR[0], fR[-1] = 0, 0
        
        # 填充半小提琴
        x_L = (i + 1) - fL * width
        x_R = (i + 1) + fR * width
        
        ax.fill_betweenx(yiL, x_L, (i + 1), facecolor=color_L, edgecolor='none', alpha=0.5, zorder=2)
        ax.fill_betweenx(yiR, (i + 1), x_R, facecolor=color_R, edgecolor='none', alpha=0.5, zorder=2)
        
        # 绘制四分位数线
        qt25L, qt75L = np.percentile(data_L, [25, 75])
        qt25R, qt75R = np.percentile(data_R, [25, 75])
        
        cap_width = 0.05
        x_center_L = (i + 1) - 0.08
        ax.plot([x_center_L - cap_width, x_center_L + cap_width], [qt75L, qt75L], color='k', linewidth=1, zorder=3)
        ax.plot([x_center_L - cap_width, x_center_L + cap_width], [qt25L, qt25L], color='k', linewidth=1, zorder=3)
        ax.plot([x_center_L, x_center_L], [qt25L, qt75L], color='k', linewidth=1, zorder=3)
        
        x_center_R = (i + 1) + 0.08
        ax.plot([x_center_R - cap_width, x_center_R + cap_width], [qt75R, qt75R], color='k', linewidth=1, zorder=3)
        ax.plot([x_center_R - cap_width, x_center_R + cap_width], [qt25R, qt25R], color='k', linewidth=1, zorder=3)
        ax.plot([x_center_R, x_center_R], [qt25R, qt75R], color='k', linewidth=1, zorder=3)
        
        # 绘制中位数点
        medL = np.median(data_L)
        medR = np.median(data_R)
        ax.scatter(x_center_L, medL, s=20, color='k', zorder=4)
        ax.scatter(x_center_R, medR, s=20, color='k', zorder=4)
        
        # 绘制显著性标签
        # 此时已经复刻了 MATLAB ksdensity 的自动边界逻辑，因此可以直接使用 max(yiL, yiR)
        ax.text((i + 1), max(yiL.max(), yiR.max()), Condition[i], fontsize=16, fontname='Times New Roman', ha='center', va='bottom', zorder=5)

    # 坐标区域修饰
    ax.set_xticks([1, 2, 3])
    ax.set_xticklabels(Name, fontname='Times New Roman', fontsize=15, rotation=30)
    ax.set_xlim(0.5, 3.5)
    
    # 边框
    for spine in ax.spines.values():
        spine.set_linewidth(1)
        spine.set_color('k')
        
    # 图例
    legend_elements = [
        Patch(facecolor=color_L, edgecolor='none', alpha=0.5, label=ClassName[0]),
        Patch(facecolor=color_R, edgecolor='none', alpha=0.5, label=ClassName[1])
    ]
    ax.legend(handles=legend_elements, loc='lower right', frameon=False, prop={'family': 'Times New Roman', 'size': 10})
    
    # 调整刻度朝内，四面都有刻度
    ax.tick_params(axis='both', which='both', direction='in', top=True, bottom=True, left=True, right=True)
    
    # 获取合适的 y 轴刻度并设置 y 轴范围，使上下两端恰好是刻度数字
    plt.draw() # 更新 figure，计算自动刻度
    yticks = ax.get_yticks()
    ax.set_ylim(yticks[0], yticks[-1])
    
    plt.tight_layout()
    plt.savefig(os.path.join(script_dir, 'result.png'), dpi=300, bbox_inches='tight')

if __name__ == '__main__':
    plot()
