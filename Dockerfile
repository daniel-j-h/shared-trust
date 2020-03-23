FROM ubuntu:18.04

ENV LANG="C.UTF-8" LC_ALL="C.UTF-8" PATH="/home/st/venv/bin:$PATH" PIP_NO_CACHE_DIR="false"

RUN apt-get update -qq && apt-get install -qq -y --no-install-recommends \
    python3 python3-pip python3-venv && \
    rm -rf /var/lib/apt/lists/*

RUN groupadd --gid 1000 st && \
    useradd  --uid 1000 --gid st --shell /bin/bash --create-home st

USER 1000
RUN mkdir /home/st/app
WORKDIR /home/st/app

COPY --chown=st:st requirements.txt .

RUN python3 -m venv /home/st/venv && \
    python3 -m pip install pip==20.0.2 pip-tools==4.5.1

RUN python3 -m piptools sync

COPY --chown=st:st . .

ENTRYPOINT ["/home/st/app/bin/st"]
CMD ["-h"]
