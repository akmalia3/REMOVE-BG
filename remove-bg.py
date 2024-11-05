import streamlit as st
from rembg import remove
from PIL import Image
import io

st.title("Remove Background🗑️")
st.write("Remove background from your image")

uploaded_files = st.file_uploader("Upload your image here⬇️", type=["jpg", "jpeg", "png"])

if uploaded_files is not None:
    # Display the uploaded image
    st.image(uploaded_files, caption="Original Image")

    # Open the image using PIL
    input_image = Image.open(uploaded_files)

    # Remove background when button is clicked
    if st.button('Remove bg'):
        # Show spinner during processing
        with st.spinner('Removing background...'):
            # Convert the PIL image to bytes for rembg
            with io.BytesIO() as output_bytes:
                input_image.save(output_bytes, format="PNG")
                img_data = output_bytes.getvalue()

            # Actual background removal
            output_image_data = remove(img_data)

            # Convert output bytes back to a PIL image and store it in session state
            st.session_state['output_image'] = Image.open(io.BytesIO(output_image_data))

        # Show success message
        st.success("Background removed successfully!")

    # Display the output image if it exists in session state
    if 'output_image' in st.session_state:
        st.image(st.session_state['output_image'], caption="Image without Background")

        # Convert the output image to bytes for downloading
        with io.BytesIO() as output_image_bytes:
            st.session_state['output_image'].save(output_image_bytes, format="PNG")
            output_image_bytes.seek(0)
            
            # Add persistent download button
            st.download_button(
                label="Download Image",
                data=output_image_bytes,
                file_name="output.png",
                mime="image/png"
            )
