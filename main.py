#  Copyright (c) Eric Draken, 2021.
import os
import sys
from pathlib import Path

from core.Daemon import Daemon
from exceptions.FadeStickException import FadeStickException

if sys.platform == "win32":
    raise FadeStickException("Windows is not supported")


def main():
    filename = os.path.basename(sys.argv[0])
    cmd = None if len(sys.argv) <= 1 else str(sys.argv[1]).strip().lower()
    if cmd == "start":
        Daemon().start()
    elif cmd == "stop":
        Daemon().stop()
    elif cmd == "kill":
        Daemon().kill()
    elif cmd == "restart":
        Daemon().restart()
    elif cmd == "status":
        Daemon().status()
    else:
        print(f"Usage: {filename} [action]")
        print("    start     : Start the daemon")
        print("    stop      : Stop the daemon")
        print("    kill      : Kill the daemon")
        print("    restart   : Restart the daemon")
        print("    status    : Get the daemon status")


if __name__ == '__main__':
    sys.exit(main())
