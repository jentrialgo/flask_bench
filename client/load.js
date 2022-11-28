import http from 'k6/http';

// This script must receive two environment variables:
// - SERVER: ip address of the server
// - NUM_IT: number of iterations to execute in the server
//
// Example:
//   k6 run -e SERVER=1.2.3.4 -e NUM_IT=53321

export default function () {
  server = __ENV.SERVER
  num_it = __ENV.NUM_IT
  http.get(`http://${server}?it1=${num_it}&it2=1`);
}
