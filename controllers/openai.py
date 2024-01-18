
import requests 
class openAI:
    base_url = "https://api.openai.com/v1/chat/completions"
    token = ""

    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    def __init__(self) -> None:
        pass

    @classmethod
    
    def do_request(cls, params=None):
        requestBody = {
            "model": "gpt-3.5-turbo",
            "messages":[
                {
                    "role": "user",
                    "content": "TEST",
                }
            ]
        };
        repsonse =  requests.post(url=cls.base_url, headers=cls.headers, json=params)
        print(repsonse)