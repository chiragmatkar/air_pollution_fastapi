docker build -t app .
docker run --name app -d -p 80:80 app