# GitHub Actions 自动打包配置指南

## 文件说明

| 文件 | 作用 |
|------|------|
| `.github/workflows/build.yml` | GitHub Actions 工作流配置 |
| `prompt_writer_windows.spec` | Windows 打包配置 |
| `prompt_writer.spec` | macOS 打包配置 |

## 使用方法

### 1. 推送到 GitHub

```bash
# 在项目目录初始化 git（如果还没做）
git init
git add .
git commit -m "Initial commit with GitHub Actions"

# 创建 GitHub 仓库并推送
git remote add origin https://github.com/YOUR_USERNAME/prompt-writer.git
git push -u origin main
```

### 2. 触发自动打包

#### 方式一：推送标签（推荐）
```bash
# 创建版本标签
git tag v1.0.0

# 推送标签（触发 GitHub Actions）
git push origin v1.0.0
```

#### 方式二：手动触发
1. 访问 GitHub 仓库
2. 点击 "Actions" 标签
3. 选择 "Build Prompt Writer" 工作流
4. 点击 "Run workflow"

### 3. 下载构建结果

打包完成后，可以在以下位置下载：
- **GitHub Actions 页面** → Artifacts
- **GitHub Releases** 页面（如果推送了标签）

## 自动发布到 Releases

推送以 `v` 开头的标签时，会自动：
1. 在 macOS 上构建 `.app`
2. 在 Windows 上构建 `.exe`
3. 打包成 zip 文件
4. 创建 GitHub Release
5. 上传两个平台的安装包

## 示例发布流程

```bash
# 1. 修改版本号（编辑 main.py 或版本文件）
# 2. 提交更改
git add .
git commit -m "Bump version to v1.0.0"

# 3. 创建标签并推送
git tag v1.0.0
git push origin main
git push origin v1.0.0

# 4. 等待 GitHub Actions 完成（约 5-10 分钟）
# 5. 访问 GitHub Releases 页面下载
```

## 注意事项

1. **GitHub 仓库必须是 Public** 或者你有付费的 Private 仓库才能使用 Actions
2. **首次运行可能需要授权** 访问 Actions
3. **构建时间**：macOS 约 3-5 分钟，Windows 约 5-8 分钟

## 故障排除

### Actions 没有触发
- 检查文件是否在 `.github/workflows/` 目录
- 检查 YAML 语法是否正确
- 确认推送到了正确的分支

### 构建失败
- 查看 Actions 日志获取详细错误
- 检查依赖是否安装完整
- 确认 icon 文件存在

## 自定义配置

修改 `.github/workflows/build.yml`：
- 修改 Python 版本：`python-version: ['3.12']`
- 添加更多平台：`os: [macos-latest, windows-latest, ubuntu-latest]`
- 修改触发条件：`on: push: branches: [main]`
