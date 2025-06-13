from fastapi import FastAPI
from app.core.database import Base, engine
from app.auth.routes import router as auth_router
from app.products.routes import router as product_router
from app.cart.routes import router as cart_router
from app.checkout.routes import router as checkout_router
from app.orders.routes import router as orders_router

from fastapi.responses import JSONResponse
from fastapi.requests import Request
from fastapi import HTTPException
from starlette.middleware.cors import CORSMiddleware

import logging

# db table create karne ke liye
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="E-commerce Backend System",
    version="1.0",
    description="FastAPI backend for E-commerce platform"
)

# Routers
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(product_router, prefix="/products", tags=["Products"])
app.include_router(cart_router, prefix="/cart", tags=["Cart"])
app.include_router(checkout_router, prefix="/checkout", tags=["Checkout"])
app.include_router(orders_router, prefix="/orders", tags=["Orders"])

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "message": exc.detail,
            "code": exc.status_code
        },
    )

# Setup your own logger
logger = logging.getLogger("myapp.request")
logger.setLevel(logging.INFO)

# Optional: Add console handler
console_handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

# Log each request (via middleware)
@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.client.host} - {request.method} {request.url.path}")
    response = await call_next(request)
    return response

@app.get("/")
def root():
    return {"message": "Welcome to the E-commerce Backend API"}
