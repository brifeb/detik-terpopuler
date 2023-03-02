from flask import Flask, request, jsonify
import json


persons = [
	{"ID": "1", "Name": "Febrianto", "Age": "39"},
	{"ID": "2", "Name": "Rossi", "Age": "41"},
]

app = Flask(__name__)

@app.route("/")
def home():
    return "ok"

@app.route("/persons", methods=['GET', 'POST'])
@app.route("/persons/<id>")
def handle_persons(id='0'):
    print("id", id)
    print(request)
    print(request.method)
    print(request.json)
    print(request.data)
    print("persons", persons)
    print("persons", type(persons))
    json_persons = json.dumps(persons)
    print("json persons", json_persons)
    print("json persons", type(json_persons))

    if request.method == 'GET':
        if id != '0':
            for d in persons:
                if d['ID'] == id:
                    print("return d", d)
                    return d
            return {}
        return json_persons

    if request.method == 'POST':
        data = json.loads(request.data)

        
        print("DATA", data)
        print(type(data))
        persons.append(data)

        return json_persons
    return "ok2"

app.run(debug=True)

