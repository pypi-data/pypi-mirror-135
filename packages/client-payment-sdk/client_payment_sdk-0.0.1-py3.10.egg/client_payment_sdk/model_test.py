# -*- coding: utf-8 -*-
from abc import ABC


class Model(ABC):
    # @classmethod
    # def from_dict(cls, model_dict):
    #     raise NotImplementedError

    def __init__(self, data):
        for key in data:
            setattr(self, key, data[key])

    def __repr__(self):
        state = ['%s=%s' % (k, repr(v)) for (k, v) in vars(self).items()]
        return '%s(%s)' % (self.__class__.__name__, ', '.join(state))


class InitPaymentResponse(Model, ABC):
    def __init__(self, status=None, payment_redirect_url=None, url=None, form_data=None):
        super(InitPaymentResponse, self).__init__()
        self.status = status
        self.payment_redirect_url = payment_redirect_url
        self.url = url
        self.form_data = form_data

    @classmethod
    def from_dict(cls, init_payment_dict):
        return cls(status=init_payment_dict['status'], url=init_payment_dict['url'])

    @classmethod
    def from_dict_sbp(cls, init_payment_dict):
        return cls(status=init_payment_dict['status'], payment_redirect_url=init_payment_dict['payment_redirect_url'])

    @classmethod
    def from_dict_h2h(cls, init_payment_dict):
        return cls(status=init_payment_dict['status'], url=init_payment_dict['url'],
                   form_data=init_payment_dict['form_data'])

    def to_dict(self):
        pass


class StatusPaymentResponse(Model, ABC):
    def __init__(self, status, payment_status, refund_status, last_payment_error_code=None, last_payment_error=None):
        super(StatusPaymentResponse, self).__init__()
        self.status = status
        self.payment_status = payment_status
        self.refund_status = refund_status
        self.last_payment_error_code = last_payment_error_code
        self.last_payment_error = last_payment_error

    @classmethod
    def from_dict(cls, status_payment_dict):
        return cls(status_payment_dict['status'], status_payment_dict['payment_status'],
                   status_payment_dict['refund_status'], status_payment_dict['last_payment_error_code'],
                   status_payment_dict['last_payment_error'])

    def to_dict(self):
        pass


class BalanceResponse(Model, ABC):
    def __init__(self, status, balance):
        super(BalanceResponse, self).__init__()
        self.status = status
        self.balance = balance

    @classmethod
    def from_dict(cls, balance_dict):
        return cls(balance_dict['status'], balance_dict['balance'])

    def to_dict(self):
        pass


class WithdrawalResponse(Model, ABC):
    def __init__(self, status, withdrawal_request):
        super(WithdrawalResponse, self).__init__()
        self.status = status
        self.withdrawal_request = withdrawal_request

    @classmethod
    def from_dict(cls, withdrawal_dict):
        return cls(withdrawal_dict['status'], withdrawal_dict['withdrawal_request'])

    def to_dict(self):
        pass


class StatusWithdrawalResponse(Model, ABC):
    def __init__(self, status, withdrawal_request):
        super(StatusWithdrawalResponse, self).__init__()
        self.status = status
        self.withdrawal_request = withdrawal_request

    @classmethod
    def from_dict(cls, status_withdrawal_dict):
        return cls(status_withdrawal_dict['status'], status_withdrawal_dict['withdrawal_request'])

    def to_dict(self):
        pass


class WebhookData:
    __slots__ = ('webhook_type', 'amount', 'product_id', 'merchant_id', 'order', 'currency', 'status', 'webhook_id',
                 'payment_error_code', 'payment_error', 'signature', 'withdrawal_request_id', 'requested_amount',
                 'invoice_id', 'customer_fee', 'masked_pan')


# class WebhookData(Model, ABC):
#     __slots__ = ('webhook_type', 'amount', 'product_id', 'merchant_id', 'order', 'currency', 'status', 'webhook_id',
#                  'payment_error_code', 'payment_error', 'signature', 'withdrawal_request_id', 'requested_amount',
#                  'invoice_id', 'customer_fee', 'masked_pan')
#
#     def __init__(self, webhook_type, amount, product_id, merchant_id, order, currency, status, webhook_id,
#                  payment_error_code, payment_error, signature, withdrawal_request_id=None, requested_amount=None,
#                  invoice_id=None, customer_fee=None, masked_pan=None):
#         super(WebhookData, self).__init__()
#
#
#         self.webhook_type = webhook_type
#         self.withdrawal_request_id = withdrawal_request_id
#         self.requested_amount = requested_amount
#         self.invoice_id = invoice_id
#         self.customer_fee = customer_fee
#         self.amount = amount
#         self.product_id = product_id
#         self.merchant_id = merchant_id
#         self.order = order
#         self.currency = currency
#         self.masked_pan = masked_pan
#         self.status = status
#         self.webhook_id = webhook_id
#         self.payment_error_code = payment_error_code
#         self.payment_error = payment_error
#         self.signature = signature
#
#     @classmethod
#     def from_dict(cls, webhook_data_dict):
#         withdrawal_request_id = None if 'withdrawal_request_id' not in webhook_data_dict else \
#             webhook_data_dict['withdrawal_request_id']
#         requested_amount = None if 'requested_amount' not in webhook_data_dict else \
#             webhook_data_dict['requested_amount']
#         masked_pan = None if 'masked_pan' not in webhook_data_dict else webhook_data_dict['masked_pan']
#         invoice_id = None if 'invoice_id' not in webhook_data_dict else webhook_data_dict['invoice_id']
#         customer_fee = None if 'customer_fee' not in webhook_data_dict else webhook_data_dict['customer_fee']
#
#         return cls(
#             webhook_type=webhook_data_dict['webhook_type'],
#             withdrawal_request_id=withdrawal_request_id,
#             requested_amount=requested_amount,
#             invoice_id=invoice_id,
#             customer_fee=customer_fee,
#             amount=webhook_data_dict['amount'],
#             product_id=webhook_data_dict['product_id'],
#             merchant_id=webhook_data_dict['merchant_id'],
#             order=webhook_data_dict['order'],
#             currency=webhook_data_dict['currency'],
#             masked_pan=masked_pan,
#             status=webhook_data_dict['status'],
#             webhook_id=webhook_data_dict['webhook_id'],
#             payment_error_code=webhook_data_dict['payment_error_code'],
#             payment_error=webhook_data_dict['payment_error'],
#             signature=webhook_data_dict['signature'])

class WebhookDebugResponse(Model, ABC):
    def __init__(self, status, url, method, signature, params):
        super(WebhookDebugResponse, self).__init__()
        self.status = status
        self.url = url
        self.method = method
        self.signature = signature
        self.params = params

    @classmethod
    def from_dict(cls, webhook_debug_dict):
        return cls(webhook_debug_dict['status'], webhook_debug_dict['url'], webhook_debug_dict['method'],
                   webhook_debug_dict['signature'], webhook_debug_dict['params'])

    def to_dict(self):
        pass
