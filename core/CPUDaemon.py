#  Copyright (c) Eric Draken, 2021.
import logging
import os
import select
import signal
import struct
import sys
import threading
import time
from logging import handlers
from typing import Final, Union

from daemon import daemon, pidfile
from usb.core import USBError

from core.CPU import CPU
from core.FadeStick import FadeStick
from core.FadeStickUSB import findFirstFadeStick
from exceptions.FadeStickUSBException import FadeStickUSBException
from utils.Colors import scaleToRGB, OFF
from utils.Types import RGB


class DaemonException(Exception):
    pass


# REF: https://www.eadan.net/blog/ipc-with-named-pipes/
def encode_msg_size(size: int) -> bytes:
    return struct.pack("<I", size)


def decode_msg_size(size_bytes: bytes) -> int:
    return struct.unpack("<I", size_bytes)[0]


def create_msg(content: bytes) -> bytes:
    size = len(content)
    return encode_msg_size(size) + content


def get_message(fifo: int) -> str:
    """Get a message from the named pipe."""
    msg_size_bytes = os.read(fifo, 4)
    msg_size = decode_msg_size(msg_size_bytes)
    msg_content = os.read(fifo, msg_size).decode("ascii")
    return msg_content


class CPUDaemon:
    _formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)s] %(message)s")

    # Log to /var/log/syslog
    _syslog_handler: Final = logging.handlers.SysLogHandler(
        facility=logging.handlers.SysLogHandler.LOG_DAEMON, address="/dev/log")
    _syslog_handler.setFormatter(_formatter)
    _syslog_handler.setLevel(logging.INFO)

    _daemon_log: Final = logging.getLogger("daemon")
    _daemon_log.addHandler(_syslog_handler)
    _daemon_log.setLevel(logging.INFO)

    # Console logging
    _console_handler: Final = logging.StreamHandler(sys.stdout)
    _console_handler.setFormatter(_formatter)
    _console_handler.setLevel(logging.WARNING)

    _main_log: Final = logging.getLogger("main")
    _main_log.addHandler(_console_handler)
    _main_log.addHandler(_syslog_handler)
    _main_log.setLevel(logging.INFO)

    _app_name: Final = "cpufadestick"
    _pidpath: Final = os.path.join(f"/tmp/{_app_name}.pid")

    _named_pipe = f"/tmp/{_app_name}.pipe"

    _cpu_per: float = 0.0
    _cur_color: RGB = OFF
    _is_running: bool = False
    _fs_present: bool = False
    _lock: Final = threading.Lock()

    def _get_context(self) -> daemon.DaemonContext:
        """Return a daemon context to use with 'with'"""
        return daemon.DaemonContext(
            pidfile=pidfile.PIDLockFile(self._pidpath),
            stdout=sys.stdout,
            stderr=sys.stderr,
            detach_process=True,
            files_preserve=self._get_log_file_handles(self._daemon_log),
            signal_map={
                signal.SIGTERM: self._end,
                signal.SIGTSTP: self._end,
                signal.SIGINT: self._end,
                signal.SIGUSR1: self._status,
                signal.SIGUSR2: self._status,
            }
        )

    @staticmethod
    def _get_log_file_handles(logger):
        """Get a list of file handle numbers from the logger to preserve"""
        handles = []
        for handler in logger.parent.handlers:
            # Try both 'stream' and 'socket'
            try:
                handles.append(handler.stream.fileno())
            except AttributeError:
                handles.append(handler.socket.fileno())
        return handles

    # Daemon methods #

    def _status(self, signum: int, _frame=None):
        self._daemon_log.debug(f"Daemon received {signal.Signals(signum).name}")
        try:
            with self._lock:
                if not self._fs_present:
                    msg = "Daemon running, but FadeStick not present."
                else:
                    msg = f"Daemon running. Current CPU load is {self._cpu_per * 100.0:.2f}% and is color {self._cur_color}."

            self._daemon_log.debug(msg)
            # Pass messages from the daemon to the controller via a named pipe
            pipe = os.open(self._named_pipe, os.O_WRONLY)
            self._daemon_log.debug("Opened IPC pipe")
            packet = create_msg(msg.encode("ascii"))
            os.write(pipe, packet)
            self._daemon_log.debug("Wrote to IPC pipe")
            # Do not close the pipe in the daemon
        except Exception as e:
            self._daemon_log.error(f"Daemon status error: {e}")

    def _end(self, signum: int, _frame=None):
        self._daemon_log.debug(f"Daemon received {signal.Signals(signum).name}")
        self._is_running = False

    def _run(self):
        if self._is_running:
            return

        self._is_running = True
        self._daemon_log.debug("Beginning FadeStick loop")
        cpu: Final = CPU()
        fs: Union[FadeStick, None] = None
        period_ms = 1000
        try:
            while True:
                # Graceful exit condition
                if not self._is_running:
                    break

                # Handle the case when the USB is unplugged
                if not fs:
                    try:
                        with self._lock:
                            fs = FadeStick(findFirstFadeStick())
                            self._fs_present = True
                    except FadeStickUSBException:
                        with self._lock:
                            self._fs_present = False
                        time.sleep(5)
                        continue

                try:
                    self._cpu_per = cpu.getCPUTimeSlicePercentage()
                    self._daemon_log.debug(f"CPU {self._cpu_per * 100.0:.2f}%")
                    self._cur_color = scaleToRGB(self._cpu_per)
                    fs.morph(self._cur_color, period_ms)
                    time.sleep(period_ms / 1000.0)
                except (USBError, FadeStickUSBException):
                    # Get a new USB handle next
                    with self._lock:
                        fs = None
                        self._fs_present = True
                except Exception as e:
                    self._daemon_log.error(f"Daemon exception: {e}")
                    time.sleep(5)  # Don't flood syslog
        finally:
            with self._lock:
                if self._fs_present:
                    self._daemon_log.debug("Shutting down FadeStick")
                    try:
                        for _ in range(60):
                            fs.turnOff()
                            if fs.getColor() == OFF:
                                break
                            else:
                                time.sleep(
                                    1)  # Don't flood FadeStick while it is processing
                    except Exception as e:
                        self._daemon_log.error(e)
                    finally:
                        with self._lock:
                            self._is_running = False
                            self._fs_present = False

    # Main methods #

    def start(self) -> str:
        self._main_log.info("Daemon start requested")
        ctx = self._get_context()
        if ctx.pidfile.read_pid():
            return "Daemon already running."

        with ctx:
            self._run()
            # This process will now die

    def stop(self) -> str:
        self._main_log.info("Daemon stop requested")
        ctx = self._get_context()
        pidf: pidfile.PIDLockFile = ctx.pidfile
        if not pidf.read_pid():
            return "Daemon already stopped."

        # The daemon will close the PID file itself
        try:
            pid = pidf.read_pid()
            self._main_log.debug(f"Sending {signal.SIGINT.name} to PID {pid}")
            os.kill(pid, signal.SIGINT)
            return "Daemon stopping."
        except Exception as e:
            self._main_log.error(f"Daemon stop error: {e}")
            # No return message on purpose

    def kill(self) -> str:
        # Try to gracefully stop first
        self.stop()

        # Give stop a chance to be graceful
        time.sleep(5)
        ctx = self._get_context()
        pidf: pidfile.PIDLockFile = ctx.pidfile
        pid = pidf.read_pid()
        if not pid:
            return "Daemon not running."

        self._main_log.info(f"Daemon kill requested for pid {pid}")
        # Will remove the PID file after
        try:
            self._main_log.debug(f"Sending {signal.SIGKILL.name} to PID {pid}")
            os.kill(pid, signal.SIGKILL)
            return "Daemon was killed."
        except Exception as e:
            self._main_log.error(f"Daemon kill error: {e}")
        finally:
            # Remove the lock file with prejudice
            pidf.break_lock()

    def status(self) -> str:
        self._main_log.info("Daemon status requested")
        pid = self._get_context().pidfile.read_pid()
        if not pid:
            return "Daemon not running."

        # Create the named pipe
        try:
            try:
                os.mkfifo(self._named_pipe)
                self._main_log.debug("Creating named IPC pipe")
            except FileExistsError:
                self._main_log.debug("IPC pipe already exists")
                pass

            # Open the pipe in non-blocking mode for reading
            pipe = os.open(self._named_pipe, os.O_RDONLY | os.O_NONBLOCK)
            self._main_log.debug("Opened IPC pipe")
            try:
                # Trigger the daemon to place a message in the queue
                self._main_log.debug(f"Sending {signal.SIGUSR1.name} to PID {pid}")
                os.kill(pid, signal.SIGUSR1)
                self._main_log.debug(f"Waiting for reply")

                # Create a polling object to monitor the pipe for new data
                poll = select.poll()
                poll.register(pipe, select.POLLIN)
                try:
                    # Check if there's data to read. Timeout after 5 sec.
                    self._main_log.debug("Starting IPC poll")
                    if (pipe, select.POLLIN) in poll.poll(5000):
                        return get_message(pipe)
                    else:
                        self._main_log.error("Daemon did not respond in time.")
                finally:
                    poll.unregister(pipe)
            finally:
                os.close(pipe)
        finally:
            os.remove(self._named_pipe)
            self._main_log.debug("Finished status request")

    def restart(self) -> str:
        self._main_log.debug("Daemon restart requested")
        try:
            msg = self.stop()
            msg += self.start()
            return msg
        except Exception as e:
            self._main_log.error(f"Daemon restart error: {e}")
