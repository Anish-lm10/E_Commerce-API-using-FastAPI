from fastapi import APIRouter, status, Depends, HTTPException
from auth_routes import user_dependency, get_current_user
from models import User, Order
from schemas import OrderModel, OrderStatusModel
from database import SessionLocal, engine

order_router = APIRouter(prefix="/orders", tags=["Orders"])

session = SessionLocal(bind=engine)


@order_router.get("/")
async def hello(user: user_dependency):
    """
    ## Sample Order Route
    This is sample order route to check routes.
    """
    return {"message": "hello orders"}


@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_an_order(
    order: OrderModel, user: user_dependency, username: str = Depends(get_current_user)
):
    """
    ## Placing an Order
    This requires following
    - quantity : Integer
    - order_size: String
    """
    current_user = username.get("username")
    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(order_size=order.order_size, quantity=order.quantity)

    new_order.user = user
    session.add(new_order)
    session.commit()
    response = {
        "order_size": new_order.order_size,
        "quantity": new_order.quantity,
        "id": new_order.user_id,
        "order_status": new_order.order_status,
    }
    return response


@order_router.get("/orders")
async def list_of_orders(
    user: user_dependency, username: str = Depends(get_current_user)
):
    """
    ## List of all Order
    This list all orders made, can be accessed by superuser
    """
    current_user = username.get("username")
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).all()

        return orders

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not superuser"
    )


@order_router.get("/order/{id}")
async def get_order_by_id(
    id: int, user: user_dependency, username: str = Depends(get_current_user)
):
    """
    ## Get Order by Id
    This is getting an order by its id and is only accessed by a superuser.
    """
    current_user = username.get("username")
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        orders = session.query(Order).filter(Order.order_id == id).first()

        return orders

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not superuser"
    )


@order_router.get("/user/orders")
async def get_user_order(
    user: user_dependency, username: str = Depends(get_current_user)
):
    """
    ## Get Current User Order
    This list the order made by the current or logged in user.
    """
    current_user = username.get("username")

    user = session.query(User).filter(User.username == current_user).first()

    return user.orders


@order_router.get("/user/order/{order_id}")
async def get_user_specific_order(
    order_id: int, user: user_dependency, username: str = Depends(get_current_user)
):
    """
    ## Get Specific Order By Current Logged In User.
    This returns an order by id for the currently logged in user.
    """
    current_user = username.get("username")
    user = session.query(User).filter(User.username == current_user).first()

    orders = user.orders

    for order in orders:
        if order.order_id == order_id:
            return order

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, detail="No order Found with such id"
    )


@order_router.put("/order/update/{order_id}")
async def update_order(
    order_id: int,
    order: OrderModel,
    user: user_dependency,
    username: str = Depends(get_current_user),
):
    """
    ## Update an Order
    This update the order and requires following fields
    - quantity : Integer
    - order_size: String
    """
    order_to_update = session.query(Order).filter(Order.order_id == order_id).first()

    order_to_update.quantity = order.quantity
    order_to_update.order_size = order.order_size

    session.commit()

    response = {
        "quantity": order_to_update.quantity,
        "order_size": order_to_update.order_size,
    }

    return response


@order_router.patch("/order/update/{id}")
async def update_order_status(
    id: int,
    order: OrderStatusModel,
    user: user_dependency,
    username: str = Depends(get_current_user),
):
    """
    ## Updating an Order Status
    This can be done only by superuser and have following field
    - order_status : String
    """
    current_user = username.get("username")
    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        order_to_update = session.query(Order).filter(Order.order_id == id).first()

        order_to_update.order_status = order.order_status

        session.commit()

        response = {"Order_status": order_to_update.order_status}

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not superuser"
    )


@order_router.delete("/order/delete/{order_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(
    order_id: int, user: user_dependency, username: str = Depends(get_current_user)
):
    """
    ## Deleting an Order
    This deletes an order by its id.
    """
    order_to_delete = session.query(Order).filter(Order.order_id == order_id).first()

    session.delete(order_to_delete)

    session.commit()

    return order_to_delete
