from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def encode_to_unicode(text, base_phrase='Hello'):
    # Validate base phrase length
    if len(base_phrase) > 300:
        raise ValueError('Base phrase must not exceed 300 characters')
    if not base_phrase:
        raise ValueError('Base phrase cannot be empty')
    
    # Convert text to binary
    binary = ''.join(format(ord(c), '08b') for c in text)
    
    # Use variation selectors to encode binary data
    # We'll use VS1-VS8 (FE00-FE07) for encoding bits
    result = base_phrase[:-1]  # Get all characters except the last one
    last_char = base_phrase[-1]  # Get the last character
    
    # Start with the last character
    encoded_last_char = last_char
    
    for i in range(0, len(binary), 3):
        chunk = binary[i:i+3]
        # Pad the chunk with zeros if needed
        chunk = chunk.ljust(3, '0')
        # Convert binary chunk to decimal (0-7)
        selector_num = int(chunk, 2)
        # Add the variation selector
        encoded_last_char += chr(0xFE00 + selector_num)
    
    return result + encoded_last_char

def decode_from_unicode(encoded):
    if not encoded:
        return ''
    
    # Find the last base character and its variation selectors
    last_char_with_selectors = ''
    base_index = -1
    
    # Find the last regular character (non-variation selector)
    for i in range(len(encoded) - 1, -1, -1):
        if not (0xFE00 <= ord(encoded[i]) <= 0xFE07):
            base_index = i
            break
    
    if base_index == -1:
        return ''
    
    # Extract the encoded part (last character with its variation selectors)
    last_char_with_selectors = encoded[base_index:]
    
    binary = ''
    # Process each variation selector after the last character
    for i in range(1, len(last_char_with_selectors)):
        char = last_char_with_selectors[i]
        # Check if it's a variation selector
        if 0xFE00 <= ord(char) <= 0xFE07:
            # Convert the selector back to binary
            selector_num = ord(char) - 0xFE00
            binary += format(selector_num, '03b')
    
    # Convert binary back to text
    text = ''
    for i in range(0, len(binary) - 7, 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            text += chr(int(byte, 2))
    
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/encode', methods=['POST'])
def encode():
    secret = request.json.get('secret', '')
    base_phrase = request.json.get('base_char', 'Hello')  # Changed parameter name for clarity
    
    if not secret:
        return jsonify({'error': 'No secret provided'}), 400
    if not base_phrase:
        return jsonify({'error': 'No base phrase provided'}), 400
    
    try:
        encoded = encode_to_unicode(secret, base_phrase)
        return jsonify({
            'encoded': encoded,
            'original': secret,
            'base_phrase': base_phrase  # Updated response field name
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/decode', methods=['POST'])
def decode():
    encoded = request.json.get('encoded', '')
    if not encoded:
        return jsonify({'error': 'No encoded text provided'}), 400
    
    try:
        decoded = decode_from_unicode(encoded)
        return jsonify({
            'decoded': decoded,
            'encoded': encoded
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)