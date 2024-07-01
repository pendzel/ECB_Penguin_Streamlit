import streamlit as st
import numpy as np
from PIL import Image
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import io

# Cache encryption functions
@st.cache_data
def encrypt_ecb(key, plaintext):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes long")
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return ciphertext, len(padded_data)

@st.cache_data
def encrypt_cbc(key, plaintext):
    if len(key) != 16:
        raise ValueError("Key must be 16 bytes long")
    
    iv = os.urandom(16)
    
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(plaintext) + padder.finalize()
    
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()
    return iv + ciphertext, len(padded_data)

@st.cache_data
def display_image_from_encrypted(encrypted_data, original_shape):
    encrypted_array = np.frombuffer(encrypted_data, dtype=np.uint8)
    if len(encrypted_array) < np.prod(original_shape):
        encrypted_array = np.pad(encrypted_array, (0, np.prod(original_shape) - len(encrypted_array)), 'constant', constant_values=(0,))
    encrypted_array = encrypted_array.reshape(original_shape)
    encrypted_image = Image.fromarray(encrypted_array)
    return encrypted_image

@st.cache_data
def convert_image_to_bytes(image):
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr

@st.cache_data
def create_gif(images, duration=500):
    gif_byte_arr = io.BytesIO()
    images[0].save(gif_byte_arr, format='GIF', save_all=True, append_images=images[1:], duration=duration, loop=0)
    gif_byte_arr.seek(0)
    return gif_byte_arr

def resize_image(image, max_size):
    # Calculate the new size preserving the aspect ratio
    width, height = image.size
    if width > height:
        new_width = max_size
        new_height = int((height / width) * max_size)
    else:
        new_height = max_size
        new_width = int((width / height) * max_size)
    return image.resize((new_width, new_height))



#################### Streamlit App ####################

## Set Streamlit layout to wide
st.set_page_config(layout="wide")
# title with penguin emoji
st.markdown("# 🐧 Create Your Own ECB Penguin 🐧\n###### Visualizing AES Encryption Modes")

st.markdown("""
    This application demonstrates the encryption of images using two different modes of AES encryption: **ECB (Electronic Codebook)** and **CBC (Cipher Block Chaining)**.""")

# Expander for ECB Penguin example and explanation
with st.expander("Why ECB Mode is Insecure: The ECB Penguin Example",icon="❓",expanded=False):
    st.markdown("""
**The ECB Encryption Example:**

When data is encrypted using **ECB mode**, identical blocks of plaintext are encrypted into identical blocks of ciphertext. This means that patterns in the plaintext are not hidden, making ECB mode highly insecure for data encryption.

The classic example of this problem is the "ECB Penguin". When an image of a penguin is encrypted using ECB mode, the encrypted data still reveals the structure of the penguin, demonstrating that ECB does not provide sufficient security.

**Issues with ECB Mode:**
- **Pattern Leakage:** Identical plaintext blocks produce identical ciphertext blocks, revealing patterns.
- **Predictability:** An attacker can predict the content of encrypted messages if they know the structure of the plaintext.
- **Lack of Confidentiality:** Does not adequately hide the structure of the plaintext.

**CBC Mode:** In contrast, **CBC mode** uses an initialization vector (IV) and chains the encryption process, ensuring that identical plaintext blocks result in different ciphertext blocks, effectively hiding patterns and providing better security. This results in a pseudo-random appearance of the encrypted data, which better preserves the confidentiality of the original content.

While CBC is used in this example, other modes like **CTR (Counter)** mode, **CFB (Cipher Feedback)** mode, and **OFB (Output Feedback)** mode can also achieve similar results in terms of hiding patterns and providing strong encryption.


""")
    ## Furter reading links
    with st.popover("Furter reading links"):
        st.markdown("""
        - [The ECB Penguin - Filippo Valsorda](https://words.filippo.io/the-ecb-penguin/)
        - [ECB Mode Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_codebook_(ECB))
        - [CBC Mode Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_(CBC))
        - [AES Encryption Wikipedia](https://en.wikipedia.org/wiki/Advanced_Encryption_Standard)
        - [Why not use ECB encryption? - Stack Exchange](https://crypto.stackexchange.com/questions/20941/why-shouldnt-i-use-ecb-encryption)
        - [Exploring an Encrypted Penguin with AES-ECB - Anthony Biondo](https://tonybox.net/posts/ecb-penguin/)
        """)
        



    original_penguin_col, ecb_penguin_col, cbc_penguin_col = st.columns(3)
    
    with original_penguin_col:
        with st.container(border=True):
            st.image("Images/original_image.png", caption='Original Image', use_column_width=True)
            

    with ecb_penguin_col:
        with st.container(border=True):
            st.image("Images/ECB_encrypted_image.png", caption='ECB Encrypted Image', use_column_width=True)
            st.image("Images/ECB_encryption.png", use_column_width=True)
    with cbc_penguin_col:
        with st.container(border=True):
            st.image("Images/CBC_encrypted_image.png", caption='CBC Encrypted Image', use_column_width=True)
            st.image("Images/CBC_encryption.png", use_column_width=True)


