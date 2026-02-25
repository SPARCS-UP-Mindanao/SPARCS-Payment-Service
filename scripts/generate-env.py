import argparse
import os

import boto3
from botocore.exceptions import ClientError


class PaymentServiceConfigAssembler:
    """
    Assembles the Payment Service config file
    """

    def __init__(self, aws_region, environment):
        self.__input_environment = environment
        self.__project_name = 'sparcs-events'

        # Determine the deployment stage, defaulting to 'dev' for None or 'local' environments
        if not self.__input_environment or self.__input_environment == 'local':
            self.__stage = 'dev'
        else:
            self.__stage = self.__input_environment

        self.__region = 'ap-southeast-1'
        self.__ssm_client = boto3.client('ssm', region_name=self.__region)
        self.__secrets_client = boto3.client('secretsmanager', region_name=self.__region)
        self.__aws_account_id = self.__sts_client.get_caller_identity()['Account']
        self.__base_dir = os.getcwd()

    def __get_parameter(self, key, decrypt=False) -> str:
        """
        Retrieves parameter values from SSM

        :param key: key of parameter value to be retrieved
        :param decrypt: flag if value is decrypted
        :return: parameter value string
        """
        kwargs = {'Name': key, 'WithDecryption': decrypt}
        value = ''
        try:
            resp = self.__ssm_client.get_parameter(**kwargs)
        except ClientError as e:
            print(f'Error: {e.response["Error"]["Code"]} - {key}')
        else:
            value = resp['Parameter']['Value']
        return value

    def __get_secret(self, secret_arn) -> str:
        """
        Retrieves secret value from AWS Secrets Manager

        :param secret_arn: ARN of the secret to retrieve
        :return: secret value string
        """
        try:
            resp = self.__secrets_client.get_secret_value(SecretId=secret_arn)
            return resp['SecretString']
        except ClientError as e:
            print(f'Error retrieving secret: {e.response["Error"]["Code"]} - {secret_arn}')
            return ''

    @staticmethod
    def escape_env_value(value: str) -> str:
        return value.replace('$', '$$')

    @staticmethod
    def write_config(file_handle, key, value) -> None:
        """
        Writes specified config key-value in the config file

        :param file_handle: File pointer
        :param key: key of config
        :param value: value of config
        :return: None
        """
        entry = f'{key}={PaymentServiceConfigAssembler.escape_env_value(str(value))}\n'
        file_handle.write(entry)

    def construct_config_file(self) -> None:
        """
        Constructs the config file for Payment Service

        :return: None
        """
        stage = self.__stage
        parameter_store_prefix = '/techtix/'

        if self.__input_environment == 'test' or stage == 'test':
            # Placeholder for email service specific test values
            pass
        else:
            # Retrieve parameters from SSM Parameter Store for non-local environments
            pass

        config_file = f'{self.__base_dir}/.env'

        # Derived variables
        region = self.__region
        # Removed entities_table, email_queue, registrations_table as they are not payment service specific environment variables in serverless.ts
        xendit_api_key_secret_name = f'{stage}-xendit-api-key'
        sqs_queue_url = (
            f'https://sqs.{region}.amazonaws.com/{self.__aws_account_id}/{stage}-durianpy-events-payment-queue.fifo'
        )

        # Variables from SSM or placeholders
        callback_base_url = ''

        if self.__input_environment == 'test' or stage == 'test':
            callback_base_url = 'http://localhost:5173/'
        else:
            parameter_store_prefix = '/techtix'

            callback_base_url = self.__get_parameter(
                f'{parameter_store_prefix}/callback-base-url-{self.__stage}', decrypt=False
            )

        with open(config_file, 'w', encoding='utf-8') as file_handle:
            self.write_config(file_handle, 'REGION', region)
            self.write_config(file_handle, 'STAGE', stage)
            self.write_config(file_handle, 'XENDIT_API_KEY_SECRET_NAME', xendit_api_key_secret_name)
            self.write_config(file_handle, 'CALLBACK_BASE_URL', callback_base_url)
            self.write_config(file_handle, 'SQS_QUEUE_URL', sqs_queue_url)

        print(f'Configuration file created successfully at: {config_file}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Payment Service Configuration Assembler')
    parser.add_argument('-r', '--region', help='AWS Region (default: ap-southeast-1)')
    parser.add_argument('-s', '--stage', help='Environment Name (default: dev)')
    args = parser.parse_args()

    print('Arguments:', args)
    region = args.region
    input_stage = args.stage

    config_assembler = PaymentServiceConfigAssembler(region, input_stage)
    config_assembler.construct_config_file()
