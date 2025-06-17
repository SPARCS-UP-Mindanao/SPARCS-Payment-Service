const functionConfig = {
    app: {
        "handler": "main.handler",
        "environment": {
          "STAGE": "${self:custom.stage}"
        },
        "layers": [
          { "Ref": "PythonRequirementsLambdaLayer" }
        ],
        "events": [
          {
            "http": {
              "path": "/",
              "method": "get",
              "cors": true
            }
          },
          {
            "http": {
              "path": "/{proxy+}",
              "method": "any",
              "cors": true
            }
          }
        ],
        "iamRoleStatements": [
          {
            "Effect": "Allow",
            "Action": [
              "ssm:GetParameter"
            ],
            "Resource":
              "arn:aws:ssm:*:*:parameter/${self:custom.stage}-xendit-api-key"
          }
        ]
      }
}

export default functionConfig;
