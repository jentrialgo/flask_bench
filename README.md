# Flask bench

This is a simple synthetic web benchmark using Flask. It only has a URL that
receives two parameters, `it1` and `it2`, which control the number of iterations
of two loops to simulate busy CPU cycles.

## Server

To build the server, run:

```bash
cd server
docker build -t flask/flask_bench_server . --build-arg SECRET_KEY="change_me"
docker run -d -p 80:80 flask/flask_bench_server
```

Remember to change the secret key with some random string.

You can test that the server works with this command:

```bash
curl "localhost/?it1=52250&it2=123"
```

## Client

To build the client, run:

```bash
cd client
docker build -t flask/flask_bench_client .
docker run -e SERVER=SERVER_IP flask/flask_bench_client
```

Remember to change the value `SERVER_IP` with the IP address of the server. For
instance:

```bash
docker run -e SERVER=172.31.0.23 flask/flask_bench_client
```
