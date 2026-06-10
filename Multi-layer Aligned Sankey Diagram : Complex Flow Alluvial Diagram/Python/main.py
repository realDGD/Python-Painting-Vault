import pandas as pd
import plotly.graph_objects as go
import numpy as np
import re

df = pd.read_csv('data.csv')
df = df.dropna(subset=['source', 'target'])
df['target'] = df['target'].replace(' ', 'OutCome')
df['source'] = df['source'].replace(' ', 'OutCome')

# 配色函数
def rgb_to_hex(r, g, b):
    return "#{:02x}{:02x}{:02x}".format(int(r), int(g), int(b))

def hex_to_rgba(h, alpha=0.3):
    h = h.lstrip('#')
    return f"rgba({int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)}, {alpha})"

CList1 = [
    rgb_to_hex(233, 163, 117),
    rgb_to_hex(150, 209, 224),
    rgb_to_hex(78, 115, 180)
]

CList2 = [
    rgb_to_hex(149, 77, 85),
    rgb_to_hex(182, 85, 90),
    rgb_to_hex(208, 91, 94),
    rgb_to_hex(208, 91, 94),
    rgb_to_hex(245, 124, 112),
    rgb_to_hex(252, 150, 128),
    rgb_to_hex(252, 173, 151),
    rgb_to_hex(253, 196, 176),
    rgb_to_hex(253, 217, 203),
    rgb_to_hex(254, 236, 228),
    rgb_to_hex(230, 230, 230)
]

def get_node_color(node_name):
    if str(node_name).startswith('A'):
        idx = int(str(node_name)[1:]) - 1
        return CList1[idx % len(CList1)]
    elif str(node_name).startswith('Residual'):
        return CList2[-1]
    elif str(node_name) == 'OutCome':
        return CList2[0]
    else:
        letter = str(node_name)[0]
        if letter in 'BCDEFGH' and len(str(node_name))>1 and str(node_name)[1:].isdigit():
            idx = int(str(node_name)[1:]) - 1
            return CList2[idx % len(CList2)]
        return "#cccccc"

all_nodes = list(pd.unique(df[['source', 'target']].values.ravel('K')))
node_dict = {node: i for i, node in enumerate(all_nodes)}

node_colors = [get_node_color(node) for node in all_nodes]

def get_col(node):
    if node.startswith('A'): return 0
    if node.startswith('B') or node == 'Residual-B': return 1
    if node.startswith('C') or node == 'Residual-C': return 2
    if node.startswith('D') or node == 'Residual-D': return 3
    if node.startswith('E') or node == 'Residual-E': return 4
    if node.startswith('F'): return 5
    if node.startswith('G'): return 6
    if str(node).startswith('H') or str(node) == 'OutCome': return 7
    return 0

node_cols = [get_col(n) for n in all_nodes]
# Just use col / 7.0 exactly like test_layout.py which worked!
x = [0.001 if col == 0 else (0.999 if col == 7 else col / 7.0) for col in node_cols] 

in_vals = df.groupby('target')['value'].sum()
out_vals = df.groupby('source')['value'].sum()
node_values = {}
for n in all_nodes:
    node_values[n] = max(in_vals.get(n, 0), out_vals.get(n, 0))

# 找到所有列中总值最大的一列
max_total_val = 0
for col in range(8):
    col_nodes = [nn for nn in all_nodes if get_col(nn) == col]
    col_val = sum(node_values[nn] for nn in col_nodes)
    if col_val > max_total_val:
        max_total_val = col_val

y = []
for i, n in enumerate(all_nodes):
    col = node_cols[i]
    col_nodes = [nn for nn in all_nodes if get_col(nn) == col]
    
    def sort_key(name):
        if name.startswith('Residual'):
            return 1000
        m = re.search(r'\d+', name)
        return int(m.group()) if m else 0
    
    col_nodes = sorted(col_nodes, key=sort_key)
    total_val = sum(node_values[nn] for nn in col_nodes)
    if total_val == 0 or max_total_val == 0:
        y.append(0.5)
        continue
    
    acc = 0
    for nn in col_nodes:
        if nn == n:
            break
        acc += node_values[nn]
        
    # 计算当前列占据总高度的比例
    col_height_ratio = total_val / max_total_val
    # 为保持居中，上方留白为 (1 - col_height_ratio) / 2
    offset_y = (1.0 - col_height_ratio) / 2.0
    
    y_pos = offset_y + (acc + node_values[n] * 0.5) / max_total_val
    # 稍微缩放以避免贴边
    y_pos = 0.05 + 0.9 * y_pos
    y.append(y_pos)

source_indices = df['source'].map(node_dict).tolist()
target_indices = df['target'].map(node_dict).tolist()
values = df['value'].tolist()
link_colors = [hex_to_rgba(get_node_color(df['source'].iloc[i]), alpha=0.4) for i in range(len(df))]
# 屏蔽 OutCome 的文本显示
display_labels = ["" if n == "OutCome" else n for n in all_nodes]

# 创建桑基图
fig = go.Figure(data=[go.Sankey(
    arrangement='snap',
    node=dict(
        pad=10,
        thickness=20,
        line=dict(color="white", width=1),
        label=display_labels,
        color=node_colors,
        x=x,
        y=y
    ),
    link=dict(
        source=source_indices,
        target=target_indices,
        value=values,
        color=link_colors
    )
)])

annotations = []
labels = ["Input", "H1", "H2", "H3", "H4", "H5", "H6", "OutCome"]
for i, label in enumerate(labels):
    # Sankey 绘图区宽度为 1200 - 50(左) - 50(右) = 1100px
    # 节点厚度 20px
    # 节点左边缘从 0 到 1080 (即 1100-20) 线性分布
    # 所以节点中心点的像素位置为：i/7.0 * 1080 + 10
    # 转换为 Plotly annotation 归一化坐标：
    exact_center_x = ((i / 7.0) * 1080.0 + 10.0) / 1100.0
    
    annotations.append(dict(
        x=exact_center_x,
        y=0.96, # 缩短与图片的距离
        text=label,
        showarrow=False,
        font=dict(size=18, family="Times New Roman", color="black"),
        xanchor='center',
        yanchor='bottom'
    ))

fig.update_layout(
    font=dict(size=12, family="Times New Roman"),
    width=1200, 
    height=500,
    plot_bgcolor='white',
    paper_bgcolor='white',
    margin=dict(t=40, l=50, r=50, b=20), # 减少上下留白
    annotations=annotations
)

fig.write_image("result.png", scale=2)
print("Successfully generated result.png")
