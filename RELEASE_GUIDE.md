# GitHub 版本迭代指南

## 版本号规范

使用语义化版本号：`v主版本.次版本.修订号`

| 版本类型 | 示例 | 说明 |
|---------|------|------|
| 主版本 | v2.0.0 | 重大更新，不兼容旧版本 |
| 次版本 | v1.1.0 | 新增功能，兼容旧版本 |
| 修订号 | v1.0.1 | Bug 修复，小优化 |

---

## 迭代流程

### 1. 本地开发测试

```bash
# 1. 确保代码能正常运行
python app.py

# 2. 测试所有功能
# - 新建/编辑/删除提示词
# - 标签管理
# - 自动保存
# - 导入/导出

# 3. 测试打包（可选）
python build.py
```

### 2. 提交代码

```bash
# 添加所有修改
git add .

# 提交（使用规范提交信息）
git commit -m "feat: 添加自动保存功能"
git commit -m "fix: 修复标签删除bug"
git commit -m "refactor: 优化页面布局"

# 推送到 GitHub
git push origin main
```

**提交信息规范：**
- `feat:` 新功能
- `fix:` Bug 修复
- `docs:` 文档更新
- `style:` 代码格式
- `refactor:` 重构
- `test:` 测试
- `chore:` 构建/工具

### 3. 打版本标签（触发自动构建）

```bash
# 查看当前版本
git tag

# 创建新版本标签
git tag v1.1.0

# 推送标签到 GitHub（这会触发 GitHub Actions 自动构建）
git push origin v1.1.0
```

### 4. 下载构建产物

推送标签后，GitHub Actions 会自动：
1. 构建 Windows 版本
2. 构建 macOS 版本
3. 创建 GitHub Release
4. 上传安装包

约 5-10 分钟后，在 GitHub 页面下载：
- `https://github.com/couragedabaofa/prompt-writer/releases`

---

## 版本发布清单

发布前检查：

- [ ] 代码已提交到 main 分支
- [ ] 本地测试通过
- [ ] 版本号已确定
- [ ] 更新了 README.md（如有新功能）
- [ ] 打了标签并推送
- [ ] GitHub Actions 构建成功
- [ ] Release 页面已发布

---

## 常见问题

### 1. GitHub Actions 构建失败

查看构建日志：
```
GitHub → Actions → Build Prompt Writer → 查看失败任务
```

常见原因：
- 依赖版本不兼容
- PyInstaller 配置错误
- 图标文件缺失

### 2. 标签推送后没有触发构建

检查标签格式：`v1.0.0`（必须带 v 前缀）

### 3. 发布页面没有显示

需要 `git push origin v1.0.0` 推送标签，不是只 `git tag`

---

## 快速发布命令

```bash
# 一键发布新版本（替换 x.x.x 为版本号）
VERSION="v1.1.0"
git add .
git commit -m "release: $VERSION"
git push origin main
git tag $VERSION
git push origin $VERSION
echo "已触发 GitHub Actions 构建，请等待 5-10 分钟"
```
