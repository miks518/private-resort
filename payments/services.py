"""
PayMongo API integration service.
Handles creating checkout sessions and processing webhooks.
"""

import base64
import requests
from django.conf import settings

PAYMONGO_API_URL = 'https://api.paymongo.com/v1'


def _get_headers():
    """Build PayMongo authorization headers using secret key."""
    secret_key = settings.PAYMONGO_SECRET_KEY
    encoded = base64.b64encode(f'{secret_key}:'.encode()).decode()
    return {
        'Authorization': f'Basic {encoded}',
        'Content-Type': 'application/json',
        'Accept': 'application/json',
    }


def create_checkout_session(payment, success_url, cancel_url):
    """
    Create a PayMongo Checkout Session (Process 3.2).
    Returns the checkout URL for the customer to complete payment.
    Supports GCash, Maya, and Cards.
    """
    payload = {
        'data': {
            'attributes': {
                'send_email_receipt': True,
                'show_description': True,
                'show_line_items': True,
                'description': f'Reservation #{payment.reservation.pk} at {payment.reservation.facility.name}',
                'line_items': [
                    {
                        'currency': 'PHP',
                        'amount': int(payment.amount * 100),  # PayMongo uses centavos
                        'name': f'{payment.reservation.facility.name} '
                                f'({payment.reservation.check_in} to {payment.reservation.check_out})',
                        'quantity': 1,
                    }
                ],
                'payment_method_types': ['gcash', 'grab_pay', 'card', 'paymaya'],
                'success_url': success_url,
                'cancel_url': cancel_url,
                'reference_number': f'RES-{payment.reservation.pk}',
            }
        }
    }

    response = requests.post(
        f'{PAYMONGO_API_URL}/checkout_sessions',
        json=payload,
        headers=_get_headers(),
    )

    if response.status_code == 200:
        data = response.json()['data']
        checkout_id = data['id']
        checkout_url = data['attributes']['checkout_url']
        return checkout_id, checkout_url

    # Log the error for debugging
    return None, None


def retrieve_checkout_session(checkout_id):
    """Retrieve the status of a checkout session from PayMongo."""
    response = requests.get(
        f'{PAYMONGO_API_URL}/checkout_sessions/{checkout_id}',
        headers=_get_headers(),
    )

    if response.status_code == 200:
        return response.json()['data']

    return None
