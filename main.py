"""
Prompt Writer - Desktop Application Entry Point
打包后的桌面应用入口
"""
import webbrowser
import threading
import time
import os
import sys
from flask import Flask, request, jsonify
from app import app, db, Tag, Prompt

# License manager
from license_manager import LicenseManager, create_license_page

# Global license manager instance
license_mgr = LicenseManager()


def get_resource_path(relative_path):
    """获取资源路径（支持打包后的路径）"""
    if hasattr(sys, '_MEIPASS'):
        # PyInstaller 打包后的临时目录
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath('.'), relative_path)


def init_app():
    """初始化应用数据和数据库"""
    with app.app_context():
        db.create_all()

        # 初始化标签（如果不存在）
        default_tags = [
            {'name': '公文写作', 'color': '#4CAF50'},
            {'name': '邮件沟通', 'color': '#2196F3'},
            {'name': '创意文案', 'color': '#FF9800'},
            {'name': '编辑润色', 'color': '#9C27B0'},
            {'name': '会议效率', 'color': '#00BCD4'},
            {'name': '社媒运营', 'color': '#E91E63'},
            {'name': '报告分析', 'color': '#3F51B5'},
            {'name': '求职简历', 'color': '#FF5722'},
            {'name': '翻译双语', 'color': '#607D8B'},
            {'name': '知识整理', 'color': '#8BC34A'},
        ]

        for tag_data in default_tags:
            if not Tag.query.filter_by(name=tag_data['name']).first():
                tag = Tag(name=tag_data['name'], color=tag_data['color'])
                db.session.add(tag)

        db.session.commit()


# License check decorator
def require_license(f):
    """验证许可证的装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        result = license_mgr.check_license()
        if not result['valid']:
            # Return license page HTML
            return create_license_page()
        return f(*args, **kwargs)
    return decorated_function


# Add license routes to app
@app.route('/activate', methods=['POST'])
def activate():
    """激活许可证"""
    data = request.get_json()
    email = data.get('email')
    license_key = data.get('license_key')

    if license_mgr.validate_license(license_key, email):
        license_mgr.save_license(license_key, email)
        return jsonify({'success': True, 'message': '激活成功'})
    else:
        return jsonify({'success': False, 'message': '许可证无效'})


@app.route('/activate_trial', methods=['POST'])
def activate_trial():
    """激活试用"""
    try:
        license_mgr.generate_trial_license()
        return jsonify({'success': True, 'message': '试用已启动'})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


def open_browser():
    """延迟打开浏览器"""
    time.sleep(1.5)
    webbrowser.open('http://127.0.0.1:8080')


def main():
    """主函数"""
    print("=" * 50)
    print("🚀 Prompt Writer 启动中...")
    print(f"📁 当前工作目录: {os.getcwd()}")
    print(f"🏠 用户目录: {os.path.expanduser('~')}")
    print("=" * 50)

    # 初始化数据
    init_app()

    # 检查许可证状态
    license_result = license_mgr.check_license()
    if license_result['valid']:
        print(f"✅ 许可证状态: {license_result['message']}")
        print(f"📧 用户: {license_result['email']}")
    else:
        print(f"⚠️  {license_result['message']}")
        print("📝 请先在浏览器中完成激活")

    # 在后台线程打开浏览器
    threading.Thread(target=open_browser, daemon=True).start()

    # 启动 Flask（ production 模式）
    print("🚀 Prompt Writer 启动中...")
    print("📝 浏览器将自动打开 http://127.0.0.1:8080")
    print("⚠️  关闭此窗口将停止服务")

    # 使用 waitress 或 werkzeug 生产服务器
    try:
        from waitress import serve
        serve(app, host='127.0.0.1', port=8080)
    except ImportError:
        # 如果没有 waitress，使用 Flask 内置（仅开发）
        app.run(host='127.0.0.1', port=8080, debug=False, threaded=True)


if __name__ == '__main__':
    main()
