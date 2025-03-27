FROM python:3.13-slim AS base

ARG TARGETARCH

RUN apt-get update && apt-get install -y unzip curl wget xz-utils && rm -rf /var/lib/apt/lists/*
ENV HTTPX_DISABLE_IPV6=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM base AS build
ARG TARGETARCH
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
RUN npm config set registry https://registry.npmmirror.com
RUN reflex export --no-zip

FROM base AS final
ENV API_URL=http://localhost:8000
WORKDIR /app
COPY --from=build /root/.bun /root/.bun
COPY --from=build /usr/local /usr/local
COPY --from=build /app /app
ENV PATH="/root/.bun/bin:/usr/local/bin:$PATH"
EXPOSE 8000
EXPOSE 3000
CMD ["reflex", "run", "--env", "prod"]