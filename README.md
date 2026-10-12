# TK Viral Toolkit

TikTok 爆款视频拆解工具包：一键下载 → 语音转写 → 结构化拆解脚手架。

A CLI toolkit for breaking down viral TikTok videos: download → transcribe → structured analysis scaffold.

## 为什么做这个

刷到爆款只看热闹没用，得拆出可复用的套路。这套工具把"下载原片 → 转写口播 → 四层深拆"做成一条命令，拆解完直接得到 Markdown 笔记。

## 安装

```bash
pip install -r requirements.txt
# 还需要系统装好 ffmpeg 和 yt-dlp
```

## 用法

```bash
# 完整流程：下载 + 转写 + 生成拆解脚手架
python -m tkv.cli process "https://www.tiktok.com/@user/video/1234567890" -o ./output --author user

# 跳过转写（只要下载）
python -m tkv.cli process "https://www.tiktok.com/@user/video/1234567890" --skip-transcribe

# 经代理下载
python -m tkv.cli process "https://www.tiktok.com/@user/video/1234567890" --proxy http://127.0.0.1:8080
```

跑完得到三个文件：
- `*_xxxx.mp4` — 原片
- `*.transcript.json` — 口播转写（含时间轴）
- `*.breakdown.md` — 拆解笔记脚手架（四层 + 五件套，填空即可）

## 拆解框架

**四层深拆**：画面（第一帧/运镜/字幕/转场）→ 声音（逐句转写/语气/BGM/音效）→ 话术（每句作用+用词技巧）→ 节奏（时间轴/卡点）

**五件套**：前3秒钩子 / 卖点证明链 / 可复用套路（含适用品类）/ 逆向提示词 / 2.0提示词（换产品直接套用）

## License

MIT
