class Account:
    def __init__(self, adto):
        self.aid = adto["id"]
        self.name = adto["name"]
        self.description = adto["description"]
        self.balance = adto["balance"]
        self.available_balance = adto["availableBalance"]
        self.owner = adto["owner"]
        self.product = adto["product"]
        self.type = adto["type"]
        self.iban = adto["iban"]
        self.links = adto["_links"]