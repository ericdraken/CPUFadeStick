#  Copyright (c) Eric Draken, 2021.
import os
import sys
from typing import Final, Union

from core.CPUDaemon import CPUDaemon
from exceptions.FadeStickException import FadeStickException

if sys.platform == "win32":
    raise FadeStickException("Windows is not supported")

daemon: Final = CPUDaemon()


def print_if_not_none(msg: Union[str, None]):
    if msg:
        print(msg)


def main():
    filename = os.path.basename(sys.argv[0])
    cmd = None if len(sys.argv) <= 1 else str(sys.argv[1]).strip().lower()
    if cmd == "start":
        print("Starting daemon.")
        print_if_not_none(daemon.start())
    elif cmd == "stop":
        print_if_not_none(daemon.stop())
    elif cmd == "kill":
        print_if_not_none(daemon.kill())
    elif cmd == "restart":
        print("Restarting daemon.")
        print_if_not_none(daemon.restart())
    elif cmd == "status":
        print_if_not_none(daemon.status())
    else:
        print(f"Usage: {filename} [action]")
        print("    start     : Start the daemon")
        print("    stop      : Stop the daemon")
        print("    kill      : Kill the daemon")
        print("    restart   : Restart the daemon")
        print("    status    : Get the daemon status")
        return 1


if __name__ == '__main__':
    sys.exit(main())
