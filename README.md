# SummarEase

## Overview
The SummarEase project is a web application that retrieves comments from a YouTube video, analyzes their sentiment, and provides a concise summary using Google Gemini AI. The application also extracts video and channel details while visualizing sentiment analysis results.

## Features ✨
-Extracts video ID from a YouTube link.

-Fetches and stores comments in a CSV file. 💬💑

-Performs sentiment analysis using mBERT (Multilingual BERT). 😃😠😐

-Summarizes comments using Google Gemini AI. 🤖

-Fetches video details like views, likes, and comments. 📺

-Retrieves YouTube channel information, including subscriber count and creation date. 🔍

-Provides data visualization with bar charts and pie charts. 📊

-User-friendly web interface built with Streamlit. 🌐


## Setup & Installation 🛠

### 1. Clone the Repository
git clone https://github.com/Heet-2405/Youtube-Comments-Analyzer.git

### 2. Install Required Dependencies
pip install -r requirements.txt

### 3. Set Up API Keys

#### YouTube API Key:
Obtain it from the Google Cloud Console and replace the placeholder in YoutubeCommentScrapper.py

#### Gemini AI API Key:
Get it from Google AI Studio and add it to Sentiment_Analysis.py.


## Running the Application 🚀

### streamlit run app.py

-Open the browser and go to http://localhost:8501/

-Enter a YouTube link in the sidebar to fetch comments and analyze sentiment.



