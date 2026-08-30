# KINE-DataPipe 勘境世界模型数据管线

**KINE-DataPipe** is an open video data pipeline for world-model pretraining: download internet videos, split them into physical-event-rich clips, and filter for quality — reproducible on a single consumer GPU machine.

勘境开源数据管线：从互联网视频到世界模型预训练数据的自动化流水线——下载、切片、质量过滤，单台消费级主机可运行。

> 勘境相信：世界模型应该可以被任何人复现。这条管线是我们交付的第一块代码。
> KINEWORLD believes world models should be reproducible by anyone. This pipeline is our first public deliverable.

## Status 状态

- `v0.3.0` — event mining shipped: motion-spike detection surfaces collision/drop/toppling candidates
- Roadmap: dedup → caption hooks

## Install 安装

```bash
git clone https://github.com/zoahdev/kine-datapipe.git
cd kine-datapipe
pip install -r requirements.txt
# ffmpeg must be on PATH: https://ffmpeg.org/download.html
```

## Quick start 快速开始

```bash
# 1. Collect videos from a keyword search (uses yt-dlp)
python -m kineworld_datapipe collect --query "robot arm pick and place" --max 20 --out data/raw
# 网络不通 YouTube 时，用 B 站源（自动处理 cookie 与 UA）：
python -m kineworld_datapipe collect --query "机械臂 抓取" --max 20 --out data/raw --source bilibili

# 2. Split into clips at scene cuts
python -m kineworld_datapipe segment --in data/raw --out data/clips --min-len 2.0 --max-len 10.0

# 3. Filter out static/low-motion clips (keep physically interesting footage)
python -m kineworld_datapipe filter --in data/clips --out data/curated --min-motion 0.35

# 4. Mine physical-event candidates (motion spikes: collisions / drops / topplings)
python -m kineworld_datapipe events --in data/curated --out data/events.json --z 3.0
```

## Why this matters 为什么重要

World models for embodied AI are starved of interaction data. Teleoperated robot data costs orders of magnitude more than internet video. This pipeline turns free video into structured pretraining material:

具身智能的世界模型面临"数据荒"：真实机器人遥操作数据的采集成本比互联网视频高出数个数量级。这条管线的目标是把免费视频转化为结构化的预训练数据。

```
internet video → scene clips → motion-filtered clips → physical-event mining → world-model pretraining
```

## Reproducibility promise 可复现承诺

Every public experiment from KINEWORLD will state hardware (we develop on a single RTX 5070 Ti laptop) and random seeds, with configs committed to this repo.

勘境所有公开实验都会注明硬件（我们的开发机是单张 RTX 5070 Ti 的笔记本）与随机种子，配置文件随仓库提交。

## License

MIT — see [LICENSE](LICENSE). Commercial use welcome; attribution appreciated.

## Links

- Website: https://kineworld.com
- 勘境 · 具身智能世界模型 · 合肥
