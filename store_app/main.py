import redis.asyncio as aioredis
from contextlib import asynccontextmanager
from fastapi_limiter import FastAPILimiter
from fastapi import FastAPI
import uvicorn
from store_app.api import category, profile, review, product, auth, social_auth, cart, favorite
from starlette.middleware.sessions import SessionMiddleware

from store_app.config import SECRET_KEY


async def init_redis():
    return aioredis.from_url('redis://localhost', encoding='utf-8', decode_responses=True)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = await init_redis()
    await FastAPILimiter.init(redis)
    yield
    await redis.close()


store_app = FastAPI(title='OnlineStore', lifespan=lifespan)
store_app.add_middleware(SessionMiddleware, secret_key="SECRET_KEY")

store_app.include_router(auth.auth_router)
store_app.include_router(profile.user_router)
store_app.include_router(category.category_router)
store_app.include_router(product.product_router)
store_app.include_router(review.review_router)
store_app.include_router(social_auth.social_router)
store_app.include_router(cart.cart_router)
store_app.include_router(favorite.favorite_router)

if __name__ == '__main__':
    uvicorn.run(store_app, host='127.0.0.1', port=8000)

