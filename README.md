# SPARCS Payment Service

A serverless REST API implemented with Clean Architecture and Domain Driven Design.

## Architecture

This project follows the [clean architecture style](http://blog.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/) and has structured the codebase accordingly.

![cleanArchitecture image](https://cdn-images-1.medium.com/max/1600/1*B7LkQDyDqLN3rRSrNYkETA.jpeg)

_Image credit to [Thang Chung under MIT terms](https://github.com/thangchung/blog-core)_

## Folder Structure 
    .devcontainer/   # DevContainer configuration for consistent local setup
    .git/            # Git metadata
    .github/         # GitHub workflows and repo config
    constants/       # Application-wide constant values
    controller/      # Request handlers / API controllers
    external/        # Integrations with external services (e.g., AWS, third-party APIs)
    functions/       # Reusable business-related functions
    model/           # Data models and schemas
    resources/       # Static resources and configuration assets
    scripts/         # Utility and maintenance scripts
    usecase/         # Core business use cases and workflows
    utils/           # General helper utilities

## Best Practices
### Naming Conventions
Follow these conventions to keep the codebase consistent and readable:
- Classes: PascalCase
    - model/ – domain and data models
    - usecase/ – business use case classes
    - functions/ – function-based service classes
- Files: snake_case.py
    - Example: payment.py, transaction.py
- Variables & Functions: snake_case
    - Example: payment_id, process_payment(), create_payment()
- Constants: UPPER_SNAKE_CASE
    - Example: XENDIT_API_KEY_SECRET, CALLBACK_BASE_URL, ONE_TIME_USE

## Clean Architecture

### Dependencies

Dependencies must follow this direction only:
```controller -> usecase -> model```

#### Rules
- Controllers
    - Handle incoming requests
    - Call use cases
    - Contain no business logic
- Usecases
    - Contain core business logic
    - Orchestrate models and operations
    - Do not depend on controllers
- Models
    - Represent domain data and rules
    - Have no dependencies on higher layers

### Layer Responsibilities
- Controller (```controller/```)
    - Handles HTTP or external requests
    - Validates and parses input
    - Delegates execution to use cases
    - Formats and returns responses
    - Contains no business logic

- Usecases (```usecase/```)
    - Implements core business rules
    - Coordinates workflows and decisions
    - Calls models and helper functions
    - Remains independent of delivery mechanisms (HTTP, CLI, etc.)

- Models (```model/```)
    - Defines domain data structures
    - Enforces domain-level rules and validations
    - Has no knowledge of controllers or use cases

## AWS SSO Authentication

1) AWS SSO — configure and verify 

```bash
aws configure sso --profile <profile>      
aws sso login --profile <profile>
aws sts get-caller-identity --profile <profile>
```
Follow the prompt to open your browser and authorize your session. Once approved, your terminal will be authenticated and ready to interact with AWS resources.

Set runtime profile for processes:
```bash
export AWS_PROFILE=<profile>
```

2) Required environment variables (set these before running)

- `REGION`=ap-southeast-1          # AWS region for boto3
- `STAGE`=dev                      # deployment stage
- `XENDIT_API_KEY_SECRET_NAME`     # SSM name containing Xendit API key
- `CALLBACK_BASE_URL`              # base URL for payment/persistence endpoints
- `SQS_QUEUE_URL`                  # SQS FIFO queue URL for status messages
- `LOG_LEVEL`=INFO                 # optional, default DEBUG

3) Secrets access

- Runtime: call `Utils.get_secret(<SSM_NAME>)` (SSM Parameter Store, WithDecryption=True).
- For local scripts only: `XENDIT_API_KEY_SECRET` may hold plaintext API key (avoid committing).

4) Lightweight wrappers

- `Utils.get_secret(name)` — central SSM reader; use for all secrets.
- `PaymentStorageGateway` — HTTP adapter for persistence; all external HTTP calls go here.
- Recommendation: implement `PaymentProvider` interface and `XenditAdapter`, then inject into `usecase/payment_usecase.py`.

5) Cross-repo fixes (apply in repo)

- Standardize parameter prefix to `/techtix`.
- Update `scripts/generate-env.py` to accept `--region` and initialize an STS client.
- Use `XENDIT_API_KEY_SECRET_NAME` at runtime; reserve plaintext env keys for local helper scripts only.

6) Run (minimal, sequential)
### generate .env and run
```bash
python scripts/generate-env.py -s dev
```

7) Verify secret retrieval (quick):

```bash
python -c "from utils.utils import Utils; print(Utils.get_secret('dev-xendit-api-key'))"
```

## Deploy to AWS Lambda
If the Serverless framework is not yet installed in the container, install it and its plugins first:
```bash
npm install -g serverless
npm install
```
Then, deploy the service:
```bash
serverless deploy --stage 'dev' --aws-profile 'default'
```
**When/Why:** Run this command to deploy the Serverless configuration and Lambda functions to AWS.

## Resources
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Serverless Framework Documentation](https://www.serverless.com/framework/docs)
- [Clean Architecture by Uncle Bob](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Clean Architectures in Python](http://blog.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/)
