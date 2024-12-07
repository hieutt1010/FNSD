import json
import os
from os import abort
from flask import request
from functools import wraps
from jose import jwt
from urllib.request import urlopen
from dotenv import load_dotenv

load_dotenv()
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = os.getenv('ALGORITHMS')
API_AUDIENCE = os.getenv('API_AUDIENCE')

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code

def get_token_auth_header():
    # Get auth type in header
    auth = request.headers.get('Authorization', None)
    if not auth:
        abort(401)
        
    # Check if not bearer type raise AuthError
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)

    elif len(parts) == 1:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Token not found.'
        }, 401)

    elif len(parts) > 2:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = parts[1]
    return token

def check_permissions(permission, payload):
    if 'permissions' not in payload:
        return 400
        
    if permission not in payload['permissions']:
        return 403
        
    return True

def verify_decode_jwt(token):
    # Verify token using Auth0 /.well-known/jwks.json
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}
    
    # Check kid exist in header
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed.'
        }, 401)
        
    # Store key-value from jwks.json
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
            
    # Decode the payload from the token
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )
            
            return payload
        
        # In case token has expired
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'The token has expired.'
            }, 401)
            
        # Common invalid claims    
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Please, check the audience and issuer.'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
            }, 400)
    raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to find the appropriate key.'
            }, 400)

def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            try:
                token = get_token_auth_header()
            except:
                return f(None,*args, **kwargs)
            payload = verify_decode_jwt(token)
            noti = check_permissions(permission, payload)
            if noti is not True: 
                return  f(noti,*args, **kwargs)
            return f(payload,*args, **kwargs)

        return wrapper
    return requires_auth_decorator