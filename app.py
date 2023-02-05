import requests
import streamlit as st
import time

IMG_URL = st.secrets.endpoints.IMG_URL
# API endpoint URLs
DALLE_API = st.secrets.endpoints.DALLE_API
STABLE_DIFFUSION_API = st.secrets.endpoints.STABLE_DIFFUSION_API

# API credentials
DALLE_API_KEY = st.secrets.credentials.DALLE_API_KEY
STABLE_DIFFUSION_API_KEY = st.secrets.credentials.STABLE_DIFFUSION_API_KEY


@st.cache
def generate_dalle_image(prompt):
    image_url = f'{IMG_URL}'
    headers = {"Authorization": f"Bearer {DALLE_API_KEY}"}
    model = "image-alpha-001"
    data = {
        "model": model,
        "prompt": prompt,
        "num_images": 1,
        "size": "1024x1024"
    }
    response = requests.post(DALLE_API, headers=headers, json=data)
    response.raise_for_status()
    image_url = response.json()["data"][0]["url"]
    return image_url


@st.cache
def generate_stable_diffusion_image(prompt):
    image_url = f'{IMG_URL}'
    headers = {
        "Authorization": f"Token {STABLE_DIFFUSION_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "version":
        "f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1",
        "input": {
            "prompt": prompt
        }
    }
    response = requests.post(STABLE_DIFFUSION_API, headers=headers, json=data)
    response.raise_for_status()

    prediction_id = response.json()["id"]
    status = response.json()["status"]

    while status == "starting" or status == "processing":
        time.sleep(5)
        prediction_response = requests.get(
            f"https://api.replicate.com/v1/predictions/{prediction_id}",
            headers=headers)
        status = prediction_response.json()["status"]

    if status == "succeeded":
        image_url = prediction_response.json()["output"][0]
    return image_url


st.title("Image Generation with DALLE and Stable Diffusion APIs")

prompt = st.text_input("Enter a prompt:")

if st.button("Submit") and prompt:
    empty1, content1, empty2, content2, empty3 = st.columns(
        [0.3, 1.2, 0.3, 1.2, 0.3])
    with empty1:
        st.empty()
    with content1:
        st.header("DALLE API output")
        dalle_image_url = generate_dalle_image(prompt)
        st.image(dalle_image_url)
    with empty2:
        st.empty()
    with content2:
        st.header("Stable Diffusion API output")
        stable_diffusion_image_url = generate_stable_diffusion_image(prompt)
        st.image(stable_diffusion_image_url)
    with empty3:
        st.empty()
