from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title = "She Crochets API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # adjust for deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return{"message": "She Crochets API is running"}