# Set up
run
docker-compose up

or
docker build -t my-flask-app .

then
docker run -d -p 5000:5000 --link rabbitmq:myrabbitmq myflaskapp

# test
python -m unittest discover -s src
