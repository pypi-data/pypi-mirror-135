from abc import ABC
from models import WebhookData

class A(ABC):
    def __init__(self):
        setattr(self, 'val', 1)


class B(A):
    __slots__ = ('val')

w = WebhookData({'amount': 10})
b = B()

print(w.__dict__)