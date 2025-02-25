# Unicode Steganography Web Tool

A web-based steganography tool that hides secret messages within regular text using Unicode variation selectors. This tool allows you to encode secret messages in a way that makes them invisible to casual observers while maintaining the appearance of normal text.

## How It Works

The tool uses Unicode variation selectors (VS1-VS8, range FE00-FE07) to encode binary data. These variation selectors are special Unicode characters that are typically invisible and are designed to modify the appearance of the preceding character. By cleverly using these selectors, we can hide information without visibly altering the text.

### Technical Details

1. **Encoding Process**:
   - Converts secret text to binary
   - Splits binary into 3-bit chunks
   - Maps each chunk to a variation selector (FE00-FE07)
   - Attaches these selectors to the last character of the base text

2. **Decoding Process**:
   - Extracts variation selectors from the encoded text
   - Converts selectors back to binary
   - Reconstructs the original secret message

## Features

- Clean, modern web interface
- Real-time encoding and decoding
- Customizable base text
- Support for any Unicode text input
- Length validation for base text (max 300 characters)

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/stegano_unicode.git
   cd stegano_unicode
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

### Encoding a Secret Message
1. Enter your secret message in the "Enter your secret text here" field
2. (Optional) Customize the base text in the "Enter base text" field
3. Click "Encode"
4. Copy the encoded result

### Decoding a Message
1. Paste the encoded text into the "Enter encoded Unicode text here" field
2. Click "Decode"
3. View the revealed secret message

## Dependencies

- Flask 2.3.3
- Werkzeug 2.3.7

## Security Considerations

While this tool provides a way to hide messages, it should not be considered a secure encryption method. The encoding is reversible by anyone who knows the technique. Use proper encryption for sensitive data.

## License

This project is open source and available under the MIT License.