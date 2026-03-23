#!/usr/bin/env python3
"""
Prompt Writer 打包脚本
用法: python build.py
"""
import subprocess
import sys
import os
import shutil

def clean():
    """清理旧的构建文件"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for d in dirs_to_remove:
        if os.path.exists(d):
            shutil.rmtree(d)
            print(f"🗑️  清理 {d}/")

def create_icon():
    """创建简单图标（如果没有）"""
    import platform

    icon_file = 'icon.icns' if platform.system() == 'Darwin' else 'icon.ico'

    if os.path.exists(icon_file):
        return

    # 创建临时图标目录
    os.makedirs('icon.iconset', exist_ok=True)

    # 使用 ImageMagick 或 sips 生成图标（简化版，实际项目中需要设计图标）
    print(f"⚠️  请准备 {icon_file} 图标文件")
    print("   临时使用文本文件代替")

    # 创建一个空文件作为占位符
    with open(icon_file, 'w') as f:
        f.write('# placeholder')

def build():
    """执行打包"""
    print("🔨 开始打包 Prompt Writer...")
    print()

    # 清理
    clean()

    # 检查图标
    create_icon()

    # 执行 PyInstaller
    cmd = [
        sys.executable, '-m', 'PyInstaller',
        'prompt_writer.spec',
        '--clean',
        '--noconfirm',
    ]

    print("📦 运行 PyInstaller...")
    print(" ".join(cmd))
    print()

    result = subprocess.run(cmd, capture_output=False)

    if result.returncode == 0:
        print()
        print("✅ 打包成功！")
        print()

        # 显示输出路径
        import platform
        system = platform.system()

        if system == 'Darwin':
            app_path = 'dist/Prompt Writer.app'
            if os.path.exists(app_path):
                print(f"📱 macOS App: {os.path.abspath(app_path)}")
                print()
                print("使用方法:")
                print(f"  1. 双击运行: {app_path}")
                print("  2. 或将应用拖到 Applications 文件夹")
        else:
            exe_path = 'dist/Prompt Writer/Prompt Writer.exe'
            if os.path.exists('dist/Prompt Writer'):
                print(f"💾 Windows 可执行文件: {os.path.abspath('dist/Prompt Writer')}")

        print()
        print("⚠️  注意：首次运行可能需要允许系统安全权限")
    else:
        print()
        print("❌ 打包失败")
        sys.exit(1)

if __name__ == '__main__':
    build()
