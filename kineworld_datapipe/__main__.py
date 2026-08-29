import argparse
import sys

from . import collect, segment, filter


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

    args = parser.parse_args()
    if args.cmd == "collect":
        collect.run(args.query, args.max, args.out, source=args.source)
    elif args.cmd == "segment":
        segment.run(args.inp, args.out, args.min_len, args.max_len)
    elif args.cmd == "filter":
        filter.run(args.inp, args.out, args.min_motion)


if __name__ == "__main__":
    sys.exit(main())
