#!/usr/bin/env python3
"""
OAuth 1.0a 3-legged flow for X API - Get PERMANENT tokens that never expire
Based on official X documentation: https://docs.x.com/resources/legacy/authentication/oauth-1-0a
"""
import sys
import os
import webbrowser
import urllib.parse
import requests
from requests_oauthlib import OAuth1Session

def oauth1_flow():
    """Complete OAuth 1.0a 3-legged flow for permanent tokens"""

    print("🔑 X API OAuth 1.0a - Permanent Token Generator")
    print("=" * 50)
    print("Following official X documentation for 3-legged OAuth flow")
    print("Result: PERMANENT tokens that NEVER EXPIRE! 🎉")
    print()

    # Get consumer credentials (same as your OAuth 2.0 app)
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    if os.path.exists(waygate_env_path):
        print("📁 Loading consumer keys from waygate...")
        with open(waygate_env_path, 'r') as f:
            lines = f.readlines()

        consumer_key = None
        consumer_secret = None

        for line in lines:
            if line.startswith('X_API_KEY='):
                consumer_key = line.split('=', 1)[1].strip()
            elif line.startswith('X_API_SECRET='):
                consumer_secret = line.split('=', 1)[1].strip()

    if not consumer_key or not consumer_secret:
        print("❌ Consumer keys not found in waygate .env")
        print("We need X_API_KEY and X_API_SECRET")
        return False

    print(f"✅ Consumer Key: {consumer_key}")
    print(f"✅ Consumer Secret: {consumer_secret[:10]}...")
    print()

    # Step 1: POST oauth/request_token
    print("📤 Step 1: Getting request token...")

    request_token_url = 'https://api.x.com/oauth/request_token'
    callback_url = 'oob'  # Out-of-band (PIN-based) for local apps

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        callback_uri=callback_url
    )

    try:
        fetch_response = oauth.fetch_request_token(request_token_url)

        resource_owner_key = fetch_response.get('oauth_token')
        resource_owner_secret = fetch_response.get('oauth_token_secret')
        callback_confirmed = fetch_response.get('oauth_callback_confirmed')

        print(f"✅ Request Token: {resource_owner_key}")
        print(f"✅ Request Token Secret: {resource_owner_secret[:10]}...")
        print(f"✅ Callback Confirmed: {callback_confirmed}")
        print()

    except Exception as e:
        print(f"❌ Failed to get request token: {e}")
        return False

    # Step 2: GET oauth/authorize
    print("🌐 Step 2: User authorization...")

    authorization_url = 'https://api.x.com/oauth/authorize'
    authorize_url = f"{authorization_url}?oauth_token={resource_owner_key}"

    print(f"Authorization URL: {authorize_url}")
    print()
    print("📋 Instructions:")
    print("1. The browser will open automatically")
    print("2. Log in to X if prompted")
    print("3. Click 'Authorize app'")
    print("4. Copy the PIN code that appears")
    print()

    # Open browser automatically
    try:
        webbrowser.open(authorize_url)
        print("✅ Browser opened automatically")
    except:
        print("⚠️  Please open the URL manually in your browser")

    print()
    oauth_verifier = input("Enter the PIN code from X: ").strip()

    if not oauth_verifier:
        print("❌ PIN code is required")
        return False

    # Step 3: POST oauth/access_token
    print()
    print("🔑 Step 3: Converting to permanent access tokens...")

    access_token_url = 'https://api.x.com/oauth/access_token'

    oauth = OAuth1Session(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=resource_owner_key,
        resource_owner_secret=resource_owner_secret,
        verifier=oauth_verifier
    )

    try:
        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens['oauth_token']
        access_token_secret = oauth_tokens['oauth_token_secret']

        print()
        print("🎉 SUCCESS! Got PERMANENT OAuth 1.0a tokens!")
        print("These tokens NEVER EXPIRE unless you revoke them!")
        print()
        print("📝 Your permanent credentials:")
        print(f"X_API_KEY={consumer_key}")
        print(f"X_API_SECRET={consumer_secret}")
        print(f"X_ACCESS_TOKEN={access_token}")
        print(f"X_ACCESS_SECRET={access_token_secret}")
        print()

        # Update waygate .env automatically
        update_waygate_env(access_token, access_token_secret)

        # Test the tokens
        print("🧪 Testing permanent tokens...")
        test_tokens(consumer_key, consumer_secret, access_token, access_token_secret)

        return True

    except Exception as e:
        print(f"❌ Failed to get access tokens: {e}")
        return False

def update_waygate_env(access_token, access_token_secret):
    """Update waygate .env with OAuth 1.0a access tokens"""
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    # Read existing file
    with open(waygate_env_path, 'r') as f:
        lines = f.readlines()

    # Update or add access tokens
    updated_access_token = False
    updated_access_secret = False

    for i, line in enumerate(lines):
        if line.startswith('X_ACCESS_TOKEN='):
            lines[i] = f"X_ACCESS_TOKEN={access_token}\n"
            updated_access_token = True
        elif line.startswith('X_ACCESS_SECRET='):
            lines[i] = f"X_ACCESS_SECRET={access_token_secret}\n"
            updated_access_secret = True

    # Add if not found
    if not updated_access_token:
        lines.append(f"X_ACCESS_TOKEN={access_token}\n")
    if not updated_access_secret:
        lines.append(f"X_ACCESS_SECRET={access_token_secret}\n")

    # Write back
    with open(waygate_env_path, 'w') as f:
        f.writelines(lines)

    print("✅ Updated waygate .env with permanent OAuth 1.0a tokens!")

def test_tokens(consumer_key, consumer_secret, access_token, access_token_secret):
    """Test OAuth 1.0a tokens with a real API call"""

    from requests_oauthlib import OAuth1

    # Create OAuth 1.0a auth
    auth = OAuth1(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
        signature_method='HMAC-SHA1',
        signature_type='AUTH_HEADER'
    )

    # Test with user info endpoint
    url = "https://api.x.com/2/users/me"

    try:
        response = requests.get(url, auth=auth)

        if response.status_code == 200:
            user_data = response.json()
            user_info = user_data['data']
            print(f"✅ OAuth 1.0a tokens working!")
            print(f"   User: {user_info['name']} (@{user_info['username']})")
            print(f"   ID: {user_info['id']}")
            print("   🎉 These tokens NEVER EXPIRE!")
            return True
        else:
            print(f"❌ Token test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error testing tokens: {e}")
        return False

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Test existing tokens
        waygate_env_path = "/home/jeremy/waygate-mcp/.env"

        if not os.path.exists(waygate_env_path):
            print("❌ Waygate .env file not found")
            return

        with open(waygate_env_path, 'r') as f:
            lines = f.readlines()

        creds = {}
        for line in lines:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                creds[key] = value

        consumer_key = creds.get('X_API_KEY')
        consumer_secret = creds.get('X_API_SECRET')
        access_token = creds.get('X_ACCESS_TOKEN')
        access_token_secret = creds.get('X_ACCESS_SECRET')

        if all([consumer_key, consumer_secret, access_token, access_token_secret]):
            print("🧪 Testing existing OAuth 1.0a tokens...")
            success = test_tokens(consumer_key, consumer_secret, access_token, access_token_secret)
        else:
            print("❌ Missing OAuth 1.0a credentials")
            print("Run: python3 oauth1_flow.py")
            success = False
    else:
        # Run full OAuth flow
        success = oauth1_flow()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()