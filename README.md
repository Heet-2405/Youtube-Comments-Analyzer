--> Summary

--> Overview
SummarEase is a web application designed to analyze YouTube video comments by retrieving them, performing sentiment analysis, and generating a meaningful summary using Google Gemini AI. Additionally, the application fetches essential video and channel details while providing insightful data visualizations for sentiment trends.

--> Features
- Extracts video ID from a YouTube link.
- Fetches and stores comments in a CSV file.
- Performs sentiment analysis using "Multilingual BERT (mBERT)".
- Summarizes comments using "Google Gemini AI".
- Retrieves video statistics, including views, likes, and comment count.
- Extracts YouTube channel details, such as subscriber count, channel creation date, and description.
- Displays sentiment analysis results using bar and pie charts.
- User-friendly web interface powered by "Streamlit".

--> Why We Chose These Models

-> Multilingual BERT (mBERT) for Sentiment Analysis
For sentiment analysis, we have chosen "Multilingual BERT (mBERT)", a transformer-based model trained on 104 languages with "Wikipedia data". This makes it highly effective for analyzing YouTube comments, which often appear in multiple languages. mBERT provides the following benefits:

- Language Versatility: Unlike traditional sentiment models trained only in English, mBERT can process diverse languages, making it ideal for global YouTube content.
- Contextual Understanding: Unlike bag-of-words approaches, mBERT leverages deep contextual embeddings to understand sentiment in a more nuanced way.
- Higher Accuracy: Compared to older models like Naïve Bayes and LSTMs, mBERT provides better sentiment classification accuracy due to its deep learning architecture.
- Scalability: mBERT efficiently handles large datasets, making it suitable for analyzing thousands of YouTube comments without significant performance loss.

While models like "VADER" and "TextBlob" work well for English sentiment analysis, they lack multilingual capabilities, making them less effective for global YouTube videos. Similarly, "GPT-based models" can be used for sentiment analysis but are often "computationally expensive" and may require extensive fine-tuning for multilingual understanding.

--> Google Gemini AI for Comment Summarization
For comment summarization, we leverage "Google Gemini AI", a powerful multimodal model trained to generate concise yet informative summaries.

Compared to OpenAI's GPT models, Gemini AI is optimized for large-scale summarization while maintaining efficiency and lower computational costs.

--> Setup & Installation

1. Clone the Repository

git clone https://github.com/Heet-2405/Youtube-Comments-Analyzer.git

2. Set Up API Keys
- YouTube API Key: Obtain it from the Google Cloud Console and replace the placeholder in 'YoutubeCommentScrapper.py'.
- Gemini AI API Key: Get it from Google AI Studio and add it to 'Sentiment_Analysis.py'.

--> Running the Application

streamlit run app.py

--> Conclusion
SummarEase provides a powerful yet easy-to-use platform for analyzing YouTube comments, offering detailed sentiment insights and AI-powered summarization. By leveraging "mBERT" for multilingual sentiment analysis and "Google Gemini AI" for summarization, this project ensures high accuracy, efficiency, and usability across diverse YouTube content. 

