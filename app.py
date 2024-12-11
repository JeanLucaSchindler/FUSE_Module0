import streamlit_authenticator as stauth
from dotenv import load_dotenv
import streamlit as st
import openai
import os
import io

# Load environment variables
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Authentication setup
names = ["Fusian"]
usernames = ["fusian"]  # Corresponding username
hashed_passwords = stauth.Hasher(["ILoveFUSE_mod0"]).generate()

authenticator = stauth.Authenticate(
    names,
    usernames,
    hashed_passwords,
    "cookie_name",
    "signature_key",
    cookie_expiry_days=30
)

# Authentication flow
name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status:
    # Set query parameter for redirection
    st.query_params.from_dict({"page": "main"})
    st.write(f"Welcome, {name}!")
    st.title("FUSE - Module 0")

    # Text input from the user
    input_text = st.text_area("Enter your text here:", height=200)

    # User provides a question
    question = st.text_input("Ask a question about the text:")

    # Button to get an answer
    if st.button("Get Answer"):
        if not input_text.strip() or not question.strip():
            st.error("Please provide both text and a question.")
        else:
            # Construct the prompt
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions about a given text."
                },
                {
                    "role": "user",
                    "content": f"Text: {input_text}\n\nQuestion: {question}\n\nPlease provide the best possible answer."
                }
            ]

            try:
                response = openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=messages,
                    max_tokens=500,
                    temperature=0.7
                )

                # Extract the answer
                answer = response.choices[0].message.content.strip()
                st.write("**Answer:**", answer)

                # Provide a download button for the answer
                download_buffer = io.StringIO(answer)
                st.download_button(
                    label="Download Answer",
                    data=download_buffer.getvalue(),
                    file_name="answer.txt",
                    mime="text/plain"
                )

                # Provide a download button for the input text
                input_buffer = io.StringIO(input_text)
                st.download_button(
                    label="Download Input Text",
                    data=input_buffer.getvalue(),
                    file_name="input_text.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"Error: {str(e)}")
elif authentication_status is False:
    st.error("Username/password is incorrect")
elif authentication_status is None:
    st.warning("Please enter your username and password")
else:
    # Redirect to login if not authenticated
    st.query_params.from_dict({"page": "login"})
