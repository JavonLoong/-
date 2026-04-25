"""
=============================================================================
  水波实验 —— 视频帧处理与波位置提取
  
  功能：从实验视频中逐帧提取水波位置，并应用折射校正
  
  使用方法：
    python video_processor.py --video 实验视频.mp4 --H 30 --h 10
    
  输出：
    - corrected_data.csv: 校正后的波位置数据
    - wave_tracking.png: 波追踪可视化
    
  作者：纪文龙
  日期：2026-04-14
=============================================================================
"""

import numpy as np
import argparse
import csv
import os

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False
    print("⚠ 未安装 OpenCV，安装方法: pip install opencv-python")

from refraction_correction import refraction_correct, batch_correct_frames


def extract_wave_positions_from_frame(frame, threshold=30):
    """
    从单帧图像中提取水波波前位置
    
    使用边缘检测 + 阈值分割来定位波纹
    
    参数
    ----------
    frame : numpy数组
        BGR 格式的图像帧
    threshold : int
        边缘检测阈值
        
    返回
    ----------
    positions : list of (x, y)
        检测到的波前像素坐标
    """
    if not HAS_CV2:
        return []
    
    # 转灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊去噪
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Canny 边缘检测
    edges = cv2.Canny(blurred, threshold, threshold * 3)
    
    # 提取边缘点坐标
    points = np.where(edges > 0)
    positions = list(zip(points[1].tolist(), points[0].tolist()))  # (x, y)
    
    return positions


def pixel_to_physical(px, py, img_width, img_height, 
                       physical_width, physical_height):
    """
    将像素坐标转换为物理坐标 (cm)
    
    假设图像中心对应物理坐标原点
    """
    x_cm = (px - img_width / 2) / img_width * physical_width
    y_cm = (py - img_height / 2) / img_height * physical_height
    return x_cm, y_cm


def process_video(video_path, H, h, n=1.33, 
                  physical_width=40, physical_height=30,
                  output_csv='corrected_data.csv',
                  skip_frames=1):
    """
    处理实验视频，提取并校正水波位置数据
    
    参数
    ----------
    video_path : str
        视频文件路径
    H : float
        相机高度 (cm)
    h : float
        水深 (cm)
    physical_width, physical_height : float
        水槽可见区域的物理尺寸 (cm)
    output_csv : str
        输出 CSV 文件名
    skip_frames : int
        每隔多少帧处理一次（加速处理）
    """
    if not HAS_CV2:
        print("错误：需要安装 OpenCV")
        return
    
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"错误：无法打开视频 {video_path}")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"视频信息: {width}x{height}, {fps}fps, 共{total_frames}帧")
    print(f"实验参数: H={H}cm, h={h}cm, n={n}")
    print(f"处理中...")
    
    xc, yc = 0, 0  # 物理坐标中心
    
    # 输出 CSV
    output_path = os.path.join(os.path.dirname(video_path) or '.', output_csv)
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['帧号', '时间(s)', 
                        '观测X(cm)', '观测Y(cm)', 
                        '真实x(cm)', '真实y(cm)',
                        '偏差(mm)'])
        
        frame_idx = 0
        processed = 0
        
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            if frame_idx % skip_frames == 0:
                # 提取波前位置
                positions = extract_wave_positions_from_frame(frame)
                
                if positions:
                    # 采样（避免数据量过大）
                    if len(positions) > 100:
                        indices = np.random.choice(len(positions), 100, replace=False)
                        positions = [positions[i] for i in indices]
                    
                    time_s = frame_idx / fps
                    
                    for px, py in positions:
                        # 像素 → 物理坐标
                        X_cm, Y_cm = pixel_to_physical(
                            px, py, width, height, 
                            physical_width, physical_height)
                        
                        # 折射校正
                        x_cm, y_cm = refraction_correct(
                            X_cm, Y_cm, xc, yc, H, h, n)
                        
                        displacement = np.sqrt((x_cm-X_cm)**2 + (y_cm-Y_cm)**2) * 10
                        
                        writer.writerow([
                            frame_idx, 
                            f"{time_s:.4f}",
                            f"{X_cm:.4f}", f"{Y_cm:.4f}",
                            f"{x_cm:.4f}", f"{y_cm:.4f}",
                            f"{displacement:.4f}"
                        ])
                
                processed += 1
                if processed % 50 == 0:
                    print(f"  已处理 {processed} 帧 / {total_frames // skip_frames} 帧")
            
            frame_idx += 1
        
        cap.release()
    
    print(f"\n✓ 数据已保存至: {output_path}")
    print(f"  共处理 {processed} 帧")


