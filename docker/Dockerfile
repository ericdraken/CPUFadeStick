FROM python:3.8-slim AS nuitkabuilder

RUN apt-get update &&\
    apt-get install -y \
    curl build-essential ccache libfuse2 file
    # Note, fuse isn't needed, but some prerequisite logic checks for it
    # file is needed if ARCH isn't set
    # See: https://github.com/AppImage/AppImageKit/blob/8bbf694455d00f48d835f56afaa1dabcd9178ba6/src/appimagetool.c#L726

RUN pip3 install --no-cache-dir Cython nuitka

FROM nuitkabuilder

ARG user=nuitka
ARG group=nuitka
ARG uid=1000
ARG gid=1000

RUN groupadd -g ${gid} ${group} &&\
    useradd -rm -d /home/${user} -s /bin/sh -g ${group} -u ${uid} ${user}

USER nuitka

WORKDIR /workdir

ARG APPIMAGE=/home/${user}/.local/share/Nuitka/appimagetool-x86_64.AppImage/x86_64/12/appimagetool-x86_64.AppImage

RUN curl -L \
    https://github.com/AppImage/AppImageKit/releases/download/12/appimagetool-x86_64.AppImage \
    -o ${APPIMAGE} \
    --create-dirs &&\
    chmod +x ${APPIMAGE}

# Avoid the whole Fuse-Docker fiasco
# REF: https://docs.appimage.org/user-guide/troubleshooting/fuse.html
# REF: https://github.com/AppImage/AppImageKit/issues/912
ENV APPIMAGE_EXTRACT_AND_RUN=1
ENV NO_CLEANUP=1

# Run once for the cache effect
RUN /home/${user}/.local/share/Nuitka/appimagetool-x86_64.AppImage/x86_64/12/appimagetool-x86_64.AppImage -h

COPY icon.xpm /

CMD pip3 install --user -r requirements.txt &&\
    python3 -m nuitka \
    --follow-imports \
    --standalone \
    --onefile \
    --show-progress \
    --lto \
    --linux-onefile-icon=/icon.xpm \
    --output-dir=build \
#    --remove-output \
    --assume-yes-for-downloads \
    main.py &&\
    mv build/main.bin cpufadestick &&\
    file cpufadestick &&\
    echo "Success!"

