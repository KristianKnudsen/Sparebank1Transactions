import json
import requests
import secrets
import cryptocode as cc
from flask import Flask, request, redirect, url_for, session

from Account import Account

app = Flask(__name__)
app.secret_key = secrets.token_urlsafe(32)

# Required json fields in the secret.txt document.
required_fields = {"access_token", "client_id", "client_secret", "fid", "redirect_uri"}


@app.route('/')
def start():
    if "access_token" in session:
        return redirect(url_for("home"))

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
            session["access_token"] = cc.encrypt(access_token, app.secret_key)
            return redirect(url_for("home", session="started"))
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
    if "access_token" not in session:
        return redirect(url_for("start"))

    access_token = cc.decrypt(session["access_token"], app.secret_key)

    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_call_response = requests.get('https://api.sparebank1.no/open/personal/banking/accounts/default',
                                     headers=api_call_headers, verify=True)
    response = json.loads(api_call_response.text)
    return "hei " + response['owner']['name']


@app.route('/accounts')
def accounts():

    data = load_keys()
    access_token = data["access_token"]

    api_call_headers = {'Authorization': 'Bearer ' + access_token}
    api_call_response = requests.get('https://api.sparebank1.no/open/personal/banking/accounts/all',
                                     headers=api_call_headers, verify=True)
    response = json.loads(api_call_response.text)
    a = Account(response["accounts"][1])
    print(a.aid)
    link = "https://api.sparebank1.no/personal/banking/accounts/DY8nvCshpcFH4hBcm8ph_yesS4k/archived-transactions-count?from=2020-08-01&to=2021-10-01"
    print(link)
    api_call_response = requests.get(link,
                                     headers=api_call_headers, verify=True)
    print(api_call_response)
    return "r"


def load_keys() -> dict:
    with open("secret.txt") as file:
        data = json.load(file)
    return data


if __name__ == '__main__':
    app.run()
