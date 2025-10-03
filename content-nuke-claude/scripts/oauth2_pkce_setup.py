#!/usr/bin/env python3
"""
OAuth 2.0 Authorization Code Flow with PKCE for X API
Part of Claude AutoBlog SlashCommands
"""
import os
import base64
import hashlib
import secrets
import urllib.parse
import requests
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import time

# Global variables to capture the callback
auth_code = None
state_value = None
server_running = False

class CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global auth_code, state_value, server_running

        # Parse the callback URL
        parsed_path = urllib.parse.urlparse(self.path)
        query_params = urllib.parse.parse_qs(parsed_path.query)

        if 'code' in query_params and 'state' in query_params:
            auth_code = query_params['code'][0]
            received_state = query_params['state'][0]

            # Verify state matches
            if received_state == state_value:
                # Send success response
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                success_html = """
                <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #1DA1F2;">🎉 Authorization Successful!</h1>
                    <p>You can close this window and return to your terminal.</p>
                    <p>Your X API access is now configured for posting.</p>
                </body>
                </html>
                """
                self.wfile.write(success_html.encode())
                server_running = False
            else:
                # State mismatch - security issue
                self.send_response(400)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                error_html = """
                <html>
                <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                    <h1 style="color: #E1306C;">❌ Authorization Failed</h1>
                    <p>State parameter mismatch. Please try again.</p>
                </body>
                </html>
                """
                self.wfile.write(error_html.encode())
        else:
            # Missing required parameters
            self.send_response(400)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            error_html = """
            <html>
            <body style="font-family: Arial, sans-serif; text-align: center; padding: 50px;">
                <h1 style="color: #E1306C;">❌ Authorization Error</h1>
                <p>Missing authorization code. Please try again.</p>
            </body>
            </html>
            """
            self.wfile.write(error_html.encode())

    def log_message(self, format, *args):
        # Suppress default HTTP server logging
        pass

def generate_pkce_challenge():
    """Generate PKCE code challenge and verifier"""
    code_verifier = base64.urlsafe_b64encode(secrets.token_bytes(32)).decode('utf-8').rstrip('=')
    code_challenge = base64.urlsafe_b64encode(
        hashlib.sha256(code_verifier.encode('utf-8')).digest()
    ).decode('utf-8').rstrip('=')
    return code_verifier, code_challenge

def get_client_credentials():
    """Get client credentials from environment or prompt user"""
    client_id = os.environ.get('X_CLIENT_ID')
    client_secret = os.environ.get('X_CLIENT_SECRET')

    if not client_id:
        print("❌ X_CLIENT_ID not found in environment variables")
        print("Please add to ~/.bashrc:")
        print('export X_CLIENT_ID="your_client_id_here"')
        return None, None

    if not client_secret:
        print("❌ X_CLIENT_SECRET not found in environment variables")
        print("Please add to ~/.bashrc:")
        print('export X_CLIENT_SECRET="your_client_secret_here"')
        return None, None

    return client_id, client_secret

def create_authorization_url(client_id, redirect_uri, code_challenge, state):
    """Create OAuth 2.0 authorization URL with PKCE"""

    # Required scopes for posting tweets
    scopes = [
        'tweet.read',
        'tweet.write',
        'users.read',
        'offline.access'  # For refresh token
    ]

    params = {
        'response_type': 'code',
        'client_id': client_id,
        'redirect_uri': redirect_uri,
        'scope': ' '.join(scopes),
        'state': state,
        'code_challenge': code_challenge,
        'code_challenge_method': 'S256'
    }

    base_url = 'https://x.com/i/oauth2/authorize'
    auth_url = f"{base_url}?{urllib.parse.urlencode(params)}"

    return auth_url

