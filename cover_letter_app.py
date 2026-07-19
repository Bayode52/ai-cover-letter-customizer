import streamlit as st
from groq import Groq

st.title("📝 AI Cover Letter Customizer")
st.write("Paste a job description and your background. Get a tailored cover letter draft in seconds.")

# --SIDEBAR: API Key---
st.sidebar.header("Settings")
api_key = st.sidebar.text_input("Enter your Groq API key", type="password")
st.sidebar.caption("Get a free key at console.groq.com")

#---Main Input---
job_description = st.text_area("Paste the job description", height=200)
your_background = st.text_area("Paste your CV or background", height=200)
#---Generate Button
if st.button("Generate Cover Letter"):
    #Validation
    if not api_key:
        st.error("Enter your Groq API key in the sidebar.")
    elif not job_description.strip():
        st.error("Paste the job description.")
    elif not your_background.strip():
        st.error("Paste your background or CV.")
    else:
        #Build the prompt
        prompt = f"""
You are a professional cover letter writer.
Write a tailored cover letter based on the job description and the candidate's background below.
Rules:
- Keep it under 300 words.
- Use a professional but warm tone.
- Highlight the candidate's relevant skills for this specific role.
-Do not invent experience that isn't listed in the background.
- Start with "Dear Hiring Manager," and end with "Sincerely,".
Job Description:
{job_description}
Candidate Background:
{your_background}

Cover Letter:
"""
        try:
            # Initialize Groq client
            client = Groq(api_key=api_key)

            # call the AI model
            response = client.chat.completions.create(
                model = "llama-3.1-8b-instant",
                messages = [
                    {"role": "system", "content": "You are a helpful career assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1024 
            )

            #Extract the response
            cover_letter = response.choices[0].message.content

            # Display the result 
            st.subheader("Your Cover Letter")
            st.write(cover_letter)

            #Download button
            st.download_button(
                label="Download as .txt",
                data = cover_letter,
                file_name = "cover_letter.txt",
                mime = "text/plain"
            )
           
        except Exception as e:
            st.error(f"Something went wrong: {e}")
