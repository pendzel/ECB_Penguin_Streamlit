
# 🐧 ECB Penguin Streamlit App

## Overview

Welcome to the **ECB Penguin Streamlit App**! This application demonstrates the encryption of images using two different modes of AES encryption: **ECB (Electronic Codebook)** and **CBC (Cipher Block Chaining)**. The app provides a visual comparison between these modes to highlight the security weaknesses of ECB encryption.

## Features

- **Upload and Encrypt Images**: Upload an image and see how it's encrypted using both ECB and CBC modes.
- **Download Options**: Download the original and encrypted images.
- **GIF Creation**: View and download GIFs that illustrate the differences between the original and encrypted images.

## Why Use This App?

When data is encrypted using **ECB mode**, identical blocks of plaintext are encrypted into identical blocks of ciphertext. This means that patterns in the plaintext are not hidden, making ECB mode highly insecure for data encryption.

**CBC mode**, on the other hand, uses an initialization vector (IV) and chains the encryption process, ensuring that identical plaintext blocks result in different ciphertext blocks. This effectively hides patterns and provides better security.

## Getting Started

Follow these steps to get the app up and running on your local machine:

### Prerequisites

- Python 3.6 or higher
- Streamlit
- Required Python packages (listed in `requirements.txt`)

### Installation

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/ECB_Penguin_Streamlit_app.git
    cd ECB_Penguin_Streamlit_app
    ```

2. **Install the required packages:**
    ```sh
    pip install -r requirements.txt
    ```

3. **Run the Streamlit app:**
    ```sh
    streamlit run ECB_Penguin_Streamlit_app.py
    ```

## Usage

1. **Upload an image** using the file uploader in the app.
2. The app will encrypt the image using both ECB and CBC modes and display the results.
3. **Download** the original and encrypted images using the provided buttons.
4. **View and download GIFs** that demonstrate the differences between the original and encrypted images.

## Learn More

### Further Reading:
- [The ECB Penguin - Filippo Valsorda](https://words.filippo.io/the-ecb-penguin/)
- [Electronic Codebook - Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Electronic_Codebook_(ECB))
- [Cipher Block Chaining (CBC) - Wikipedia](https://en.wikipedia.org/wiki/Block_cipher_mode_of_operation#Cipher_Block_Chaining_(CBC))
- [Block Cipher Modes of Operation - NIST](https://csrc.nist.gov/publications/detail/sp/800-38a/final)
- [Why not use ECB encryption? - Stack Exchange](https://crypto.stackexchange.com/questions/20941/why-shouldnt-i-use-ecb-encryption)
- [Modes of Operation - Crypto101](https://crypto101.io/chapter6/)
- [Introduction to Block Cipher Modes - Applied Crypto Hardening](https://bettercrypto.org/applied-crypto-hardening/book/v1.0.0/9-Block-cipher-modes.html)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or feedback, feel free to reach out to the repository owner.

---

Feel free to customize this README to better fit your specific needs or preferences.
