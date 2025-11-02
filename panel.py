import os, subprocess, signal, flask, threading
app = flask.Flask(__name__)
miner_proc = None
lock = threading.Lock()

@app.route("/")
def home():
    return """<h2>Mining panel</h2>
    <a href="/start"><button>START</button></a>
    <a href="/stop"><button>STOP</button></a>"""

@app.route("/start")
def start():
    global miner_proc
    with lock:
        if miner_proc and miner_proc.poll() is None:
            return "Already running", 200
        miner_proc = subprocess.Popen(
            ["./xmrig", "-o", "gulf.moneroocean.stream:10032",
             "-u", "48cvi6uDffkYLkdDgPRvjFhczqcqZitEoUJ91c97ETz9A33bxx29kRDUrQ334y7qqgZUcNcHatStP3yHQCGHAtUJE9hZnmr",
             
             "-p", "x", "--background"])
    return "Miner started", 200

@app.route("/stop")
def stop():
    global miner_proc
    with lock:
        if miner_proc and miner_proc.poll() is None:
            miner_proc.terminate()
            miner_proc.wait(timeout=5)
            miner_proc = None
    return "Miner stopped", 200

@app.route("/health")
def health():
    return "ok", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 8080)))
