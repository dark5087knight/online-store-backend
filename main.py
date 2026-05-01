from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from database import init_db
from routers import products, categories, orders, cart, wishlist, recent, banners, reviews

# Load environment variables from .env file
load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)


def verify_api_key(api_key: str = Security(api_key_header)):
    frontend_key = os.getenv("FRONTEND_API_KEY")
    admin_key = os.getenv("ADMIN_API_KEY")

    # Validate that API keys are configured
    if not frontend_key or not admin_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="API keys are not configured. Check your .env file."
        )

    if api_key in [frontend_key, admin_key] and api_key is not None:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate API KEY"
    )


app = FastAPI(title="ShopSphere AI Backend", lifespan=lifespan,
              dependencies=[Depends(verify_api_key)])

# Allow the frontend to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(products.router)
app.include_router(categories.router)
app.include_router(orders.router)
app.include_router(cart.router)
app.include_router(wishlist.router)
app.include_router(recent.router)
app.include_router(banners.router)
app.include_router(reviews.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to ShopSphere AI API"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
