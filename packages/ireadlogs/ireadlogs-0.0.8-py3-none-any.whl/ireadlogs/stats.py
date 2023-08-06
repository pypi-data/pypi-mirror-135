try:
    from logline import LogLine
except ModuleNotFoundError:
    from .logline import LogLine


class Stats:
    """Calculates statistics for a log file according to run configuration"""

    def __init__(self, config):
        # run configuration for this instance
        self.config = config
        # that's the basic stats index based on hosts
        self.hosts = {}
        # secondary index to help with pages stats
        self.pages = {}
        # another index to keep error lines
        self.errors = []

    def _calc_indexes(self):
        """
        Read log file and keep stats as you go along.
        This is linear and not multicore.
        We can follow a map-reduce approach if we break up the log file
        (more on the second part of the take home assignment).
        """
        lineno = 0
        with open(self.config.logfile, "r", errors="replace") as logf:
            # Can't do better than O(n) - we need to read through all log file
            for line in logf:
                lineno += 1
                try:
                    lg = LogLine(line=line)
                    # keep pages-based stats
                    if lg.page not in self.pages:
                        self.pages[lg.page] = {"count": 1, "fails": 0}
                    else:
                        self.pages[lg.page]["count"] += 1
                    # keep hosts-based stats...
                    if lg.host not in self.hosts:
                        self.hosts[lg.host] = {
                            "count": 1,
                            "fails": 0,
                            "pages": {lg.page: 1},
                        }
                    else:
                        self.hosts[lg.host]["count"] += 1
                        # ...keep stats that relate hosts to pages
                        if lg.page not in self.hosts[lg.host]["pages"]:
                            self.hosts[lg.host]["pages"][lg.page] = 1
                        else:
                            self.hosts[lg.host]["pages"][lg.page] += 1
                    # ...and stats relating hosts to http errors
                    if int(lg.status) >= 400 or int(lg.status) < 200:
                        self.hosts[lg.host]["fails"] += 1
                        self.pages[lg.page]["fails"] += 1
                # any error contributes to errors index
                except (UnicodeDecodeError, AttributeError, ValueError):
                    self.errors.append(lineno)
                    continue

    def _calc_stats(self):
        """Calculate statistics based on the pages and host indexes"""
        res = {
            "top_req_pages": [],
            "perc_succ_reqs": 0,
            "perc_fail_reqs": 0,
            "top_hosts": [],
        }

        # extract stats for pages
        pages_freq = sorted(
            self.pages.keys(), key=lambda x: self.pages[x]["count"], reverse=True
        )
        for p in pages_freq[: self.config.top_req_pages]:
            res["top_req_pages"].append((p, self.pages[p]["count"]))
        # extract success/failure rates
        fails, total = 0, 0
        for h in self.hosts:
            fails += self.hosts[h]["fails"]
            total += self.hosts[h]["count"]
        succ = total - fails
        res["perc_succ_reqs"] = f"{100 * succ/total:.2f}"
        res["perc_fail_reqs"] = f"{100 * fails/total:.2f}"
        # extract host-based stats
        hosts_freq = sorted(
            self.hosts.keys(), key=lambda x: self.hosts[x]["count"], reverse=True
        )
        # get config.top_hosts most active hosts
        for h in hosts_freq[: self.config.top_hosts]:
            res["top_hosts"].append(
                {"host": h, "count": self.hosts[h]["count"], "breakdown": []}
            )
            pages_freq_for_host = sorted(
                self.hosts[h]["pages"].keys(),
                key=lambda x: self.hosts[h]["pages"][x],
                reverse=True,
            )
            # get top config.top_pages_per_host pages breakdown for host
            for p in pages_freq_for_host[: self.config.top_pages_per_host]:
                res["top_hosts"][-1]["breakdown"].append((p, self.hosts[h]["pages"][p]))
        # errors
        if self.config.show_errors:
            res["error_in_lines"] = self.errors
        # all stats return as a dictionary
        return res

    def stats(self):
        self._calc_indexes()
        return self._calc_stats()
