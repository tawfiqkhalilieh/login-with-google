from fastapi import FastAPI, Request, HTTPException, FastAPI, Request
from fastapi.responses import RedirectResponse
import urllib.parse
import requests
from googleapiclient.errors import HttpError

# import secrets from the constants.py file
from constants import CLIENT_ID,CLIENT_SECRET,REDIRECT_URI

# CLIENT_ID = '*******************.apps.googleusercontent.com' # google client_id
# REDIRECT_URI = 'http://localhost:8000/google-auth'
# CLIENT_SECRET = "GOCSPX-Jf2MBre1_****************" # google client_secret

app = FastAPI()

# Handle the Google Sign-In flow
@app.get('/google-auth')
async def google_auth_redirect(request: Request):
    # Get the authorization code from the request query parameters
    code = request.query_params.get('code')
    if not code:
        raise HTTPException(status_code=400, detail='Authorization code not found')

    try:
        # Exchange authorization code for access token
        token_response = requests.post('https://oauth2.googleapis.com/token', params={
            'code': code,
            'client_id': CLIENT_ID,
            'client_secret': CLIENT_SECRET,
            'redirect_uri': REDIRECT_URI,
            'grant_type': 'authorization_code',
            'scope': 'https://www.googleapis.com/auth/gmail.send'
        })

        token_response.raise_for_status() # check if response status code is 200

        # Extract access token and other info from token response
        token_json = token_response.json()
        access_token = token_json['access_token']
        expires_in = token_json['expires_in']
        id_token = token_json['id_token']
        refresh_token = token_json.get('refresh_token')
        
        

    except HttpError as error:
        print(f'An error occurred: {error}')
        raise HTTPException(status_code=500, detail='Failed to send email')

    return "I'm happy"

@app.get("/login-with-google")
async def login_with_google(request: Request):
    # Generate a random state value to include in the Google Sign-In URL
    state = 'xyz123'

    # Encode the state value as a URL-safe string
    encoded_state = urllib.parse.quote(state)

    # Construct the Google Sign-In URL with the necessary parameters
    google_signin_url = f'https://accounts.google.com/o/oauth2/v2/auth?response_type=code&client_id={CLIENT_ID}&redirect_uri={REDIRECT_URI}&scope=email%20profile&state={encoded_state}'

    # Redirect the user to the Google Sign-In page
    return RedirectResponse(url=google_signin_url)
