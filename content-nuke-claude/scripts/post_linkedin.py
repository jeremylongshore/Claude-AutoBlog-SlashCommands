#!/usr/bin/env python3
"""
Post to LinkedIn using OAuth2 authentication
Part of Claude AutoBlog SlashCommands Content Nuke
Supports both personal profiles and company pages
"""
import os
import sys
import requests
import json
from datetime import datetime

def load_linkedin_credentials():
    """Load LinkedIn API credentials from waygate .env file"""
    waygate_env_path = "/home/jeremy/waygate-mcp/.env"

    if not os.path.exists(waygate_env_path):
        return None, None

    creds = {}
    with open(waygate_env_path, 'r') as f:
        for line in f:
            if '=' in line and not line.startswith('#'):
                key, value = line.strip().split('=', 1)
                creds[key] = value

    access_token = creds.get('LINKEDIN_ACCESS_TOKEN')
    person_id = creds.get('LINKEDIN_PERSON_ID')  # or organization ID for company pages

    return access_token, person_id

def get_user_info(access_token):
    """Get LinkedIn user/organization info"""
    url = "https://api.linkedin.com/v2/userinfo"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ Failed to get user info: {response.status_code}")
            print(f"Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error getting user info: {e}")
        return None

def post_to_linkedin(text_content, access_token, person_id=None):
    """Post content to LinkedIn"""

    # If no person_id provided, get it from user info
    if not person_id:
        user_info = get_user_info(access_token)
        if not user_info:
            return None
        person_id = user_info.get('sub')  # LinkedIn user ID

    # LinkedIn API v2 endpoint for creating posts
    url = "https://api.linkedin.com/v2/ugcPosts"

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "X-Restli-Protocol-Version": "2.0.0"
    }

    # Post payload for LinkedIn
    payload = {
        "author": f"urn:li:person:{person_id}",
        "lifecycleState": "PUBLISHED",
        "specificContent": {
            "com.linkedin.ugc.ShareContent": {
                "shareCommentary": {
                    "text": text_content
                },
                "shareMediaCategory": "NONE"
            }
        },
        "visibility": {
            "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)

        if response.status_code == 201:
            result = response.json()
            post_id = result.get('id', '').split(':')[-1]
            return post_id
        else:
            print(f"❌ Failed to post to LinkedIn: {response.status_code}")
            print(f"Response: {response.text}")
            return None

    except Exception as e:
        print(f"❌ Error posting to LinkedIn: {e}")
        return None

def post_linkedin_content(content_file_path):
    """Post LinkedIn content from file"""

    if not os.path.exists(content_file_path):
        print(f"❌ LinkedIn content file not found: {content_file_path}")
        return False

    print(f"📖 Reading LinkedIn content from: {content_file_path}")

    with open(content_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract content before posting instructions
    parts = content.split('---')
    linkedin_text = parts[0].strip()

    # Load credentials
    access_token, person_id = load_linkedin_credentials()

    if not access_token:
        print("❌ Missing LinkedIn API credentials:")
        print("   Add LINKEDIN_ACCESS_TOKEN to waygate .env file")
        print("   Run LinkedIn API setup first")
        return False

    print(f"📝 Posting to LinkedIn...")
    print(f"Content preview: {linkedin_text[:100]}...")

    # Post to LinkedIn
    post_id = post_to_linkedin(linkedin_text, access_token, person_id)

    if post_id:
        print(f"✅ Posted to LinkedIn successfully!")
        print(f"Post ID: {post_id}")

        # Save posting record
        posted_file = content_file_path.replace('.txt', '-POSTED.txt')
        with open(posted_file, 'w') as f:
            f.write(f"POSTED TO LINKEDIN: {datetime.now().isoformat()}\n")
            f.write(f"Post ID: {post_id}\n")
            f.write(f"Content:\n{linkedin_text}\n")

        return True
    else:
        print("❌ Failed to post to LinkedIn")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  Post LinkedIn content: python3 post_linkedin.py /path/to/linkedin-content.txt")
        print("  Test connection: python3 post_linkedin.py test")
        sys.exit(1)

    if sys.argv[1] == "test":
        # Test connection
        access_token, person_id = load_linkedin_credentials()
        if access_token:
            user_info = get_user_info(access_token)
            if user_info:
                print("✅ LinkedIn API connection successful!")
                print(f"User: {user_info.get('name', 'Unknown')}")
                print(f"User ID: {user_info.get('sub', 'Unknown')}")
            else:
                print("❌ LinkedIn API connection failed")
        else:
            print("❌ LinkedIn credentials not found")
        return

    content_file = sys.argv[1]
    success = post_linkedin_content(content_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()