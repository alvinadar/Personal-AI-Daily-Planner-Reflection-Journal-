import streamlit as st 
import google.generativeai as genai
import pandas as pd
import os#Operating system library to access environment variables
from datetime import datetime
from dotenv import load_dotenv


#Load the API KEY from the .env file
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
#We need to define what model we want to use. 
model = genai.GenerativeModel("gemini-2.5-pro")

#Page SetUp 
st.set_page_config(page_title="AI Daily Planner ",layout="centered")
st.title("Personal AI Daily Planner & Reflection Journal")
st.caption("Your AI daily companion")

#File for storing the daily plans and reflections
DATA_FILE = "journal_data.csv"

#Take the inputs from the journal and store them in a dataframe
def save_entry(entry_type,content,mood = None):
    """Create a new entry in the journal data file."""
    new_row = pd.DataFrame([{
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "type": entry_type,
        "content": content,
        "mood": mood
    }])
    if os.path.exists(DATA_FILE):#Checking for the file 
        new_row.to_csv(DATA_FILE, mode="a", header=False, index=False)
    else:
        new_row.to_csv(DATA_FILE, index=False)

#Function to send a prompt to the model and get a response
def ask_gemini(prompt):
   try:
       response = model.generate_content(prompt)
       return response.text
   except Exception as e:
       return f"Error : {e}"

#Tabs 
tab1,tab2,tab3,tab4 = st.tabs(["☀️ Morning","☁️ Mood","🌙 Evening","📈 Insights"])

# --- MORNING PLANNER ---
with tab1:
    st.subheader("Plan your day")
    task = st.text_area("What do you want to get done today?",
                        placeholder="e.g. Finish math homework , read 20 pages,gym at 6Pm")
    if st.button("Get my plan",key="plan"):
        if task.strip():
            with st.spinner("Generating your plan..."):
                 prompt = f"""You are a friendly productivity coach. The user listed these tasks for today:

{task}

Give a short response (under 150 words) with:
1. A suggested priority order
2. Rough time blocks
3. One warning if the day looks overpacked, OR one encouragement if it looks balanced.

Be warm, practical, and concise."""
                 plan = ask_gemini(prompt)
                 st.success(plan)
                 save_entry("morning",task)
        else:
            st.warning("Please enter some tasks to get a plan!")