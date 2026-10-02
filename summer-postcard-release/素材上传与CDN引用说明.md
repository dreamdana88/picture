# 夏日像素明信片：素材上传与 CDN 引用

本次从当前成品 JSON 提取所有实际引用的素材，保留 Grok 已有修改，在此基础上修正控件覆盖和正文留白。22 个运行素材约 6.33 MB，另附像素字体许可文件。旧版草稿、未使用的原始 PNG 和重复背景不需要上传。

## 批量上传

1. 打开公开仓库 `dreamdana88/picture`，进入或建立 `summer-postcard/assets/`。
2. 将本地 `assets` 文件夹内全部 23 个文件上传到该目录并提交到 `main`。文件名保持不变；不要把文件再次套进一层 assets。
3. 先检查桌面背景、手机背景、图标及字体的 CDN 地址能正常返回。GitHub 上传网页地址不是图片直链。
4. 确认资源可访问后，在酒馆导入同目录的 `Dream-夏日像素明信片-CDN.json`。主题名称保持现有名称，检查选中的是新导入的版本。

CDN 前缀：

`https://cdn.jsdelivr.net/gh/dreamdana88/picture@main/summer-postcard/assets/`

例如：

`https://cdn.jsdelivr.net/gh/dreamdana88/picture@main/summer-postcard/assets/summer-desktop.webp`

```css
background-image: url("https://cdn.jsdelivr.net/gh/dreamdana88/picture@main/summer-postcard/assets/summer-desktop.webp");
```

`asset-manifest.json` 包含每个文件的完整地址、大小和 SHA-256。CDN JSON 已替换全部图片、SVG 与字体内嵌引用，没有残留 data URL。

## 素材清单

| 文件名 | 用途 | 字节数 |
|---|---|---:|
| `user-stamp.svg` | User 西瓜邮票 | 2,633 |
| `bot-stamp.svg` | AI 海鸥邮票 | 2,706 |
| `summer-desktop.webp` | 桌面夏日背景 | 1,748,478 |
| `toast-border.svg` | 提示框像素边框 | 201 |
| `control-edit.svg` | 原生操作按钮的像素图标：edit | 210 |
| `control-copy.svg` | 原生操作按钮的像素图标：copy | 188 |
| `control-delete.svg` | 原生操作按钮的像素图标：delete | 199 |
| `control-check.svg` | 原生操作按钮的像素图标：check | 205 |
| `control-close.svg` | 原生操作按钮的像素图标：close | 233 |
| `control-send.svg` | 原生操作按钮的像素图标：send | 195 |
| `control-stop.svg` | 原生操作按钮的像素图标：stop | 163 |
| `control-menu.svg` | 原生操作按钮的像素图标：menu | 186 |
| `control-more.svg` | 原生操作按钮的像素图标：more | 184 |
| `topbar-icons.png` | 顶栏图标及头像花朵使用的像素图集 | 821,380 |
| `fusion-pixel-12px-sc.woff2` | 姓名与楼层数据的中文像素字体 | 661,212 |
| `sailboat-postmark.png` | 帆船邮戳 | 546,941 |
| `hello-summer-signature.png` | Hello Summer 手写装饰 | 373,576 |
| `star.svg` | 姓名旁星星及滑杆控件 | 314 |
| `ice.svg` | 冰块滑杆控件 | 325 |
| `flower.svg` | 花朵滑杆控件 | 393 |
| `lemon.svg` | 柠檬滑杆控件 | 372 |
| `summer-mobile.webp` | 手机夏日背景 | 2,170,314 |
| `fusion-pixel-license.txt` | Fusion Pixel 字体的 SIL OFL 许可；请随字体上传 | 4,418 |

## 本次界面修改

- 移除任意 HTML button 的全局方框样式；原生控件样式限制到酒馆原生区域，插件弹窗、扩展设置和消息中的前端控件保留自己的样式。字段样式也同步收窄，避免插件输入框被覆盖。
- AI 和 User 正文：桌面左右外边距从 16px 降至 6px，左右内边距从 28px 降至 12px；手机分别从 8px 降至 4px、16px 降至 8px。保留格纹、蓝粉色和虚线框。
- 根目录原来的主题 JSON 同步包含界面修正，仍为内嵌版，上传素材前可继续使用。`before-fix.json` 是改动前的完整备份。

## 后续维护与验收

本次以当前成品为基准，新的可编辑源为 `theme.css` 和 `theme-settings.json`，素材在 `assets/`。执行 `python build.py` 会生成 CDN JSON 和根目录内嵌版；以后修改此处，不要用旧 v1.0 的构建脚本覆盖本次成品。

`verify.py` 对三种宽度的本地浏览器测试页面进行检查；这是控件隔离、间距和文件完整性检查，不是实际酒馆/插件验收。实际还需要在酒馆查看插件面板、状态栏/前端、AI/User 长文、390/430px 手机宽度。当前素材尚未上传，CDN 在线可用性没有通过验收。

## 外链的边界

你已选择 jsDelivr，以小文件与加载便利为主。公开资源仍可被另存和重新打包，外链不是防盗措施。jsDelivr 官方明确说明会永久存储首次访问的 GitHub 文件；删除仓库文件不能保证已有 CDN 链接失效。`@main` 同名更新也可能受缓存影响，明确更新时用新文件名并修改引用。

官方说明：https://github.com/jsdelivr/jsdelivr#github
