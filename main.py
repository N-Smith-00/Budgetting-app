import marshmallow
from classes import AppSchema, App

with open("data.txt", "r") as file:
    data = file.read()
    if data != '':
        app = AppSchema().loads(data)
    else:
        app = App()
file.close()
app.run()