## expander for instructions
with st.expander(label= "📋 Instructions",expanded=False):
    st.markdown("""
    1. 📂 **Upload an image** using the file uploader below.
    2. 🔒 **The app will encrypt the image using both ECB and CBC modes** and display the results.
    3. 📥 **You can download the original and encrypted images** using the provided buttons.
    4. 🎞️ **Additionally, GIFs are created** to visually demonstrate the differences between the original and encrypted images, emphasizing the security weaknesses of ECB mode.

    **⚠️ Note:** ECB mode is not recommended for encrypting data due to its security weaknesses, as demonstrated below.
    """)

# Load an image from file
uploaded_file = st.file_uploader("Choose an image...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Get file size and name
    file_size = uploaded_file.size
    file_name = uploaded_file.name
    
    # Inform user about the file size and name
    st.toast(f"Uploaded file: {file_name} ({file_size / 1024:.2f} KB)")
    
    # Read the image using PIL
    image = Image.open(uploaded_file)
    image = image.convert('RGB')  # Ensure image is in RGB format
    image_array = np.array(image)
    
    # Flatten the image array for encryption
    image_bytes = image_array.tobytes()
    
    # Define a key for encryption
    key = b'0123456789abcdef'  # Example key (16 bytes)

    # Encrypt the image bytes using ECB and CBC modes
    ecb_encrypted_bytes, ecb_padded_length = encrypt_ecb(key, image_bytes)
    cbc_encrypted_bytes, cbc_padded_length = encrypt_cbc(key, image_bytes)
    
    # Truncate data to fit the original length
    ecb_encrypted_bytes = ecb_encrypted_bytes[:len(image_bytes)]
    cbc_encrypted_bytes = cbc_encrypted_bytes[:len(image_bytes)]
    
    # Create 3 columns for displaying images
    col1, col2, col3 = st.columns(3)
    with col1:
        with st.container(border=True):
            st.image(image, caption='Original Image', use_column_width=True)
            # Convert original image to bytes for download
            original_img_bytes = convert_image_to_bytes(image)
            st.download_button(label="Download Original Image", data=original_img_bytes, file_name="original_image.png", mime="image/png")
    with col2:
        with st.container(border=True):
            ecb_encrypted_image = display_image_from_encrypted(ecb_encrypted_bytes, image_array.shape)
            st.image(ecb_encrypted_image, caption='ECB Encrypted Image', use_column_width=True)

            # Convert ECB encrypted image to bytes for download
            ecb_img_bytes = convert_image_to_bytes(ecb_encrypted_image)
            st.download_button(label="Download ECB Encrypted Image", data=ecb_img_bytes, file_name="ecb_encrypted_image.png", mime="image/png")



            st.divider()
            # Create and display a GIF with the original and ECB encrypted images
            gif_images_ecb = [image, ecb_encrypted_image]
            original_gif_bytes_ecb = create_gif(gif_images_ecb, duration=500)  # Set duration to 0.5 second for better visualization

            # Resize images for GIF display to fixed resolution while maintaining aspect ratio
            resized_image = resize_image(image, max_size=480)
            resized_ecb_encrypted_image = resize_image(ecb_encrypted_image, max_size=480)
            
            display_gif_bytes_ecb = create_gif([resized_image, resized_ecb_encrypted_image], duration=500)

            

            st.image(display_gif_bytes_ecb, caption='Original and ECB Encrypted Image GIF (Resized for display)', use_column_width=True)
            st.download_button(label="Download Original GIF (ECB)", data=original_gif_bytes_ecb, file_name="original_ecb.gif", mime="image/gif")
        
    
    with col3:
        with st.container(border=True):
            cbc_encrypted_image = display_image_from_encrypted(cbc_encrypted_bytes, image_array.shape)
            st.image(cbc_encrypted_image, caption='CBC Encrypted Image', use_column_width=True)
    
            # Convert CBC encrypted image to bytes for download
            cbc_img_bytes = convert_image_to_bytes(cbc_encrypted_image)
            st.download_button(label="Download CBC Encrypted Image", data=cbc_img_bytes, file_name="cbc_encrypted_image.png", mime="image/png")


            st.divider()


            # Create and display a GIF with the original and CBC encrypted images
            gif_images_cbc = [image, cbc_encrypted_image]
            original_gif_bytes_cbc = create_gif(gif_images_cbc, duration=500)  # Set duration to 0.5 second for better visualization

            # Resize images for GIF display to fixed resolution while maintaining aspect ratio
            resized_image = resize_image(image, max_size=480)
            resized_cbc_encrypted_image = resize_image(cbc_encrypted_image, max_size=480)
            
            display_gif_bytes_cbc = create_gif([resized_image, resized_cbc_encrypted_image], duration=500)
            
            st.image(display_gif_bytes_cbc, caption='Original and CBC Encrypted Image GIF (Resized for display)', use_column_width=True)
            st.download_button(label="Download Original GIF (CBC)", data=original_gif_bytes_cbc, file_name="original_cbc.gif", mime="image/gif")