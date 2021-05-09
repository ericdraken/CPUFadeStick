# CPUFadeStick

### Description

Let's write a Python 3 daemon to colorize, fade smoothly, and animate an RGB LED
according to the CPU load and more. We'll use
the <a href="http://staging.ericdraken.com/digispark-blinkstick-microcontroller-hacking/" target="_blank">
modified BlinkStick (FadeStick)</a> to offload LED animation processing away from the
host CPU. Let's also **learn Python 3** from scratch as a Java developer.

See a full write-up at https://ericdraken.com/python-cpu-monitor.

### Building

From the project root, run

```shell
docker build \
  -t nuitka:latest \
  ./docker
```

and then

```shell
docker run \
  -it \
  -v ${PWD}:/workdir \
  -v ${PWD}/build/.ccache:/home/nuitka/.cache \
  nuitka:latest
```

This will compile the CPUFadeStick daemon into a standalone binary in the project root
called `cpufadestick`.

Plug in a FadeStick and run `./cpufadestick start`.

### Usage

```shell
Usage: cpufadestick [action]
    start     : Start the daemon
    stop      : Stop the daemon
    kill      : Kill the daemon
    restart   : Restart the daemon
    status    : Get the daemon status
```

### Copyright

Eric Draken, 2021\
ericdraken.com
