import streamlit as st
import os
from Sentiment_Analysis import extract_video_id, analyze_sentiment, bar_chart, plot_sentiment, summarize_comments
from YoutubeCommentScrapper import save_video_comments_to_csv, get_channel_info, youtube, get_channel_id, get_video_stats

def delete_non_matching_csv_files(directory_path, video_id):
    for file_name in os.listdir(directory_path):
        if not file_name.endswith('.csv'):
            continue
        if file_name == f'{video_id}.csv':
            continue
        os.remove(os.path.join(directory_path, file_name))

st.set_page_config(page_title="Sentiment Analysis", layout="centered")

# **Project Title and Team Name**
st.markdown("<h1 style='text-align: center;'>YT Sentiment Analysis</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: grey;'>By Team "CodeBros"</h3>", unsafe_allow_html=True)

# Hide Streamlit Style Elements
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

# Centered URL input box
st.markdown("""
    <style>
    .centered-textbox { display: flex; justify-content: center; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='centered-textbox'>", unsafe_allow_html=True)
youtube_link = st.text_input("Enter YouTube Link", "", key="youtube_link")
st.markdown("</div>", unsafe_allow_html=True)

if youtube_link:
    video_id = extract_video_id(youtube_link)
    channel_id = get_channel_id(video_id)
    if video_id and channel_id:
        csv_file = save_video_comments_to_csv(video_id)
        delete_non_matching_csv_files(os.getcwd(), video_id)
        
        st.write("### The video ID is:", video_id)
        
        with open(csv_file, 'rb') as file:
            st.download_button(label="Download Comments", data=file, file_name=os.path.basename(csv_file), mime="text/csv")
        
        # Fetch channel information
        channel_info = get_channel_info(channel_id)
        if channel_info:
            st.image(channel_info['channel_logo_url'], width=250)
            st.subheader("YouTube Channel Name")
            st.title(channel_info['channel_title'])
            st.write(f"**Total Videos:** {channel_info['video_count']}")
            st.write(f"**Channel Created:** {channel_info['channel_created_date'][:10]}")
            st.write(f"**Subscriber Count:** {channel_info['subscriber_count']}")
        
        # Fetch video statistics
        stats = get_video_stats(video_id)
        if stats:
            st.write("### Video Information")
            st.write(f"**Total Views:** {stats.get('viewCount', 'N/A')}")
            st.write(f"**Like Count:** {stats.get('likeCount', 'N/A')}")
            st.write(f"**Comment Count:** {stats.get('commentCount', 'N/A')}")
        
        st.video(youtube_link)
        
        # Perform Sentiment Analysis
        results = analyze_sentiment(csv_file)
        st.write("### Sentiment Analysis Results")
        st.write(f"**Positive Comments:** {results['num_positive']}")
        st.write(f"**Negative Comments:** {results['num_negative']}")
        st.write(f"**Neutral Comments:** {results['num_neutral']}")
        
        # Plot sentiment analysis results
        bar_chart(csv_file)
        plot_sentiment(csv_file)
        
        # Summarize Comments using AI
        st.write("### AI-Powered Summary of Comments")
        summary = summarize_comments(csv_file)
        st.write(summary)
    else:
        st.error("Invalid YouTube link")
