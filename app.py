import streamlit as st 
from dotenv import load_dotenv

load_dotenv() # loads all the environment variables
import os
import google.generativeai as genai 

from youtube_transcript_api import YouTubeTranscriptApi

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

prompt = """Act like an YouTube video summarizer, and  you are going to take the
        transcript text and you are going to summarize the entire video provide 
        the important summary in points about the video within 200-220 words.     
        """

# prompt = """Create a YouTube video summary with detailed information. Extract the YouTube channel name, 
#             the Person's name, the video's topic, and then provide a concise summary within 200-220 words. 
#             Utilize the provided transcript text below for the summary:

#             [Insert Transcript Text Here]

#             Ensure to include key points and highlight the main ideas discussed in the video.
#             Please provide information on the YouTube channel's name, the host speaking in the video, 
#             the topic they are addressing, ou are going to summarize the entire video provide 
#             the important summary in points about the video within 200-220 words.  
#             here is the text you need
#             """


# Extract the transcript text from the Youtube video
def extract_transcript(YouTube_URL):
    try:
        video_id = YouTube_URL.split('=')[1]
        print(video_id)
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        transcript_t = ""
        for i in transcript:
            transcript_t += " " + i["text"]

        return transcript_t

    except Exception as e:
        raise e


# Extract the summary from transcript text using Google gemini Pro
def generate_gemini_con(transcript, prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt+transcript)
    return response.text





st.set_page_config(
    page_title="YouTube Video Summary App",
    page_icon="🎥",
    layout="wide"
)

# Load the YouTube icon image from your local system
youtube_icon_path = "youtube_icon.png"

# Streamlit app
st.image(youtube_icon_path, width=50, caption="")
st.title("Get the Summary of a YouTube Video")


Youtube_link = st.text_input("Paste YouTube video Link Here")

if Youtube_link:
    video_id = Youtube_link.split('=')[1]
    image_url = f"http://img.youtube.com/vi/{video_id}/0.jpg"
    
    # Display the image using HTML
    st.markdown(f'<img src="{image_url}" alt="YouTube Thumbnail" style="width:450px;">', unsafe_allow_html=True)

# if Youtube_link:
#     video_id = Youtube_link.split('=')[1] 
#     print(video_id)
#     image_url = "http://img.youtube.com/vi/" + video_id + "/0.jpg"
#     st.image(image_url, width=50, use_column_width=True)

if st.button("Get the Detailed Summary"):
    transcript = extract_transcript(Youtube_link)

    if transcript:
        summary = generate_gemini_con(transcript,prompt)
        st.subheader("Here is the summary")    
        st.write(summary)




