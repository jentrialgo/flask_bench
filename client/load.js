import http from 'k6/http';

// This script must receive two environment variables:
// - SERVER: ip address of the server
// - NUM_IT: number of iterations to execute in the server
//
// Example:
//   k6 run -e SERVER=1.2.3.4 -e NUM_IT=53321 --duration=30s --vus=10 load.js

export default function () {
  const server = __ENV.SERVER;
  const num_it = __ENV.NUM_IT;
  http.get(`http://${server}?it1=${num_it}&it2=1`);
}

export function handleSummary(data) {
  // Print on the stdout the rps, the p95 of the response time and the number
  // of failed requests
  const resp_time = data.metrics.http_req_duration.values["p(95)"];
  const rps = data.metrics.http_reqs.values.rate;
  const failed_reqs = data.metrics.http_req_failed.values.passes;
  const result = `${rps},${resp_time},${failed_reqs}\n`;
  return {
    'stdout': result,
  };
}
