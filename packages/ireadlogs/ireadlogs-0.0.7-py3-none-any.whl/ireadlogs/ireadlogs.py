import sys
import json

try:
    from parser import Parser
    from runconfig import RunConfig
    from stats import Stats
except (ModuleNotFoundError, ImportError):
    from .parser import Parser
    from .runconfig import RunConfig
    from .stats import Stats


def main():
    args = Parser().parser.parse_args(sys.argv[1:])
    # create config for this run
    cfg = RunConfig(
        {
            "logfile": args.logfile,
            "top_req_pages": args.pages,
            "perc_succ_reqs": True,
            "perc_fail_reqs": True,
            "top_hosts": args.hosts,
            "top_pages_per_host": args.hosts_breakdown,
            "show_errors": args.show_errors,
        }
    )
    stats = Stats(config=cfg)
    res = stats.stats()
    print(json.dumps(res, indent=4))


if __name__ == "__main__":
    main()
