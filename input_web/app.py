from flask import Flask, render_template, request
import pandas as pd
import threading
from time import sleep
from flask_cors import CORS, cross_origin
import requests

from intelligence import magic_time

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
from sklearn import preprocessing
from sklearn.linear_model import LinearRegression
from sklearn.neural_network import MLPRegressor

@app.route('/')
@cross_origin(origin='*')
def index():
    return render_template('index2.html',data=[])


@app.route('/to_ai/', methods = ['POST'])
@cross_origin(origin='*')
def get_post_javascript_data():
    sceneario = request.form['scenario']
    temperature = request.form['temperature']
    building_year = request.form['building_year']
    living_space = request.form['living_space']
    basement_available = request.form['basement_available']
    roof_insulation = request.form['roof_insulation']
    input_data = pd.read_csv('static/data_fl.csv')
    lr_results = clean_dataset(input_data,building_year,living_space,basement_available,roof_insulation)

    print(sceneario,temperature,lr_results)

    magic_time(int(30),int(sceneario),float(lr_results))
    sleep(60)

    on_off = requests.get('http://localhost:8888/schedule?key=[APIKEY]')

    rs = requests.get('http://localhost:8888/get_renewable_share?key=[APIKEY]')

    increased_rs = requests.get('http://localhost:8888/get_total_energy_saved?key=[APIKEY]').json()


    results_on_off = ([[1, 0][val == "off"] for val in on_off.json()][-24:])
    data = rs.json()[-24:]

    results_rs = [d/100 for d in data]

    processThread = threading.Thread(target=turn_on_off, args=(results_on_off,))  # <- note extra ','
    processThread.start()



    print(results_on_off, data,increased_rs)
    return [results_on_off,results_rs,increased_rs]


def clean_dataset(input_data,building_year,living_space,basement_available,roof_insulation):
    CATEGORICAL = ['keller', 'dawd']
    CONTINOUS = ['gbj', 'wfl', 'verbkw']

    df = pd.DataFrame([{
        'gbj':building_year,
        'wfl':living_space,
        'keller':basement_available,
        'dawd':roof_insulation,
        'verbkw':0
    }])

    Dataset = input_data[CATEGORICAL + CONTINOUS]
    Dataset = pd.concat([Dataset,df])

    index = Dataset.index
    Dataset = pd.get_dummies(data=Dataset, columns=CATEGORICAL)
    columns = list(Dataset.columns)
    scaled = preprocessing.minmax_scale(Dataset[columns], axis=0, )

    Dataset_scaled= pd.DataFrame(scaled,columns=columns,index=index)
    Y_dataset = Dataset_scaled['verbkw']
    X_dataset = Dataset_scaled.drop(['verbkw'], axis=1)

    reg = MLPRegressor().fit(X_dataset, Y_dataset)

    value = reg.predict([X_dataset.iloc[-1]])[0]
    value = value if value > 0.0 else 0.0
    value = value if value < 1.0 else 1.0

    return value


def turn_on_off(results_on_off):
    requests.get('https://maker.ifttt.com/trigger/turn_off/with/key/[APIKEY]')
    sleep(5)
    prev_state = 0
    for on_off in results_on_off:
        if on_off == prev_state:
            print('Skip')
            sleep(1)
            continue
        else:
            prev_state = on_off
            sleep(1)

        if on_off == 1:
            print('change to 1')
            requests.get('https://maker.ifttt.com/trigger/turn_on/with/key/[APIKEY]')
            sleep(5)
        else:
            print('change to 0')

            requests.get('https://maker.ifttt.com/trigger/turn_off/with/key/[APIKEY]')
            sleep(5)


    sleep(5)
    requests.get('https://maker.ifttt.com/trigger/turn_off/with/key/[APIKEY]')
    return None