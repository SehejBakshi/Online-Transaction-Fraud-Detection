import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    f1 = request.form.get('step')
    f2 = request.form.get('type')
    f3 = request.form.get('amt')
    f4 = request.form.get('oldBalanceOrig')
    f5 = request.form.get('newBalanceOrig')
    f6 = request.form.get('oldBalanceDest')
    f7 = request.form.get('newBalanceDest')
    #f8 = request.form.get('isFlaggedFraud')
    f8 = 0
    #f9 = request.form.get('errorBalanceOrig')
    f9=0
    #f10 = request.form.get('errorBalanceDest')
    f10=0
    g1 = request.form.get('avgCredit')
    g2 = request.form.get('minCredit')
    g3 = request.form.get('maxCredit')
    features = [f1, f2, f3, f4, f5, f6, f7, f8, f9, f10]
    print(features)
    g_result = 0.0
    try:
        g1 = float(g1)
        g2 = float(g2)
        g3 = float(g3)
        f3 = float(f3)
        print(g1, g2, g3, f3)
        if f3 > g3:
            x = (f3 - g3) * 0.7
            g_result = 1/(1+np.exp(-x))
        if f3 < g2:
            x = (g2 - f3) * 0.3
            g_result = 1/(1+np.exp(-x))
    except:
        print('hululu')

    final_features = np.array([features])
    model = pickle.load(open('model.pk', 'rb'))
    prediction = model.predict(final_features)
    print(prediction)
    print(g_result)
    prediction = (prediction * 0.7) + (g_result * 0.3)
    if prediction[0] > 0.50:
        output = 'Fraud'
    else:
        output = 'Not Fraud'
    #output = round(prediction[0], 2)

    return render_template('index.html', prediction_text='{}'.format(output))
    #return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
