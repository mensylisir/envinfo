FROM python:3.12 AS builder
ARG TARGETARCH
WORKDIR /app
RUN apt-get update && apt-get install -y unzip curl wget xz-utils xclip xvfb && rm -rf /var/lib/apt/lists/*

RUN if [ "$TARGETARCH" = "arm64" ]; then \
        wget https://nodejs.org/dist/v18.18.0/node-v18.18.0-linux-arm64.tar.xz && \
        tar -xJf node-v18.18.0-linux-arm64.tar.xz -C /usr/local --strip-components=1 && \
        rm node-v18.18.0-linux-arm64.tar.xz; \
    else \
        wget https://nodejs.org/dist/v18.18.0/node-v18.18.0-linux-x64.tar.xz && \
        tar -xJf node-v18.18.0-linux-x64.tar.xz -C /usr/local --strip-components=1 && \
        rm node-v18.18.0-linux-x64.tar.xz; \
    fi

RUN curl -fsSL https://bun.sh/install | bash
ENV PATH="/root/.bun/bin:/usr/local/bin:$PATH"
COPY . .
RUN pip install -r requirements.txt
RUN npm config set registry https://registry.npmmirror.com
RUN reflex export --frontend-only --no-zip

FROM nginx

COPY --from=builder /app/.web/_static /usr/share/nginx/html
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
