import json

from prompts import PromptType
from term import generate


def lambda_handler(event, context):
    """
    AWS Lambda handler that calls generate from term.py
    
    Expected input event:
    {
        "prompt_type": "DICTIONARY_EN" or "ENCYCLOPEDIA_EN",
        "term": "word or phrase to explain"
    }
    
    Returns:
    {
        "statusCode": 200,
        "body": JSON string containing the generated explanation
    }
    """
    try:
        # Parse input from the event body if it's a string (API Gateway format)
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event

        # Extract parameters
        prompt_type_str = body.get('prompt_type', 'ENCYCLOPEDIA_EN')
        term = body.get('term')

        # Validate inputs
        if not term:
            return create_response(400, {'error': 'Missing required parameter: term'})

        # Convert string to PromptType enum
        try:
            prompt_type = PromptType(prompt_type_str)
        except ValueError:
            return create_response(400, {'error': f'Invalid prompt_type: {prompt_type_str}'})

        # Call generate function
        result = generate(prompt_type, term)

        # Return success response
        return create_response(200, {'result': result})

    except Exception as e:
        # Return error response
        return create_response(500, {'error': str(e)})


def create_response(status_code: int, body: object) -> dict:
    """
    Generate an HTTP response dictionary with the given status code and body.

    :param status_code: HTTP status code for the response.
    :type status_code: int
    :param body: The content of the response, which will be JSON-encoded.
    :type body: object
    :return: A dictionary with `statusCode` and `body` keys representing the HTTP response.
    :rtype: dict
    """
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


if __name__ == "__main__":
    response = lambda_handler({"prompt_type": "DICTIONARY_EN", "term": "flash"}, {})
    print(response)
