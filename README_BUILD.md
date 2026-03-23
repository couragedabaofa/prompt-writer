# Prompt Writer - 桌面版打包指南

## 环境准备

```bash
# 确保在虚拟环境中
cd "/Users/james/00Tool/Prompt MS"
source venv/bin/activate

# 安装依赖（已安装）
pip install pyinstaller waitress
```

## 打包步骤

### 1. 快速打包（测试用）

```bash
python build.py
```

### 2. 手动打包

```bash
# 清理旧构建
rm -rf build dist

# 执行打包
pyinstaller prompt_writer.spec --clean --noconfirm
```

### 3. 输出位置

- **macOS**: `dist/Prompt Writer.app`
- **Windows**: `dist/Prompt Writer/`

## 许可证系统

### 生成许可证

```bash
# 测试许可证生成
python license_manager.py
```

输出示例：
```
测试许可证信息:
  邮箱: user@example.com
  机器ID: A1B2C3D4E5F67890
  许可证密钥: 3A7B9C2D4E6F8A1B5C7D9E
```

### 许可证验证逻辑

1. 首次运行：显示激活页面
2. 试用模式：点击"7天免费试用"自动激活
3. 正式激活：输入邮箱 + 许可证密钥
4. 机器绑定：密钥与设备ID绑定

### 给客户生成许可证

在 Python 中：

```python
from license_manager import LicenseManager

lm = LicenseManager()
email = "customer@example.com"
key = lm._generate_license_key(email, "客户的机器ID")
print(f"许可证: {key}")
```

## 发布前检查

- [ ] 测试打包后的应用能正常启动
- [ ] 测试试用激活流程
- [ ] 测试正式激活流程
- [ ] 测试数据持久化（关闭后数据不丢失）
- [ ] 测试自动打开浏览器
- [ ] macOS: 检查是否被杀毒软件拦截

## 定价策略

| 版本 | 价格 | 功能 |
|------|------|------|
| 试用版 | 免费 | 7天全部功能 |
| 个人版 | ¥49 | 永久使用，单设备 |
| 专业版 | ¥99 | 永久使用，3台设备 |

## 销售渠道

1. **爱发电** (afdian.net) - 国内首选
2. **Gumroad** - 国际市场
3. **个人网站** - 独立域名

## 后续更新

### 自动更新（可选）

可考虑集成：`pyupdater` 或自定义更新检查

### 版本号管理

修改 `prompt_writer.spec` 中的：
```python
'CFBundleShortVersionString': '1.0.0',
'CFBundleVersion': '1.0.0',
```
