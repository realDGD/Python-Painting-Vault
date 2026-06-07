import matplotlib.pyplot as plt
import numpy as np
import csv
import os

"""
图表：Truncated Bar Chart with Jittered Scatter and Error Bars
依赖：matplotlib, numpy
数据输入：data.csv
"""

def load_data():
    dataA = []
    dataB = []
    with open("Python/data.csv", "r") as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            if row[0].startswith('DataA'):
                dataA.append([float(x) for x in row[1:]])
            elif row[0].startswith('DataB'):
                dataB.append([float(x) for x in row[1:]])
    return {"DataA": dataA, "DataB": dataB}

def main():
    data = load_data()
    dataA = np.array(data["DataA"])
    dataB = np.array(data["DataB"])

    meanA = np.mean(dataA, axis=1)
    meanB = np.mean(dataB, axis=1)
    stdA = np.std(dataA, axis=1, ddof=1)
    stdB = np.std(dataB, axis=1, ddof=1)

    CList1 = (188/255, 188/255, 240/255)
    CList2 = (160/255, 161/255, 166/255)

    NameList = [
        'Cortex',
        'Hippocampus',
        'Cerebellum',
        'Brainstem',
        'Cervical spinal cord',
        'Thoracic spinal cord',
        'Lumbar spinal cord'
    ]

    # Create figure and two subplots with no gap
    fig, (ax_top, ax_bottom) = plt.subplots(2, 1, sharex=True, figsize=(7, 6), gridspec_kw={'height_ratios': [1, 1]})
    fig.subplots_adjust(hspace=0.12, left=0.15, bottom=0.2)

    x = np.arange(len(NameList))
    width = 0.30
    gap = 0.04
    offset_A = -width/2 - gap/2
    offset_B = width/2 + gap/2

    def plot_on_ax(ax):
        # Bars
        ax.bar(x + offset_A, meanA, width, color=CList1, alpha=0.5, edgecolor='none')
        ax.bar(x + offset_B, meanB, width, color=CList2, alpha=0.5, edgecolor='none')

        # Jittered scatter
        # MATLAB uses 'XJitterWidth', 0.15. Uniform distribution between -0.075 and +0.075
        np.random.seed(42) # For reproducible jitter
        
        for i in range(len(NameList)):
            jitterA = np.random.uniform(-0.075, 0.075, size=5)
            ax.scatter(np.repeat(x[i] + offset_A, 5) + jitterA, dataA[i, :], 
                       s=55, c=[CList1], edgecolors='k', linewidths=0.8, zorder=3)
            
            jitterB = np.random.uniform(-0.075, 0.075, size=5)
            ax.scatter(np.repeat(x[i] + offset_B, 5) + jitterB, dataB[i, :], 
                       s=55, c=[CList2], edgecolors='k', linewidths=0.8, zorder=3)

        # Error bars
        ax.errorbar(x + offset_A, meanA, yerr=stdA, fmt='none', ecolor='k', elinewidth=1, capsize=3, zorder=4)
        ax.errorbar(x + offset_B, meanB, yerr=stdB, fmt='none', ecolor='k', elinewidth=1, capsize=3, zorder=4)

        # Significance markers
        # Helper to plot only on correct axis
        def plot_sig(X_pos, Y_pos, text):
            if (Y_pos > 1.4 and ax == ax_top) or (Y_pos <= 1.0 and ax == ax_bottom):
                # Use a horizontal errorbar to simulate the significance bracket with vertical caps
                ax.errorbar(X_pos, Y_pos, xerr=0.15, fmt='none', ecolor='k', elinewidth=1, capsize=3)
                ax.text(X_pos, Y_pos, text, ha='center', va='bottom', fontsize=15, fontweight='bold', fontname='Arial')

        # N=2 (index 1)
        X_pos = x[1] + offset_A
        Y_pos = np.max(dataA[1, :]) + 0.1
        plot_sig(X_pos, Y_pos, '***')

        # N=3 (index 2)
        X_pos = x[2] + offset_A
        Y_pos = np.max(dataA[2, :]) + 0.1
        plot_sig(X_pos, Y_pos, '****')

        # N=6 (index 5)
        X_pos = x[5] + offset_A
        Y_pos = np.max(dataA[5, :]) + 0.1
        plot_sig(X_pos, Y_pos, '****')

    plot_on_ax(ax_top)
    plot_on_ax(ax_bottom)

    # Axis limits
    ax_top.set_ylim(1.4, 2.5)
    ax_bottom.set_ylim(0, 1.0)

    # Hide spines to make the break effect
    ax_top.spines['bottom'].set_visible(False)
    ax_bottom.spines['top'].set_visible(False)
    
    # Configure ticks
    ax_top.tick_params(bottom=False, labelbottom=False, direction='out', labelsize=11)
    ax_bottom.tick_params(top=False, direction='out', labelsize=11)

    for ax in [ax_top, ax_bottom]:
        for label in ax.get_yticklabels():
            label.set_fontname('Arial')
            label.set_fontweight('bold')

    # Draw the break diagonals
    d = 0.025  # Size of diagonal lines in axes coordinates
    kwargs = dict(transform=ax_top.transAxes, color='k', clip_on=False, lw=1.5)
    ax_top.plot((-d/4.5, +d/4.5), (-d, +d), **kwargs)        # Top-left diagonal
    ax_top.plot((1 - d/4.5, 1 + d/4.5), (-d, +d), **kwargs)  # Top-right diagonal

    kwargs.update(transform=ax_bottom.transAxes)  # Switch to bottom axes
    ax_bottom.plot((-d/4.5, +d/4.5), (1 - d, 1 + d), **kwargs)  # Bottom-left diagonal
    ax_bottom.plot((1 - d/4.5, 1 + d/4.5), (1 - d, 1 + d), **kwargs)  # Bottom-right diagonal

    # Dotted lines across the gap
    ax_top.plot((0, 1), (0, 0), transform=ax_top.transAxes, ls=':', color='gray', alpha=0.6, lw=1.5, clip_on=False)
    ax_bottom.plot((0, 1), (1, 1), transform=ax_bottom.transAxes, ls=':', color='gray', alpha=0.6, lw=1.5, clip_on=False)

    # Set x-ticks
    ax_bottom.set_xticks(x)
    ax_bottom.set_xticklabels(NameList, rotation=35, ha='right', fontname='Arial', fontweight='bold', fontsize=11)

    # Adjust axis linewidths to match Matlab
    for ax in [ax_top, ax_bottom]:
        ax.spines['top'].set_linewidth(1.5)
        ax.spines['right'].set_linewidth(1.5)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

    # Remove right and top spines entirely to match standard minimalist plots if needed
    # Actually, MATLAB code does ax.Box='off' inside truncAxis for some conditions, let's remove top/right
    for ax in [ax_top, ax_bottom]:
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)

    # Add y-axis label spanning both subplots
    fig.text(0.06, 0.5, 'ug of Ab/ g wet weight of tissue', va='center', rotation='vertical',
             fontsize=15, fontname='Arial', fontweight='bold')

    # Fix layout to make it look like Matlab
    ax_top.patch.set_facecolor('none')
    ax_bottom.patch.set_facecolor('none')
    fig.patch.set_facecolor('w')

    plt.savefig('Python/result.png', dpi=300, bbox_inches='tight')
    print("Plot saved to Python/result.png")

if __name__ == "__main__":
    main()
