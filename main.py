import os

import lambdawarmer
from controller.app_controller import api_controller
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from lambda_decorators import cors_headers
from mangum import Mangum

STAGE = os.environ.get('STAGE')
root_path = f'/{STAGE}' if STAGE else '/'

app = FastAPI(
    root_path=root_path,
    title='Serverless API',
    contact={
        'name': 'Arnel Jan Sarmiento',
        'email': 'rneljan@gmail.com',
    },
)


@app.get('/', include_in_schema=False)
def welcome():
    html_content = """
    <html>
        <head>
            <title>Serverless API</title>
        </head>
        <body>
            <h1>Serverless API</h1>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content, status_code=200)


api_controller(app)
mangum_handler = Mangum(app, lifespan='off')


@cors_headers
@lambdawarmer.warmer
def handler(event, context):
    return mangum_handler(event, context)
