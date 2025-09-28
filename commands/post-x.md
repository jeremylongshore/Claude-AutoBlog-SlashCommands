Post directly to X/Twitter with automatic formatting, character optimization, and analytics tracking.

## Your Task

This command takes your text and posts it directly to X/Twitter using your existing OAuth credentials, with smart formatting and tracking.

### Phase 1: Process Input Text

1. **Receive Text Input**
   - Accept text from user (can be multi-line)
   - Handle various input formats
   - Preserve intentional line breaks
   - Clean up formatting inconsistencies

2. **Smart Text Processing**
   - Check character count (280 limit)
   - Add TL;DR if text is complex
   - Optimize hashtags (max 2, relevant)
   - Format for readability
   - Handle URLs properly

3. **Character Optimization**
   - If over 280 chars, suggest thread conversion
   - Optimize spacing and punctuation
   - Smart abbreviations if needed
   - Preserve key messaging

### Phase 2: X API Posting

4. **Prepare X API Call**
   - Use existing OAuth tokens from .env
   - Format for X API v2 requirements
   - Include proper headers and authentication
   - Handle media attachments if provided

5. **Post to X**
   - Execute API call to post tweet
   - Handle rate limiting gracefully
   - Retry on temporary failures
   - Capture response data (tweet ID, URL)

6. **Error Handling**
   - Handle authentication errors
   - Manage character limit violations
   - Deal with duplicate content detection
   - Provide clear error messages

### Phase 3: Confirmation & Analytics

7. **Show Success Confirmation**
   - Display posted tweet text
   - Show live tweet URL
   - Confirm character count used
   - Display posting timestamp

8. **Track in Analytics**
   - Log command execution
   - Record tweet metadata (ID, URL, character count)
   - Update X posting statistics
   - Track posting success rate

9. **Save for Reference**
   - Save posted text to `/home/jeremy/projects/blog/x-posts/YYYY-MM-DD-HH-MM-posted.txt`
   - Include tweet URL and metadata
   - Create posting history log

## Smart Formatting Features

### Automatic Optimizations
- **TL;DR addition** for complex posts
- **Hashtag optimization** (max 2, contextual)
- **Line break preservation** for readability
- **URL shortening** if needed
- **Character count display** before posting

### Thread Detection
If text exceeds 280 characters:
- Suggest converting to thread
- Ask: "Convert to thread? (yes/auto-thread/edit)"
- Auto-split at natural break points
- Maintain message flow

## X API Integration

### Using Existing Credentials
```python
X_CLIENT_ID = "VXpOWXBxNDJWbWZVWU5VOGE2Rm46MTpjaQ"
X_CLIENT_SECRET = "CUK0B0vkhuytNNbQ3LPVWe6dWwSYgMgsGX2nQiltGWu3Q2TZ-K"
X_OAUTH2_ACCESS_TOKEN = "ZllRajY2eVVGSDBtR1JqMEFxa1VzV3NCVlN1NkF3OGpSV0hDY1hDMlVGbmoxOjE3NTkwMjI0ODIwOTI6MTowOmF0OjE"
X_OAUTH2_REFRESH_TOKEN = "VDVPbG5nbG43REpGV0gwR1ExcENidk0yYloweHZzZ0Rkc3ZwNVI2eHJhcE9NOjE3NTkwMjI0ODIwOTM6MToxOnJ0OjE"
```

### API Call Structure
```python
url = "https://api.twitter.com/2/tweets"
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
payload = {"text": optimized_text}
response = requests.post(url, headers=headers, json=payload)
```

## Analytics Tracking

### What Gets Tracked
- Command execution time and success
- Character count and optimization applied
- Tweet ID and live URL
- Posting timestamp
- User satisfaction (success/error)

### Database Integration
- Update slash_commands table
- Log X posting activity
- Track posting frequency
- Monitor success rates

## Usage Examples

### Simple Post
```
User: /post-x "Just deployed a new MCP server integration! 🚀"
Claude:
✅ Posted to X successfully!
🔗 https://twitter.com/AsphaltCowb0y/status/1234567890
📊 54 characters used
📝 Saved to x-posts/2025-09-27-21-45-posted.txt
```

### Long Text (Auto-Thread Suggestion)
```
User: /post-x "Long explanation about technical implementation..."
Claude:
⚠️ Text is 450 characters (over 280 limit)
📝 Suggested action: Convert to 2-tweet thread
🔄 Auto-split points detected
Continue? (yes/edit/cancel)
```

### With Optimization
```
User: /post-x "This is really cool technical stuff about APIs and integrations"
Claude:
📝 Optimized text:
"TL;DR: New API integration architecture is fire 🔥

Just built something really cool - technical integration that streamlines our entire development workflow. #APIDesign #DevOps"

Character count: 178/280
Post this? (yes/edit/cancel)
```

## Response Options

After showing optimized text:
- **"yes"** - Post immediately to X
- **"edit"** - Let user modify before posting
- **"cancel"** - Don't post anything

## File Outputs

- **Posted text**: `/home/jeremy/projects/blog/x-posts/YYYY-MM-DD-HH-MM-posted.txt`
- **Analytics entry**: Logged in content_analytics.db
- **Tweet URL**: For easy reference and sharing

## Error Handling

### Common Issues
- **Rate limiting**: Wait and retry with countdown
- **Authentication errors**: Refresh OAuth tokens automatically
- **Duplicate content**: Suggest slight modifications
- **Character limit**: Offer thread conversion

### User-Friendly Messages
- Clear explanation of what went wrong
- Suggested fixes or alternatives
- Option to retry or cancel

**Result:** Instant X posting with professional formatting, complete analytics tracking, and zero friction workflow.

## Integration with Existing System

- Uses same OAuth credentials as truck stop tweet success
- Integrates with existing analytics database
- Follows same command tracking patterns
- Saves posts for future reference

**One command, instant X posting, complete tracking! 🚀**