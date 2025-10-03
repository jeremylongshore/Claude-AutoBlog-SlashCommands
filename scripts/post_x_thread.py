#!/usr/bin/env python3
"""
Post X (Twitter) thread using OAuth2 authentication
Part of Claude AutoBlog SlashCommands
Updated to work with waygate MCP OAuth2 credentials
"""
import os
import sys
import time
import requests

def load_waygate_credentials():
    """Load all X API credentials from waygate .env file"""
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

def load_waygate_oauth2_credentials():
    """Load OAuth2 credentials specifically"""
    creds = load_waygate_credentials()
    client_id = creds.get('X_CLIENT_ID')
    client_secret = creds.get('X_CLIENT_SECRET')
    access_token = creds.get('X_OAUTH2_ACCESS_TOKEN')
    return client_id, client_secret, access_token

def auto_refresh_x_token():
    """Automatically refresh X token before posting"""
    import subprocess
    import os

    # Use simplified script directory structure
    script_dir = "/home/jeremy/projects/content-nuke/scripts"
    refresh_script = os.path.join(script_dir, 'refresh_tokens.py')

    try:
        # Run token refresh
        result = subprocess.run([sys.executable, refresh_script, 'x'],
                              capture_output=True, text=True)
        return result.returncode == 0
    except Exception as e:
        print(f"⚠️  Token refresh failed: {e}")
        return False

def post_tweet(tweet_text, reply_to_id=None):
    """Post a single tweet using OAuth 1.0a (permanent) or OAuth2 authentication"""

    # First try OAuth 1.0a from waygate (PERMANENT TOKENS - never expire!)
    creds = load_waygate_credentials()
    oauth1_consumer_key = creds.get('X_API_KEY') if creds else None
    oauth1_consumer_secret = creds.get('X_API_SECRET') if creds else None
    oauth1_access_token = creds.get('X_ACCESS_TOKEN') if creds else None
    oauth1_access_secret = creds.get('X_ACCESS_SECRET') if creds else None

    # Also check environment variables
    env_consumer_key = os.environ.get('X_API_KEY')
    env_consumer_secret = os.environ.get('X_API_SECRET')
    env_access_token = os.environ.get('X_ACCESS_TOKEN')
    env_access_secret = os.environ.get('X_ACCESS_SECRET')

    # Use OAuth 1.0a if available (PERMANENT - never expires!)
    if all([oauth1_consumer_key, oauth1_consumer_secret, oauth1_access_token, oauth1_access_secret]):
        print("🔑 Using OAuth 1.0a (permanent tokens)")
        from requests_oauthlib import OAuth1
        auth = OAuth1(
            oauth1_consumer_key,
            client_secret=oauth1_consumer_secret,
            resource_owner_key=oauth1_access_token,
            resource_owner_secret=oauth1_access_secret,
            signature_method='HMAC-SHA1',
            signature_type='AUTH_HEADER'
        )
        headers = {}
    elif all([env_consumer_key, env_consumer_secret, env_access_token, env_access_secret]):
        print("🔑 Using OAuth 1.0a from environment (permanent tokens)")
        from requests_oauthlib import OAuth1
        auth = OAuth1(
            env_consumer_key,
            client_secret=env_consumer_secret,
            resource_owner_key=env_access_token,
            resource_owner_secret=env_access_secret,
            signature_method='HMAC-SHA1',
            signature_type='AUTH_HEADER'
        )
        headers = {}
    else:
        # Fallback to OAuth2 (expires every 2 hours - not ideal)
        print("⚠️  Using OAuth2 (expires every 2 hours)")
        client_id, client_secret, oauth2_access_token = load_waygate_oauth2_credentials()

        if not all([client_id, client_secret, oauth2_access_token]):
            print("❌ Missing X API credentials:")
            print("   Preferred: OAuth 1.0a (permanent): X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET")
            print("   Fallback: OAuth2 (2hr expiry): X_CLIENT_ID, X_CLIENT_SECRET, X_OAUTH2_ACCESS_TOKEN")
            print("   Run: python3 scripts/get_oauth1_tokens.py")
            return None

        # Use OAuth2 Bearer token authentication
        auth = None
        headers = {
            "Authorization": f"Bearer {oauth2_access_token}",
            "Content-Type": "application/json"
        }

    # Twitter API v2 endpoint for posting tweets
    url = "https://api.twitter.com/2/tweets"

    # Tweet payload
    payload = {"text": tweet_text}

    # If this is a reply, add the reply_to field
    if reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

    try:
        # Make the request with appropriate authentication
        if auth:  # OAuth 1.0a
            response = requests.post(url, auth=auth, json=payload)
        else:  # OAuth2 Bearer token
            response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            result = response.json()
            tweet_id = result['data']['id']
            return tweet_id
        else:
            print(f"❌ Failed to post tweet: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error posting tweet: {e}")
        return None

