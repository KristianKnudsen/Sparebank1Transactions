import json
import requests
import secrets
from flask import Flask, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Required json fields in the secret.txt document.
required_fields = {"access_token", "client_id", "client_secret", "fid", "redirect_uri"}


@app.route('/')
def start():
    authorization_code = request.args.get('code')
    data = load_keys()
    content = ""

    client_id = data["client_id"]
    client_secret = data["client_secret"]
    access_token = data["access_token"]
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
    if access_token:
        api_call_headers = {'Authorization': 'Bearer ' + access_token}
        api_call_response = requests.get('https://api.sparebank1.no/open/personal/banking/accounts/default',
                                         headers=api_call_headers, verify=True)

        if api_call_response.text == 'Unauthorized':
            access_token = ''
        else:
            response = json.loads(api_call_response.text)
            content = 'All seems to be in order. Acount owner: ' + response['owner']['name']
            session[""]
            return redirect(url_for("home", name=response['owner']['name']))
    if not access_token:
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


@app.route('/home')
def home():
    return "hai"


def load_keys() -> dict:
    with open("secret.txt") as file:
        data = json.load(file)
    return data


if __name__ == '__main__':
    app.run()
