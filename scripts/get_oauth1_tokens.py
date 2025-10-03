#!/usr/bin/env python3
"""
Get permanent OAuth 1.0a tokens for X API (never expire!)
This replaces the annoying OAuth2 tokens that expire every 2 hours
"""
import sys
import os
import webbrowser
from urllib.parse import parse_qs
import requests
from requests_oauthlib import OAuth1Session

def get_oauth1_tokens():
    """
    Get permanent OAuth 1.0a tokens from X Developer app
    These tokens NEVER EXPIRE (unlike OAuth2)
    """

    print("🔑 Getting permanent X API OAuth 1.0a tokens...")
    print("(These never expire unlike OAuth2!)")
    print()

    # You need to get these from your X Developer Portal
    # Same app that has OAuth2 should also have OAuth 1.0a
    print("📝 First, get your OAuth 1.0a credentials from X Developer Portal:")
    print("   1. Go to: https://developer.x.com/en/portal/dashboard")
    print("   2. Click your app")
    print("   3. Go to 'Keys and tokens' tab")
    print("   4. Under 'Consumer Keys' find:")
    print("      - API Key (Consumer Key)")
    print("      - API Secret (Consumer Secret)")
    print()

    consumer_key = input("Enter your API Key (Consumer Key): ").strip()
    consumer_secret = input("Enter your API Secret (Consumer Secret): ").strip()

    if not consumer_key or not consumer_secret:
        print("❌ Consumer key and secret are required")
        return False

    print()
    print("🔄 Starting OAuth 1.0a flow...")

    # OAuth 1.0a URLs
    request_token_url = 'https://api.twitter.com/oauth/request_token'
    authorization_url = 'https://api.twitter.com/oauth/authorize'
    access_token_url = 'https://api.twitter.com/oauth/access_token'

    try:
        # Step 1: Get request token
        oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

        print("📤 Step 1: Getting request token...")
        response = oauth.fetch_request_token(request_token_url)

        resource_owner_key = response['oauth_token']
        resource_owner_secret = response['oauth_token_secret']

        # Step 2: Get authorization
        authorization_url_with_token = oauth.authorization_url(authorization_url)

        print("🌐 Step 2: Opening browser for authorization...")
        print(f"Authorization URL: {authorization_url_with_token}")

        # Try to open browser automatically
        try:
            webbrowser.open(authorization_url_with_token)
            print("✅ Browser opened automatically")
        except:
            print("⚠️  Please open the URL manually in your browser")

        print()
        print("📋 After authorizing:")
        print("   1. You'll be redirected to a URL")
        print("   2. Copy the 'oauth_verifier' parameter from that URL")
        print()

        oauth_verifier = input("Enter the oauth_verifier from the callback URL: ").strip()

        if not oauth_verifier:
            print("❌ OAuth verifier is required")
            return False

        # Step 3: Get access token (permanent!)
        print("🔑 Step 3: Getting permanent access tokens...")

        oauth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=resource_owner_key,
            resource_owner_secret=resource_owner_secret,
            verifier=oauth_verifier
        )

        oauth_tokens = oauth.fetch_access_token(access_token_url)

        access_token = oauth_tokens['oauth_token']
        access_token_secret = oauth_tokens['oauth_token_secret']

        print()
        print("🎉 SUCCESS! Got permanent OAuth 1.0a tokens!")
        print("These tokens NEVER EXPIRE (unless you revoke them)")
        print()
        print("📝 Add these to your waygate .env file:")
        print(f"X_API_KEY={consumer_key}")
        print(f"X_API_SECRET={consumer_secret}")
        print(f"X_ACCESS_TOKEN={access_token}")
        print(f"X_ACCESS_SECRET={access_token_secret}")
        print()

        # Ask if we should update waygate .env automatically
        update = input("Update waygate .env file automatically? (y/N): ").strip().lower()

        if update == 'y':
            update_waygate_env(consumer_key, consumer_secret, access_token, access_token_secret)
            print("✅ Updated waygate .env with permanent OAuth 1.0a tokens!")

        return True

    except Exception as e:
        print(f"❌ Error getting OAuth 1.0a tokens: {e}")
        return False

def update_waygate_env(consumer_key, consumer_secret, access_token, access_token_secret):
    """Update waygate .env with OAuth 1.0a credentials"""
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    # Read existing .env file
    lines = []
    if os.path.exists(waygate_env_path):
        with open(waygate_env_path, 'r') as f:
            lines = f.readlines()

    # Update or add OAuth 1.0a credentials
    oauth1_vars = {
        'X_API_KEY': consumer_key,
        'X_API_SECRET': consumer_secret,
        'X_ACCESS_TOKEN': access_token,
        'X_ACCESS_SECRET': access_token_secret
    }

    # Update existing lines or mark for addition
    updated_vars = set()
    for i, line in enumerate(lines):
        for var, value in oauth1_vars.items():
            if line.startswith(f"{var}="):
                lines[i] = f"{var}={value}\n"
                updated_vars.add(var)
                break

    # Add new variables that weren't found
    for var, value in oauth1_vars.items():
        if var not in updated_vars:
            lines.append(f"{var}={value}\n")

    # Write back to file
    with open(waygate_env_path, 'w') as f:
        f.writelines(lines)

def test_oauth1_tokens():
    """Test OAuth 1.0a tokens by making an API call"""
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    if not os.path.exists(waygate_env_path):
        print("❌ Waygate .env file not found")
        return False

    # Load credentials
    creds = {}
    with open(waygate_env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                creds[key] = value

    consumer_key = creds.get('X_API_KEY')
    consumer_secret = creds.get('X_API_SECRET')
    access_token = creds.get('X_ACCESS_TOKEN')
    access_token_secret = creds.get('X_ACCESS_SECRET')

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("❌ Missing OAuth 1.0a credentials in waygate .env")
        return False

    print("🧪 Testing OAuth 1.0a tokens...")

    try:
        # Create OAuth 1.0a session
        auth = OAuth1Session(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=access_token,
            resource_owner_secret=access_token_secret
        )

        # Test API call
        response = auth.get('https://api.twitter.com/2/users/me')

        if response.status_code == 200:
            user_data = response.json()
            print("✅ OAuth 1.0a tokens working!")
            print(f"   User: {user_data['data']['name']} (@{user_data['data']['username']})")
            print("   These tokens NEVER EXPIRE! 🎉")
            return True
        else:
            print(f"❌ Token test failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error testing tokens: {e}")
        return False

def main():
    print("X API OAuth 1.0a Token Generator")
    print("================================")
    print("Get permanent tokens that NEVER EXPIRE!")
    print()

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        success = test_oauth1_tokens()
    else:
        success = get_oauth1_tokens()

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()