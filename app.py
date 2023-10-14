import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from seo_tool import train_model
import requests
import re

def is_valid_email(email):
    # Basic regex for email validation
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))

def send_webhook(email):
    webhook_url = "https://eogjf6zxl5coqhm.m.pipedream.net"
    payload = {"email": email}
    try:
        response = requests.post(webhook_url, json=payload)
        return response.status_code == 200
    except:
        return False

def main():
    
    # Variable to track if the user is logged in
    session_state = st.session_state
    if "logged_in" not in session_state:
        session_state.logged_in = False

    # Email form at the top of the sidebar
    st.sidebar.title("Login to Use Boring Vision")
    entered_email = st.sidebar.text_input("Enter your email:", key="email_input", disabled=session_state.logged_in)
    
    login_button = st.sidebar.button("Login", key="login_button", disabled=session_state.logged_in)

    # Now, handle the logic upon button click
    if login_button:
        if not entered_email:
            st.sidebar.warning("Please enter your email to login.")
            return
        if is_valid_email(entered_email):
            if send_webhook(entered_email):
                st.sidebar.success("Logged in successfully!")
                session_state.logged_in = True
            else:
                st.sidebar.error("Failed to login. Try again.")
        else:
            st.sidebar.error("Please enter a valid email address.")

    if not session_state.logged_in:
        st.warning("Please login from the sidebar to use this tool.")
        return  # Stop execution here to prevent further code running

    # Sidebar Navigation
    st.sidebar.title("Navigation")
    show_analysis = st.sidebar.button("Boring Vision Tool 📊")
    show_docs = st.sidebar.button("Docs 🗄️")

    if show_analysis or (not show_analysis and not show_docs):  # If Analysis button is pressed or no button is pressed
        analysis_page()
    elif show_docs:
        docs_page()

def analysis_page():
    st.title("Boring Vision V0.1 📊")
    st.write("""
    Developed by Boring Marketing, Boring Vision is your go-to tool for insightful SEO analysis. Using advanced models, it predicts clicks from CTR, position, and impressions. To begin:
    1. Download your data from Google Search Console.
    2. Upload it here.
    3. Analyze, predict, and optimize.

    Need help? Check our Docs for guidance.
    """)


    # Upload CSV
    uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded_file:
        data = pd.read_csv(uploaded_file)
        
        # Convert CTR to decimal format
        data['CTR'] = data['CTR'].str.rstrip('%').astype('float') / 100.0
        
        # Model selection
        model_option = st.selectbox("Choose a regression model", ["RandomForest", "LinearRegression", "MLPRegressor"])
        
        # Train the regression model
        model, mse = train_model(data, model_option)
        st.write(f"Mean Squared Error for {model_option}: {mse:.2f}")

        # Predictive bubble chart
        data['Predicted_Clicks'] = np.maximum(model.predict(data[['CTR', 'Position', 'Impressions']]), 0.01)
        fig = px.scatter(data, 
                        x="CTR", 
                        y="Position", 
                        size="Predicted_Clicks",
                        hover_name="Top queries",
                        hover_data=["Impressions", "Clicks", "CTR", "Position", "Predicted_Clicks"],
                        log_x=True, 
                        title="Bubble Chart Analysis of SEO Performance"
                        )
        
        # Add average lines
        avg_ctr = np.mean(data['CTR'])
        avg_position = np.mean(data['Position'])

        fig.add_vline(x=avg_ctr, line_dash="dash", line_color="red", annotation_text="Avg CTR")
        fig.add_hline(y=avg_position, line_dash="dash", line_color="red", annotation_text="Avg Position")
        fig.update_layout(showlegend=True)
        fig.update_yaxes(autorange="reversed")

        st.plotly_chart(fig, use_container_width=True)

        # Categorizing data for better analysis
        top_pos_high_ctr = data[(data['CTR'] > avg_ctr) & (data['Position'] <= avg_position)]
        low_pos_high_ctr = data[(data['CTR'] > avg_ctr) & (data['Position'] > avg_position)]
        low_pos_low_ctr = data[(data['CTR'] <= avg_ctr) & (data['Position'] > avg_position)]
        top_pos_low_ctr = data[(data['CTR'] <= avg_ctr) & (data['Position'] <= avg_position)]

        # Displaying the categorized data
        col1, col2 = st.columns(2)

        col1.subheader("Top Right (Top Position, High CTR)")
        col1.write("""
        * **Meaning**: These are your rock stars. They rank high and have a commendable click-through rate.
        * **Action**: Keep monitoring and ensure consistency. These do not need immediate action.
                   """)
        col1.dataframe(top_pos_high_ctr)

        col2.subheader("Bottom Right (Low Position, High CTR)")
        col2.write("""
        * **Meaning**: These queries are relevant to users (hence the high CTR), but they don’t rank as high as they could.
        * **Action**: Optimize your content around these queries to boost their rank.
                   """)
        col2.dataframe(low_pos_high_ctr)

        col1.subheader("Bottom Left (Low Position, Low CTR)")
        col1.write("""
        * **Meaning**: These rank low and also have a low CTR. However, the bubble size might suggest potential.
        * **Action**: Evaluate if they're worth the effort. Some might need better content; others might not be relevant.
                   """)
        col1.dataframe(low_pos_low_ctr)

        col2.subheader("Top Left (Top Position, Low CTR)")
        col2.write("""
        * **Meaning**: These queries rank high but aren’t getting clicks, potentially due to competing content.
        * **Action**: Investigate why users aren't clicking. Revamp meta descriptions, or ensure the content matches user intent.
                   """)
        col2.dataframe(top_pos_low_ctr)

        # Purpose and Understanding
        st.subheader('Purpose & Understanding')
        st.write("""
        **Purpose of the Bubble Chart:**
        - Visual representation of Search performance.
        - Understand performance of queries.
        - Identify effective and optimization needed queries.

        **Understanding the Chart:**
        - Represents relationships and patterns.
        - Displays metrics and dimensions.
        """)

