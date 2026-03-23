#!/usr/bin/env python3
"""创建应用图标"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建 1024x1024 的图标（macOS 推荐尺寸）
    size = 1024
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 绘制圆角矩形背景
    bg_color = (99, 102, 241)  # #6366f1 - 主题色
    corner_radius = 200

    # 绘制圆角矩形
    draw.rounded_rectangle(
        [(0, 0), (size, size)],
        radius=corner_radius,
        fill=bg_color
    )

    # 绘制文字 "P"
    try:
        # 尝试使用系统字体
        font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 600)
    except:
        font = ImageFont.load_default()

    text = "P"
    # 获取文字尺寸（PIL 不同版本兼容）
    try:
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
    except:
        text_width, text_height = 400, 400

    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 50

    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)

    # 保存为 PNG
    img.save('icon.png')
    print("✅ 已生成 icon.png")

    # 为 macOS 创建 .icns（需要多个尺寸）
    os.makedirs('icon.iconset', exist_ok=True)

    sizes = [16, 32, 64, 128, 256, 512, 1024]
    for s in sizes:
        resized = img.resize((s, s), Image.LANCZOS)
        resized.save(f'icon.iconset/icon_{s}x{s}.png')
        if s <= 512:
            resized2x = img.resize((s*2, s*2), Image.LANCZOS)
            resized2x.save(f'icon.iconset/icon_{s}x{s}@2x.png')

    print("✅ 已生成 icon.iconset/")

    # 使用 iconutil 生成 .icns（仅 macOS）
    import platform
    if platform.system() == 'Darwin':
        os.system('iconutil -c icns icon.iconset -o icon.icns')
        print("✅ 已生成 icon.icns")
        # 清理临时文件
        import shutil
        shutil.rmtree('icon.iconset')
        os.remove('icon.png')
    else:
        # Windows 使用 .ico
        img.save('icon.ico', format='ICO', sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)])
        print("✅ 已生成 icon.ico")

if __name__ == '__main__':
    create_icon()
