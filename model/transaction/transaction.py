from decimal import Decimal
from typing import Union

from pydantic import BaseModel, Extra, Field
from typing_extensions import Annotated

from model.payment.payment_constants import (
    DirectDebitChannels,
    EWalletChannels,
    PaymentMethod,
)


class GetTransactionDetailsIn(BaseModel):
    class Config:
        extra = Extra.forbid

    ticket_price: Annotated[Decimal, Field(decimal_places=2)]
    payment_method: PaymentMethod = Field(..., title='Payment Method')
    payment_channel: Union[DirectDebitChannels, EWalletChannels] = Field(..., title='Payment Channel')


class GetTransactionDetailsOut(BaseModel):
    class Config:
        extra = Extra.ignore

    ticket_price: Annotated[Decimal, Field(decimal_places=2)]
    transaction_fee: Annotated[Decimal, Field(decimal_places=2)]
    total_price: Annotated[Decimal, Field(decimal_places=2)]
