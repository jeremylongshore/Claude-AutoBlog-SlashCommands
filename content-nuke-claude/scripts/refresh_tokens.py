#!/usr/bin/env python3
"""
Auto-refresh API tokens for Content Nuke
Handles X (Twitter) and LinkedIn token refresh automatically
"""
import os
import sys
import requests
import json
from datetime import datetime, timedelta

def load_credentials_from_waygate():
    """Load all API credentials from waygate .env file"""
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    if not os.path.exists(waygate_env_path):
        return {}

    creds = {}
    with open(waygate_env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                creds[key] = value

    return creds

def update_waygate_env(key, value):
    """Update a specific key in waygate .env file"""
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    # Read all lines
    with open(waygate_env_path, 'r') as f:
        lines = f.readlines()

    # Update the specific key
    updated = False
    for i, line in enumerate(lines):
        if line.startswith(f"{key}="):
            lines[i] = f"{key}={value}\n"
            updated = True
            break

    # If key doesn't exist, add it
    if not updated:
        lines.append(f"{key}={value}\n")

    # Write back to file
    with open(waygate_env_path, 'w') as f:
        f.writelines(lines)

def refresh_x_token():
    """Refresh X (Twitter) OAuth2 access token"""
    print("🔄 Refreshing X API token...")

    creds = load_credentials_from_waygate()
    client_id = creds.get('X_CLIENT_ID')
    client_secret = creds.get('X_CLIENT_SECRET')
    refresh_token = creds.get('X_OAUTH2_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        print("❌ Missing X API credentials for refresh")
        return False

    # X API token refresh endpoint
    url = "https://api.twitter.com/2/oauth2/token"

    auth = (client_id, client_secret)
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }

    try:
        response = requests.post(url, auth=auth, data=data)

        if response.status_code == 200:
            tokens = response.json()

            # Update waygate .env with new tokens
            update_waygate_env('X_OAUTH2_ACCESS_TOKEN', tokens['access_token'])
            update_waygate_env('X_OAUTH2_REFRESH_TOKEN', tokens['refresh_token'])

            print(f"✅ X token refreshed successfully")
            print(f"   New token expires in: {tokens['expires_in']} seconds (2 hours)")
            return True
        else:
            print(f"❌ Failed to refresh X token: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error refreshing X token: {e}")
        return False

def refresh_linkedin_token():
    """Refresh LinkedIn access token"""
    print("🔄 Refreshing LinkedIn API token...")

    creds = load_credentials_from_waygate()
    client_id = creds.get('LINKEDIN_CLIENT_ID')
    client_secret = creds.get('LINKEDIN_CLIENT_SECRET')
    refresh_token = creds.get('LINKEDIN_REFRESH_TOKEN')

    if not all([client_id, client_secret, refresh_token]):
        print("❌ Missing LinkedIn API credentials for refresh")
        print("   LinkedIn tokens may need manual renewal every 60 days")
        return False

    # LinkedIn token refresh endpoint
    url = "https://www.linkedin.com/oauth/v2/accessToken"

    data = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret
    }

    try:
        response = requests.post(url, data=data)

        if response.status_code == 200:
            tokens = response.json()

            # Update waygate .env with new tokens
            update_waygate_env('LINKEDIN_ACCESS_TOKEN', tokens['access_token'])
            if 'refresh_token' in tokens:
                update_waygate_env('LINKEDIN_REFRESH_TOKEN', tokens['refresh_token'])

            print(f"✅ LinkedIn token refreshed successfully")
            print(f"   New token expires in: {tokens.get('expires_in', '60 days')} seconds")
            return True
        else:
            print(f"❌ Failed to refresh LinkedIn token: {response.status_code}")
            print(f"Response: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Error refreshing LinkedIn token: {e}")
        return False

def check_token_expiry():
    """Check when tokens might expire and refresh if needed"""
    print("🔍 Checking token expiry status...")

    # For X tokens, we refresh every time since they expire in 2 hours
    x_success = refresh_x_token()

    # For LinkedIn, check if token exists and refresh if we have refresh token
    creds = load_credentials_from_waygate()
    if 'LINKEDIN_ACCESS_TOKEN' in creds:
        linkedin_success = refresh_linkedin_token()
    else:
        print("ℹ️  LinkedIn token not configured yet")
        linkedin_success = True  # Don't fail if not set up

    return x_success and linkedin_success

def main():
    if len(sys.argv) > 1:
        if sys.argv[1] == "x":
            success = refresh_x_token()
        elif sys.argv[1] == "linkedin":
            success = refresh_linkedin_token()
        elif sys.argv[1] == "check":
            success = check_token_expiry()
        else:
            print("Usage: python3 refresh_tokens.py [x|linkedin|check]")
            sys.exit(1)
    else:
        # Default: refresh all tokens
        success = check_token_expiry()

    print(f"\n{'✅' if success else '❌'} Token refresh {'completed' if success else 'failed'}")
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()