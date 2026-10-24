import os
import streamlit as st
import pandas as pd
import requests

# ==========================================
# Backend Configuration
# ==========================================

BACKEND_URL = os.getenv("BACKEND_URL", "http://backend:7860")

# ==========================================
# Page Title
# ==========================================

st.title("SuperKart System")
st.write(
    "Enter the product and store details below to predict the total sales."
)

# ==========================================
# Backend Health Check
# ==========================================

with st.sidebar:
    st.header("System Status")

    try:
        health_response = requests.get(
            f"{BACKEND_URL}/health",
            timeout=5
        )

        if health_response.status_code == 200:
            st.success("Backend Connected")
        else:
            st.error("Backend Unavailable")

    except Exception:
        st.error("Backend Not Reachable")

# ==========================================
# Input Fields
# ==========================================

Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66
)

Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027
)

Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08
)

Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

Store_Type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Supermarket Type3",
        "Departmental Store",
        "Food Mart"
    ]
)

Product_Id_char = st.selectbox(
    "Product ID Character",
    ["FD", "DR", "NC"]
)

Store_Age_Years = st.number_input(
    "Store Age (Years)",
    min_value=0,
    value=16
)

Product_Type_Category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)

# ==========================================
# Payload
# ==========================================

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category
}

# ==========================================
# Single Prediction
# ==========================================

if st.button("Predict", type="primary"):

    try:

        response = requests.post(
            f"{BACKEND_URL}/v1/predict",
            json=product_data,
            timeout=30
        )

        response.raise_for_status()

        result = response.json()

        predicted_sales = result["Sales"]

        st.success(
            f"Predicted Product Store Sales Total: ₹{predicted_sales:,.2f}"
        )

    except Exception as e:
        st.error(f"Prediction failed: {e}")

# ==========================================
# Batch Prediction
# ==========================================

st.subheader("Batch Prediction")

uploaded_file = st.file_uploader(
    "Upload a CSV File",
    type=["csv"]
)

if uploaded_file is not None:

    if st.button("Predict for Batch", type="primary"):

        try:

            response = requests.post(
                f"{BACKEND_URL}/v1/predictbatch",
                files={"file": uploaded_file},
                timeout=60
            )

            response.raise_for_status()

            results = response.json()

            st.success("Predictions completed successfully!")

            if isinstance(results, dict):
                df = pd.DataFrame(
                    list(results.items()),
                    columns=["Row", "Predicted Sales"]
                )
            else:
                df = pd.DataFrame(results)

            st.dataframe(
                df,
                use_container_width=True
            )

        except Exception as e:
            st.error(f"Batch prediction failed: {e}")
