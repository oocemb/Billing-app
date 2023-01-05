import requests


def validate_params_in_billing_api(api_url, params, provider, body={}):
    api_url = api_url.replace("<provider>", provider)
    auth_header = {"Token": "Django-bro"}
    payload = {"url": params, "provider": provider, "body": body}
    try:
        response = requests.post(api_url, headers=auth_header, json=payload)
    except requests.exceptions.ConnectionError:
        return  # todo: error to log 'Connection to billing error'
    if response.status_code == 200:
        return response.json()
    return {"msg": "error"}  # todo: else error to log
