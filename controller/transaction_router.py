from fastapi import APIRouter

from model.common import Message
from model.transaction.transaction import (
    GetTransactionDetailsIn,
    GetTransactionDetailsOut,
)
from usecase.transaction_usecase import TransactionUsecase

transaction_router = APIRouter()


@transaction_router.post(
    '/fees',
    response_model=GetTransactionDetailsOut,
    responses={
        400: {'model': Message, 'description': 'Bad request'},
        500: {'model': Message, 'description': 'Internal server error'},
    },
    summary='Get Transaction total for fees',
)
@transaction_router.post(
    '/fees/',
    response_model=GetTransactionDetailsOut,
    response_model_exclude_none=True,
    response_model_exclude_unset=True,
    include_in_schema=False,
)
def get_transaction_details(
    transaction_details_in: GetTransactionDetailsIn,
):
    transaction_usecase = TransactionUsecase()
    return transaction_usecase.get_transaction_details(transaction_details_in)
