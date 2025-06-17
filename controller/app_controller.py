def api_controller(app):
    from controller.direct_debit_router import direct_debit_router
    from controller.e_wallet_router import e_wallet_router
    from controller.transaction_router import transaction_router

    app.include_router(direct_debit_router, prefix='/direct_debit', tags=['Direct Debit'])
    app.include_router(e_wallet_router, prefix='/e_wallet', tags=['eWallets'])
    app.include_router(transaction_router, prefix='/transaction', tags=['Transactions'])
