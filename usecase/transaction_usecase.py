from sympy import Eq, solve, symbols

from model.payment.payment_constants import EWalletChannels, PaymentMethod
from model.transaction.transaction import (
    GetTransactionDetailsIn,
    GetTransactionDetailsOut,
)


class TransactionUsecase:
    def get_transaction_details(self, get_transaction_details_in: GetTransactionDetailsIn):
        e_wallet_fee_map = {EWalletChannels.GCASH.value: 0.023, EWalletChannels.PAYMAYA.value: 0.018}
        ticket_price = get_transaction_details_in.ticket_price
        vat = 0.12

        # Define the symbol P (the price we want to find)
        P = symbols('P')

        if get_transaction_details_in.payment_method == PaymentMethod.E_WALLET.value:
            transaction_fee_percentage = e_wallet_fee_map.get(get_transaction_details_in.payment_channel)
            transaction_fee = P * transaction_fee_percentage

        elif get_transaction_details_in.payment_method == PaymentMethod.DIRECT_DEBIT.value:
            transaction_fee_percentage = 0.01
            default_fee = 15

            # 1500 (1% == default_fee) - 15 (default_fee) - (1.8) default_fee * vat
            min_ticket_price_for_default = 1483.2

            is_fee_greater_than_default = ticket_price > min_ticket_price_for_default
            transaction_fee = (P * transaction_fee_percentage) if is_fee_greater_than_default else default_fee

        equation = Eq(P - transaction_fee - (transaction_fee * vat), ticket_price)

        # Solve the equation for P
        total_price = solve(equation, P)[0]
        transaction_fee = total_price - ticket_price

        return GetTransactionDetailsOut(
            ticket_price=round(ticket_price, 2),
            total_price=round(total_price, 2),
            transaction_fee=round(transaction_fee, 2),
        )
