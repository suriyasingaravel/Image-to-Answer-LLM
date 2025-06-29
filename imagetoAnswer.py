import streamlit as st
import base64
from openai import OpenAI


# Set your OpenAI API key here (store securely in production)
api_key = st.secrets["OPENAI_API_KEY"]
client = OpenAI(api_key=api_key)

st.title("OpenAI Vision Chat App")
st.write("Upload an image and ask a question about it.")

# Image upload
uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])

# Prompt input
user_prompt = st.text_input("Enter your prompt/question:")

# Process on button click
if uploaded_file and user_prompt:
    # Encode image in base64
    image_bytes = uploaded_file.read()
    encoded_image = base64.b64encode(image_bytes).decode("utf-8")

    # Construct image prompt
    image_prompt = f"I have uploaded an image. Based on the image please answer: {user_prompt}. Be detailed and show any calculation or reasoning steps if required."

    # Make request to OpenAI
    with st.spinner("Generating response..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4.1-mini",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": image_prompt},
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}}
                        ]
                    }
                ]
            )
            answer = response.choices[0].message.content
            st.success("Response:")
            st.markdown(answer)
        except Exception as e:
            st.error(f"Error: {e}")
else:
    st.info("Please upload an image and enter a prompt.")
