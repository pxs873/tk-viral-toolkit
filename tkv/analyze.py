"""Breakdown framework - 4-layer deep analysis + 5-piece reusable set.

四层深拆：画面 / 声音 / 话术 / 节奏
五件套：前3秒钩子 / 卖点证明链 / 可复用套路 / 逆向提示词 / 2.0提示词
"""

import json
from pathlib import Path
from datetime import datetime

FOUR_LAYERS = {
    "visual": "画面层：第一帧 / 运镜 / 字幕样式 / 转场",
    "audio": "声音层：逐句转写 / 语气 / BGM / 音效",
    "script": "话术层：每句话的作用 + 用词技巧",
    "rhythm": "节奏层：时间轴 / 卡点 / 时长分配",
}

FIVE_PIECES = {
    "hook": "前3秒钩子：类型 + 原文 + 为什么有效",
    "proof_chain": "卖点证明链：每个卖点对应的证明动作",
    "pattern": "可复用套路：命名 + 适用品类",
    "reverse_prompt": "逆向提示词：还原这条视频的生成指令",
    "v2_prompt": "2.0提示词：换产品可直接套用的版本",
}


def new_breakdown(video_id: str, author: str, video_path: str | Path,
                  transcript: list[dict] | None = None) -> dict:
    """Create a blank breakdown scaffold for a video."""
    return {
        "meta": {
            "video_id": video_id,
            "author": author,
            "video_file": str(video_path),
            "created_at": datetime.now().isoformat(timespec="seconds"),
            "toolkit_version": "0.1.0",
        },
        "transcript": transcript or [],
        "layers": {k: {"notes": "", "checklist": v} for k, v in FOUR_LAYERS.items()},
        "five_pieces": {k: {"notes": "", "guide": v} for k, v in FIVE_PIECES.items()},
    }


def save_breakdown(breakdown: dict, out_path: str | Path) -> Path:
    out_path = Path(out_path)
    out_path.write_text(json.dumps(breakdown, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    return out_path


def render_markdown(breakdown: dict) -> str:
    """Render breakdown as Markdown for review."""
    m = breakdown["meta"]
    lines = [
        f"## @{m['author']} · {m['video_id']}",
        "",
        f"- 视频文件：`{m['video_file']}`",
        f"- 拆解时间：{m['created_at']}",
        "",
        "### 四层深拆",
        "",
    ]
    for key, layer in breakdown["layers"].items():
        lines += [f"#### {key}", f"> {layer['checklist']}", "", layer["notes"] or "_待填写_", ""]
    lines += ["### 五件套", ""]
    for key, piece in breakdown["five_pieces"].items():
        lines += [f"#### {key}", f"> {piece['guide']}", "", piece["notes"] or "_待填写_", ""]
    if breakdown.get("transcript"):
        lines += ["### 口播转写", ""]
        for seg in breakdown["transcript"]:
            lines.append(f"- [{seg['start']:.1f}s] {seg['text']}")
    return "\n".join(lines)
