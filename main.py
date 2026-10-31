# MILESTONE 1

import argparse

from cache_calculations import calculate_cache
from memory_calculations import calculate_memory
from output import write_results


CACHE_SIZES_KB = (8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192)
BLOCK_SIZES = (8, 16, 32, 64)
ASSOCIATIVITIES = (1, 2, 4, 8, 16)
PHYSICAL_MEMORY_SIZES_MB = (128, 256, 512, 1024, 2048, 4096)


def parse_time_slice(value):
    # return a valid instruction count, or -1 to represent all instructions
    try:
        count = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("enter a whole number") from exc

    if count == 0 or count < -1:
        raise argparse.ArgumentTypeError("enter a positive number or -1 for all")

    return count


def build_parser():
    parser = argparse.ArgumentParser(
        description = "Calculate the Milestone 1 cache and physical-memory values."
    )

    parser.add_argument("-s", type=int, required=True, metavar="KB",
                        help="cache size in KB (8 through 8192, powers of 2)")
    parser.add_argument("-b", type=int, required=True, metavar="BYTES",
                        help="cache block size: 8, 16, 32, or 64 bytes")
    parser.add_argument("-a", type=int, required=True, metavar="WAYS",
                        help="associativity: 1, 2, 4, 8, or 16")
    parser.add_argument("-r", type=str.upper, choices=("RR", "RND"), required=True,
                        metavar="{RR,RND}", help="replacement policy")
    parser.add_argument("-p", type=int, required=True, metavar="MB",
                        help="physical memory size in MB (128 through 4096, powers of 2)")
    parser.add_argument("-u", type=float, required=True, metavar="PERCENT",
                        help="percentage of physical memory used by the OS (0 to 100)")
    parser.add_argument("-n", type=parse_time_slice, required=True, metavar="COUNT",
                        help="instructions per time slice; use -1 for all instructions")
    parser.add_argument("-f", dest="trace_files", action="append", required=True,
                        metavar="TRACE",
                        help="trace filename; use a separate -f for each file (1 to 3)")
    parser.add_argument("--team", default="XX",
                        help="team number used in the output filename (default: XX)")
    parser.add_argument("--run", type=int, choices=(1, 2, 3), default=1,
                        help="Milestone 1 output run number: 1, 2, or 3 (default: 1)")
    parser.add_argument("--output-dir", default="results",
                        help="folder for the generated output file (default: results)")

    return parser


def validate_arguments(parser, args):
    # check combinations and value ranges required
    if args.s not in CACHE_SIZES_KB:
        parser.error(f"-s must be one of: {', '.join(map(str, CACHE_SIZES_KB))}")

    if args.b not in BLOCK_SIZES:
        parser.error(f"-b must be one of: {', '.join(map(str, BLOCK_SIZES))}")

    if args.a not in ASSOCIATIVITIES:
        parser.error(f"-a must be one of: {', '.join(map(str, ASSOCIATIVITIES))}")

    if args.p not in PHYSICAL_MEMORY_SIZES_MB:
        parser.error(
            "-p must be one of: "
            + ", ".join(map(str, PHYSICAL_MEMORY_SIZES_MB))
        )

    if not 0 <= args.u <= 100:
        parser.error("-u must be between 0 and 100")

    if not 1 <= len(args.trace_files) <= 3:
        parser.error("provide 1, 2, or 3 trace files, each preceded by -f")

    if args.s * 1024 < args.b * args.a:
        parser.error("the selected cache must have enough space for at least one set")

    if not args.team.strip():
        parser.error("--team cannot be blank")


def run_simulation(args):
    # calculate Milestone 1 values and write one formatted output file
    inputs = {
        "cache_size_kb": args.s,
        "block_size": args.b,
        "associativity": args.a,
        "replacement_policy": args.r,
        "physical_memory_mb": args.p,
        "os_percent": args.u,
        "instructions_per_time_slice": args.n,
        "trace_files": args.trace_files,
        "team_number": args.team,
    }

    cache_results = calculate_cache(
        cache_size_kb=args.s,
        block_size=args.b,
        associativity=args.a,
        physical_memory_mb=args.p,
    )

    memory_results = calculate_memory(
        physical_memory_mb=args.p,
        os_percent=args.u,
        num_processes=len(args.trace_files),
    )

    output_file = write_results(
        team_number=args.team,
        trace_files=args.trace_files,
        inputs=inputs,
        cache_results=cache_results,
        memory_results=memory_results,
        run_number=args.run,
        output_directory=args.output_dir,
    )

    print(f"\nOutput saved to: {output_file}")


def main():
    parser = build_parser()
    args = parser.parse_args()
    validate_arguments(parser, args)
    run_simulation(args)


if __name__ == "__main__":
    main()
