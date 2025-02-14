import json

with open("sample-data.json","r") as file:
    data = json.load(file)
print("Interface Status")
print("=" * 100)
print("{:<60} {:<20} {:<10} {:<10}".format("DN","Description","Speed","MTU"))
print("{:<60} {:<20} {:<10} {:<10}".format("-"*60,"-"*20,"-"*10,"-"*10))

for a in data["imdata"]:
    first = a["l1PhysIf"]["attributes"]
    dn = first["dn"]
    description = first.get("descr", "")
    speed = first["speed"]
    mtu = first["mtu"]


    print("{:<60} {:<20} {:<10} {:<10}".format(dn, description, speed, mtu))