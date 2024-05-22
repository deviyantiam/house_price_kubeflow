import streamlit as st
import requests

def input_fields():
    st.sidebar.title("Input Details")
    st.sidebar.write("Example:")
    st.sidebar.write({
        'area': 1200.0,
        'bedrooms': 3,
        'bathrooms': 2,
        'stories': 2,
        'mainroad': 'yes',
        'guestroom': 'no',
        'basement': 'yes',
        'hotwaterheating': 'yes',
        'airconditioning': 'yes',
        'parking': 1,
        'prefarea': 'yes',
        'furnishingstatus': 'semi-furnished'
    })

    area = st.sidebar.number_input("Area", value=1200.0)
    bedrooms = st.sidebar.number_input("Bedrooms", value=3, step=1)
    bathrooms = st.sidebar.number_input("Bathrooms", value=2, step=1)
    stories = st.sidebar.number_input("Stories", value=2, step=1)
    mainroad = st.sidebar.selectbox("Main Road", ['yes', 'no'])
    guestroom = st.sidebar.selectbox("Guest Room", ['yes', 'no'])
    basement = st.sidebar.selectbox("Basement", ['yes', 'no'])
    hotwaterheating = st.sidebar.selectbox("Hot Water Heater", ['yes', 'no'])
    airconditioning = st.sidebar.selectbox("Air Conditioner", ['yes', 'no'])
    parking = st.sidebar.number_input("Parking", value=1, step=1)
    prefarea = st.sidebar.selectbox("Preferred Area", ['yes', 'no'])
    furnishingstatus = st.sidebar.selectbox("Furnishing Status", ['furnished', 'semi-furnished', 'unfurnished'])

    return {
        'area': area,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'stories': stories,
        'mainroad': mainroad,
        'guestroom': guestroom,
        'basement': basement,
        'hotwaterheating': hotwaterheating,
        'airconditioning': airconditioning,
        'parking': parking,
        'prefarea': prefarea,
        'furnishingstatus': furnishingstatus
    }

def main():
    st.set_page_config(page_title="HOUSE PRICE PREDICTION", page_icon="🏠", initial_sidebar_state="expanded")
    st.title("HOUSE PRICE PREDICTION")
    st.write("""
    **Welcome to the House Price Prediction App!**

    We help you estimate the price of a house based on its features. Enter details like area, bedrooms, and more, then click "Predict" to see the estimated price
    """)

    input_data = input_fields()
    
    def send_prediction_request(input_data):
        url = "http://localhost:8000/predict"
        response = requests.post(url, json=input_data)
        return response
    
    if st.sidebar.button("Predict"):
        with st.expander("Selected Features"):
            for key, value in input_data.items():
                st.write(f"{key}: {value}")
        response = send_prediction_request(input_data)
        if response.status_code == 200:
            st.write("Predicted House Price:", response.json()["predictions"])
        else:
            st.error("Failed to get prediction. Please try again later.")

if __name__ == "__main__":
    main()
