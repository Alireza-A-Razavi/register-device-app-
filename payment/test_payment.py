# from django.conf import settings
# from mollie.api.client import Client
# from mollie.api.error import NotFoundError

# mollie_client = Client()
# mollie_client.set_api_key(settings.MOLLIE_API_KEY)

# def create_payment(value, redirectUrl, webhookUrl, desc=None,):
#     payment = mollie_client.payments.create({
#         'amount': {
#             'currency': 'EUR',
#             'value': f'{value}' 
#         },
#         'description': f'{desc}',
#         'redirectUrl': f'{redirectUrl}',
#         'webhookUrl': f'{webhookUrl}',
#     })
#     return payment

# def get_payment(payment_id):
#     try:
#         return {
#             "status": "Success",
#             "paymen": mollie_client.payments.get(payment_id),
#             "message": "Received the payment."
#         }
#     except NotFoundError:
#         return {
#             "status": "Failed",
#             "paymen": None,
#             "message": "A payment with that Id doesn't exist."
#         }