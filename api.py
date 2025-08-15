from flask import Flask, request, jsonify
from flask_cors import CORS
import joblib

app = Flask(__name__)
model = joblib.load("models/news_classifier_v1.0.pkl")

CORS(app)

@app.route("/classify", methods=["POST"])

def classify():
    json_input = request.get_json()

    if not json_input or 'text' not in json_input:

        json_result = {
            "title": "Erro: A entrada não é um JSON válido.",
            "details": "A entrada deve ser um JSON válido e conter uma entrada de texto",
            "status": 400
        }

        return jsonify(json_result), 400  
    
    text_to_classify = json_input['text']

    predict = model.predict([text_to_classify])
    result = predict[0]

    if result:

        json_result = {
            "title": "Categoria Prevista",
            "status": 200,
            "category_predict": result
        }
        
        return jsonify(json_result)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000', debug=True)
