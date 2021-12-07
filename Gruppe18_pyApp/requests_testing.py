

variable = "dog"
variable2 = 1

data = {
        "store_owner": f"{variable}",
        "bought_item": f"{variable2}",
        "submit": "Buy+product"
    }

for dat in data.values():
    print(dat)


def afunc():
    value1 = "1"
    value2 = "2"

    return value1, value2

print(afunc())

values = afunc()
print(values[0])

print(type(afunc()))