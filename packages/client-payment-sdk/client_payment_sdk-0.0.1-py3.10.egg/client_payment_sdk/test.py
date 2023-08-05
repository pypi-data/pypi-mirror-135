from client_payment_sdk import Webhook, WebhookData, SignatureVerificationError


api_secret = 'aa21444f3f71'

payload = {
    'amount': '50.0000',
    'currency': 'RUB',
    'customer_fee': '0.0000',
    'invoice_id': '811',
    'masked_pan': '411111XXXXXX1111',
    'merchant_id': '15',
    'order': '241eeda4-7491-11ec-9c7f-0242ac130024',
    'product_id': '17',
    'signature': 'TKb9K1AtITVTPsOg6lFj7nruot-BD-UyUypOlxcLQUM',
    'status': 'complete',
    'webhook_id': '405',
    'webhook_type': 'invoice'
}

data = WebhookData(payload)
print(Webhook.verify_signature('/webhooks', 'POST', data, api_secret))