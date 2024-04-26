from fastapi import FastAPI

from app.v1.router.user_router import router as user_router
# import uvicorn
app = FastAPI()
app.include_router(user_router)

# opcional inicarlo desde python 
#if __name__ == '__main__':
    #uvicorn.run(app, host="127.0.0.1", port=4321, reload=True)