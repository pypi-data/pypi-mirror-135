class RunConfig:
    """
    Captures run configuration.
    Keep this as a class constructed directly from a dictionary (json),
    so that we can convert the whole thing to web service easily.
    """

    def __init__(self, cfgdict):
        self.logfile = cfgdict["logfile"]
        self.top_req_pages = cfgdict["top_req_pages"]
        self.perc_succ_reqs = cfgdict["perc_succ_reqs"]
        self.perc_fail_reqs = cfgdict["perc_fail_reqs"]
        self.top_hosts = cfgdict["top_hosts"]
        self.top_pages_per_host = cfgdict["top_pages_per_host"]
        self.show_errors = cfgdict["show_errors"]
