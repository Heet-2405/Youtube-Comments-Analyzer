
import csv
import pandas as pd
import torch
import plotly.express as px
import plotly.graph_objects as go
from transformers import BertTokenizer, BertForSequenceClassification
import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Load the mBERT model and tokenizer
MODEL_NAME = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = BertTokenizer.from_pretrained(MODEL_NAME)
model = BertForSequenceClassification.from_pretrained(MODEL_NAME)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def extract_video_id(youtube_link: str) -> str:
    if "youtube.com/watch?v=" in youtube_link:
        return youtube_link.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_link:
        return youtube_link.split("youtu.be/")[1].split("?")[0]
    return None

# Configure Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)

def summarize_comments(csv_file):
    """Summarizes YouTube comments using Google Gemini API."""
    with open(csv_file, "r", encoding="utf-8") as file:
        comments = file.read()

    prompt = f"""Summarize the following YouTube comments into a minimum of 2-3 paragraphs but not indicats paragraph number. The summary should capture the overall sentiment, key themes, and main opinions expressed in the comments. Each paragraph should be at least 5-10 lines long and should provide a balanced view of both positive and negative feedback. Highlight any common trends, recurring topics, or unique insights shared by users.\n\n{comments}"""

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)

    return response.text if response else "No summary generated."

def analyze_sentiment(csv_file: str):
    """Uses mBERT model to classify sentiment as Positive, Negative, or Neutral."""
    comments = []
    try:
        with open(csv_file, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if 'Comment' in row:
                    comments.append(row['Comment'])
    except FileNotFoundError:
        return {'num_neutral': 0, 'num_positive': 0, 'num_negative': 0}

    num_neutral, num_positive, num_negative = 0, 0, 0

    for comment in comments:
        inputs = tokenizer(comment, return_tensors="pt", truncation=True, padding=True, max_length=512)
        inputs = {key: val.to(device) for key, val in inputs.items()}  

        with torch.no_grad():
            outputs = model(**inputs)

        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1).cpu().numpy()
        sentiment_class = probabilities.argmax(axis=1)[0] + 1  

        if sentiment_class in [1, 2]:
            num_negative += 1
        elif sentiment_class == 3:
            num_neutral += 1
        else:
            num_positive += 1

    return {'num_neutral': num_neutral, 'num_positive': num_positive, 'num_negative': num_negative}

def bar_chart(csv_file: str):
    """Generates a bar chart of sentiment analysis results."""
    results = analyze_sentiment(csv_file)
    
    df = pd.DataFrame({
        "Sentiment": ["Positive", "Negative", "Neutral"],
        "Count": [results['num_positive'], results['num_negative'], results['num_neutral']]
    })

    fig = px.bar(df, x="Sentiment", y="Count", color="Sentiment", title="Sentiment Analysis Results")
    st.plotly_chart(fig)

def plot_sentiment(csv_file: str):
    """Generates a pie chart visualization of sentiment analysis results."""
    results = analyze_sentiment(csv_file)

    labels = ['Positive', 'Negative', 'Neutral']
    values = [results['num_positive'], results['num_negative'], results['num_neutral']]

    fig = go.Figure(data=[go.Pie(labels=labels, values=values, hole=0.3)])
    fig.update_layout(title_text="Sentiment Distribution")
    st.plotly_chart(fig)