def docs_page():
    st.title("Documentation")

    st.write("""
    ## Tutorial:
    """)

    st.image('tutorial.gif')


    
    st.write("""
    ## **Boring Vision V0.1 📊**: Uncover SEO Performance Patterns

    ### Introduction:
    **Boring Vision V0.1 📊** is a cutting-edge tool that seamlessly blends data visualization with machine learning. Through intuitive bubble charts and predictive analysis, it provides a comprehensive understanding of your search performance. Dive in to unearth hidden trends, and garner insights to bolster your SEO strategy.

    ### **1. Getting Started with Boring Vision V0.1 📊**:
    #### **Uploading Your Data**:
    - Download the CSV from Google Search Console.
    - Unzip it and find Query.csv
    - Navigate to the **Boring Vision V0.1 📊** dashboard.
    - Use the "Upload CSV" button on the left sidebar.
    - Ensure your CSV contains these crucial columns: 'CTR', 'Position', 'Impressions', and 'Clicks'.
    - The tool will handle the 'CTR' column conversion from percentage to decimal format for you.

    #### **Choosing a Regression Model**:
    - After uploading, select a preferred regression model from the dropdown.
    - The tool utilizes this model to train on your data and subsequently make predictions.

    ### **2. Interpreting the Bubble Chart Analysis**:
    - The chart provides a visual analysis of your search performance.
    - It aids in understanding the potency of your search queries and offers clues for optimization.

    #### **Quadrant Analysis**:

    - **Top Right (Top Position, High CTR)**: 
        * **Meaning**: These are your rock stars. They rank high and have a commendable click-through rate.
        * **Action**: Keep monitoring and ensure consistency. These do not need immediate action.
        
    - **Bottom Right (Low Position, High CTR)**:
        * **Meaning**: These queries are relevant to users (hence the high CTR), but they don’t rank as high as they could.
        * **Action**: Optimize your content around these queries to boost their rank.
        
    - **Bottom Left (Low Position, Low CTR)**:
        * **Meaning**: These rank low and also have a low CTR. However, the bubble size might suggest potential.
        * **Action**: Evaluate if they're worth the effort. Some might need better content; others might not be relevant.
        
    - **Top Left (Top Position, Low CTR)**:
        * **Meaning**: These queries rank high but aren’t getting clicks, potentially due to competing content.
        * **Action**: Investigate why users aren't clicking. Revamp meta descriptions, or ensure the content matches user intent.

    ### **3. Dive Deeper: Understanding the Regression Models**:
    - **RandomForest**:
        * **Overview**: Employs a collection of decision trees. It utilizes bootstrap aggregation, enhancing accuracy and curbing overfitting.
        * **Best Used**: When your dataset has many features or complex interactions.

    - **LinearRegression**:
        * **Overview**: Presupposes a linear bond between input and output. It's simple and interpretable.
        * **Best Used**: For datasets showcasing a clear linear trend.

    - **MLPRegressor**:
        * **Overview**: This is a type of neural network. It's adept at discerning non-linear relationships.
        * **Best Used**: When dealing with larger datasets or when suspecting intricate non-linear patterns. Beware of overfitting with smaller datasets.
    """)

if __name__ == "__main__":
    main()
