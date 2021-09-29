import requests, json
import cgi
from flask import Flask, request

app = Flask(__name__)


@app.route('/')
def start():

    authorization_code = request.args.get('code')

    data = load_keys()

    client_id = data["client_id"]
    client_secret = data["client_secret"]
    fid = "fid-nord-norge"

    redirect_uri = "http://127.0.0.1:5000/"
    authorize_uri = "https://api.sparebank1.no/oauth/authorize"
    token_uri = "https://api.sparebank1.no/oauth/token"

    if authorization_code:
        data = {'grant_type': 'authorization_code', 'code': authorization_code, 'redirect_uri': redirect_uri}
        token_response = requests.post(token_uri, data=data, verify=False, allow_redirects=False,
                                       auth=(client_id, client_secret))
        access_tokens = json.loads(token_response.text)
        access_token = access_tokens['access_token']

        content = 'Access token: ' + access_token
    else:
        content = '<a href=' + authorize_uri + \
              '?response_type=code&client_id=' + client_id + \
              '&redirect_uri=' + redirect_uri + \
              '&finInst=' + fid + \
              '&state=state' + \
              '>Login</a>'

    r = f"""<html>
        <head><title>Personal client</title></head>
        <body>
        {content}
        </body>
        </html>
        """

    return r


@app.route('/test')
def test():
    load_keys()
    return "hai"


def load_keys() -> dict:
    with open("secret.txt") as file:
        data = json.load(file)
        return data


if __name__ == '__main__':
    app.run()
    apik, skey = load_keys()
    print(apik)
    print(skey)
