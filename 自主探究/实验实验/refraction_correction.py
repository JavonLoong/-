"""
=============================================================================
  水波实验 —— 光的折射校正换算程序
  
  功能：将手机相机拍到的水波观测坐标 (X, Y) 换算为水中的真实坐标 (x, y)
  
  原理：基于 Snell 折射定律，校正光线穿过水面时因折射引起的位置偏差
  
  作者：纪文龙
  日期：2026-04-14
=============================================================================
"""

import numpy as np


# ========================== 核心换算函数 ==========================

def refraction_correct(X, Y, xc, yc, H, h, n=1.33):
    """
    【直接法】将相机观测坐标换算为水下真实坐标
    
    当相机固定在水面上方，从观测图像中读取的坐标，由于光的折射
    会与真实坐标存在偏差。本函数进行校正。
    
    参数
    ----------
    X, Y : float 或 numpy数组
        从图像中读取的观测坐标（像素或物理坐标均可，但需与 H 统一单位）
    xc, yc : float
        相机光轴在水面的投影点坐标（通常是图像中心）
    H : float
        相机到水面的垂直距离
    h : float
        水深
    n : float, 可选
        水的折射率，默认 1.33
        
    返回
    ----------
    x, y : float 或 numpy数组
        校正后的真实坐标
        
    示例
    ----------
    >>> # 单点校正
    >>> x, y = refraction_correct(150, 200, 100, 100, H=30, h=10)
    
    >>> # 批量校正（多个点）
    >>> X = np.array([150, 200, 250])
    >>> Y = np.array([200, 250, 300])
    >>> x, y = refraction_correct(X, Y, 100, 100, H=30, h=10)
    """
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    
    # 相对于光轴中心的偏移
    dX = X - xc
    dY = Y - yc
    
    # tan²θ₁ = r² / H²
    tan2_theta1 = (dX**2 + dY**2) / H**2
    
    # 分母项: sqrt(n² + (n²-1)·tan²θ₁)
    denominator = np.sqrt(n**2 + (n**2 - 1) * tan2_theta1)
    
    # 比例系数 (观测坐标到真实坐标的缩放)
    # 真实偏移 = 观测偏移 / k，其中 k = H / (H + h/denominator)
    # 所以 真实偏移 = 观测偏移 * (H + h/denominator) / H
    #              = 观测偏移 * (1 + h / (H * denominator))
    scale = 1.0 + h / (H * denominator)
    
    # 换算
    x = xc + dX * scale
    y = yc + dY * scale
    
    return x, y


def refraction_correct_iterative(X, Y, xc, yc, H, h, n=1.33, 
                                  max_iter=50, tol=1e-8):
    """
    【迭代法】高精度折射校正
    
    对于需要更高精度的场景（如水面有轻微弯曲），使用迭代法求解。
    适用于隐含方程无法直接求解的情况。
    
    参数同 refraction_correct，额外参数：
    
    max_iter : int
        最大迭代次数
    tol : float
        收敛阈值（坐标变化量小于此值时停止）
        
    返回
    ----------
    x, y : float 或 numpy数组
        校正后的真实坐标
    converged : bool
        是否收敛
    """
    X = np.asarray(X, dtype=float)
    Y = np.asarray(Y, dtype=float)
    
    # 用直接法的结果作为初始值（加速收敛）
    x, y = refraction_correct(X, Y, xc, yc, H, h, n)
    
    converged = False
    for iteration in range(max_iter):
        # 用当前估计的真实坐标重新计算角度
        dx = x - xc
        dy = y - yc
        tan2_theta1 = (dx**2 + dy**2) / H**2
        
        denominator = np.sqrt(n**2 + (n**2 - 1) * tan2_theta1)
        scale = 1.0 + h / (H * denominator)
        
        x_new = xc + (X - xc) * scale
        y_new = yc + (Y - yc) * scale
        
        # 检查收敛
        max_change = max(np.max(np.abs(x_new - x)), np.max(np.abs(y_new - y)))
        if max_change < tol:
            converged = True
            break
        
        x, y = x_new, y_new
    
    return x, y, converged


# ========================== 辅助函数 ==========================

def calculate_displacement(X, Y, xc, yc, H, h, n=1.33):
    """
    计算折射导致的位置偏差量
    
    返回
    ----------
    dx, dy : float 或 numpy数组
        x 和 y 方向的偏差（真实位置 - 观测位置）
    total_displacement : float 或 numpy数组
        总偏差距离
    """
    x, y = refraction_correct(X, Y, xc, yc, H, h, n)
    
    dx = x - np.asarray(X, dtype=float)
    dy = y - np.asarray(Y, dtype=float)
    total_displacement = np.sqrt(dx**2 + dy**2)
    
    return dx, dy, total_displacement


