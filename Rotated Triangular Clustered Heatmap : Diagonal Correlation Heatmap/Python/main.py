"""
图表：Rotated Triangular Clustered Heatmap
依赖：matplotlib, pandas, numpy, scipy
数据输入：Python/data.csv
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram
from matplotlib.patches import Polygon

def main():
    # 1. Load Data
    # Path is relative to project root, assumed execution from root: uv run Python/main.py
    # or just data.csv if run from Python folder. Using standard relative path.
    df = pd.read_csv('Python/data.csv', index_col=0)
    Data = df.values
    NameList = df.columns.tolist()
    
    n = Data.shape[0]

    # 2. Hierarchical clustering
    # Using correlation data as feature vectors directly mimics Matlab's default
    # behavior where `linkage` computes Euclidean distance between rows.
    Z = linkage(Data, method='average', metric='euclidean')
    
    # Get dendrogram data (without plotting it as a standard vertical plot)
    ddata = dendrogram(Z, no_plot=True)
    order = ddata['leaves']
    
    # 3. Reorder Data and NameList
    Data = Data[np.ix_(order, order)]
    NameList = [NameList[i] for i in order]
    
    # 4. Start plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 5. Plot rotated dendrogram
    icoord = ddata['icoord']
    dcoord = ddata['dcoord']
    
    # Find max Y in dendrogram
    maxY1 = max([max(y) for y in dcoord])
    
    for x_coords, y_coords in zip(icoord, dcoord):
        # x_coords are in units of 10, with first leaf at 5.
        # we convert scipy x_coords to matlab 1-based indices space: (x - 5)/10
        tX = ((np.array(x_coords) - 5) / 10) * np.sqrt(2)
        # scale Y like matlab, but add an offset so the dendrogram touches 
        # the square boundaries rather than penetrating to their centers.
        # An offset of 0.5 * sqrt(2) in tY shifts the points exactly to the top-left edge midpoint.
        tY = np.array(y_coords) / maxY1 * n / 3 + 0.5 * np.sqrt(2)
        
        # rotation by 45 degrees
        nX = tX * np.cos(np.pi/4) - tY * np.sin(np.pi/4)
        nY = tX * np.sin(np.pi/4) + tY * np.cos(np.pi/4)
        
        ax.plot(nX, nY, color='k', linewidth=1)
        
    # 6. Plot rotated heatmap
    sqX = np.array([-1, 0, 1, 0])
    sqY = np.array([0, 1, 0, -1])
    
    # Create colormap from slanCM_Data.mat
    import scipy.io as sio
    from matplotlib.colors import ListedColormap
    try:
        # Load custom colormap from slanCM_Data.mat (using 100th color)
        # Note: path is relative to project root
        mat = sio.loadmat('Matlab/slanCM_Data.mat')
        colors_list = []
        for item in mat['slandarerCM'][0]:
            colors_list.extend(item['Colors'][0])
        cmap = ListedColormap(colors_list[99])
    except Exception as e:
        print("Could not load slanCM, falling back to winter:", e)
        cmap = plt.get_cmap('winter')
    
    for i in range(n):
        for j in range(i, n):
            # i, j are 0-indexed:
            x_poly = sqX + i + j
            y_poly = sqY - i + j
            
            val = Data[i, j]
            # Normalize to [0, 1] for colormap
            norm_val = (val + 1) / 2 # Data is correlation matrix, clim([-1, 1])
            norm_val = max(0, min(1, norm_val))
            color = cmap(norm_val)
            
            poly = Polygon(np.column_stack([x_poly, y_poly]), facecolor=color, edgecolor='none')
            ax.add_patch(poly)
            
    # 7. Add Colorbar
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=plt.Normalize(vmin=-1, vmax=1))
    sm.set_array([])
    # Place colorbar at the bottom, matching the triangle base width.
    # Triangle base spans from x = -1 to x = 2*n - 1 (width = 2*n)
    # y = -3 sets it slightly below the triangle (whose bottom tip is at y = -1)
    cb_ax = ax.inset_axes([-1, -3, 2*n, 1], transform=ax.transData)
    cbar = fig.colorbar(sm, cax=cb_ax, orientation='horizontal')
    plt.rcParams['font.family'] = 'Times New Roman'
    # 刻度在里面 (direction='in')，减小字体大小到10
    cbar.ax.tick_params(direction='in', labelsize=10)
    
    # 8. Add text annotations (Right-top side labels)
    for i in range(n):
        x_text = -0.5 + i + n
        y_text = -0.5 + n - i
        ax.text(x_text, y_text, " " + NameList[i], fontsize=13, fontfamily='Times New Roman', 
                ha='left', va='center', rotation=45, rotation_mode='anchor')
        
    # Set limits and save
    ax.autoscale_view()
    
    plt.savefig('Python/result.png', dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    main()
