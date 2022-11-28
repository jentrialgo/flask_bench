# Copyright 2018 PerfKitBenchmarker Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Flask benchmark.

Executes https://github.com/jentrialgo/flask_bench
"""

from absl import flags

from perfkitbenchmarker import configs
from perfkitbenchmarker import sample

BENCHMARK_NAME = "flask_benchmark"
BENCHMARK_CONFIG = """
flask_benchmark:
  description: Runs a sample benchmark.
  vm_groups:
    server:
      os_type: ubuntu2004
      vm_spec: *default_single_core
      vm_count: 1
    client:
      os_type: ubuntu2004
      vm_spec: *default_single_core
      vm_count: 1
"""

FLAGS = flags.FLAGS

flags.DEFINE_integer(
    "flask_iterations", 60_000, "Number of iterations for flask_benchmark."
)
flags.DEFINE_string(
    "flask_duration", "30s", "Duration of each injection in flask_benchmark."
)


def GetConfig(user_config):
    """Returns the configuration of a benchmark."""
    return configs.LoadConfig(BENCHMARK_CONFIG, user_config, BENCHMARK_NAME)


def Prepare(benchmark_spec):
    """Prepares the VMs and other resources for running the benchmark.

    Args:
      benchmark_spec: The benchmark spec for this sample benchmark.
    """
    server = benchmark_spec.vm_groups["server"][0]
    client = benchmark_spec.vm_groups["client"][0]

    server.InstallPackages("python3 docker.io git")
    client.InstallPackages("python3 docker.io git")

    server.RemoteCommand("git clone https://github.com/jentrialgo/flask_bench.git")
    client.RemoteCommand("git clone https://github.com/jentrialgo/flask_bench.git")

    server.RemoteCommand(
        "sudo docker build -t flask/flask_bench_server flask_bench/server --build-arg SECRET_KEY='adljfaljdf3'"
    )
    client.RemoteCommand(
        "sudo docker build -t flask/flask_bench_client flask_bench/client"
    )

    server.RemoteCommand("sudo docker run -d -p 80:80 flask/flask_bench_server")


def Run(benchmark_spec):
    """Runs the benchmark and returns a dict of performance data.

    Args:
      benchmark_spec: The benchmark spec for this sample benchmark.

    Returns:
      A list of performance samples.
    """
    server = benchmark_spec.vm_groups["server"][0]
    client = benchmark_spec.vm_groups["client"][0]

    cmd = (
        f"sudo docker run -e SERVER={server.internal_ip} "
        f"-e ITERATIONS={FLAGS.flask_iterations} "
        f"-e DURATION={FLAGS.flask_duration} "
        f"flask/flask_bench_client"
    )
    stdout, _ = client.RemoteCommand(cmd)

    lines = stdout.strip().split("\n")

    # The last line is the maximum throughput and has the format:
    #   vus,rps,response_time,req_failed
    metrics = lines[-1].split(",")
    vus, rps, resp_time, req_failed = metrics
    return [
        sample.Sample("vus", int(vus), "vus"),
        sample.Sample("rps", float(rps), "rps"),
        sample.Sample("resp_time", float(resp_time), "ms"),
        sample.Sample("req_failed", float(req_failed), "requests"),
    ]


def Cleanup(benchmark_spec):
    """Cleans up after the benchmark completes.

    The state of the VMs should be equivalent to the state before Prepare was
    called.

    Args:
      benchmark_spec: The benchmark spec for this sample benchmark.
    """
    del benchmark_spec
