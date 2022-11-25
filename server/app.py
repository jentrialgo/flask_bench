import socket
import os
from flask import Flask, request
from datetime import datetime
from prometheus_flask_exporter import PrometheusMetrics

app = Flask(__name__)
metrics = PrometheusMetrics(app)

for variable, value in os.environ.items():
    app.config[variable] = value

if "SECRET_KEY" not in app.config:
    raise Exception("You must set an environment variable with the SECRET_KEY")


@app.route("/")
def hello_world():
    it1 = int(request.args.get("it1"))
    it2 = int(request.args.get("it2"))
    start = datetime.now()
    c = 0
    for i in range(it1):
        for j in range(it2):
            if i % 554 == 0:
                c += c + j
    end = datetime.now()

    comp = (end - start).total_seconds()
    current_time = end.strftime("%H:%M:%S")
    ip_addr = socket.gethostbyname(socket.gethostname())
    return f"Server: {ip_addr}. Time: {current_time}. Computation took {comp} s\n"


if __name__ == "__main__":
    app.run(debug=True)
