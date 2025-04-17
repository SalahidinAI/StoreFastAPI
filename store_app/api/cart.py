from sqlalchemy.orm import Session
from store_app.db.database import SessionLocal
from store_app.db.models import Cart, CartItem, Product, UserProfile
from store_app.db.schema import CartSchema, CartItemCreateSchema, CartItemSchema
from fastapi import APIRouter, HTTPException, Depends

cart_router = APIRouter(prefix='/cart', tags=['Cart'])


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@cart_router.get('/', response_model=CartSchema)
async def cart_list(user_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart_db:
        raise HTTPException(status_code=404, detail='Cart not found')

    cart_items = db.query(CartItem).filter(CartItem.cart_id == cart_db.id).all()

    total_price = sum(db.query(Product.price).filter(Product.id == item.product_id).scalar() for item in cart_items)

    return {
        'id': cart_db.id,
        'user_id': cart_db.user_id,
        'items': cart_db.items,
        'total_price': total_price
    }


@cart_router.post('/', response_model=CartItemSchema)
async def cart_add(item_data: CartItemCreateSchema, user_id: int,
                   db: Session = Depends(get_db)):
    user_db = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not user_db:
        raise HTTPException(status_code=404, detail='User not found')

    cart_db = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart_db:
        cart_db = Cart(user_id=user_id)
        db.add(cart_db)
        db.commit()
        db.refresh(cart_db)

    product_db = db.query(Product).filter(Product.id == item_data.product_id).first()
    if not product_db:
        raise HTTPException(status_code=404, detail='Product not found')

    product_item_db = db.query(CartItem).filter(CartItem.cart_id == cart_db.id,
                                                CartItem.product_id == item_data.product_id).first()
    if product_item_db:
        raise HTTPException(status_code=404, detail='Product already exists in the cart')

    cart_item_db = CartItem(cart_id=cart_db.id, product_id=item_data.product_id)
    db.add(cart_item_db)
    db.commit()
    db.refresh(cart_item_db)
    return cart_item_db


@cart_router.delete('/{product_id}/')
async def product_delete(product_id: int, user_id: int, db: Session = Depends(get_db)):
    cart_db = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart_db:
        raise HTTPException(status_code=404, detail='Cart not found')

    cart_item_db = db.query(CartItem).filter(CartItem.cart_id == cart_db.id,
                                             CartItem.product_id == product_id).first()
    if not cart_item_db:
        raise HTTPException(status_code=404, detail='Product not found')

    db.delete(cart_item_db)
    db.commit()
    return {'message': 'Product is deleted'}