def post_thread(thread_file_path):
    """Post a thread from a file"""

    if not os.path.exists(thread_file_path):
        print(f"❌ Thread file not found: {thread_file_path}")
        return False

    print(f"📖 Reading thread from: {thread_file_path}")

    # Auto-refresh OAuth2 token before posting (ensures fresh token)
    print("🔄 Refreshing X API token...")
    if not auto_refresh_x_token():
        print("⚠️  Token refresh failed, attempting with existing token...")

    with open(thread_file_path, 'r') as f:
        content = f.read()

    # Parse thread content - handle Content Nuke format
    tweets = []

    # Use regex to extract TWEET X/Y: sections properly
    import re
    tweet_pattern = r'TWEET (\d+)/(\d+):\s*(.*?)(?=TWEET \d+/\d+:|===== CHARACTER COUNTS =====|$)'
    matches = re.findall(tweet_pattern, content, re.DOTALL)

    for match in matches:
        tweet_num, total_tweets, tweet_content = match
        # Clean up the tweet content
        clean_content = tweet_content.strip()

        # Skip empty tweets
        if not clean_content:
            continue

        tweets.append(clean_content)

    if not tweets:
        print("❌ No tweets found in thread file")
        return False

    print(f"📝 Found {len(tweets)} tweets in thread")

    # Post the thread
    first_tweet_id = None
    last_tweet_id = None

    for i, tweet in enumerate(tweets):
        print(f"📤 Posting tweet {i+1}/{len(tweets)}...")

        # Clean up the tweet text (remove numbering if it exists)
        tweet_text = tweet
        if tweet_text.startswith(('1/', '2/', '3/', '4/', '5/', '6/', '7/', '8/', '9/')):
            # Remove the "1/7" part
            lines = tweet_text.split('\n')
            if lines:
                lines[0] = ' '.join(lines[0].split()[1:])  # Remove first part
                tweet_text = '\n'.join(lines).strip()

        # Post the tweet
        reply_to = last_tweet_id if i > 0 else None
        tweet_id = post_tweet(tweet_text, reply_to)

        if tweet_id:
            if i == 0:
                first_tweet_id = tweet_id
            last_tweet_id = tweet_id
            print(f"✅ Tweet {i+1} posted: https://twitter.com/i/web/status/{tweet_id}")

            # Wait between tweets to avoid rate limits
            if i < len(tweets) - 1:
                time.sleep(2)
        else:
            print(f"❌ Failed to post tweet {i+1}")
            return False

    if first_tweet_id:
        print(f"🎉 Thread posted successfully!")
        print(f"Thread URL: https://twitter.com/i/web/status/{first_tweet_id}")
        return True

    return False

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Post single tweet: python3 post_x_thread.py 'Your tweet text here'")
        print("  Post thread:       python3 post_x_thread.py /path/to/thread.txt")
        sys.exit(1)

    input_arg = sys.argv[1]

    # Check if it's a file path or tweet text
    if os.path.exists(input_arg):
        # It's a file - post as thread
        success = post_thread(input_arg)
    else:
        # It's tweet text - post single tweet
        tweet_id = post_tweet(input_arg)
        if tweet_id:
            print(f"🎉 Tweet posted successfully!")
            print(f"Tweet URL: https://twitter.com/i/web/status/{tweet_id}")
            success = True
        else:
            success = False

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()