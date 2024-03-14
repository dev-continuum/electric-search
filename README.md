# electric-search
Electric Vehicles charging stations search service.

# Tech Stack
- Python 3.9
- FastAPI (for server deployment.)
- OpenSearch
- AWS Lambda

# Fast API Service.
## Run the test cases from CI.
    $export ACTIVE_ENVIRONMENT=test
    $python -m unittest discover -s tests

## How to build and run.?
    cd to /electric-search  directory.
### Build electric-search image locally.
```
$docker build -t <image_name> .
$docker image ls     - you must  see image with <image_name>

Ex. $docker image -t esearch .
```

### Run docker compose to bring up the all services.
```
$docker compose up -d
$docker ps -a     - you must see 3 container running opensearch-node1, opensearch-dashboard and electric-search-api 
```

Wait for sometime as it may take a while to bring up all service.

### Accessing Opensearch DevTools.
Open browser and try accessing Opensearch dashboard here,
    localhost:5601
And navigate DevTools from left side menu under "Management"

#### Indexing documents on Opensearch.
In DevTools 

Creating Index.

    PUT /charging_stations  
        
    {
      "settings": {
        "index": {
          "number_of_shards": 2,
          "number_of_replicas": 2
        }
      },
      "mappings": {
        "properties": {
          "name": {
            "type": "text"
          },
          "address": {
            "type": "text"
          },
          "pincode": {
            "type": "integer"
          },
          "point": {
            "type": "geo_point"
          }
        }
      },
      "aliases": {
        "sample-alias1": {}
      }
    }`

Indexing document.

    POST /charging_stations/_doc
    {
      "name": "Satwik Entergies Limited",
      "address": "Bangalore, Channasandra",
      "pincode": 560067,
      "point": [12.9789812857621, 77.76822537088698]
    }

Insert as many documents as you wish.

List documents,
    
    POST /charging_stations/_search?scroll=1m
    {
        "size": 100,
        "query": {
            "match_all": {}
        }
    }

### How to access search API?
Access swagger API doc her,

    localhost:8080/docs

Note: No authentication, will integrate soon.

### Lambda function.

Build image locally

    $docker build -t electric-search-lambda . -f lambda.Dockerfile

Tag and Push image to ECR

    $aws configure
    # authentica ecr from local.
    $aws ecr get-login-password --region ap-south-1 | docker login --username AWS --password-stdin 683563489644.dkr.ecr.ap-south-1.amazonaws.com
    $docker tag <docker_image_name:tag> <ecr_repo_url>:<tag_name>
    $docker push <ecr_repo_url>:<tag_name>    -- tag_name must be same as above.

Test lambda function local.

    $pip install python-lambda-local

    $python-lambda-local -l lib -f handler ./app/lambda.py test/event.json









