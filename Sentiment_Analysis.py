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

def extract_video_id(youtube_link: str) -> str:
    if "youtube.com/watch?v=" in youtube_link:
        return youtube_link.split("v=")[1].split("&")[0]
    elif "youtu.be/" in youtube_link:
        return youtube_link.split("youtu.be/")[1].split("?")[0]
    return None

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