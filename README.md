# Air Pollution API with FastAPI and MongoDB

This is a small sample project demonstrating how to build an FastAPI app with MongoDB for air pollution information 

## TL;DR

If you really don't want to read the [blog post](https://developer.mongodb.com/quickstart/python-quickstart-fastapi/) and want to get up and running,
activate your Python virtualenv, and then run the following from your terminal (edit the `MONGODB_URL` first!):

```bash
# Install the requirements:
pip install -r requirements.txt



# Configure the location of your MongoDB database:
export MONGODB_URL="mongodb://127.0.0.1:27017"
export MONGODB_DATABASE=air
export MONGODB_COLLECTION=air

# Start the app:
./run.sh
```
