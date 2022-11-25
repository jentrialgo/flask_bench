# Flask bench

This is a simple synthetic web benchmark using Flask. It only has a URL that
receives two parameters, `it1` and `it2`, which control the number of iterations
of two loops to simulate busy CPU cycles.

## Server

To build the server, run:

```bash
cd server
docker build -t flask/flask_bench . --build-arg SECRET_KEY="change_me"
docker run -d -p 80:80 flask/flask_bench
```

Remember to change the secret key with some random string.

You can test that the server works with this command:

```bash
curl "localhost/?it1=52250&it2=123"
```

## Client

TODO
