"""
=============================================================================
  水波实验 —— 折射校正可视化演示
  
  生成直观的图表，展示折射校正的效果和误差分布
  
  输出文件：
    - 校正效果对比图.png
    - 误差分布热力图.png  
    - 不同水深误差对比图.png
    - 不同相机高度误差对比图.png
    
  作者：纪文龙
  日期：2026-04-14
=============================================================================
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from refraction_correction import refraction_correct, calculate_displacement

# 设置中文字体
matplotlib.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 输出目录
import os
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))


def plot_correction_demo():
    """图1：折射校正效果对比图"""
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # 实验参数
    H = 30.0   # 相机高度 cm
    h = 10.0   # 水深 cm
    n = 1.33
    xc, yc = 0, 0
    
    # 生成网格点（模拟水槽底部的标定网格）
    grid_x = np.arange(-20, 21, 5)
    grid_y = np.arange(-15, 16, 5)
    Xg, Yg = np.meshgrid(grid_x, grid_y)
    Xg_flat = Xg.flatten()
    Yg_flat = Yg.flatten()
    
    # 校正
    x_real, y_real = refraction_correct(Xg_flat, Yg_flat, xc, yc, H, h, n)
    
    # --- 左图：校正前后对比 ---
    ax1 = axes[0]
    ax1.scatter(Xg_flat, Yg_flat, c='#FF6B6B', marker='x', s=60, 
                label='观测位置 (有折射偏差)', zorder=3, linewidths=1.5)
    ax1.scatter(x_real, y_real, c='#4ECDC4', marker='o', s=40, 
                label='校正后真实位置', zorder=3, alpha=0.8)
    
    # 画偏移箭头
    for i in range(len(Xg_flat)):
        if abs(Xg_flat[i]) > 2 or abs(Yg_flat[i]) > 2:  # 排除中心点附近
            ax1.annotate('', xy=(x_real[i], y_real[i]), 
                        xytext=(Xg_flat[i], Yg_flat[i]),
                        arrowprops=dict(arrowstyle='->', color='#95A5A6', 
                                       lw=0.8, alpha=0.6))
    
    ax1.axhline(y=0, color='gray', linestyle='--', alpha=0.3)
    ax1.axvline(x=0, color='gray', linestyle='--', alpha=0.3)
    ax1.set_xlabel('X (cm)', fontsize=12)
    ax1.set_ylabel('Y (cm)', fontsize=12)
    ax1.set_title(f'折射校正效果对比\n(H={H}cm, h={h}cm, n={n})', fontsize=13)
    ax1.legend(loc='upper left', fontsize=9)
    ax1.set_aspect('equal')
    ax1.grid(True, alpha=0.2)
    
    # --- 右图：偏差量随距离变化 ---
    ax2 = axes[1]
    distances = np.linspace(0, 25, 100)
    _, _, displacements = calculate_displacement(
        distances, np.zeros_like(distances), xc, yc, H, h, n)
    
    ax2.plot(distances, displacements * 10, color='#E74C3C', linewidth=2.5,
             label=f'h={h}cm')
    
    # 多个水深对比
    for h_test, color in [(5, '#3498DB'), (15, '#F39C12'), (20, '#9B59B6')]:
        _, _, disp = calculate_displacement(
            distances, np.zeros_like(distances), xc, yc, H, h_test, n)
        ax2.plot(distances, disp * 10, color=color, linewidth=1.5, 
                 linestyle='--', alpha=0.7, label=f'h={h_test}cm')
    
    ax2.set_xlabel('距画面中心的距离 (cm)', fontsize=12)
    ax2.set_ylabel('位置偏差 (mm)', fontsize=12)
    ax2.set_title(f'折射偏差量 vs 距离\n(H={H}cm, n={n})', fontsize=13)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, '校正效果对比图.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 已保存: {path}")


def plot_error_heatmap():
    """图2：误差分布热力图"""
    
    H = 30.0
    h = 10.0
    n = 1.33
    xc, yc = 0, 0
    
    # 二维网格
    x_range = np.linspace(-25, 25, 200)
    y_range = np.linspace(-25, 25, 200)
    X_grid, Y_grid = np.meshgrid(x_range, y_range)
    
    # 计算每个点的偏差
    _, _, displacement = calculate_displacement(
        X_grid, Y_grid, xc, yc, H, h, n)
    displacement_mm = displacement * 10  # 转 mm
    
    fig, ax = plt.subplots(figsize=(8, 7))
    
    im = ax.pcolormesh(X_grid, Y_grid, displacement_mm, 
                        cmap='YlOrRd', shading='auto')
    
    # 画等高线
    contour = ax.contour(X_grid, Y_grid, displacement_mm, 
                          levels=[1, 2, 3, 5, 8, 10], 
                          colors='white', linewidths=0.8, alpha=0.8)
    ax.clabel(contour, inline=True, fontsize=8, fmt='%.0f mm')
    
    # 标注相机位置
    ax.plot(0, 0, 'w*', markersize=15, label='相机正下方')
    
    cbar = plt.colorbar(im, ax=ax, label='位置偏差 (mm)')
    ax.set_xlabel('X (cm)', fontsize=12)
    ax.set_ylabel('Y (cm)', fontsize=12)
    ax.set_title(f'折射偏差空间分布\n(H={H}cm, h={h}cm, n={n})', fontsize=13)
    ax.set_aspect('equal')
    ax.legend(loc='upper left', fontsize=10, 
              facecolor='black', edgecolor='white', labelcolor='white')
    
    path = os.path.join(OUTPUT_DIR, '误差分布热力图.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 已保存: {path}")


def plot_depth_comparison():
    """图3：不同水深的误差对比"""
    
    H = 30.0
    n = 1.33
    xc, yc = 0, 0
    
    fig, axes = plt.subplots(1, 2, figsize=(14, 5.5))
    
    # --- 左图：不同水深下，偏差随距离的变化 ---
    ax1 = axes[0]
    distances = np.linspace(0, 20, 100)
    depths = [2, 5, 8, 10, 15, 20]
    colors = plt.cm.viridis(np.linspace(0.1, 0.9, len(depths)))
    
    for h_val, color in zip(depths, colors):
        _, _, disp = calculate_displacement(
            distances, np.zeros_like(distances), xc, yc, H, h_val, n)
        ax1.plot(distances, disp * 10, color=color, linewidth=2, 
                 label=f'h = {h_val} cm')
    
    ax1.set_xlabel('距画面中心距离 (cm)', fontsize=12)
    ax1.set_ylabel('位置偏差 (mm)', fontsize=12)
    ax1.set_title(f'不同水深的折射偏差\n(H={H}cm)', fontsize=13)
    ax1.legend(fontsize=9)
    ax1.grid(True, alpha=0.3)
    
    # --- 右图：固定距离下，偏差随水深的变化 ---
    ax2 = axes[1]
    h_range = np.linspace(1, 25, 100)
    fixed_distances = [5, 10, 15, 20]
    colors2 = ['#E74C3C', '#3498DB', '#2ECC71', '#F39C12']
    
    for dist, color in zip(fixed_distances, colors2):
        disps = []
        for h_val in h_range:
            _, _, d = calculate_displacement(dist, 0, xc, yc, H, h_val, n)
            disps.append(d * 10)
        ax2.plot(h_range, disps, color=color, linewidth=2, 
                 label=f'r = {dist} cm')
    
    ax2.set_xlabel('水深 h (cm)', fontsize=12)
    ax2.set_ylabel('位置偏差 (mm)', fontsize=12)
    ax2.set_title(f'偏差随水深的变化\n(H={H}cm)', fontsize=13)
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, '不同水深误差对比图.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 已保存: {path}")


def plot_height_comparison():
    """图4：不同相机高度的误差对比"""
    
    h = 10.0
    n = 1.33
    xc, yc = 0, 0
    
    fig, ax = plt.subplots(figsize=(8, 5.5))
    
    distances = np.linspace(0, 20, 100)
    heights = [15, 20, 30, 40, 50, 60]
    colors = plt.cm.plasma(np.linspace(0.1, 0.9, len(heights)))
    
    for H_val, color in zip(heights, colors):
        # 只计算角度合理的范围 (θ < 60°)
        max_dist = H_val * np.tan(np.radians(60))
        valid = distances <= max_dist
        _, _, disp = calculate_displacement(
            distances[valid], np.zeros(valid.sum()), xc, yc, H_val, h, n)
        ax.plot(distances[valid], disp * 10, color=color, linewidth=2, 
                label=f'H = {H_val} cm')
    
    ax.set_xlabel('距画面中心距离 (cm)', fontsize=12)
    ax.set_ylabel('位置偏差 (mm)', fontsize=12)
    ax.set_title(f'不同相机高度的折射偏差\n(h={h}cm, n={n})', fontsize=13)
    ax.legend(fontsize=9)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, '不同相机高度误差对比图.png')
    plt.savefig(path, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"[OK] 已保存: {path}")


def print_summary_table():
    """打印实验参数下的误差汇总表"""
    
    print("\n" + "=" * 65)
    print("  典型实验参数下的折射偏差汇总")
    print("=" * 65)
    
    H = 30.0
    n = 1.33
    xc, yc = 0, 0
    
    print(f"\n  相机高度 H = {H} cm, 折射率 n = {n}")
    print("-" * 65)
    print(f"  {'水深(cm)':>8} | {'距中心5cm':>10} | {'距中心10cm':>11} | "
          f"{'距中心15cm':>11} | {'距中心20cm':>11}")
    print("-" * 65)
    
    for h_val in [2, 5, 8, 10, 12, 15, 20]:
        row = f"  {h_val:>8} |"
        for dist in [5, 10, 15, 20]:
            _, _, d = calculate_displacement(dist, 0, xc, yc, H, h_val, n)
            row += f" {d*10:>9.2f}mm |"
        print(row)
    
    print("-" * 65)
    print("  ※ 所有偏差值单位为 mm\n")


# ========================== 主程序 ==========================

if __name__ == "__main__":
    print("=" * 50)
    print("  生成折射校正可视化图表")
    print("=" * 50)
    
    # 生成所有图表
    print("\n正在生成图表...")
    plot_correction_demo()
    plot_error_heatmap()
    plot_depth_comparison()
    plot_height_comparison()
    
    # 打印汇总表
    print_summary_table()
    
    print("=" * 50)
    print("  所有图表生成完成！")
    print("=" * 50)
