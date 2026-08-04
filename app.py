import streamlit as st
from google import genai
from PIL import Image

st.set_page_config(
    page_title="Gemini Health App",
    page_icon="🥗",
    layout="centered"
)

st.sidebar.title("⚙️ Settings")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password"
)

def get_gemini_response(client, prompt, image, user_input):
    response = client.models.generate_content(
        model="gemini-3.5-flash",
        contents=[
            prompt,
            image,
            user_input
        ]
    )

    return response.text

def input_image_setup(upload_file):
    if upload_file is None:
        raise FileNotFoundError("Please upload an image.")

    return Image.open(upload_file)



st.title("🥗 Gemini Health App")

st.write(
    "Upload a food image and Gemini will estimate the calories of each food item."
)

user_input = st.text_input(
    "Additional Prompt (Optional)"
)

uploaded_file = st.file_uploader(
    "Choose a food image...",
    type=["jpg", "jpeg", "png"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file)

    st.image(
        image,
        caption="Uploaded Image",
        use_container_width=True
    )

submit = st.button("🍽 Tell me the Total Calories")

input_prompt = """
You are an expert nutritionist.

Analyze the uploaded food image carefully.

For every food item:
1. Identify the food item.
2. Estimate the calories.
3. Mention the approximate serving size.

Finally provide:
- Total Calories
- Whether this meal is Healthy, Average or Unhealthy
- Suggest healthier alternatives if necessary.

Format:

1. Food Item - Calories
2. Food Item - Calories
3. Food Item - Calories

-------------------

Total Calories:
Health Rating:
Suggestions:
"""

if submit:

    if not api_key:
        st.error("Please enter your Gemini API Key in the sidebar.")
        st.stop()

    if uploaded_file is None:
        st.error("Please upload a food image.")
        st.stop()

    try:
        client = genai.Client(api_key=api_key)

        image = input_image_setup(uploaded_file)

        response = get_gemini_response(
            client,
            input_prompt,
            image,
            user_input
        )

        st.subheader("🍴 Nutrition Analysis")
        st.write(response)

    except Exception as e:
        st.error(f"Error: {e}")