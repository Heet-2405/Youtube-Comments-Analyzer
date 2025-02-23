import streamlit as st
import os
from Sentiment_Analysis import extract_video_id, analyze_sentiment, bar_chart, plot_sentiment, summarize_comments
from Scrapper import save_video_comments_to_csv, get_channel_info, youtube, get_channel_id, get_video_stats

def delete_non_matching_csv_files(directory_path, video_id):
    for file_name in os.listdir(directory_path):
        if not file_name.endswith('.csv'):
            continue
        if file_name == f'{video_id}.csv':
            continue
        os.remove(os.path.join(directory_path, file_name))

st.set_page_config(page_title="Sentiment Analysis", layout="centered")
st.sidebar.title("Sentiment Analysis")
st.sidebar.header("Enter YouTube Link")
youtube_link = st.sidebar.text_input("Link")
directory_path = os.getcwd()

# Hide Streamlit Style Elements
hide_st_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
st.markdown(hide_st_style, unsafe_allow_html=True)

if youtube_link:
    video_id = extract_video_id(youtube_link)
    channel_id = get_channel_id(video_id)
    if video_id and channel_id:
        st.sidebar.write("The video ID is:", video_id)     
        csv_file = save_video_comments_to_csv(video_id)
        delete_non_matching_csv_files(directory_path, video_id)
        st.sidebar.write("Comments saved to CSV!")
        
        with open(csv_file, 'rb') as file:
            st.sidebar.download_button(label="Download Comments", data=file, file_name=os.path.basename(csv_file), mime="text/csv")
        
        # Fetch channel information
        channel_info = get_channel_info(channel_id)
        
        if channel_info:
            col1, col2 = st.columns(2)
            with col1:
                st.image(channel_info['channel_logo_url'], width=250)
            with col2:
                st.subheader("YouTube Channel Name")
                st.title(channel_info['channel_title'])
        
            col3, col4, col5 = st.columns(3)
            with col3:
                st.header("Total Videos")
                st.subheader(channel_info['video_count'])
            with col4:
                st.header("Channel Created")
                st.subheader(channel_info['channel_created_date'][:10])
            with col5:
                st.header("Subscriber Count")
                st.subheader(channel_info['subscriber_count'])
        
        # Fetch video statistics
        stats = get_video_stats(video_id)
        if stats:
            st.header("Video Information")
            col6, col7, col8 = st.columns(3)
            with col6:
                st.header("Total Views")
                st.subheader(stats.get("viewCount", "N/A"))
            with col7:
                st.header("Like Count")
                st.subheader(stats.get("likeCount", "N/A"))
            with col8:
                st.header("Comment Count")
                st.subheader(stats.get("commentCount", "N/A"))
            
        st.video(youtube_link)

         # Perform Sentiment Analysis
        results = analyze_sentiment(csv_file)
        col9, col10, col11 = st.columns(3)
        with col9:
            st.header("Positive Comments")
            st.subheader(results['num_positive'])
        with col10:
            st.header("Negative Comments")
            st.subheader(results['num_negative'])
        with col11:
            st.header("Neutral Comments")
            st.subheader(results['num_neutral'])
        
        # Plot sentiment analysis results
        bar_chart(csv_file)
        plot_sentiment(csv_file)

        # Summarize Comments using OpenAI
        st.header("AI-Powered Summary of Comments")
        summary = summarize_comments(csv_file)
        st.write(summary)

    else:
        st.error("Invalid YouTube link")