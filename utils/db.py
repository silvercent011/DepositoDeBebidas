import psycopg2, json
def connect():
    #Database
    with open('../env.json','r') as env:
        db = json.loads(env.read())
    connection = psycopg2.connect(db['uri'])
    return connection