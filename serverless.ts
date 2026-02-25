import type { AWS } from "@serverless/typescript";
import packageConfig from "./resources/package.ts";
import functionConfig from "./resources/api.ts";

const serverlessConfiguration: AWS = {
  service: "techtix-payment",
  custom: {
    projectName: "techtix",
    serviceName: "paymentService",
    stage: "${opt:stage, self:provider.stage}",
    sqsQueueArn:
      "arn:aws:sqs:${aws:region}:${aws:accountId}:${self:custom.stage}-${self:custom.projectName}-events-payment-queue.fifo",
    sqsQueueUrl:
      "https://sqs.${aws:region}.amazonaws.com/${aws:accountId}/${self:custom.stage}-${self:custom.projectName}-events-payment-queue.fifo",
    pythonRequirements: {
      dockerizePip: "non-linux",
      noDeploy: ["boto3", "botocore"],
      layer: {
        name: "${self:custom.serviceName}-events-${self:custom.stage}-python-requirements",
        compatibleRuntimes: ["python3.10"],
        slim: true,
      },
    },
  },
  package: packageConfig,
  provider: {
    name: "aws",
    runtime: "python3.10",
    stage: "dev",
    region: "ap-southeast-1",
    memorySize: 3008,
    versionFunctions: false,
    timeout: 30,
    apiGateway: {
      resourcePolicy: [
        {
          Effect: "Allow",
          Action: "execute-api:Invoke",
          Principal: "*",
          Resource: "execute-api:/*/*/*",
        },
      ],
    },
    environment: {
      REGION: "${self:provider.region}",
      STAGE: "${self:custom.stage}",
      XENDIT_API_KEY_SECRET_NAME: "${self:custom.stage}-xendit-api-key",
      CALLBACK_BASE_URL:
        "${ssm:/techtix/callback-base-url-${self:custom.stage}}",
      SQS_QUEUE_URL: "${self:custom.sqsQueueUrl}",
    },
    logs: {
      restApi: {
        role: {
          "Fn::GetAtt": ["ApiGatewayCloudWatchRole", "Arn"],
        },
      },
    },
  },
  functions: {
    ...functionConfig,
  },
  resources: {
    Resources: {
      ApiGatewayCloudWatchRole: {
        Type: "AWS::IAM::Role",
        Properties: {
          RoleName:
            "serverlessApiGatewayCloudWatchRole-${self:custom.serviceName}-${self:custom.stage}",
          AssumeRolePolicyDocument: {
            Version: "2012-10-17",
            Statement: [
              {
                Effect: "Allow",
                Principal: {
                  Service: "apigateway.amazonaws.com",
                },
                Action: "sts:AssumeRole",
              },
            ],
          },
          Policies: [
            {
              PolicyName: "AllowCloudWatchLogs",
              PolicyDocument: {
                Version: "2012-10-17",
                Statement: [
                  {
                    Effect: "Allow",
                    Action: [
                      "logs:CreateLogGroup",
                      "logs:CreateLogStream",
                      "logs:DescribeLogGroups",
                      "logs:DescribeLogStreams",
                      "logs:PutLogEvents",
                    ],
                    Resource: "*",
                  },
                ],
              },
            },
          ],
        },
      },
      PaymentServiceApiEndpointParameter: {
        Type: "AWS::SSM::Parameter",
        Properties: {
          Name: "/techtix/payments-api-url-${self:custom.stage}",
          Type: "String",
          Value: {
            "Fn::Join": [
              "",
              [
                "https://",
                { Ref: "ApiGatewayRestApi" },
                ".execute-api.",
                { Ref: "AWS::Region" },
                ".amazonaws.com/",
                "${self:provider.stage}",
              ],
            ],
          },
        },
      },
    },
    Outputs: {
      ApiGatewayCloudWatchRoleArn: {
        Value: { "Fn::GetAtt": ["ApiGatewayCloudWatchRole", "Arn"] },
        Export: {
          Name: "ApiGatewayCloudWatchRole-${self:custom.serviceName}-${self:custom.stage}",
        },
      },
    },
  },
  plugins: [
    "serverless-better-credentials",
    "serverless-python-requirements",
    "serverless-iam-roles-per-function",
  ],
};

export = serverlessConfiguration;
