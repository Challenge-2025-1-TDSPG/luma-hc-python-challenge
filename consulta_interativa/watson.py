import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

authenticator = IAMAuthenticator('{}')
assistant = AssistantV2(
    version='2024-08-25',
    authenticator = authenticator
)

assistant.set_service_url('{}')

response = assistant.message(
    assistant_id='{environment_id}',
    session_id='{session_id}',
    input={
        'message_type': 'text',
        'text': 'Hello'
    }   
).get_result()

print(json.dumps(response, indent=2))