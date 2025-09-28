#!/usr/bin/env python3
"""
Post X (Twitter) thread using OAuth 1.0a authentication
Part of Claude AutoBlog SlashCommands
Based on Twitter API v2 sample code from xdevplatform
"""
import os
import sys
import time
import requests
from requests_oauthlib import OAuth1

def post_tweet(tweet_text, reply_to_id=None):
    """Post a single tweet using OAuth 1.0a authentication"""

    # Get credentials from environment
    consumer_key = os.environ.get('X_API_KEY')
    consumer_secret = os.environ.get('X_API_SECRET')
    access_token = os.environ.get('X_ACCESS_TOKEN')
    access_token_secret = os.environ.get('X_ACCESS_SECRET')

    if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
        print("❌ Missing required environment variables:")
        print("   X_API_KEY, X_API_SECRET, X_ACCESS_TOKEN, X_ACCESS_SECRET")
        print("   Run the setup guide: docs/X_API_SETUP.md")
        return None

    # Create OAuth 1.0a authentication
    auth = OAuth1(
        consumer_key,
        client_secret=consumer_secret,
        resource_owner_key=access_token,
        resource_owner_secret=access_token_secret,
        signature_method='HMAC-SHA1',
        signature_type='AUTH_HEADER'
    )

    # Twitter API v2 endpoint for posting tweets
    url = "https://api.twitter.com/2/tweets"

    # Tweet payload
    payload = {"text": tweet_text}

    # If this is a reply, add the reply_to field
    if reply_to_id:
        payload["reply"] = {"in_reply_to_tweet_id": reply_to_id}

    try:
        # Make the request
        response = requests.post(url, auth=auth, json=payload)

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