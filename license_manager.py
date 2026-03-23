"""
Prompt Writer - License Manager
简单的许可证管理系统
"""
import hashlib
import json
import os
import uuid
from datetime import datetime, timedelta


class LicenseManager:
    """许可证管理器"""

    def __init__(self):
        # 许可证文件存储在用户目录
        self.license_file = os.path.expanduser('~/.prompt_writer/license.json')
        self.machine_id = self._get_machine_id()

    def _get_machine_id(self):
        """获取机器唯一标识"""
        # 使用 MAC 地址的哈希作为机器 ID
        try:
            mac = uuid.getnode()
            return hashlib.sha256(str(mac).encode()).hexdigest()[:16]
        except:
            # 备用方案：生成随机 ID 并存储
            fallback_file = os.path.expanduser('~/.prompt_writer/machine_id')
            if os.path.exists(fallback_file):
                with open(fallback_file, 'r') as f:
                    return f.read().strip()
            else:
                new_id = hashlib.sha256(str(datetime.now()).encode()).hexdigest()[:16]
                os.makedirs(os.path.dirname(fallback_file), exist_ok=True)
                with open(fallback_file, 'w') as f:
                    f.write(new_id)
                return new_id

    def _generate_license_key(self, email, machine_id):
        """生成许可证密钥（用于验证）"""
        data = f"{email}:{machine_id}:PROMPT_WRITER_V1"
        return hashlib.sha256(data.encode()).hexdigest().upper()[:24]

    def validate_license(self, license_key, email):
        """验证许可证"""
        expected = self._generate_license_key(email, self.machine_id)
        return license_key == expected

    def save_license(self, license_key, email):
        """保存许可证到本地"""
        os.makedirs(os.path.dirname(self.license_file), exist_ok=True)
        data = {
            'license_key': license_key,
            'email': email,
            'machine_id': self.machine_id,
            'activated_at': datetime.now().isoformat(),
        }
        with open(self.license_file, 'w') as f:
            json.dump(data, f)

    def load_license(self):
        """加载本地许可证"""
        if not os.path.exists(self.license_file):
            return None
        try:
            with open(self.license_file, 'r') as f:
                return json.load(f)
        except:
            return None

    def check_license(self):
        """检查许可证状态"""
        license_data = self.load_license()

        if not license_data:
            return {'valid': False, 'message': '未找到许可证'}

        # 检查机器 ID 是否匹配
        if license_data.get('machine_id') != self.machine_id:
            return {'valid': False, 'message': '许可证与当前设备不匹配'}

        # 验证密钥
        if not self.validate_license(license_data['license_key'], license_data['email']):
            return {'valid': False, 'message': '许可证无效'}

        return {
            'valid': True,
            'message': '许可证有效',
            'email': license_data['email'],
            'activated_at': license_data['activated_at']
        }

    def generate_trial_license(self):
        """生成试用许可证（7天）"""
        trial_email = f"trial@{self.machine_id}.local"
        trial_key = self._generate_license_key(trial_email, self.machine_id)

        os.makedirs(os.path.dirname(self.license_file), exist_ok=True)
        data = {
            'license_key': trial_key,
            'email': trial_email,
            'machine_id': self.machine_id,
            'activated_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(days=7)).isoformat(),
            'type': 'trial'
        }
        with open(self.license_file, 'w') as f:
            json.dump(data, f)

        return trial_key, trial_email


def create_license_page():
    """创建许可证页面 HTML"""
    return '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>Prompt Writer - 激活</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #0d0d0f;
            color: #f0f0f5;
            height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            width: 400px;
            padding: 40px;
            background: #16161a;
            border-radius: 16px;
            border: 1px solid #2a2a35;
        }
        .logo {
            text-align: center;
            margin-bottom: 32px;
        }
        .logo-icon {
            width: 64px;
            height: 64px;
            background: #6366f1;
            border-radius: 16px;
            margin: 0 auto 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            font-weight: bold;
        }
        h1 {
            font-size: 24px;
            margin-bottom: 8px;
        }
        p {
            color: #9ca3af;
            font-size: 14px;
            margin-bottom: 24px;
        }
        .form-group {
            margin-bottom: 16px;
        }
        label {
            display: block;
            font-size: 13px;
            color: #9ca3af;
            margin-bottom: 6px;
        }
        input {
            width: 100%;
            padding: 12px 16px;
            background: #1e1e24;
            border: 1px solid #2a2a35;
            border-radius: 10px;
            color: #f0f0f5;
            font-size: 14px;
            outline: none;
        }
        input:focus {
            border-color: #6366f1;
        }
        button {
            width: 100%;
            padding: 14px;
            background: #6366f1;
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 15px;
            font-weight: 500;
            cursor: pointer;
            margin-top: 8px;
        }
        button:hover {
            background: #4f46e5;
        }
        .trial-btn {
            background: transparent;
            border: 1px solid #6366f1;
            margin-top: 12px;
        }
        .trial-btn:hover {
            background: #6366f1;
        }
        .machine-id {
            font-family: monospace;
            font-size: 11px;
            color: #6b7280;
            text-align: center;
            margin-top: 24px;
            padding-top: 24px;
            border-top: 1px solid #2a2a35;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">
            <div class="logo-icon">P</div>
            <h1>激活 Prompt Writer</h1>
            <p>请输入您的许可证密钥</p>
        </div>
        <form id="licenseForm">
            <div class="form-group">
                <label>邮箱</label>
                <input type="email" id="email" placeholder="your@email.com" required>
            </div>
            <div class="form-group">
                <label>许可证密钥</label>
                <input type="text" id="licenseKey" placeholder="XXXX-XXXX-XXXX-XXXX" required>
            </div>
            <button type="submit">激活</button>
        </form>
        <button class="trial-btn" onclick="startTrial()">开始 7 天免费试用</button>
        <div class="machine-id">设备 ID: <span id="machineId"></span></div>
    </div>

    <script>
        document.getElementById('machineId').textContent = 'LOADING...';

        document.getElementById('licenseForm').addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('email').value;
            const key = document.getElementById('licenseKey').value;

            fetch('/activate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({email, license_key: key})
            })
            .then(r => r.json())
            .then(data => {
                if (data.success) {
                    alert('激活成功！');
                    window.location.href = '/';
                } else {
                    alert('激活失败: ' + data.message);
                }
            });
        });

        function startTrial() {
            fetch('/activate_trial', {method: 'POST'})
                .then(r => r.json())
                .then(data => {
                    if (data.success) {
                        alert('试用已启动！');
                        window.location.href = '/';
                    }
                });
        }
    </script>
</body>
</html>
'''


if __name__ == '__main__':
    # 测试：生成示例许可证
    lm = LicenseManager()
    test_email = "user@example.com"
    test_key = lm._generate_license_key(test_email, lm.machine_id)
    print(f"测试许可证信息:")
    print(f"  邮箱: {test_email}")
    print(f"  机器ID: {lm.machine_id}")
    print(f"  许可证密钥: {test_key}")
