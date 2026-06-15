"""
图表：有向弦图-桑基组合图 / 复杂关系流向串联复合图
依赖：matplotlib, numpy, pandas
数据输入：data.csv，首列 Region 为节点名称，其余列为同名节点的有向流量矩阵
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.patches import PathPatch, Polygon, Rectangle, Wedge
from matplotlib.path import Path as MplPath


COLORS = np.array(
    [
        [1, 201, 117],
        [197, 169, 255],
        [247, 191, 142],
        [252, 235, 79],
        [78, 149, 241],
        [190, 190, 190],
    ],
    dtype=float,
) / 255.0


def bezier(points, samples=100):
    points = np.asarray(points, dtype=float)
    t = np.linspace(0, 1, samples)[:, None]
    return (1 - t) ** 2 * points[0] + 2 * (1 - t) * t * points[1] + t**2 * points[2]


def arc_points(theta1, theta2, radius=1.0, samples=64):
    theta = np.linspace(theta1, theta2, samples)
    return np.column_stack([np.cos(theta) * radius, np.sin(theta) * radius])


def add_ribbon(ax, theta1, theta2, theta3, theta4, color):
    p1 = np.array([np.cos(theta1), np.sin(theta1)])
    p2 = np.array([np.cos(theta2), np.sin(theta2)])
    p3 = np.array([np.cos(theta3), np.sin(theta3)])
    p4 = np.array([np.cos(theta4), np.sin(theta4)])
    curve1 = bezier([p1, [0, 0], p4 * 0.965], 96)
    curve2 = bezier([p2, [0, 0], p3 * 0.965], 96)
    arrow_tip = np.array(
        [
            [np.cos(theta4) * 0.965, np.sin(theta4) * 0.965],
            [np.cos((theta3 + theta4) / 2) * 0.998, np.sin((theta3 + theta4) / 2) * 0.998],
            [np.cos(theta3) * 0.965, np.sin(theta3) * 0.965],
        ]
    )
    inner_arc = arc_points(theta2, theta1, 1.0, 32)
    poly = np.vstack([curve1, arrow_tip, curve2[::-1], inner_arc])
    ax.add_patch(Polygon(poly, closed=True, facecolor=color, edgecolor="none", alpha=0.30))


def get_tick_step(length, compact_degree=3.2):
    raw = length / compact_degree
    power = np.ceil(np.log10(raw))
    return round(round(raw / 10 ** (power - 2)) / 5) * 5 * 10 ** (power - 2)


def setup_chord_geometry(mat, sep=0.10):
    n = mat.shape[0]
    total = np.abs(mat).sum()
    row_ratio = np.abs(mat).sum(axis=1) / total
    col_ratio = np.abs(mat).sum(axis=0) / total
    ratio = (row_ratio + col_ratio) / 2
    sep_len = 2 * np.pi * sep / n
    base_len = 2 * np.pi * (1 - sep)
    starts = []
    ends = []
    offset = 0.0
    acc = 0.0
    for i, r in enumerate(ratio):
        starts.append(sep_len / 2 + acc * base_len + i * sep_len + offset)
        acc += r
        ends.append(sep_len / 2 + acc * base_len + i * sep_len + offset)
    return np.array(starts), np.array(ends)


def draw_chord(ax, labels, mat):
    starts, ends = setup_chord_geometry(mat)
    n = len(labels)
    ax.set_aspect("equal")
    ax.set_xlim(-1.42, 1.42)
    ax.set_ylim(-1.42, 1.42)
    ax.axis("off")

    for i, (a0, a1) in enumerate(zip(starts, ends)):
        ax.add_patch(
            Wedge(
                (0, 0),
                1.15,
                np.degrees(a0),
                np.degrees(a1),
                width=0.10,
                facecolor=COLORS[i],
                edgecolor="none",
            )
        )
        theta = np.linspace(a0, a1, 140)
        ax.plot(np.cos(theta) * 1.17, np.sin(theta) * 1.17, color="black", lw=1.5)
        mid = (a0 + a1) / 2
        rot = np.degrees(mid)
        text_rot = rot - 90 if 0 < rot % 360 < 180 else rot - 270
        ax.text(
            np.cos(mid) * 1.31,
            np.sin(mid) * 1.31,
            labels[i],
            ha="center",
            va="center",
            rotation=text_rot,
            fontsize=22,
        )

    theta_full = [[np.nan] * (2 * n + 1) for _ in range(n)]
    for i in range(n):
        for j in range(n):
            value = mat[i, j]
            if value <= 0:
                continue
            in_i = mat[:, i].sum()
            out_i = mat[i, :].sum()
            in_j = mat[:, j].sum()
            out_j = mat[j, :].sum()
            split_i = starts[i] + (ends[i] - starts[i]) * in_i / max(in_i + out_i, 1e-9)
            split_j = starts[j] + (ends[j] - starts[j]) * in_j / max(in_j + out_j, 1e-9)
            row_i = mat[i, :] / max(out_i, 1e-9)
            col_j = mat[:, j] / max(in_j, 1e-9)
            theta1 = ends[i] + (split_i - ends[i]) * row_i[:j].sum()
            theta2 = ends[i] + (split_i - ends[i]) * row_i[: j + 1].sum()
            theta3 = split_j + (starts[j] - split_j) * col_j[:i].sum()
            theta4 = split_j + (starts[j] - split_j) * col_j[: i + 1].sum()
            theta_full[i][j] = theta1
            theta_full[i][j + 1] = theta2
            theta_full[j][i + n] = theta3
            theta_full[j][i + n + 1] = theta4
            add_ribbon(ax, theta1, theta2, theta3, theta4, COLORS[i])

    for i in range(n):
        total = mat[i].sum() + mat[:, i].sum()
        valid_theta = []
        for th in theta_full[i]:
            if np.isnan(th):
                continue
            if not valid_theta or abs(th - valid_theta[-1]) > 1e-10:
                valid_theta.append(th)
        if len(valid_theta) < 2 or total <= 0:
            valid_theta = [starts[i], ends[i]]
        tick_values = np.arange(0, np.floor(total) + 1, 1)
        tick_theta = (valid_theta[-1] - valid_theta[0]) / total * tick_values + valid_theta[0]
        for value, th in zip(tick_values, tick_theta):
            is_major = value % 5 == 0
            length = 0.030 if is_major else 0.015
            ax.plot(
                [np.cos(th) * 1.17, np.cos(th) * (1.17 + length)],
                [np.sin(th) * 1.17, np.sin(th) * (1.17 + length)],
                color="black",
                lw=1.0,
            )
            if is_major:
                rotation = np.degrees(th) % 360
                if 90 < rotation < 270:
                    rotation += 180
                ax.text(
                    np.cos(th) * 1.22,
                    np.sin(th) * 1.22,
                    f"{value:g}",
                    fontsize=9,
                    rotation=rotation,
                    ha="center",
                    va="center_baseline",
                    rotation_mode="anchor",
                )
        if i == 0:
            target_th = tick_theta[34] if 34 < len(tick_theta) else tick_theta[-1]
            intertidal_tick34_th = target_th

    return {"starts": starts, "ends": ends, "tick34_th": intertidal_tick34_th}


def sankey_curve(x0, x1, y0a, y0b, y1a, y1b, samples=96):
    xs = np.linspace(x0, x1, samples)
    t = (xs - x0) / (x1 - x0)
    smooth = 3 * t**2 - 2 * t**3
    upper = y0a + (y1a - y0a) * smooth
    lower = y0b + (y1b - y0b) * smooth
    return xs, upper, lower


def add_gradient_band(ax, xs, upper, lower, c0, c1, alpha=0.34):
    path = MplPath(
        np.column_stack([np.r_[xs, xs[::-1]], np.r_[upper, lower[::-1]]]),
        [MplPath.MOVETO] + [MplPath.LINETO] * (len(xs) * 2 - 2) + [MplPath.CLOSEPOLY],
    )
    patch = PathPatch(path, facecolor="none", edgecolor="none")
    ax.add_patch(patch)
    grad = np.linspace(0, 1, 512)[None, :]
    cmap = LinearSegmentedColormap.from_list("link", [c0, c1])
    im = ax.imshow(
        grad,
        extent=(xs.min(), xs.max(), min(lower.min(), upper.min()), max(lower.max(), upper.max())),
        origin="lower",
        cmap=cmap,
        alpha=alpha,
        aspect="auto",
        zorder=1,
    )
    im.set_clip_path(patch)


def draw_sankey(ax, labels, mat):
    vals = mat[1:, 0].astype(float)
    total = vals.sum()
    n_targets = len(vals)
    # Sep = 0.02 in Matlab
    dst_gap = total * 0.02
    src_gap = 0
    x0, x1 = 0.0, 0.9
    block_w = 0.1
    dst_extent = total + dst_gap * (n_targets - 1)
    src_extent = total
    src_offset = (dst_extent - src_extent) / 2
    ax.set_xlim(-0.15, 1.05)
    ax.set_ylim(0, dst_extent)
    ax.invert_yaxis()
    ax.axis("off")

    source_y0, source_y1 = src_offset, src_offset + src_extent
    ax.add_patch(Rectangle((x0, source_y0), block_w, source_y1 - source_y0, facecolor=COLORS[0], edgecolor="black", lw=1.0, zorder=3))
    ax.text(x0 - 0.08, (source_y0 + source_y1) / 2, labels[0], rotation=90, ha="center", va="center", fontsize=23)

    src_cursor = source_y0
    dst_cursor = 0
    for i, value in enumerate(vals, start=1):
        y0a, y0b = src_cursor, src_cursor + value
        y1a, y1b = dst_cursor, dst_cursor + value
        xs, upper, lower = sankey_curve(x0 + block_w, x1, y0a, y0b, y1a, y1b)
        add_gradient_band(ax, xs, upper, lower, COLORS[0], COLORS[i])
        ax.add_patch(Rectangle((x1, y1a), block_w, value, facecolor=COLORS[i], edgecolor="black", lw=1.0, zorder=4))
        ax.text(x1 - 0.025, (y1a + y1b) / 2, labels[i], ha="right", va="center", fontsize=22)
        src_cursor += value
        dst_cursor += value + dst_gap
    return {"source_x": x0, "source_y_mid": (source_y0 + source_y1) / 2}


def main():
    base = Path(__file__).resolve().parent
    df = pd.read_csv(base / "data.csv", index_col=0)
    labels = [label.replace("\\_", "_") for label in df.index]
    mat = df.to_numpy(dtype=float)

    fig = plt.figure(figsize=(15.4, 10.6), facecolor="white")
    ax_chord = fig.add_axes([0.015, 0.025, 0.66, 0.95])
    ax_sankey = fig.add_axes([0.69, 0.025, 0.30, 0.95])
    chord_info = draw_chord(ax_chord, labels, mat)
    sankey_info = draw_sankey(ax_sankey, labels, mat)

    # 起始端放在左边主图的intertidal_zone节点绿色区域上，方向经过刻度 34
    intertidal_theta = chord_info["tick34_th"]
    chord_xy = (np.cos(intertidal_theta) * 1.10, np.sin(intertidal_theta) * 1.10) # 1.10 位于 wedge 的绿色区域内 (1.05 到 1.15 之间)
    chord_fig_xy = fig.transFigure.inverted().transform(ax_chord.transData.transform(chord_xy))
    
    # 虚线末端指向右端intertidal_zone 的 ne 中间
    # 动态计算偏移量以对齐 "ne"
    y_mid = sankey_info["source_y_mid"]
    target_y = y_mid * (1 - 0.23) # 根据 23pt 字体和15字符长度推算的相对偏移
    
    sankey_fig_xy = fig.transFigure.inverted().transform(
        ax_sankey.transData.transform((sankey_info["source_x"] - 0.08, target_y))
    )
    
    fig.lines.append(
        plt.Line2D(
            [chord_fig_xy[0], sankey_fig_xy[0]],
            [chord_fig_xy[1], sankey_fig_xy[1]],
            transform=fig.transFigure,
            color="black",
            lw=1.5,
            ls=(0, (6, 6)),
        )
    )
    fig.savefig(base / "result.png", dpi=160, bbox_inches="tight", pad_inches=0.02)


if __name__ == "__main__":
    main()
