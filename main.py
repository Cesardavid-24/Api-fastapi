from fastapi import FastAPI

# import uvicorn
app = FastAPI()

@app.get('/')
def index():
    return {"message" : "Hello World"}

# opcional inicarlo desde python 
#if __name__ == '__main__':
    #uvicorn.run(app, host="127.0.0.1", port=4321, reload=True)