import spotipy 
import time
from spotipy.oauth2 import SpotifyOAuth

from flask import Flask, request, url_for, session, redirect


app = Flask(__name__)

app.config['SESSION_COOKIE_NAME'] = "Spot Coook"

app.secret_key = 'helooree120238#1!'

TOKEN_INFO = 'token_info'


@app.route('/')
def login(): 
    auth_url = create_spotify_oauth().get_authorize_url()
    return redirect(auth_url)

@app.route('/redirect')
def redirect_page():
    session.clear()
    code = request.args.get('code')
    token_info = create_spotify_oauth().get_access_token(code)
    session[TOKEN_INFO] = token_info
    return redirect(url_for('save_discover_weekly', external = True))

@app.route('/saveDiscoverWeekly')

def save_discover_weekly():
    try: 
        token_info = get_token()

    except: 
        print("user not logged in")
        return redirect('/')

    return("OAUTH SUCCESSFUL")

def get_token():
    token_info = session.get(TOKEN_INFO, None)
    if not token_info: 
        redirect(url_for('login', external = False))
    
    now = int(time.time())

    is_expired = token_info[expires_at] - now < 60 

    if(is_expired): 
        spotify_oauth = create_spotify_oauth()
        token_info = spotify_oauth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

def create_spotify_oauth():
    return SpotifyOAuth(
        client_id = "ba0504f38dff41a592e86ec4ba424018",
        client_secret = "cecdaf4ffeae4de68e7cf57e1d15fb4b",
        redirect_uri = url_for('redirect_page', _external=True),
        scope = 'user-library-read playlist-modify-public playlist-modify-private'
    )


app.run(debug=True)