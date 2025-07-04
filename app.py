import streamlit as st
import requests

API_KEY = st.secrets["STABILITY_API_KEY"]

def generate_image(prompt, bw=False):
    url = "https://api.stability.ai/v2beta/stable-image/generate/core"

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Accept": "image/*"
    }

    # Modify prompt if B&W selected
    if bw:
        prompt = "black and white photo of " + prompt

    files = {
        "prompt": (None, prompt),
        "model": (None, "stable-diffusion-xl-v1"),
        "output_format": (None, "png")
    }

    response = requests.post(url, headers=headers, files=files)


    if response.status_code == 200:
        return response.content, None
    else:
        try:
            return None, response.json().get("error", {}).get("message", "Image generation failed.")
        except:
            return None, f"Error: {response.status_code} - {response.text}"


st.set_page_config(page_title="Text to Image Generator", layout="centered")
st.title("🎨 AI Text To Image Generator")

prompt = st.text_area("Enter your prompt:", height= 150)
bw_option = st.selectbox("Choose Image Style:", ["Color", "Black & White"])

if st.button("Generate Image"):
    if not prompt:
        st.warning("Please enter a prompt.")
    else:
        with st.spinner("Generating image..."):
            is_bw = bw_option == "Black & White"
            image_data, error = generate_image(prompt, is_bw)

            if error:
                st.error(error)
            else:
                st.image(image_data,  use_column_width=True)

                # Download button
                st.download_button(
                    label="📥 Download Image",
                    data=image_data,
                    file_name="generated_image.png",
                    mime="image/png"
                )
