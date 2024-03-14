FROM python:3.9

# Copy function code
COPY ./app ${LAMBDA_TASK_ROOT}/app

# Install the function's dependencies using file requirements.txt
# from your project folder.

COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
# CMD [ "lambda.handler" ]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]