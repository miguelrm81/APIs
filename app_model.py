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
@app.route('/predict', methods=['GET'])


def predict():
    model = pickle.load(open('data/advertising_model','rb'))
    data = request.get_json()

    input_values = data['data'][0]
    tv, radio, newspaper = map(int, input_values)

    prediction = model.predict([[tv, radio, newspaper]])
    return jsonify({'prediction': round(prediction[0], 2)})

# 2 End point para crear nuevos registros 

@app.route('/ingest', methods=['POST'])
def ingest_data():
    data = request.get_json().get('data', [])

    for row in data:
        tv, radio, newpaper, sales = row
        query = "INSERT INTO Advertising (tv, radio, newpaper, sales) VALUES (?, ?, ?, ?)"
        connection = sqlite3.connect('data/db.db')
        crsr = connection.cursor()
        crsr.execute(query, (tv, radio, newpaper, sales))
        connection.commit()
        connection.close()

    return jsonify({'message': 'Datos ingresados correctamente'})


# 3. Posibilidad de reentrenar de nuevo el modelo con los posibles nuevos registros que se recojan. (/v2/retrain)

@app.route('/retrain', methods=['POST'])

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
    return jsonify({'message': 'Modelo reentrenado correctamente.'})




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)