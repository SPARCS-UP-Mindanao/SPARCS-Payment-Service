from pprint import pprint
from uuid import uuid4

import xendit
from xendit.apis import CustomerApi, PaymentMethodApi, PaymentRequestApi
from xendit.customer.model.country_code import CountryCode
from xendit.customer.model.customer_request import CustomerRequest
from xendit.customer.model.individual_detail import IndividualDetail


def ewallet_payment_request():
    xendit_api_key = 'xnd_development_kCZQnq8jmVHn3TmwExDuA2lH2TmWhlC4g2dSJnliUgVxdAkzNV9qdWqsDwem'

    # See configuration.py for a list of all supported configuration parameters.
    xendit.set_api_key(xendit_api_key)

    # Enter a context with an instance of the API client
    api_client = xendit.ApiClient()

    # Create an instance of the API class# Enter a context with an instance of the API client
    # Create an instance of the API class
    api_instance = PaymentRequestApi(api_client)
    idempotency_key = str(uuid4())
    reference_id = str(uuid4())
    payment_request_parameters = {
        'country': 'PH',
        'amount': 50,
        'currency': 'PHP',
        'reference_id': reference_id,
        'payment_method': {
            'type': 'EWALLET',
            'ewallet': {
                'channel_properties': {
                    'success_return_url': 'http://localhost:5173',
                    'failure_return_url': 'http://localhost:5173',
                },
                'channel_code': 'GCASH',
            },
            'reusability': 'ONE_TIME_USE',
        },
    }

    try:
        # Create Payment Request
        api_response = api_instance.create_payment_request(
            idempotency_key=idempotency_key, payment_request_parameters=payment_request_parameters
        )
        pprint(api_response)
    except xendit.XenditSdkException as e:
        print('Exception when calling PaymentRequestApi->create_payment_request: %s\n' % e)


def create_customer(email: str, given_names: str, surname: str, nationality: CountryCode):
    xendit_api_key = 'xnd_development_kCZQnq8jmVHn3TmwExDuA2lH2TmWhlC4g2dSJnliUgVxdAkzNV9qdWqsDwem'

    # See configuration.py for a list of all supported configuration parameters.
    xendit.set_api_key(xendit_api_key)

    # Enter a context with an instance of the API client
    api_client = xendit.ApiClient()

    idempotency_key = str(uuid4())
    reference_id = str(uuid4())

    # Create an instance of the API class
    api_instance = CustomerApi(api_client)
    customer_request = CustomerRequest(
        reference_id=reference_id,
        email=email,
        type='INDIVIDUAL',
        individual_detail=IndividualDetail(given_names=given_names, surname=surname, nationality=nationality),
    )

    try:
        # Create Customer
        api_response = api_instance.create_customer(idempotency_key=idempotency_key, customer_request=customer_request)
        pprint(api_response)
        customer_id = api_response.id
        return customer_id

    except xendit.XenditSdkException as e:
        print('Exception when calling CustomerApi->create_customer: %s\n' % e)

    return None


def create_payment_method(given_names: str, surname: str, email: str, success_return_url: str, failure_return_url: str):
    xendit_api_key = 'xnd_development_kCZQnq8jmVHn3TmwExDuA2lH2TmWhlC4g2dSJnliUgVxdAkzNV9qdWqsDwem'

    # See configuration.py for a list of all supported configuration parameters.
    xendit.set_api_key(xendit_api_key)

    reference_id = str(uuid4())

    # Enter a context with an instance of the API client
    api_client = xendit.ApiClient()

    # Create an instance of the API class
    api_instance = PaymentMethodApi(api_client)
    payment_method_parameters = {
        'type': 'DIRECT_DEBIT',
        'direct_debit': {
            'channel_code': 'BPI',
            'channel_properties': {
                'success_return_url': 'https://redirect.me/success',
                'failure_return_url': 'https://redirect.me/failure',
                'email': email,
            },
        },
        'customer': {
            'reference_id': reference_id,
            'type': 'INDIVIDUAL',
            'individual_detail': {
                'given_names': given_names,
                'surname': surname,
            },
        },
        'reusability': 'ONE_TIME_USE',
    }  # PaymentMethodParameters

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Creates payment method
        api_response = api_instance.create_payment_method(payment_method_parameters=payment_method_parameters)
        pprint(api_response)
        return api_response.id
    except xendit.XenditSdkException as e:
        print('Exception when calling PaymentMethodApi->create_payment_method: %s\n' % e)

    return None


def direct_debit_payment(payment_method_id: str, callback_url: str):
    idempotency_key = str(uuid4())
    reference_id = str(uuid4())
    xendit_api_key = 'xnd_development_kCZQnq8jmVHn3TmwExDuA2lH2TmWhlC4g2dSJnliUgVxdAkzNV9qdWqsDwem'

    # See configuration.py for a list of all supported configuration parameters.
    xendit.set_api_key(xendit_api_key)

    # Enter a context with an instance of the API client
    api_client = xendit.ApiClient()

    # Create an instance of the API class
    api_instance = PaymentRequestApi(api_client)
    payment_request_parameters = {
        'reference_id': reference_id,
        'amount': 50,
        'currency': 'PHP',
        'payment_method_id': payment_method_id,
        'enable_otp': False,
        'callback_url': callback_url,
    }

    try:
        # Create Payment Request
        api_response = api_instance.create_payment_request(
            idempotency_key=idempotency_key, payment_request_parameters=payment_request_parameters
        )
        pprint(api_response)
    except xendit.XenditSdkException as e:
        print('Exception when calling PaymentRequestApi->create_payment_request: %s\n' % e)


def main():
    ewallet_payment_request()

    # create_customer(
    #     email="rneljan@gmail.com",
    #     given_names="Rnel",
    #     surname="Jan",
    #     nationality=CountryCode("PH")

    # create_payment_method(
    #     given_names='Rnel',
    #     surname='Jan',
    #     email='rneljan@gmail.com',
    #     success_return_url='http://localhost:5173',
    #     failure_return_url='http://localhost:5173',
    # )
    # direct_debit_payment('pm-fd8b1cd5-6002-4eb0-8b9e-41faac5d36fa', 'http://localhost:5173')


if __name__ == '__main__':
    main()
