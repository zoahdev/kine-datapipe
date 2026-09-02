# KINE-DataPipe

An open, lightweight video preprocessing pipeline for world-model research: collection adapters, scene segmentation, motion filtering, event-candidate mining and pair construction.

> **Status:** engineering utility. Motion spikes are candidate events, not verified collisions, causal labels or proof that a model understands physics.

## Install

```bash
git clone https://github.com/kineworld/kine-datapipe.git
cd kine-datapipe
python -m pip install -r requirements.txt
```

`ffmpeg` must be available on `PATH`.

## Example

```bash
python -m kineworld_datapipe collect --query "robot arm pick and place" --max 20 --out data/raw
python -m kineworld_datapipe segment --in data/raw --out data/clips --min-len 2.0 --max-len 10.0
python -m kineworld_datapipe filter --in data/clips --out data/curated --min-motion 0.35
python -m kineworld_datapipe events --in data/curated --out data/events.json --z 3.0
```

Users are responsible for source-site terms, copyright, privacy and dataset licenses. The code's MIT license does not grant rights to downloaded media.

## Reproducibility

Public KineWorld experiments aim to record hardware, configuration, random seeds, upstream versions and known limitations. Current development is performed primarily on one RTX 5070 Ti laptop.

Website: [kineworld.com](https://kineworld.com)  
Evaluation: [KINE-Bench](https://github.com/kineworld/kine-bench)

## License

MIT for KineWorld-authored code.
