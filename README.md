# 软软’s Blog · Modern refresh

在现有 GitHub Pages 静态博客上进行的展示层翻新。借鉴参考站的卡片、侧栏和清爽阅读体验，不复制对方主题或文章；不迁移到 Astro，也不依赖 Hexo 源项目。

## 这版做了什么
- 蓝紫色、留白充足的双栏布局，移动端单栏和折叠菜单。
- 主题切换、浏览器本地记忆；键盘 `/` 打开本地全文搜索。
- 首页摘要卡片、文章归档、分类/标签、文章目录、阅读时间。
- 原有 19 篇文章正文、标题锚点、76 个页面路径保持不变。
- 保留 `CNAME` 中的 `blog.rmbgame.net`，未擅自改为 `rmbgame.net`。
- 用可配置的 giscus 替代旧 Disqus 页面嵌入，**尚未启用**。
- 不再加载旧页面中的百度/腾讯统计、Disqus、动画库。旧资产仍保留，便于回溯。

## 内容与构建
仓库原来只有 Hexo 已生成 HTML，没有 Markdown 源码。`content/site.json` 保存了从原站提取的文章 HTML、元数据、关于页和路由。这不是原始 Markdown 的恢复。

```bash
python3 scripts/build.py
python3 -m http.server 8080
# 打开 http://localhost:8080
```

构建仅需 Python 3.12+ 标准库，无生产依赖。根目录 HTML 是生成产物。后续修改正文或元数据应改 `content/site.json`，布局改 `scripts/build.py`，样式和交互改 `assets/`，然后重新生成。

添加文章：在 `posts` 中添加相同结构的记录，并在 `routes` 添加 `{ "url": "/你的路径/", "kind": "post" }`。文章 URL 必须以 `/` 开头和结尾，`html` 使用可信的作者内容而非访客输入。更新首页分页需在 `routes` 为新增页添加 `home` 记录。本次没有改变写作工具链；长期高频写作建议另行恢复 Markdown 源项目。

## 启用 GitHub 留言
目前仓库 Discussions 关闭，也未确认安装 giscus 应用。请在明确决定后进行以下操作：

1. 在 GitHub 仓库设置中开启 Discussions。
2. 在 https://github.com/apps/giscus 安装应用，范围仅选该博客仓库。
3. 创建合适的 Discussion 分类，推荐 Announcements 类型；在 https://giscus.app/ 获取真实 `repoId` 和 `categoryId`。
4. 修改 `assets/comments.json` 的 ID、分类名称，并将 `enabled` 设为 `true`。
5. 发布后登录 GitHub 留言实测。**代码中不应保存令牌、client secret 或密码。**

留言采用 pathname 严格映射，每篇原有 URL 继续作为识别键，支持浅色/深色同步。只有文章页和关于页加载配置。未启用时展示提示，不伪造留言内容。giscus 客户端从第三方加载，评论者需通过 GitHub 授权。旧 Disqus 评论未迁移、未删除远端数据。

## 校验
```bash
python3 -m unittest discover -s tests -v
node --check assets/app.js
node --check assets/theme.js
npm install --ignore-scripts
npm test
```

Python 验证路由、内容、域名和本地链接；Node/jsdom 验证主题、菜单、搜索、目录和留言配置。实际 Chrome/移动端视觉验收与上线后 GitHub 留言测试仍需进行。本次云环境禁止浏览器所需的 socket，不能声称已完成真实浏览器截图验证。

## 发布与回滚
改版提交在独立审核分支，尚未合并、未发布，也未更改 GitHub 权限。请先本地预览后审核 diff，再按仓库现有 GitHub Pages 方式发布根目录静态文件。无需引入新的构建平台。实际 Pages 发布来源未从账号设置中核实，请保留现有设置；不擅自改 DNS/CNAME。

旧内容有历史 `http://rmbgame.net/wp-content/uploads/...` 外链图片。原链接保留，是否仍可访问未全部核验。历史文章与旧关于页已标注时效性，避免把当年的工作地点或软件版本当成当前信息。

回滚可还原到改版前提交 `f3c6aa594d9974a6555ba3a8605aa8ee1b723f98`。这是基于该提交的独立改版分支，不应覆盖用户后续独立提交。
