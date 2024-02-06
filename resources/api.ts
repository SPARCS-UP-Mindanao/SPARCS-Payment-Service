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
              "dynamodb:*"
            ],
            "Resource": [
              { "Fn::GetAtt": ["Entities", "Arn"] }
            ]
          }
        ]
      }
}

export default functionConfig;
