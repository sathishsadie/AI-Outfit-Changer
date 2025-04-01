import streamlit as st
from PIL import Image
from model import detect_human
from inpaint import change_outfit

st.title("AI Outfit Changer 👗")
st.write("Upload an image of a person, and change their outfit!")

uploaded_file = st.file_uploader("Upload an Image", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded Image", use_column_width=True)
    person_image, human_mask = detect_human(uploaded_file)
    if person_image:
        st.image(person_image, caption="Detected Person", use_column_width=True)
        st.image(human_mask, caption="Generated Mask", use_column_width=True)

        outfit_style = st.selectbox("Select Outfit", ["Saree", "Tuxedo", "Casual", "Traditional"])

        outfit_prompts = {
            "Saree": "Change outfit to a traditional Indian saree",
            "Tuxedo": "Change outfit to a formal black tuxedo",
            "Casual": "Change outfit to a casual hoodie and jeans",
            "Traditional": "Change outfit to a cultural traditional dress"
        }

        if st.button("Generate Outfit"):
            output_image = change_outfit(person_image, human_mask, prompt=outfit_prompts[outfit_style])
            st.image(output_image, caption="Modified Outfit", use_column_width=True)
            output_image.save("output.png")
            st.download_button("Download Image", "output.png", "image/png")
    else:
        st.error("No human detected in the image!")
