import json

def load_keys():
    with open("secret.txt") as file:
        data = json.load(file)
        api_key = data["api_key"]
        secret_key = data["secret_key"]
        return api_key, secret_key


if __name__ == '__main__':
    apik, skey = load_keys()
    print(apik)
    print(skey)