def demo_without_video():
    """无视频时的模拟演示"""
    
    print("\n" + "=" * 50)
    print("  模拟数据演示（无实际视频）")
    print("=" * 50)
    
    # 模拟参数
    H = 30.0
    h = 10.0
    n = 1.33
    xc, yc = 0, 0
    
    # 模拟波纹扩散：圆形波从中心向外扩散
    print("\n模拟圆形波扩散（10帧）：")
    print("-" * 50)
    
    frames_data = []
    for frame_idx in range(10):
        t = frame_idx * 0.033  # 30fps
        radius = 2 + t * 15   # 波前半径随时间增大 (cm)
        
        # 沿圆周取点
        angles = np.linspace(0, 2*np.pi, 36, endpoint=False)
        X_obs = (radius * np.cos(angles)).tolist()
        Y_obs = (radius * np.sin(angles)).tolist()
        
        frames_data.append({
            "frame": frame_idx,
            "X": X_obs,
            "Y": Y_obs
        })
    
    # 批量校正
    corrected = batch_correct_frames(frames_data, xc, yc, H, h, n)
    
    for frame in corrected[:3]:  # 只打印前3帧
        avg_obs_r = np.mean(np.sqrt(
            np.array(frame["original_X"])**2 + 
            np.array(frame["original_Y"])**2))
        avg_real_r = np.mean(np.sqrt(
            np.array(frame["x"])**2 + 
            np.array(frame["y"])**2))
        
        print(f"帧{frame['frame']:2d}: 观测半径={avg_obs_r:.2f}cm → "
              f"真实半径={avg_real_r:.2f}cm "
              f"(偏差={avg_real_r-avg_obs_r:.2f}cm)")
    
    print("  ...")
    print(f"  共校正 {len(corrected)} 帧数据")
    
    # 保存模拟数据
    output_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        'simulated_corrected_data.csv')
    
    with open(output_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['帧号', '观测X(cm)', '观测Y(cm)', 
                        '真实x(cm)', '真实y(cm)', '偏差(mm)'])
        
        for frame in corrected:
            for i in range(len(frame["x"])):
                X_i = frame["original_X"][i]
                Y_i = frame["original_Y"][i]
                x_i = frame["x"][i]
                y_i = frame["y"][i]
                disp = np.sqrt((x_i-X_i)**2 + (y_i-Y_i)**2) * 10
                writer.writerow([
                    frame["frame"],
                    f"{X_i:.4f}", f"{Y_i:.4f}",
                    f"{x_i:.4f}", f"{y_i:.4f}",
                    f"{disp:.4f}"
                ])
    
    print(f"\n[OK] 模拟数据已保存至: {output_path}")


# ========================== 主程序 ==========================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='水波实验视频处理与折射校正')
    parser.add_argument('--video', type=str, default=None,
                       help='实验视频文件路径')
    parser.add_argument('--H', type=float, default=30.0,
                       help='相机高度 (cm)')
    parser.add_argument('--h', type=float, default=10.0,
                       help='水深 (cm)')
    parser.add_argument('--n', type=float, default=1.33,
                       help='水的折射率')
    parser.add_argument('--width', type=float, default=40.0,
                       help='水槽可见区域宽度 (cm)')
    parser.add_argument('--height', type=float, default=30.0,
                       help='水槽可见区域高度 (cm)')
    parser.add_argument('--skip', type=int, default=1,
                       help='跳帧数')
    parser.add_argument('--demo', action='store_true',
                       help='使用模拟数据演示')
    
    args = parser.parse_args()
    
    if args.video:
        process_video(args.video, args.H, args.h, args.n,
                     args.width, args.height, skip_frames=args.skip)
    else:
        print("未指定视频文件，运行模拟演示...")
        demo_without_video()
