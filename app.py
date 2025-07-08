from flask import Flask, request, jsonify, render_template
import pandas as pd
import joblib
#from transformers import pipeline
import os
import joblib

app = Flask(__name__)

# Load your trained Random Forest model here
model_path = os.path.join(os.path.dirname(__file__), 'land_value_model.pkl')
model = joblib.load(model_path)

# Load lightweight text generation model
#generator = pipeline("text-generation", model="sshleifer/tiny-gpt2")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    input_df = pd.DataFrame([data])

    # Predict land value
    predicted_value = model.predict(input_df)[0]
    predicted_dollar_m2 = predicted_value/data['Land_Area']

    # Create prompt for LLM generation
    prompt = (
        f"This commercial property is located in Ho Chi Minh City and comprises a land area of {data['Land_Area']} square meters, with a total floor space area of {data['FSA']} square meters. "
f"Geographically, it is situated at latitude {data['Latitude']} and longitude {data['Longitude']}. "
f"Based on current market conditions and location-specific factors, the estimated land value of this property is approximately {predicted_value:,.0f} USD. "
f"This corresponds to an estimated unit price of {predicted_dollar_m2:,.0f} USD per square meter. "
f"The valuation is based on the prices of similar properties and geospatial considerations."
    )

    # Generate text (you can tweak max_length etc)
    #llm_output = llm_output = generator(prompt, max_new_tokens=30, do_sample=True)[0]['generated_text']

    #return jsonify({'generated_text': llm_output})
    return jsonify({'generated_text': prompt})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
