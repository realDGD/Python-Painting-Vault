"""
图表：定制化双边无向弦图 / 带自定义图例的关系映射弦图
依赖：matplotlib, numpy, pandas
数据输入：data.csv，第一列为 Taxon_name，后续列为各 Day 节点的数值矩阵
"""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib.patches import Patch


ROOT = Path(__file__).resolve().parent
DATA_PATH = ROOT / "data.csv"
OUTPUT_PATH = ROOT / "result.png"


COLORS_TO = np.array(
    [
        [204, 103, 99],
        [232, 183, 183],
        [252, 168, 133],
        [206, 96, 16],
        [61, 114, 176],
        [1, 7, 172],
    ],
    dtype=float,
) / 255

COLORS_FROM = np.array(
    [
        [32, 180, 2],
        [95, 167, 255],
        [85, 77, 150],
        [253, 224, 169],
        [215, 234, 209],
        [177, 229, 253],
        [255, 239, 206],
        [163, 184, 209],
        [207, 225, 226],
        [219, 210, 234],
    ],
    dtype=float,
) / 255


def load_data() -> tuple[np.ndarray, list[str], list[str]]:
    frame = pd.read_csv(DATA_PATH)
    row_names = frame.iloc[:, 0].astype(str).tolist()
    col_names = frame.columns[1:].tolist()
    data = frame.iloc[:, 1:].to_numpy(dtype=float)
    return data, row_names, col_names


def pol2cart(theta: np.ndarray | float, radius: float = 1.0) -> np.ndarray:
    return np.column_stack([np.cos(theta) * radius, np.sin(theta) * radius])


def arc_points(theta1: float, theta2: float, radius: float = 1.0, n: int = 100) -> np.ndarray:
    theta = np.linspace(theta1, theta2, n)
    return pol2cart(theta, radius)


def quadratic_bezier(points: np.ndarray, n: int = 200) -> np.ndarray:
    t = np.linspace(0, 1, n)[:, None]
    return (1 - t) ** 2 * points[0] + 2 * (1 - t) * t * points[1] + t**2 * points[2]


def draw_annular_segment(
    ax: plt.Axes,
    theta1: float,
    theta2: float,
    color: np.ndarray,
    *,
    inner_radius: float = 1.075,
    outer_radius: float = 1.15,
    zorder: int = 3,
) -> None:
    inner = arc_points(theta1, theta2, inner_radius)
    outer = arc_points(theta2, theta1, outer_radius)
    polygon = np.vstack([inner, outer])
    ax.fill(
        polygon[:, 0],
        polygon[:, 1],
        facecolor=color,
        edgecolor="none",
        zorder=zorder,
        antialiased=True,
    )


def draw_chord(
    ax: plt.Axes,
    theta_source_a: float,
    theta_source_b: float,
    theta_target_a: float,
    theta_target_b: float,
    color: np.ndarray,
) -> None:
    p1 = pol2cart(theta_source_a)[0]
    p2 = pol2cart(theta_source_b)[0]
    p3 = pol2cart(theta_target_a)[0]
    p4 = pol2cart(theta_target_b)[0]
    center = np.array([0.0, 0.0])

    line1 = quadratic_bezier(np.vstack([p1, center, p3]))
    line2 = quadratic_bezier(np.vstack([p2, center, p4]))
    target_arc = arc_points(theta_target_a, theta_target_b)
    source_arc = arc_points(theta_source_b, theta_source_a)
    polygon = np.vstack([line1, target_arc, line2[::-1], source_arc])

    ax.fill(
        polygon[:, 0],
        polygon[:, 1],
        facecolor=color,
        edgecolor="none",
        alpha=0.4,
        zorder=1,
        antialiased=True,
    )


def matlab_tick_step(length: float, compact_degree: float) -> float:
    step = length / compact_degree
    exponent = np.ceil(np.log10(step))
    return round(round(step / 10 ** (exponent - 2)) / 5) * 5 * 10 ** (exponent - 2)


def format_tick(value: float) -> str:
    if abs(value - round(value)) < 1e-8:
        return str(int(round(value)))
    return f"{value:g}"


def draw_tick_segment(
    ax: plt.Axes,
    theta1: float,
    theta2: float,
    total: float,
    tick_step: float,
) -> None:
    outline = arc_points(theta1, theta2, 1.17, 160)
    ax.plot(outline[:, 0], outline[:, 1], color="black", linewidth=1.5, zorder=4)

    if total <= 0:
        return

    major_values = np.arange(0, total + 1e-9, tick_step)
    minor_values = np.arange(0, total + 1e-9, tick_step / 5)

    for value in minor_values:
        theta = (theta2 - theta1) / total * value + theta1
        p0 = pol2cart(theta, 1.17)[0]
        p1 = pol2cart(theta, 1.18)[0]
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="black", linewidth=1.5, zorder=4)

    for value in major_values:
        theta = (theta2 - theta1) / total * value + theta1
        p0 = pol2cart(theta, 1.17)[0]
        p1 = pol2cart(theta, 1.19)[0]
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color="black", linewidth=1.5, zorder=5)
        rotation = np.degrees(theta)
        horizontal_alignment = "left"
        if 90 < rotation < 270:
            rotation += 180
            horizontal_alignment = "right"
        label_pos = pol2cart(theta, 1.205)[0]
        ax.text(
            label_pos[0],
            label_pos[1],
            format_tick(value),
            rotation=rotation,
            rotation_mode="anchor",
            ha=horizontal_alignment,
            va="center_baseline",
            fontsize=10.5,
            color="#202020",
            family="Arial",
            zorder=6,
        )


