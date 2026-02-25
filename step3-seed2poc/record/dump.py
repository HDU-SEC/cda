import gdb

class WatchWriteOps(gdb.Breakpoint):
    cleared = False

    def __init__(self):
        super().__init__("ehci_opreg_write", internal=False)

        if not WatchWriteOps.cleared:
            open("../poc/mmio.log", "w").close()
            WatchWriteOps.cleared = True

        self.logfile = open("../poc/mmio.log", "a")
        print("[*] Breakpoint set at ehci_opreg_write to track read & write ops")

    def log(self, msg):
        self.logfile.write(msg + "\n")
        self.logfile.flush()

    def stop(self):
        try:
            ptr = gdb.parse_and_eval("ptr")
            addr = gdb.parse_and_eval("addr")
            val = gdb.parse_and_eval("val")
            size = gdb.parse_and_eval("size")

            self.log(f"ehci_opreg_write({hex(int(ptr))}, {hex(addr)}, {hex(int(val))}, {int(size)})")

        except Exception as e:
            self.log(f"[!] Error in stop: {e}")
        return False

WatchWriteOps()