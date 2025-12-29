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
        # Parse input from event body if it's a string (API Gateway format)
        if isinstance(event.get('body'), str):
            body = json.loads(event['body'])
        else:
            body = event

        # Extract parameters
        prompt_type_str = body.get('prompt_type', 'ENCYCLOPEDIA_EN')
        term = body.get('term')

        # Validate inputs
        if not term:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': 'Missing required parameter: term'
                })
            }

        # Convert string to PromptType enum
        try:
            prompt_type = PromptType(prompt_type_str)
        except KeyError:
            return {
                'statusCode': 400,
                'body': json.dumps({
                    'error': f'Invalid prompt_type.'
                })
            }

        # Call generate function
        result = generate(prompt_type, term)

        # Return success response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'result': result
            })
        }

    except Exception as e:
        # Return error response
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': str(e)
            })
        }

def create_response(status_code: int, body: str) -> dict:
    return {
        'statusCode': status_code,
        'body': json.dumps(body)
    }


if __name__ == "__main__":
    response = lambda_handler({"prompt_type": "DICTIONARY_EN", "term": "flash"}, {})
    print(response)
