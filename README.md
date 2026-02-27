# Serverless API Starter

A serverless REST API implemented with Clean Architecture and Domain Driven Design.

## Architecture

This project follows the [clean architecture style](http://blog.thedigitalcatonline.com/blog/2016/11/14/clean-architectures-in-python-a-step-by-step-example/) and has structured the codebase accordingly.

![cleanArchitecture image](https://cdn-images-1.medium.com/max/1600/1*B7LkQDyDqLN3rRSrNYkETA.jpeg)

_Image credit to [Thang Chung under MIT terms](https://github.com/thangchung/blog-core)_

### Most Important Rule:

> Source code dependencies can only point inward. Nothing in an inner circle can know anything about something in an outer circle. In particular, the name of something declared in an outer circle must not be mentioned by the code in an inner circle. That includes functions and classes, variables, or any other named software entity.

## Setup Local Environment

1. **Pre-requisites:**
   - Ensure Python 3.10 is installed

2. **Install pipenv:**
   ```shell
   pip install pipenv==2023.4.29 --user
   ```

3. **Install Python Dependencies:**
   ```shell
   pipenv install
   ```

4. **Activate Virtual Environment:**
   ```shell
   pipenv shell
   ```

5. **Add Environment Variables:**
    -  Add the `.env` file provided to you in the `backend` directory

## Run Locally

1. **Activate Virtual Environment:**
   ```shell
   pipenv shell
   ```

2. **Start Local Server:**
   ```shell
   uvicorn main:app --reload --log-level debug --env-file .env
   ```

## Setup AWS CLI

1. **Download and Install AWS CLI:**
   - [AWS CLI Installation Guide](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

2. **Create AWS Profile:**
   ```shell
   aws configure --profile {profile}
   ```

   - **Input your AWS Access Key ID and AWS Secret Access Key provided to you.**
   - **Input `ap-southeast-1` for the default region name.**
   - **Leave blank for the default output format.**


## Setup Serverless Framework

1. **Pre-requisites:**
   - Ensure `Node 14` or later is installed

2. **Install serverless framework:**
   ```shell
   npm install -g serverless
   ```

3. **Install serverless plugins:**
   ```shell
   npm install
   ```

3. **Install Python Requirements Plugin:**
   ```shell
   sls plugin install -n serverless-python-requirements
   ```

## Deploy to AWS
1. Setup Docker (Only for Non-Linux Users)
   - [Docker Installation Guide](https://docs.docker.com/engine/install)
   - Make sure Docker is Running on your Machine
2.
   ```shell
   pipenv shell
   ```
3.
   ```shell
   serverless deploy --stage 'dev' --aws-profile {profile} --verbose
   ```

## Resources

- [FastAPI](https://fastapi.tiangolo.com/)
- [Serverless Framework Documentation](https://www.serverless.com/framework/docs)
- [Clean Coder Blog](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
---

# AWS, Auth & Readability QA Lead

1) AWS SSO — configure and verify (profile: `techtix`)

```powershell
aws configure sso --profile techtix      # run interactively, supply SSO URL/region/account/role
aws sso login --profile techtix
aws sts get-caller-identity --profile techtix
```

Set runtime profile for processes:

```powershell
export AWS_PROFILE=techtix
```

Confirm SSM access (example):

```powershell
aws ssm get-parameter --name /techtix/callback-base-url-dev --region ap-southeast-1 --profile techtix
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


### prepare
```powershell
pip install uv
uv sync
```
### authenticate
```powershell
aws sso login --profile techtix
export AWS_PROFILE=techtix
```

### generate .env and run
```powershell
python scripts/generate-env.py -s dev
python main.py
```

7) Verify secret retrieval (quick):

```powershell
python -c "from utils.utils import Utils; print(Utils.get_secret('dev-xendit-api-key'))"
```