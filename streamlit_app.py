import os

import streamlit as st
import requests

API_URL = os.environ.get("API_URL", "http://" + "127.0.0.1:5000/predict")

st.set_page_config(
    page_title="ExtraaLearn Lead Conversion",
    page_icon="📊",
    layout="centered"
)

st.title("ExtraaLearn Lead Conversion Predictor")
st.write(
    "Enter a lead's details to estimate the likelihood "
    "of conversion."
)

with st.form("lead_form"):
    st.subheader("Lead Information")

    age = st.number_input(
        "Age", min_value=18, max_value=100, value=35, step=1
    )

    occupation = st.selectbox(
        "Current Occupation",
        ["Professional", "Unemployed", "Student"]
    )

    first_interaction = st.selectbox(
        "First Interaction",
        ["Website", "Mobile App"]
    )

    profile_completed = st.selectbox(
        "Profile Completed",
        ["High", "Medium", "Low"]
    )

    website_visits = st.number_input(
        "Website Visits", min_value=0, value=4, step=1
    )

    time_spent = st.number_input(
        "Time Spent on Website (seconds)",
        min_value=0, value=1200, step=1
    )

    page_views = st.number_input(
        "Page Views per Visit",
        min_value=0.0, value=3.5, step=0.1
    )

    last_activity = st.selectbox(
        "Last Activity",
        ["Website Activity", "Email Activity", "Phone Activity"]
    )

    print_media_1 = st.selectbox("Print Media Type 1", ["No", "Yes"])
    print_media_2 = st.selectbox("Print Media Type 2", ["No", "Yes"])
    digital_media = st.selectbox("Digital Media", ["No", "Yes"])
    educational_channels = st.selectbox(
        "Educational Channels", ["No", "Yes"]
    )
    referral = st.selectbox("Referral", ["No", "Yes"])

    submitted = st.form_submit_button(
        "Predict Conversion", use_container_width=True
    )

if submitted:
    lead_data = {
        "age": age,
        "current_occupation": occupation,
        "first_interaction": first_interaction,
        "profile_completed": profile_completed,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent,
        "page_views_per_visit": page_views,
        "last_activity": last_activity,
        "print_media_type1": print_media_1,
        "print_media_type2": print_media_2,
        "digital_media": digital_media,
        "educational_channels": educational_channels,
        "referral": referral
    }

    try:
        with st.spinner("Generating prediction..."):
            response = requests.post(
                API_URL, json=lead_data, timeout=15
            )

        if response.status_code == 200:
            result = response.json()
            probability = result["conversion_probability"]

            st.subheader("Prediction Result")

            if result["prediction"] == 1:
                st.success("Prediction: Converted")
            else:
                st.info("Prediction: Not Converted")

            st.metric(
                "Estimated Conversion Probability",
                f"{probability:.1%}"
            )

            st.progress(max(0.0, min(1.0, probability)))

            st.caption(
                "This is a model estimate, not a guarantee "
                "of future conversion."
            )
        else:
            st.error(
                f"API returned status {response.status_code}: "
                f"{response.text}"
            )

    except requests.exceptions.ConnectionError:
        st.error(
            "Cannot connect to Flask. Start the Flask backend "
            "at http://127.0.0.1:5000 and try again."
        )
    except requests.exceptions.RequestException as error:
        st.error(f"Request failed: {error}")
