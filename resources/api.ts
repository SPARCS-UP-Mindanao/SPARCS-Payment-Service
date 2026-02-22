const functionConfig = {
  app: {
    handler: "main.handler",
    environment: {
      STAGE: "${self:custom.stage}",
    },
    layers: [{ Ref: "PythonRequirementsLambdaLayer" }],
    events: [
      {
        http: {
          path: "/",
          method: "get",
          cors: true,
        },
      },
      {
        http: {
          path: "/{proxy+}",
          method: "any",
          cors: true,
        },
      },
    ],
    iamRoleStatements: [
      {
        Effect: "Allow",
        Action: ["ssm:GetParameter"],
        Resource:
          "arn:aws:ssm:*:*:parameter/${self:custom.stage}-xendit-api-key",
      },
    ],
  },
  cronPaymentProcessor: {
    handler: "functions.payment_tracking_handler.handler",
    environment: {
      STAGE: "${self:custom.stage}",
      SQS_QUEUE_URL: "${self:custom.sqsQueueUrl}",
    },
    layers: [{ Ref: "PythonRequirementsLambdaLayer" }],
    events: [
      {
        schedule: {
          rate: ["rate(10 minutes)"],
          enabled: true,
        },
      },
    ],
    iamRoleStatements: [
      {
        Effect: "Allow",
        Action: ["ssm:GetParameter"],
        Resource:
          "arn:aws:ssm:*:*:parameter/${self:custom.stage}-xendit-api-key",
      },
      {
        Effect: "Allow",
        Action: [
          "sqs:SendMessage",
          "sqs:GetQueueAttributes",
          "sqs:GetQueueUrl",
        ],
        Resource: "${self:custom.sqsQueueArn}",
      },
    ],
  },
};

export default functionConfig;
