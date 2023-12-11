from flask import Flask, request, jsonify
import os
import pickle
# from sklearn.model_selection import cross_val_score
import pandas as pd
import sqlite3
import pickle


os.chdir(os.path.dirname(__file__))

app = Flask(__name__)
app.config['DEBUG'] = True

@app.route("/", methods=['GET'])
def hello():
    return "Bienvenido a mi API del modelo advertising"

# 1. Endpoint que devuelva la predicción de los nuevos datos enviados mediante argumentos en la llamada
@app.route('/v1/predict', methods=['GET'])
def predict():
    conn = sqlite3.connect('data/db.db')
    df = pd.read_sql_query("SELECT * FROM advertising", conn)
    conn.close()
    
    model = pickle.load(open('data/advertising_model','rb'))

    tv = request.args.get('tv', None)
    radio = request.args.get('radio', None)
    newspaper = request.args.get('newspaper', None)

    if tv is None or radio is None or newspaper is None:
        return "Missing args, the input values are needed to predict"
    else:
        prediction = model.predict([[int(tv),int(radio),int(newspaper)]])
        return "The prediction of sales investing that amount of money in TV, radio and newspaper is: " + str(round(prediction[0],2)) + 'k €'

# 2 End point para crear nuevos registros 

@app.route('/v2/ingest_data', methods=['POST'])

def ingest_data():
    try:
        conn = sqlite3.connect('data/db.db')
        data = request.json
        print("datos recibidos:", data) 
        query = "INSERT INTO Advertising (tv, radio, newpaper, sales) VALUES (?, ?, ?,?)"
        conn.execute(query, (data['tv'], data['radio'], data['newpaper'], data['sales']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Datos actualizados'})
    except Exception as e:
        print("Error al conectar con la base de datos:", str(e))

# 3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan. (/v2/retrain)

@app.route('/v2/retrain', methods=['POST'])

def retrain_model():
    
    conn = sqlite3.connect(os.path.join('data/db.db'))
    df = pd.read_sql_query("SELECT * FROM advertising", conn)
    conn.close()
    model = pickle.load(open('data/advertising_model','rb'))
    
    X = df[['TV', 'radio', 'newpaper']]
    y = df['sales']

    model.fit(X, y)

    with open('data/advertising_model', 'wb') as archivo_salida :
        pickle.dump(model, archivo_salida)
    return jsonify({'message': 'Modelo actualizado correctamente'})




app.run()