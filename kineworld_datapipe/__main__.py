import argparse
import sys


def main() -> None:
    parser = argparse.ArgumentParser(prog="kineworld_datapipe", description="KINE-DataPipe CLI")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_collect = sub.add_parser("collect", help="download videos by keyword search")
    p_collect.add_argument("--query", required=True)
    p_collect.add_argument("--max", type=int, default=10)
    p_collect.add_argument("--out", required=True)
    p_collect.add_argument("--source", choices=["youtube", "bilibili"], default="youtube")

    p_segment = sub.add_parser("segment", help="split videos into scene clips")
    p_segment.add_argument("--in", dest="inp", required=True)
    p_segment.add_argument("--out", required=True)
    p_segment.add_argument("--min-len", type=float, default=2.0)
    p_segment.add_argument("--max-len", type=float, default=10.0)

    p_filter = sub.add_parser("filter", help="keep clips with enough motion")
    p_filter.add_argument("--in", dest="inp", required=True)
    p_filter.add_argument("--out", required=True)
    p_filter.add_argument("--min-motion", type=float, default=0.35)

    p_events = sub.add_parser("events", help="mine physical-event candidates (motion spikes)")
    p_events.add_argument("--in", dest="inp", required=True)
    p_events.add_argument("--out", required=True)
    p_events.add_argument("--z", type=float, default=3.0)

    p_pairs = sub.add_parser("pairs", help="write intervention pair catalog")
    p_pairs.add_argument("--out", required=True)
    p_pairs.add_argument("--n", type=int, default=200)
    p_pairs.add_argument("--events", default=None)
    p_pairs.add_argument("--length", type=int, default=16)
    p_pairs.add_argument("--z", type=float, default=3.0)

    args = parser.parse_args()
    if args.cmd == "collect":
        from . import collect
        collect.run(args.query, args.max, args.out, source=args.source)
    elif args.cmd == "segment":
        from . import segment
        segment.run(args.inp, args.out, args.min_len, args.max_len)
    elif args.cmd == "filter":
        from . import filter as filt
        filt.run(args.inp, args.out, args.min_motion)
    elif args.cmd == "events":
        from . import events
        events.run(args.inp, args.out, args.z)
    elif args.cmd == "pairs":
        from . import pairs
        from pathlib import Path
        extra_kwargs = {}
        if args.events:
            extra_kwargs["events"] = args.events
        pairs.run(args.out, n_synthetic=args.n, events=args.events, length=args.length)


if __name__ == "__main__":
    sys.exit(main())
