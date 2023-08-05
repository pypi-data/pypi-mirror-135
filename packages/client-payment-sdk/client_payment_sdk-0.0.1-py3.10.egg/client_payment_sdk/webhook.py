from copy import deepcopy
from .sign import sign
from .models import WebhookData
from .exceptions import SignatureVerificationError, PassedTypeError


class Webhook:
    @staticmethod
    def verify_signature(endpoint, method, data, secret):
        if not isinstance(data, WebhookData):
            raise PassedTypeError('data must be WebhookData')

        payload = deepcopy(data.to_dict())
        del payload['signature']

        if sign(endpoint, method, payload, secret) not in data.signature:
            raise SignatureVerificationError('signatures not match')

        return True

