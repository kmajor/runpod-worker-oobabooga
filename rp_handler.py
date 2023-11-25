import os
import json
import time
import requests
import runpod
from runpod.serverless.utils.rp_validator import validate
from runpod.serverless.modules.rp_logger import RunPodLogger
from requests.adapters import HTTPAdapter, Retry
from schemas.api import API_SCHEMA
from schemas.chat import CHAT_SCHEMA
from schemas.generate import GENERATE_SCHEMA
from schemas.token_count import TOKEN_COUNT_SCHEMA
from schemas.model import MODEL_SCHEMA
from schemas.chat_completions import CHAT_COMPLETIONS_SCHEMA

BASE_URL = 'http://127.0.0.1:5000/v1'
TIMEOUT = 600

VALIDATION_SCHEMAS = {
    'chat': CHAT_SCHEMA,
    'generate': GENERATE_SCHEMA,
    'token-count': TOKEN_COUNT_SCHEMA,
    'chat/completions': CHAT_COMPLETIONS_SCHEMA
}

# Fetch the authentication token from the environment variable

session = requests.Session()
retries = Retry(total=10, backoff_factor=0.1, status_forcelist=[502, 503, 504])
session.mount('http://', HTTPAdapter(max_retries=retries))
logger = RunPodLogger()


# ---------------------------------------------------------------------------- #
# Application Functions                                                        #
# ---------------------------------------------------------------------------- #
def wait_for_service(url):
    logger.log('Waiting for service to become available...', 'INFO')
    retries = 0

    while True:
        try:
            requests.get(url)
            logger.log('Service is now available.', 'INFO')
            return
        except requests.exceptions.RequestException:
            retries += 1

            # Only log every 15 retries so the logs don't get spammed
            if retries % 15 == 0:
                logger.log('Service not ready yet. Retrying...', 'INFO')
        except Exception as err:
            logger.log(f'Error: {err}', 'ERROR')

        time.sleep(0.2)


def send_get_request(endpoint):
    logger.log(f'Sending GET request to endpoint: {endpoint}', 'INFO')
    return session.get(
        url=f'{BASE_URL}/{endpoint}',
        timeout=TIMEOUT
    )

def transform_payload(response):
    logger.log(f"Dumping entire response object: {vars(response)}", 'INFO')
    
    # Initialize status and status_message
    status = 'failed'  # Default to 'failed'
    status_message = 'Unknown error'
    chat_response = None  # Initialize to None
    
    # Check if the response contains valid JSON
    try:
        response_data = response.json()
        
        # Extract the second value within 'internal', if it exists
        results = response_data.get('results', [])
        if results:
            history = results[0].get('history', {})
            internal = history.get('internal', [])
            if internal and len(internal[-1]) > 1:
                chat_response = internal[-1][1]
                
        if chat_response:
            status = 'received'
            status_message = 'Payload received successfully'
        else:
            status_message = 'Chat response is empty'
            
    except json.JSONDecodeError:
        logger.log(f'Invalid JSON received: {response.text}', 'ERROR')
        status_message = f'Invalid JSON received: {response.text}'
        
    # Create the payload
    payload = {
        'status_code': status,
        'status_message': status_message,
        'chat_response': chat_response  # This will be None if not set
    }
    return payload
    
    # Pretty-print the payload
    #payload_json = json.dumps(payload)
    #logger.log(f"Pretty Payload: \n{payload_json}", 'INFO')
    #return payload_json




# Update the send_post_request to include the callback
def send_post_request(endpoint, payload):
    logger.log(f"Sending POST request to endpoint: {endpoint}", 'INFO')
    response = session.post(
        url=f'{BASE_URL}/{endpoint}',
        json=payload,
        timeout=TIMEOUT
    )

    try:
        # Parse JSON response and return as a dictionary
        response_data = response.json()
        return response_data
    except json.JSONDecodeError:
        # Handle case where response is not in JSON format
        logger.log(f'Invalid JSON response: {response.text}', 'ERROR')
        return {'error': 'Invalid JSON response'}

def validate_api(event):
    logger.log('Validating API...', 'INFO')
    logger.log(event['input']);
    if 'api' not in event['input']:
        return {
            'errors': '"api" is a required field in the "input" payload'
        }

    api = event['input']['api']

    if type(api) is not dict:
        return {
            'errors': '"api" must be a dictionary containing "method" and "endpoint"'
        }

    api['endpoint'] = api['endpoint'].strip('/')
    # logger.log('KEVIN the endpoint is')
    # logger.log(api)

    #KEVIN this is hack because we can't get the endpoint to validate
    #I suspect to the the validator not treating slashes properly
    #return {'success': True, 'validated_input': api}

    return validate(api, API_SCHEMA)



def validate_payload(event):
    logger.log('Validating payload...', 'INFO')
    method = event['input']['api']['method']
    endpoint = event['input']['api']['endpoint']
    payload = event['input']['payload']
    validated_input = {}

    if endpoint == 'generate':
        validated_input = validate(payload, GENERATE_SCHEMA)
    elif endpoint == 'chat':
        validated_input = validate(payload, CHAT_SCHEMA)
    elif endpoint == 'token-count':
        validated_input = validate(payload, TOKEN_COUNT_SCHEMA)
    elif endpoint == 'model' and method == 'POST':
        validated_input = validate(payload, MODEL_SCHEMA)
    elif endpoint == 'chat/completions':  # Add this condition for 'chat/completions'
        validated_input = validate(payload, CHAT_COMPLETIONS_SCHEMA)  # Assuming such a schema exists


    return endpoint, event['input']['api']['method'], validated_input

# ---------------------------------------------------------------------------- #
# RunPod Handler                                                               #
# ---------------------------------------------------------------------------- #
def handler(event):
    logger.log('Handling event...', 'INFO')
    if 'heartbeat' in event['input'] and event['input']['heartbeat'] == True:
        return {'status': 'ok'}

    validated_api = validate_api(event)
    if 'errors' in validated_api:
        return {'error': validated_api['errors']}

    endpoint, method, validated_input = validate_payload(event)
    if 'errors' in validated_input:
        return {'error': validated_input['errors']}

    payload = validated_input.get('validated_input', {})
    try:
        logger.log(f'Sending {method} request to: {endpoint}', 'INFO')
        if method == 'GET':
            response_data = send_get_request(endpoint)
        elif method == 'POST':
            response_data = send_post_request(endpoint, payload)

        if isinstance(response_data, dict):
            return response_data
        else:
            return {'error': 'Invalid response format'}
    except Exception as e:
        logger.log(f'Error occurred: {str(e)}', 'ERROR')
        return {'error': str(e)}


if __name__ == '__main__':
    while True:  # Keep running indefinitely
        try:
            wait_for_service(url='http://127.0.0.1:5000/v1/models')
            logger.log('Oobabooga API is ready', 'INFO')
            logger.log('Starting RunPod Serverless...', 'INFO')
            runpod.serverless.start(
                {
                    'handler': handler
                }
            )
        except Exception as e:
            logger.log(f"An error occurred: {str(e)}. Restarting...", 'ERROR')