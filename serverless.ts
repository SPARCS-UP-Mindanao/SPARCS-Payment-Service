import type { AWS } from '@serverless/typescript';
import packageConfig from "./resources/package.ts";
import functionConfig from "./resources/api.ts";

const serverlessConfiguration: AWS = {
  "service": "techtix-payment",
  "custom": {
    "projectName": "techtix",
    "serviceName": "paymentService",
    "stage": "${opt:stage, self:provider.stage}",
    "pythonRequirements": {
      "dockerizePip": "non-linux",
      "noDeploy": [
        "boto3",
        "botocore"
      ],
      "layer": {
        "name": "${self:custom.serviceName}-events-${self:custom.stage}-python-requirements",
        "compatibleRuntimes": [
          "python3.10"
        ],
      "slim": true
      }
    }
  },
  "package": packageConfig,
  "provider": {
    "name": "aws",
    "runtime": "python3.10",
    "stage": "dev",
    "region": "ap-southeast-1",
    "memorySize": 3008,
    "versionFunctions": false,
    "timeout": 30,
    "apiGateway": {
      "resourcePolicy": [
        {
          "Effect": "Allow",
          "Action": "execute-api:Invoke",
          "Principal": "*",
          "Resource": "execute-api:/*/*/*"
        }
      ]
    },
    "environment": {
      "REGION": "${self:provider.region}",
      "STAGE": "${self:custom.stage}",
      "XENDIT_API_KEY_SECRET_NAME": "${self:custom.stage}-xendit-api-key",
      "CALLBACK_BASE_URL": "${ssm:/techtix/callback-base-url-${self:custom.stage}}"
    },
    "logs": {
      "restApi": true
    }
  },
  "functions": {
    ...functionConfig
  },
  "plugins": [
    "serverless-better-credentials",
    "serverless-python-requirements",
    "serverless-iam-roles-per-function"
  ]
}

export = serverlessConfiguration;