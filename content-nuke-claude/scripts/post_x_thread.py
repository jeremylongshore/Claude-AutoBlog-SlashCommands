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
    """Load X API credentials from waygate .env file"""
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    if not os.path.exists(waygate_env_path):
        return None, None, None

    creds = {}
    with open(waygate_env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                creds[key] = value

    client_id = creds.get('X_CLIENT_ID')
    client_secret = creds.get('X_CLIENT_SECRET')
    access_token = creds.get('X_OAUTH2_ACCESS_TOKEN')

    return client_id, client_secret, access_token

def auto_refresh_x_token():
    """Automatically refresh X token before posting"""
    import subprocess
    import os

    script_dir = os.path.dirname(os.path.abspath(__file__))
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
    """Post a single tweet using OAuth2 authentication"""

    # Try to get credentials from environment first (OAuth 1.0a style)
    consumer_key = os.environ.get('X_API_KEY')
    consumer_secret = os.environ.get('X_API_SECRET')
    oauth1_access_token = os.environ.get('X_ACCESS_TOKEN')
    access_token_secret = os.environ.get('X_ACCESS_SECRET')

    # If OAuth 1.0a credentials available, use them
    if all([consumer_key, consumer_secret, oauth1_access_token, access_token_secret]):
        from requests_oauthlib import OAuth1
        auth = OAuth1(
            consumer_key,
            client_secret=consumer_secret,
            resource_owner_key=oauth1_access_token,
            resource_owner_secret=access_token_secret,
            signature_method='HMAC-SHA1',
            signature_type='AUTH_HEADER'
        )
        headers = {}
    else:
        # Try waygate OAuth2 credentials
        client_id, client_secret, access_token = load_waygate_credentials()

        if not all([client_id, client_secret, access_token]):
            print("❌ Missing X API credentials:")
            print("   Either set OAuth 1.0a: X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET")
            print("   Or ensure waygate .env has: X_CLIENT_ID, X_CLIENT_SECRET, X_OAUTH2_ACCESS_TOKEN")
            return None

        # Use OAuth2 Bearer token authentication
        auth = None
        headers = {
            "Authorization": f"Bearer {access_token}",
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

    # Auto-refresh X token before posting (X tokens expire every 2 hours)
    print("🔄 Refreshing X API token...")
    if not auto_refresh_x_token():
        print("⚠️  Token refresh failed, attempting with existing token...")

    with open(thread_file_path, 'r') as f:
        content = f.read()

    # Parse thread content - handle Content Nuke format
    tweets = []

    # Split by "---" to separate thread content from instructions
    parts = content.split('---')
    thread_content = parts[0].strip()

    # Split thread content by double newlines (paragraph breaks)
    paragraphs = [p.strip() for p in thread_content.split('\n\n') if p.strip()]

    # Each paragraph becomes a tweet
    for paragraph in paragraphs:
        # Clean up paragraph text
        tweet_text = paragraph.strip()

        # Skip empty paragraphs
        if not tweet_text:
            continue

        # Add to tweets list
        tweets.append(tweet_text)

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