"""
图表：Combined Horizontal Stacked Bar and Conditional Dumbbell Plot
依赖：matplotlib, pandas, numpy
数据输入：data.csv，需要包含 Name, Shallow, Intermediate, Deep, Median, Low, High, Exact 列
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import numpy as np
import os

def main():
    script_dir = os.path.dirname(__file__)
    data_path = os.path.join(script_dir, 'data.csv')
    
    # Load data
    Data = pd.read_csv(data_path)
    N = len(Data)
    
    # Set Font
    plt.rcParams['font.family'] = 'Times New Roman'
    
    # Figure setup
    fig = plt.figure(figsize=(9, 9), facecolor='white')
    
    # -------------------------------------------------------------------------
    # Left axes (Stacked Barh)
    ax1 = fig.add_axes([0.12, 0.1, 0.3, 0.88])
    ax1.set_xlim(-0.01, 1)
    ax1.set_ylim(0.5, N + 0.5)
    
    # White vertical line at x=-0.01
    ax1.plot([-0.01, -0.01], [0.5, N + 0.5], color='white', linewidth=2, zorder=5)
    
    ax1.set_yticks(np.arange(1, N + 1))
    ax1.set_yticklabels(Data['Name'])
    ax1.invert_yaxis()
    
    # Hide X-axis line, ticks, labels
    for spine in ax1.spines.values():
        spine.set_visible(False)
    
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax1.tick_params(axis='y', which='both', length=0, labelsize=11)
    
    # Draw stacked barh
    colors = ['#b0e0e6', '#2c8eb5', '#16465b']
    labels = ['Shallow', 'Intermediate', 'Deep']
    
    widths_shallow = Data['Shallow'].values
    widths_intermediate = Data['Intermediate'].values
    widths_deep = Data['Deep'].values
    
    y_pos = np.arange(1, N + 1)
    
    bar1 = ax1.barh(y_pos, widths_shallow, height=0.8, color=colors[0], edgecolor='none')
    bar2 = ax1.barh(y_pos, widths_intermediate, left=widths_shallow, height=0.8, color=colors[1], edgecolor='none')
    bar3 = ax1.barh(y_pos, widths_deep, left=widths_shallow + widths_intermediate, height=0.8, color=colors[2], edgecolor='none')
    
    # Legend 1
    # Placed directly below the stacked bar chart, closer to the axis
    ax1.legend([bar1, bar2, bar3], labels, loc='upper center', bbox_to_anchor=(0.5, -0.005), ncol=2, frameon=True, edgecolor='black', fontsize=13, handlelength=1.5, handleheight=1.5, handletextpad=0.5)
    
    # -------------------------------------------------------------------------
    # Right axes (Dumbbell Plot)
    ax2 = fig.add_axes([0.44, 0.1, 0.54, 0.88])
    ax2.set_xlim(-5, 80)
    ax2.set_ylim(0.5, N + 0.5)
    ax2.invert_yaxis()
    ax2.set_xticks([0, 20, 40, 60])
    
    # Hide Y-axis line, ticks, labels
    ax2.spines['left'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax2.spines['bottom'].set_linewidth(0.8)
    
    ax2.tick_params(axis='y', which='both', left=False, right=False, labelleft=False)
    ax2.tick_params(axis='x', which='both', direction='out', labelsize=11, length=4, width=0.8)
    
    ax2.set_xlabel('Number of Transitions', fontsize=16)
    
    # Plot gray horizontal lines
    for i in range(1, N + 1):
        ax2.plot([-5, 80], [i, i], color='#e5e5e5', linewidth=0.8, zorder=1)
        
    # Plot rounded rectangles
    for i in range(N):
        y = i + 1
        low = Data['Low'].iloc[i]
        high = Data['High'].iloc[i]
        w = high - low
        h = 0.8
        
        rect = patches.FancyBboxPatch(
            (low, y - 0.4), w, h,
            boxstyle="round,pad=0,rounding_size=0.4",
            facecolor='#e5e5e5', edgecolor='none', zorder=2
        )
        ax2.add_patch(rect)
        
    # Plot line between Median and Exact
    for i in range(N):
        y = i + 1
        median = Data['Median'].iloc[i]
        exact = Data['Exact'].iloc[i]
        ax2.plot([median, exact], [y, y], color='#666666', linewidth=1.5, zorder=3)
        
    # Plot Median dots
    ax2.scatter(Data['Median'], y_pos, s=120, facecolor='white', edgecolor='#666666', linewidth=1.5, zorder=4)
    
    # Plot Exact dots with conditional colors
    cond_above = (Data['Exact'] > Data['High']).values
    cond_within = ((Data['Exact'] <= Data['High']) & (Data['Exact'] >= Data['Low'])).values
    cond_below = (Data['Exact'] < Data['Low']).values
    
    if cond_above.any():
        ax2.scatter(Data.loc[cond_above, 'Exact'], y_pos[cond_above], s=120, facecolor='#00a08a', edgecolor='#00a08a', linewidth=1.5, zorder=5)
    if cond_within.any():
        ax2.scatter(Data.loc[cond_within, 'Exact'], y_pos[cond_within], s=120, facecolor='#666666', edgecolor='#666666', linewidth=1.5, zorder=5)
    if cond_below.any():
        ax2.scatter(Data.loc[cond_below, 'Exact'], y_pos[cond_below], s=120, facecolor='#f1af01', edgecolor='#f1af01', linewidth=1.5, zorder=5)
    
    # Legend 2
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Above expectation', markerfacecolor='#00a08a', markeredgecolor='#00a08a', markersize=11),
        Line2D([0], [0], marker='o', color='w', label='Within expectation', markerfacecolor='#666666', markeredgecolor='#666666', markersize=11),
        Line2D([0], [0], marker='o', color='w', label='Below expectation', markerfacecolor='#f1af01', markeredgecolor='#f1af01', markersize=11)
    ]
    lgd2 = ax2.legend(handles=legend_elements, loc='lower right', fontsize=13, frameon=True, edgecolor='black')
    # Matplotlib legend text color cannot be set directly in the legend constructor easily in older versions, 
    # but we can set it via loop:
    for text in lgd2.get_texts():
        text.set_color('#666666')
    
    # Save figure
    result_path = os.path.join(script_dir, 'result.png')
    plt.savefig(result_path, dpi=300)
    plt.close(fig)

if __name__ == '__main__':
    main()
