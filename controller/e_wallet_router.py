from fastapi import APIRouter

from model.common import Message
from model.payment.payment import EWalletPaymentIn, PaymentRequestOut
from usecase.payment_usecase import PaymentUsecase

e_wallet_router = APIRouter()


@e_wallet_router.post(
    '/payment_method',
    response_model=PaymentRequestOut,
    responses={
        400: {'model': Message, 'description': 'Bad request'},
        500: {'model': Message, 'description': 'Internal server error'},
    },
    summary='Create EWallet Payment Request',
)
@e_wallet_router.post(
    '/payment_method/',
    response_model=PaymentRequestOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    include_in_schema=False,
)
def create_ewallet_payment_request(
    create_ewallet_payment_request_in: EWalletPaymentIn,
):
    payment_usecase = PaymentUsecase()
    return payment_usecase.e_wallet_payment_request(create_ewallet_payment_request_in)
