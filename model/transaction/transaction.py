from decimal import Decimal
from typing import Union, Optional, TypeAlias

from pydantic import BaseModel, Extra, Field
from typing_extensions import Annotated

from model.payment.payment_constants import (
    DirectDebitChannels,
    EWalletChannels,
    PaymentMethod,
)


Price: TypeAlias = Annotated[Decimal, Field(decimal_places=2)]


class GetTransactionDetailsIn(BaseModel):
    class Config:
        extra = Extra.forbid

    ticket_price: Price
    payment_method: PaymentMethod = Field(..., title='Payment Method')
    payment_channel: Union[DirectDebitChannels, EWalletChannels] = Field(..., title='Payment Channel')


class GetTransactionDetailsOut(BaseModel):
    class Config:
        extra = Extra.ignore

    ticket_price: Price
    transaction_fee: Price
    total_price: Price
