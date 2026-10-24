
# Import Required Libraries

import joblib
import pandas as pd

from flask import Flask, jsonify, request

# Initialize Flask Application

superkart_api = Flask("SuperKart")

# Load Trained Model

model = joblib.load("superkart_model.joblib")

# Home Endpoint

@superkart_api.get("/")
def home():
    return "Welcome to the SuperKart System"

# Health Check Endpoint

@superkart_api.get("/health")
def health():
    return jsonify(
        {
            "status": "healthy",
            "message": "SuperKart API is running",
        }
    ), 200

# Single Prediction Endpoint

@superkart_api.post("/v1/predict")
def predict_sales():

    try:

        data = request.get_json()

        input_record = {
            "Product_Weight": data["Product_Weight"],
            "Product_Sugar_Content": data["Product_Sugar_Content"],
            "Product_Allocated_Area": data["Product_Allocated_Area"],
            "Product_MRP": data["Product_MRP"],
            "Store_Size": data["Store_Size"],
            "Store_Location_City_Type": data["Store_Location_City_Type"],
            "Store_Type": data["Store_Type"],
            "Product_Id_char": data["Product_Id_char"],
            "Store_Age_Years": data["Store_Age_Years"],
            "Product_Type_Category": data["Product_Type_Category"],
        }

        input_df = pd.DataFrame([input_record])

        prediction = model.predict(input_df)[0]

        return jsonify(
            {
                "Sales": round(float(prediction), 2)
            }
        )

    except KeyError as error:

        return jsonify(
            {
                "error": f"Missing field: {error}"
            }
        ), 400

    except Exception as error:

        return jsonify(
            {
                "error": str(error)
            }
        ), 500


# Batch Prediction Endpoint

@superkart_api.post("/v1/predictbatch")
def predict_sales_batch():

    try:

        if "file" not in request.files:

            return jsonify(
                {
                    "error": "CSV file not provided."
                }
            ), 400

        file = request.files["file"]

        input_df = pd.read_csv(file)

        predictions = model.predict(input_df)

        output_dict = {
            str(index): round(float(prediction), 2)
            for index, prediction in enumerate(predictions)
        }

        return jsonify(output_dict)

    except Exception as error:

        return jsonify(
            {
                "error": str(error)
            }
        ), 500


# Run Flask Application


if __name__ == "__main__":
    superkart_api.run(
        host="0.0.0.0",
        port=7860,
        debug=True
    )
