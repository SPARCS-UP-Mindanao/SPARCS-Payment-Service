import json
import os
from http import HTTPStatus
from uuid import uuid4

import boto3

from external.payment_storage_gateway import PaymentStorageGateway
from model.payment.payment import PaymentTransactionOut, TransactionStatus
from model.payment.payment_constants import PaymentRequestConstants
from usecase.payment_usecase import PaymentUsecase
from utils.logger import logger


class PaymentTrackingUsecase:
    def __init__(self):
        self.payment_storage_gateway = PaymentStorageGateway()
        self.payment_usecase = PaymentUsecase()
        self.queue_url = os.environ.get('SQS_QUEUE_URL')
        self.sqs_client = boto3.client('sqs')

    def _send_payment_status_update_to_queue(self, payment: PaymentTransactionOut, status: TransactionStatus):
        """Send payment status update message to SQS queue"""
        try:
            logger.info(f'Sending payment status update to SQS: Transaction Status {status} for Payment {payment}')

            message_body = {
                'registration_details': payment.dict(),
                'status': status.value,
            }

            response = self.sqs_client.send_message(
                QueueUrl=self.queue_url,
                MessageBody=json.dumps(message_body),
                MessageGroupId=f'payment-{payment.entryId}',
                MessageDeduplicationId=f'payment-{payment.entryId}-{uuid4()}',
            )

            logger.info(f'Successfully sent message to SQS: {response["MessageId"]}')
            return True

        except Exception as e:
            logger.error(f'Failed to send message to SQS: {str(e)}')
            return False

    def track_pending_payments(self):
        """
        Track pending payments and send status updates to SQS queue

        Arguments:
            payment -- Payment transaction details
        """
        status, pending_payments, error_message = self.payment_storage_gateway.get_pending_payment_transactions()
        if status != HTTPStatus.OK:
            logger.error(f'Failed to get pending payments: {error_message}')
            return

        for payment in pending_payments:
            if not payment.paymentRequestId:
                logger.error(f'Payment {payment.entryId} has no payment request ID')
                continue

            payment_request_details = self.payment_usecase.get_payment_request_details(
                payment_request_id=payment.paymentRequestId,
            )
            payment_request_status = str(payment_request_details.status)

            if payment_request_status in PaymentRequestConstants.PENDING_STATUSES or not payment_request_status:
                logger.info(f'Payment {payment.entryId} is still pending')
                continue

            transaction_status = TransactionStatus.PENDING

            if payment_request_status in PaymentRequestConstants.SUCCESS_STATUSES:
                logger.info(f'Payment {payment.entryId} succeeded')
                transaction_status = TransactionStatus.SUCCESS

            elif payment_request_status in PaymentRequestConstants.ERROR_STATUSES:
                logger.info(f'Payment {payment.entryId} failed')
                transaction_status = TransactionStatus.FAILED

            else:
                logger.error(f'Payment {payment.entryId} has an unknown status: {payment_request_status}')
                continue

            result = self._send_payment_status_update_to_queue(payment, transaction_status)
            if not result:
                logger.error(f'Failed to send payment status update to SQS: {payment.entryId}')
                continue
