"""This script runs the benchmark looking for the maximum throughput"""
import subprocess

import click


class InjectionResult:
    def __init__(self, rps, resp_time, req_failed):
        self.rps = rps
        self.resp_time = resp_time
        self.req_failed = req_failed

    def to_csv(self):
        return f"{self.rps},{self.resp_time},{self.req_failed}"

    def __repr__(self):
        return f"rps={self.rps} resp_time={self.resp_time} res_failed={self.req_failed}"


def different_enough_rps(prev_run: InjectionResult, this_run: InjectionResult) -> bool:
    """Checks that the rps from the previous run and this one is more than
    10%."""
    if not prev_run:
        return True

    prev_rps = prev_run.rps
    this_rps = this_run.rps
    diff = this_rps - prev_rps
    diff_pct = diff * 100 / this_rps

    if diff_pct >= 10:
        return True

    return False


def inject(server: str, iterations: int, vus: int, duration: str) -> InjectionResult:
    """Runs k6 and returns an InjectionResult"""
    command = f"k6 run -e SERVER={server} -e NUM_IT={iterations} --duration={duration} --vus={vus} load.js"
    result = subprocess.run(command.split(" "), stdout=subprocess.PIPE).stdout.decode(
        "utf-8"
    )
    last_line = result.strip().split("\n")[-1].split(",")
    return InjectionResult(
        rps=float(last_line[0]),
        resp_time=float(last_line[1]),
        req_failed=int(last_line[2]),
    )


def print_results(results: dict):
    print("\nvus,rps,resp_time,req_failed")
    for vus, i in results.items():
        print(f"{vus},{i.to_csv()}")


@click.command("cli", context_settings={"show_default": True})
@click.option("--server", type=str, required=True, help="IP of the server")
@click.option(
    "--iterations",
    type=int,
    default=60000,
    help="Number of iterations to run in the server",
)
@click.option(
    "--duration",
    type=str,
    default="30s",
    help="Duration of each injection",
)
def run(server: str, iterations: int, duration: str):
    vus = 1
    results = {}
    prev_run = None
    while True:
        print(f"Injecting with {vus} vus")
        this_run = inject(server, iterations, vus, duration)

        if (not different_enough_rps(prev_run, this_run)) or this_run.req_failed > 0:
            break

        results[vus] = this_run

        vus = vus * 2
        prev_run = this_run

    print_results(results)


if __name__ == "__main__":
    run()