def batch_correct_frames(frames_data, xc, yc, H, h, n=1.33):
    """
    批量校正多帧数据
    
    参数
    ----------
    frames_data : list of dict
        每帧数据，格式为 [{"frame": 帧号, "X": [...], "Y": [...]}, ...]
    xc, yc, H, h, n : 同上
    
    返回
    ----------
    corrected_frames : list of dict
        校正后的数据，格式为 [{"frame": 帧号, "x": [...], "y": [...]}, ...]
    """
    corrected_frames = []
    
    for frame in frames_data:
        X = np.array(frame["X"])
        Y = np.array(frame["Y"])
        x, y = refraction_correct(X, Y, xc, yc, H, h, n)
        
        corrected_frames.append({
            "frame": frame["frame"],
            "x": x.tolist(),
            "y": y.tolist(),
            "original_X": frame["X"],
            "original_Y": frame["Y"]
        })
    
    return corrected_frames


def generate_error_table(H, h, n=1.33, center=(0, 0), 
                         distances=None):
    """
    生成不同距离处的误差表（用于实验报告）
    
    参数
    ----------
    H : float
        相机高度
    h : float
        水深
    distances : list, 可选
        要计算的距离列表，默认自动生成
        
    返回
    ----------
    table : list of dict
        误差表数据
    """
    if distances is None:
        max_dist = H * 0.8  # 不超过相机高度的80%
        distances = np.linspace(0, max_dist, 10)
    
    xc, yc = center
    table = []
    
    for d in distances:
        X = xc + d  # 沿 x 轴方向
        Y = yc
        
        theta1_deg = np.degrees(np.arctan(d / H))
        _, _, displacement = calculate_displacement(X, Y, xc, yc, H, h, n)
        
        table.append({
            "距离 (cm)": round(d, 2),
            "入射角 θ₁ (°)": round(theta1_deg, 1),
            "位置偏差 (mm)": round(displacement * 10, 2),  # cm 转 mm
            "相对误差 (%)": round(displacement / d * 100, 2) if d > 0 else 0
        })
    
    return table


# ========================== 主程序（直接运行时的演示） ==========================

if __name__ == "__main__":
    print("=" * 60)
    print("  水波实验 —— 光的折射校正换算程序")
    print("=" * 60)
    
    # === 1. 基本使用示例 ===
    print("\n【示例 1】单点校正")
    print("-" * 40)
    
    # 实验参数
    H = 30.0   # 相机高度 30 cm
    h = 10.0   # 水深 10 cm
    n = 1.33   # 水的折射率
    xc, yc = 0, 0  # 相机正下方为原点
    
    # 观测到水波在 (15, 10) cm 处
    X_obs, Y_obs = 15.0, 10.0
    x_real, y_real = refraction_correct(X_obs, Y_obs, xc, yc, H, h, n)
    
    print(f"实验参数: H={H}cm, h={h}cm, n={n}")
    print(f"观测坐标: ({X_obs}, {Y_obs}) cm")
    print(f"真实坐标: ({x_real:.4f}, {y_real:.4f}) cm")
    print(f"偏差量:   ({x_real-X_obs:.4f}, {y_real-Y_obs:.4f}) cm")
    
    # === 2. 批量校正示例 ===
    print("\n【示例 2】多点批量校正")
    print("-" * 40)
    
    X_batch = np.array([5, 10, 15, 20, 25])
    Y_batch = np.array([0, 0, 0, 0, 0])
    
    x_batch, y_batch = refraction_correct(X_batch, Y_batch, xc, yc, H, h, n)
    
    print(f"{'观测X(cm)':>10} {'真实x(cm)':>10} {'偏差(mm)':>10} {'相对误差%':>10}")
    for X_i, x_i in zip(X_batch, x_batch):
        displacement = (x_i - X_i) * 10  # cm 转 mm
        relative_err = (x_i - X_i) / X_i * 100
        print(f"{X_i:>10.1f} {x_i:>10.4f} {displacement:>10.2f} {relative_err:>10.2f}")
    
    # === 3. 误差表 ===
    print("\n【示例 3】误差分析表")
    print("-" * 40)
    
    table = generate_error_table(H, h, n)
    print(f"{'距离(cm)':>10} {'入射角(°)':>10} {'偏差(mm)':>10} {'相对误差%':>12}")
    for row in table:
        print(f"{row['距离 (cm)']:>10.1f} {row['入射角 θ₁ (°)']:>10.1f} "
              f"{row['位置偏差 (mm)']:>10.2f} {row['相对误差 (%)']:>12.2f}")
    
    # === 4. 迭代法对比 ===
    print("\n【示例 4】直接法 vs 迭代法对比")
    print("-" * 40)
    
    x_direct, y_direct = refraction_correct(20, 15, xc, yc, H, h, n)
    x_iter, y_iter, conv = refraction_correct_iterative(20, 15, xc, yc, H, h, n)
    
    print(f"直接法: ({x_direct:.6f}, {y_direct:.6f})")
    print(f"迭代法: ({x_iter:.6f}, {y_iter:.6f}), 收敛: {conv}")
    print(f"两种方法差异: {np.sqrt((x_direct-x_iter)**2 + (y_direct-y_iter)**2):.10f} cm")
    
    print("\n" + "=" * 60)
    print("  程序运行完成！")
    print("=" * 60)
