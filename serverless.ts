import type { AWS } from '@serverless/typescript';
import packageConfig from "./resources/package";
import functionConfig from "./resources/api";

const serverlessConfiguration: AWS = {
  "service": "techtix-payment",
  "custom": {
    "projectName": "techtix",
    "serviceName": "paymentService",
    "stage": "${opt:stage, self:provider.stage}",
    "pythonRequirements": {
      "dockerizePip": "non-linux",
      "noDeploy": [
        "requests",
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
      "USER_POOL_ID": {
        "!ImportValue": "UserPoolId-${self:custom.stage}"
      },
      "USER_POOL_CLIENT_ID": {
        "!ImportValue": "AppClientId-${self:custom.stage}"
      }
    },
    "logs": {
      "restApi": true
    }
  },
  "functions": functionConfig,
  "plugins": [
    "serverless-python-requirements",
    "serverless-iam-roles-per-function"
  ]
}

module.exports = serverlessConfiguration;
