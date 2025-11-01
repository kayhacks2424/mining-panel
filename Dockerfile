FROM alpine:3.18 AS build
RUN apk add --no-cache git cmake make gcc g++ libuv-dev openssl-dev hwloc-dev
WORKDIR /src
RUN git clone --branch v6.21.0 --depth 1 https://github.com/xmrig/xmrig.git . && \
    mkdir build && cd build && \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_STATIC=ON && \
    make -j$(nproc)

FROM alpine:3.18
RUN apk add --no-cache libstdc++ libuv openssl hwloc
WORKDIR /app
COPY --from=build /src/build/xmrig /app/xmrig
COPY panel.py start.sh stop.sh ./
HEALTHCHECK --interval=30s --timeout=3s CMD python3 panel.py health || exit 1
ENV PORT=8080
EXPOSE 8080
CMD ["python3", "panel.py"]
