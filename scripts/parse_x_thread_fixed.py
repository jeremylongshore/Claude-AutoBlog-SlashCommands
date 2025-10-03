#!/usr/bin/env python3
"""
Fixed X thread parser that correctly handles TWEET X/Y: format
"""
import re
import sys

def extract_tweets_from_file(file_path):
    """Extract individual tweets from properly formatted thread file"""
    with open(file_path, 'r') as f:
        content = f.read()

    # Find all TWEET X/Y: sections
    tweet_pattern = r'TWEET (\d+)/(\d+):\s*(.*?)(?=TWEET \d+/\d+:|===== CHARACTER COUNTS =====|$)'
    matches = re.findall(tweet_pattern, content, re.DOTALL)

    tweets = []
    for match in matches:
        tweet_num, total_tweets, tweet_content = match
        # Clean up the tweet content
        clean_content = tweet_content.strip()
        tweets.append(clean_content)

    return tweets

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 parse_x_thread_fixed.py <thread_file>")
        sys.exit(1)

    thread_file = sys.argv[1]
    tweets = extract_tweets_from_file(thread_file)

    print(f"Found {len(tweets)} tweets:")
    for i, tweet in enumerate(tweets, 1):
        print(f"\n--- TWEET {i} ---")
        print(tweet)
        print(f"Characters: {len(tweet)}")