import base64

# Decode JWT
def decode_jwt(token):
    headers, payload, signature = token.split('.')
    headers_decoded = base64.urlsafe_b64decode(headers + '==').decode('utf-8')
    payload_decoded = base64.urlsafe_b64decode(payload + '==').decode('utf-8')
    return headers_decoded, payload_decoded