

variable = "dog"
variable2 = 1

data = {
        "store_owner": f"{variable}",
        "bought_item": f"{variable2}",
        "submit": "Buy+product"
    }

for dat in data.values():
    print(dat)
