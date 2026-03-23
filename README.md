# Prompt Writer - 完整使用与发布指南

## 📦 Windows 用户使用方式

### 方式一：直接运行（适合开发者）

```bash
# 1. 安装 Python 3.10+（勾选 Add to PATH）
# 下载地址：https://python.org

# 2. 下载项目
git clone https://github.com/couragedabaofa/prompt-writer.git
cd prompt-writer

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行
python app.py
# 浏览器自动打开 http://localhost:8080
```

### 方式二：使用打包好的 EXE（适合普通用户）

1. 前往 GitHub Releases 页面：
   `https://github.com/couragedabaofa/prompt-writer/releases`

2. 下载 `Prompt-Writer-Windows.zip`

3. 解压后双击 `Prompt Writer.exe` 运行

---

## 🔄 GitHub 版本迭代流程

### 第 1 步：本地开发

```bash
# 确保代码能正常运行
python app.py

# 测试所有功能正常
# - 卡片网格展示
# - 标签筛选/新增/删除
# - 提示词编辑/自动保存
# - 导入/导出
```

### 第 2 步：提交代码

```bash
# 查看修改
git status

# 添加修改
git add .

# 提交（使用规范格式）
git commit -m "feat: 添加自动保存功能"

# 推送
git push origin main
```

### 第 3 步：发布新版本

```bash
# 创建版本标签（例如 v1.1.0）
git tag v1.1.0

# 推送标签（这会触发 GitHub Actions 自动构建）
git push origin v1.1.0
```

### 第 4 步：等待构建完成

约 5-10 分钟后，GitHub Actions 会自动：
- ✅ 构建 Windows 版本
- ✅ 构建 macOS 版本
- ✅ 创建 GitHub Release
- ✅ 上传安装包

### 第 5 步：下载发布版本

访问：
```
https://github.com/couragedabaofa/prompt-writer/releases
```

下载对应系统的安装包。

---

## 📝 版本号规范

| 格式 | 说明 | 示例 |
|------|------|------|
| v2.0.0 | 重大更新 | 重构架构、不兼容旧版 |
| v1.1.0 | 新增功能 | 添加自动保存、标签管理 |
| v1.0.1 | Bug修复 | 修复保存失败问题 |

---

## 🐛 常见问题

### Windows 运行问题

**Q: 提示 "python" 不是内部命令**
- 安装 Python 时未勾选 Add to PATH
- 重新安装 Python 并勾选

**Q: 端口被占用**
- 修改 `app.py` 最后一行：`port=8081`

**Q: 防火墙拦截**
- 点击「允许访问」即可

### GitHub 构建问题

**Q: Actions 构建失败**
- 查看日志：GitHub → Actions → 选择失败的任务
- 常见原因：依赖版本不兼容

**Q: 推送标签后没有触发构建**
- 标签格式必须是 `v1.0.0`（带 v 前缀）

---

## 📚 相关文档

| 文档 | 说明 |
|------|------|
| `README_WINDOWS.md` | Windows 详细安装指南 |
| `RELEASE_GUIDE.md` | 版本发布完整指南 |
| `README_BUILD.md` | 打包构建指南 |

---

## 🚀 快速发布（一键命令）

```bash
# 设置版本号
VERSION="v1.1.0"

# 提交代码
git add .
git commit -m "release: $VERSION"
git push origin main

# 打标签并推送（触发构建）
git tag $VERSION
git push origin $VERSION

echo "✅ 已触发 GitHub Actions 构建"
echo "⏳ 请等待 5-10 分钟"
echo "📥 下载地址：https://github.com/couragedabaofa/prompt-writer/releases"
```
