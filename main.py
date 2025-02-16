import streamlit as st
import requests
import base64
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from groq import Groq

# Initialize Groq client with API key (Replace with your actual API key)
client = Groq(api_key="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")

st.title("QGIS Moon Terrain Analyzer using Groq Vision")
st.write("Upload a Moon Terrain image and get detailed analysis including crater sizes, path distance, and rover configurations.")

# File uploader
uploaded_file = st.file_uploader("Choose a Moon Terrain image", type=["png", "jpg", "jpeg", "tiff"])

question = """Analyze the Moon terrain image and provide the following details in a table format:

- Number of craters
- Path distance in meters
- Biggest crater size
- Smallest crater size
- Suggested rover configurations (Height, Weight)
- Suggested rover speed
- Terrain analysis
- Path analysis

Ensure that crater boundaries are marked in green and paths are shown as dotted red lines."""

if uploaded_file:
    image_bytes = uploaded_file.read()
    image_base64 = base64.b64encode(image_bytes).decode("utf-8")
    image_url = f"data:image/png;base64,{image_base64}"

    # Call Groq Vision model
    completion = client.chat.completions.create(
        model="llama-3.2-11b-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": question},
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )

    # Extract response
    response_text = completion.choices[0].message.content

    # Simulated extracted structured data (Modify based on actual output)
    analysis_data = {
        "Number of craters": np.random.randint(50, 100),
        "Path distance (m)": np.random.randint(500, 2000),
        "Biggest crater size (m)": np.random.randint(100, 500),
        "Smallest crater size (m)": np.random.randint(10, 50),
        "Suggested rover height (m)": np.random.uniform(1, 3),
        "Suggested rover weight (kg)": np.random.randint(100, 500),
        "Suggested rover speed (m/s)": np.random.uniform(0.5, 3)
    }

    # Display response
    st.subheader("Analysis Report")
    st.write(response_text)

    # Display structured data in a table
    df_analysis = pd.DataFrame(list(analysis_data.items()), columns=["Metric", "Value"])
    st.subheader("Analysis Data Table")
    st.table(df_analysis)

    # Visualization 1: Pie Chart (Craters vs. Flat Terrains)
    st.subheader("Crater vs Flat Terrain Distribution")
    labels = ["Craters", "Flat Terrains"]
    sizes = [analysis_data["Number of craters"], 1000 - analysis_data["Number of craters"]]
    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=["red", "green"], startangle=90)
    ax1.axis("equal")
    st.pyplot(fig1)

    # Visualization 2: Bar Chart (Crater Sizes)
    st.subheader("Crater Size Distribution")
    crater_sizes = np.random.randint(10, analysis_data["Biggest crater size (m)"], size=10)
    df_crater_sizes = pd.DataFrame({"Crater ID": range(1, 11), "Size (m)": crater_sizes})
    fig2, ax2 = plt.subplots()
    sns.barplot(x="Crater ID", y="Size (m)", data=df_crater_sizes, palette="Blues", ax=ax2)
    ax2.set_xlabel("Crater ID")
    ax2.set_ylabel("Size (m)")
    st.pyplot(fig2)

    # Visualization 3: Line Chart (Path Distance Analysis)
    st.subheader("Path Distance Analysis")
    path_points = np.cumsum(np.random.randint(50, 200, size=10))
    fig3, ax3 = plt.subplots()
    ax3.plot(range(1, 11), path_points, marker="o", linestyle="-", color="blue")
    ax3.set_xlabel("Path Segments")
    ax3.set_ylabel("Distance (m)")
    ax3.set_title("Path Distance Over Terrain")
    st.pyplot(fig3)
