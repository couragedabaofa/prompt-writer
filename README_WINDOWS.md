# Prompt Writer - Windows 使用指南

## 方式一：直接运行（开发模式）

### 1. 安装 Python
- 下载并安装 Python 3.10+：[https://python.org](https://python.org)
- **重要**：安装时勾选「Add Python to PATH」

### 2. 下载项目
```bash
# 使用 git 克隆
git clone https://github.com/couragedabaofa/prompt-writer.git
cd prompt-writer

# 或者直接下载 ZIP 解压
```

### 3. 安装依赖
```bash
# 创建虚拟环境（推荐）
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install flask flask-sqlalchemy
```

### 4. 运行应用
```bash
python app.py
```

浏览器会自动打开 http://localhost:8080

---

## 方式二：打包为 EXE（推荐分发）

### 1. 安装 PyInstaller
```bash
pip install pyinstaller
```

### 2. 打包
```bash
# 使用 Windows 配置文件打包
pyinstaller prompt_writer_windows.spec --clean --noconfirm

# 或一键打包
python build.py
```

### 3. 输出位置
打包完成后，可执行文件在：
```
dist\Prompt Writer\Prompt Writer.exe
```

### 4. 分发
将整个 `dist\Prompt Writer` 文件夹压缩为 ZIP，即可分发给其他 Windows 用户使用。

---

## 数据存储位置

SQLite 数据库默认保存在：
- Windows: `%APPDATA%\prompt_writer\prompts.db`
- 也可放在程序同目录下（修改 `app.py` 中的数据库路径）

---

## 常见问题

### 1. 端口被占用
修改 `app.py` 最后一行：
```python
app.run(debug=True, host='0.0.0.0', port=8081)  # 改为其他端口
```

### 2. 防火墙拦截
首次运行时 Windows 防火墙可能拦截，点击「允许访问」即可。

### 3. 中文显示乱码
确保系统已安装中文字体，或在浏览器中设置编码为 UTF-8。

---

## 许可证激活

首次运行需要激活：
1. **试用**：点击「7天免费试用」
2. **正式版**：输入邮箱 + 许可证密钥

如需购买许可证，请联系开发者。
