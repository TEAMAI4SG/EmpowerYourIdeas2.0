import os
import openai
import streamlit as st 
import time
import pandas as pd
import toml
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# --- Load API key correctly from secrets.toml ---
openai.api_key = st.secrets["OPENAI_API_KEY"] 

# Layout settings
col1, col2 = st.columns([1, 4])
with col1:
    st.image("Logo.jpg", width=125)
with col2:
    st.header("Empower Your Ideas", divider="blue")

# Create a wrapper function
def get_completion(prompt, model="gpt-3.5-turbo"):
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": f"""
                You are an expert AI researcher and developer.  
                
                First, summarize the {articles}. Based on the summary, list the problems for all stakeholders.  
                Then, clearly explain how each stakeholder's needs can be met.  
                
                Suggest some creative project ideas to address the {problem} and incorporate the {technologies} 
                along with {oth_technologies}.  
                
                For each of the {technologies} and {oth_technologies}, provide an example of how the project 
                could be implemented in real life.  
                
                Finally, provide sample {datasets} related to the {problem} formatted in a table.  
                Organize the information using bolded headings, add bullet points, and incorporate emojis.  
                
                Provide consistent output for the user every time.
                """
            },
            {"role": "user", "content": prompt},
        ]
    )
    return completion.choices[0].message.content

# Fix missing "major" variable in get_image()
def get_image(prompt):
    if not prompt.strip():  # Ensure prompt is not empty or just spaces
        st.warning("Error: A valid prompt is required for image generation.")
        return None  # Prevents making an invalid API call

    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        size="1024x1024",
        quality="standard",
        n=1,
    )
    
    return response.data[0].url

# Streamlit app description
st.caption("Welcome to Empower Your Ideas, the ultimate platform for students to brainstorm and develop projects that contribute to a better world. \
           Here, we encourage you to harness your creativity and passion to create new AI-powered solutions. Together, we can build a sustainable future!")

with st.form(key="chat"):
    problem = st.text_input("Please enter the community problem you're trying to solve:")
    articles = st.text_area("Enter the website links associated with your chosen problem:")
    technologies = st.multiselect("**Select the technologies you're interested in:**", ["Text Generation", "Image Generation", "Speech to Text", "Text Summarization", "Key Point Extraction", "Action Item Extraction", "Sentiment Analysis", "Language Translation", "Text to Speech", "Computer Vision", "Chatbot"])
    oth_technologies = st.text_input("If your preferred technologies aren't listed, enter them here:")
    datasets = st.text_input("List any datasets you might consider including:")
    major = st.text_input("Enter the subject or major you want an image for:")
    submitted = st.form_submit_button("Submit")

    prompt = f"For a community member solving {problem} who is interested in experimenting with {technologies}, reading {articles}, and plans to use {datasets}"

    with st.spinner("Here we go!"):
        time.sleep(5)

    if submitted:
        missing_fields = []  # List to store missing fields

        if not problem.strip():
            missing_fields.append("Problem")
        if not technologies:  # Ensure at least one technology is selected
            missing_fields.append("Technologies")

        if missing_fields:  
            st.error(f"Please fill out the following required fields: {', '.join(missing_fields)}.")
        else:
            st.success("Gathering project ideas...")
            response_text = get_completion(prompt)
            st.write(response_text)

            # Generate an image only if 'major' is provided (optional)
            if major.strip():  
                st.image(get_image(major), caption="Generated Image")