def label_rotation(theta: float) -> float:
    rotation = np.degrees(theta) % 360
    if 0 < rotation < 180:
        return np.degrees(theta - np.pi / 2)
    return np.degrees(theta - 1.5 * np.pi)


def draw_label(
    ax: plt.Axes,
    theta: float,
    text: str,
    *,
    radius: float = 1.32,
    fontsize: float = 30,
) -> None:
    x, y = pol2cart(theta, radius)[0]
    ax.text(
        x,
        y,
        text,
        rotation=label_rotation(theta),
        ha="center",
        va="center",
        fontsize=fontsize,
        color="#202020",
        family="Arial",
        zorder=7,
    )


def build_geometry(data: np.ndarray) -> tuple[list[tuple[float, float]], list[tuple[float, float]], float]:
    sep1 = 1 / 20
    sep2 = 1 / 80
    total = data.sum()
    ratio_from = np.r_[0, data.sum(axis=1) / total]
    ratio_to = np.r_[0, data.sum(axis=0) / total]
    row_count, col_count = data.shape

    sep_len = np.pi * (1 - 2 * sep1) * sep2
    base_len_from = np.pi * (1 - sep1) - (row_count - 1) * sep_len
    base_len_to = np.pi * (1 - sep1) - (col_count - 1) * sep_len

    from_arcs = []
    for i in range(row_count):
        theta1 = 2 * np.pi - np.pi * sep1 / 2 - ratio_from[: i + 1].sum() * base_len_from - i * sep_len
        theta2 = 2 * np.pi - np.pi * sep1 / 2 - ratio_from[: i + 2].sum() * base_len_from - i * sep_len
        from_arcs.append((theta1, theta2))

    to_arcs = []
    for j in range(col_count):
        theta1 = np.pi - np.pi * sep1 / 2 - ratio_to[: j + 1].sum() * base_len_to - j * sep_len
        theta2 = np.pi - np.pi * sep1 / 2 - ratio_to[: j + 2].sum() * base_len_to - j * sep_len
        to_arcs.append((theta1, theta2))

    average_span = total / (row_count + col_count) * 2
    tick_step = matlab_tick_step(average_span, 1.7)
    return from_arcs, to_arcs, tick_step


def draw_chart() -> None:
    data, row_names, col_names = load_data()
    from_arcs, to_arcs, tick_step = build_geometry(data)

    fig = plt.figure(figsize=(13.79, 11.47), dpi=100, facecolor="white")
    ax = fig.add_axes([0.02, 0.025, 0.78, 0.95])
    ax.set_aspect("equal")
    ax.set_xlim(-1.38, 1.38)
    ax.set_ylim(-1.38, 1.38)
    ax.axis("off")

    row_count, col_count = data.shape

    for i in range(row_count):
        row_total = data[i, :].sum()
        if row_total <= 0:
            continue
        theta1, theta2 = from_arcs[i]
        row_values = np.r_[0, data[i, ::-1] / row_total]
        for j in range(col_count - 1, -1, -1):
            col_total = data[:, j].sum()
            if data[i, j] <= 0 or col_total <= 0:
                continue

            to_theta1, to_theta2 = to_arcs[j]
            col_values = np.r_[0, data[:, j] / col_total]
            left_index = col_count - j

            theta5 = (theta2 - theta1) * row_values[:left_index].sum() + theta1
            theta6 = (theta2 - theta1) * row_values[: left_index + 1].sum() + theta1
            theta7 = (to_theta1 - to_theta2) * col_values[: i + 1].sum() + to_theta2
            theta8 = (to_theta1 - to_theta2) * col_values[: i + 2].sum() + to_theta2
            draw_chord(ax, theta5, theta6, theta7, theta8, COLORS_FROM[i])

    for j, (theta1, theta2) in enumerate(to_arcs):
        draw_annular_segment(ax, theta1, theta2, COLORS_TO[j])
        draw_tick_segment(ax, theta1, theta2, data[:, j].sum(), tick_step)
        draw_label(ax, (theta1 + theta2) / 2, col_names[j], fontsize=25)

    hidden_rows = {0, 4, 5, 7, 8, 9}
    for i, (theta1, theta2) in enumerate(from_arcs):
        draw_annular_segment(ax, theta1, theta2, COLORS_FROM[i])
        draw_tick_segment(ax, theta1, theta2, data[i, :].sum(), tick_step)
        if i == 6:
            draw_label(ax, (theta1 + theta2) / 2, "Others", fontsize=25)
        elif i not in hidden_rows:
            draw_label(ax, (theta1 + theta2) / 2, row_names[i], fontsize=25)

    legend_order = [9, 8, 7, 6, 5, 4, 0]
    handles = [Patch(facecolor=COLORS_FROM[i], edgecolor="none") for i in legend_order]
    labels = [row_names[i] for i in legend_order]
    fig.legend(
        handles,
        labels,
        loc="center left",
        bbox_to_anchor=(0.79, 0.235),
        frameon=False,
        fontsize=21,
        handlelength=1.1,
        handleheight=1.3,
        handletextpad=0.35,
        labelspacing=0.75,
        borderaxespad=0,
    )

    fig.savefig(OUTPUT_PATH, dpi=100, facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    draw_chart()
