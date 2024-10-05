from enum import Enum


class OrderStatus(Enum):
    pending = 'pending'
    shipping = 'shipping'
    delivered = 'delivered'

    @classmethod
    def get_status(cls):
        return (
            (i.name, i.value) for i in cls
        )
