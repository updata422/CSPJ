import urllib.request
import base64
import json

base_url = 'https://api.typingdna.com'
apiKey = 'd2eb92bc4126eeb22ccceb4be9b93426'
apiSecret = 'ecf18b249d44b42ca858960483530ed5'


def send_typing_data(user_id, pattern):
    authstring = f"{apiKey}:{apiSecret}"
    base64string = base64.encodebytes(
        authstring.encode()).decode().replace('\n', '')
    data = urllib.parse.urlencode({'tp': pattern})
    url = f'{base_url}/auto/{user_id}'

    request = urllib.request.Request(url, data.encode('utf-8'), method='POST')
    request.add_header("Authorization", f"Basic {base64string}")
    request.add_header("Content-type", "application/x-www-form-urlencoded")

    res = urllib.request.urlopen(request)
    res_body = res.read()
    return json.loads(res_body.decode('utf-8'))