def exchange_code_for_tokens(client_id, client_secret, code, redirect_uri, code_verifier):
    """Exchange authorization code for access and refresh tokens"""

    token_url = 'https://api.x.com/2/oauth2/token'

    data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'code': code,
        'redirect_uri': redirect_uri,
        'code_verifier': code_verifier
    }

    # Use Basic Auth with client credentials
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(token_url, data=data, auth=auth, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Token exchange failed: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error during token exchange: {e}")
        return None

def save_tokens_to_env(tokens):
    """Save OAuth 2.0 tokens to environment variables"""

    access_token = tokens.get('access_token')
    refresh_token = tokens.get('refresh_token')

    if not access_token:
        print("❌ No access token received")
        return False

    # Add to ~/.bashrc
    bashrc_path = os.path.expanduser('~/.bashrc')

    with open(bashrc_path, 'a') as f:
        f.write('\n# X API OAuth 2.0 Tokens\n')
        f.write(f'export X_OAUTH2_ACCESS_TOKEN="{access_token}"\n')
        if refresh_token:
            f.write(f'export X_OAUTH2_REFRESH_TOKEN="{refresh_token}"\n')

    print("✅ OAuth 2.0 tokens saved to ~/.bashrc")
    print("✅ Run 'source ~/.bashrc' to load them")

    return True

def main():
    global state_value, server_running

    print("🔐 Setting up OAuth 2.0 Authorization Code Flow with PKCE")
    print("=" * 60)

    # Get client credentials
    client_id, client_secret = get_client_credentials()
    if not client_id or not client_secret:
        return

    # OAuth parameters
    redirect_uri = 'http://localhost:8081/callback'
    state_value = secrets.token_urlsafe(32)
    code_verifier, code_challenge = generate_pkce_challenge()

    # Create authorization URL
    auth_url = create_authorization_url(client_id, redirect_uri, code_challenge, state_value)

    print(f"📱 Client ID: {client_id[:10]}...")
    print(f"🔗 Redirect URI: {redirect_uri}")
    print(f"🎲 State: {state_value[:10]}...")
    print(f"🔒 Code Challenge: {code_challenge[:10]}...")
    print()

    # Start local server for callback
    server = HTTPServer(('localhost', 8081), CallbackHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_running = True

    print("🚀 Starting local callback server on http://localhost:8081")
    server_thread.start()

    print()
    print("🌐 Opening authorization URL in your browser...")
    print(f"URL: {auth_url}")
    print()
    print("📋 Steps:")
    print("1. Authorize the app in your browser")
    print("2. You'll be redirected back to localhost")
    print("3. Return here to complete the setup")
    print()

    # Open browser
    webbrowser.open(auth_url)

    # Wait for callback
    print("⏳ Waiting for authorization callback...")

    timeout = 300  # 5 minutes
    start_time = time.time()

    while server_running and auth_code is None:
        time.sleep(1)
        if time.time() - start_time > timeout:
            print("❌ Authorization timeout. Please try again.")
            server.shutdown()
            return

    server.shutdown()

    if auth_code:
        print("✅ Authorization code received!")
        print("🔄 Exchanging code for tokens...")

        # Exchange code for tokens
        tokens = exchange_code_for_tokens(
            client_id, client_secret, auth_code, redirect_uri, code_verifier
        )

        if tokens:
            print("🎉 OAuth 2.0 setup complete!")
            print()
            print("📋 Received tokens:")
            print(f"   Access Token: {tokens.get('access_token', 'N/A')[:20]}...")
            if tokens.get('refresh_token'):
                print(f"   Refresh Token: {tokens.get('refresh_token', 'N/A')[:20]}...")
            print(f"   Token Type: {tokens.get('token_type', 'N/A')}")
            print(f"   Expires In: {tokens.get('expires_in', 'N/A')} seconds")

            # Save tokens
            if save_tokens_to_env(tokens):
                print()
                print("🚀 Ready to post tweets with OAuth 2.0!")
                print("Run: source ~/.bashrc")
                print("Then test: python3 scripts/post_x_thread_oauth2.py 'Test message'")
        else:
            print("❌ Failed to exchange code for tokens")
    else:
        print("❌ No authorization code received")

if __name__ == "__main__":
    main()