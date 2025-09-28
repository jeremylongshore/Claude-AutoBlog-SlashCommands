#!/usr/bin/env python3
"""
Post X (Twitter) thread using OAuth 2.0 Access Token
Part of Claude AutoBlog SlashCommands
OAuth 2.0 Authorization Code Flow with PKCE implementation
"""
import os
import sys
import time
import requests

def post_tweet_oauth2(tweet_text, reply_to_id=None):
    """Post a single tweet using OAuth 2.0 access token"""

    # Get OAuth 2.0 access token from environment
    access_token = os.environ.get('X_OAUTH2_ACCESS_TOKEN')

    if not access_token:
        print("❌ Missing X_OAUTH2_ACCESS_TOKEN environment variable")
        print("   Run: python3 scripts/oauth2_pkce_setup.py")
        print("   Then: source ~/.bashrc")
        return None

    # Twitter API v2 endpoint for posting tweets
    url = "https://api.twitter.com/2/tweets"

    # Authorization header with OAuth 2.0 Bearer token
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # Tweet payload
    payload = {"text": tweet_text}

    # If this is a reply, add the reply_to field
    if reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

    try:
        # Make the request
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            result = response.json()
            tweet_id = result['data']['id']
            return tweet_id
        elif response.status_code == 401:
            print("❌ OAuth 2.0 token expired or invalid")
            print("   Run: python3 scripts/oauth2_pkce_setup.py")
            return None
        else:
            print(f"❌ Failed to post tweet: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error posting tweet: {e}")
        return None

def post_thread_oauth2(thread_file_path):
    """Post a thread from a file using OAuth 2.0"""

    if not os.path.exists(thread_file_path):
        print(f"❌ Thread file not found: {thread_file_path}")
        return False

    print(f"📖 Reading thread from: {thread_file_path}")

    with open(thread_file_path, 'r') as f:
        content = f.read()

    # Parse thread content - look for numbered tweets
    tweets = []
    lines = content.split('\n')
    current_tweet = ""

    for line in lines:
        # Look for tweet numbers (1/7, 2/7, etc.)
        if line.strip().startswith(('1/', '2/', '3/', '4/', '5/', '6/', '7/', '8/', '9/')):
            if current_tweet.strip():
                tweets.append(current_tweet.strip())
            current_tweet = line.strip()
        elif line.strip() == "---":
            if current_tweet.strip():
                tweets.append(current_tweet.strip())
                current_tweet = ""
        elif current_tweet:
            current_tweet += "\n" + line

    # Add the last tweet
    if current_tweet.strip():
        tweets.append(current_tweet.strip())

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
        tweet_id = post_tweet_oauth2(tweet_text, reply_to)

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

def refresh_access_token():
    """Refresh the OAuth 2.0 access token using refresh token"""

    refresh_token = os.environ.get('X_OAUTH2_REFRESH_TOKEN')
    client_id = os.environ.get('X_CLIENT_ID')

    if not refresh_token or not client_id:
        print("❌ Missing refresh token or client ID")
        print("   Run: python3 scripts/oauth2_pkce_setup.py")
        return False

    url = 'https://api.x.com/2/oauth2/token'

    data = {
        'refresh_token': refresh_token,
        'grant_type': 'refresh_token',
        'client_id': client_id
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            tokens = response.json()
            new_access_token = tokens.get('access_token')

            if new_access_token:
                # Update environment variable for current session
                os.environ['X_OAUTH2_ACCESS_TOKEN'] = new_access_token
                print("✅ Access token refreshed successfully")
                return True

        print(f"❌ Failed to refresh token: {response.status_code}")
        print(f"Response: {response.text}")
        return False

    except Exception as e:
        print(f"❌ Error refreshing token: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Post single tweet: python3 post_x_thread_oauth2.py 'Your tweet text here'")
        print("  Post thread:       python3 post_x_thread_oauth2.py /path/to/thread.txt")
        print()
        print("Setup OAuth 2.0 first:")
        print("  python3 scripts/oauth2_pkce_setup.py")
        sys.exit(1)

    input_arg = sys.argv[1]

    # Check if it's a file path or tweet text
    if os.path.exists(input_arg):
        # It's a file - post as thread
        success = post_thread_oauth2(input_arg)
    else:
        # It's tweet text - post single tweet
        tweet_id = post_tweet_oauth2(input_arg)
        if tweet_id:
            print(f"🎉 Tweet posted successfully!")
            print(f"Tweet URL: https://twitter.com/i/web/status/{tweet_id}")
            success = True
        else:
            # Try refreshing token and retry once
            print("🔄 Attempting to refresh access token...")
            if refresh_access_token():
                tweet_id = post_tweet_oauth2(input_arg)
                if tweet_id:
                    print(f"🎉 Tweet posted successfully after token refresh!")
                    print(f"Tweet URL: https://twitter.com/i/web/status/{tweet_id}")
                    success = True
                else:
                    success = False
            else:
                success = False

    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()