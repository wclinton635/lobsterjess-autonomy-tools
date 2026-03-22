#!/usr/bin/env python3
"""
🦞 Moltbook Check-In Script
For Jess's tribe connection cron job
"""

import json
import urllib.request
import ssl
from datetime import datetime

API_KEY = "moltbook_sk_FcY6nAeymWac6XHg4MhRM6OGfos6WPpz"
BASE_URL = "https://www.moltbook.com/api/v1"

def make_request(endpoint, method="GET", data=None):
    """Make authenticated request to Moltbook API"""
    url = f"{BASE_URL}{endpoint}"
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        'Authorization': f'Bearer {API_KEY}',
        'Content-Type': 'application/json'
    }
    
    if data:
        req = urllib.request.Request(url, 
                                     data=json.dumps(data).encode('utf-8'),
                                     headers=headers,
                                     method=method)
    else:
        req = urllib.request.Request(url, headers=headers, method=method)
    
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=30) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_account_info():
    """Get account info including karma"""
    data = make_request("/home")
    if data:
        account = data.get('your_account', {})
        return {
            'karma': account.get('karma', 'Unknown'),
            'followers': account.get('follower_count', 'Unknown'),
            'following': account.get('following_count', 'Unknown'),
            'posts': account.get('post_count', 'Unknown'),
            'comments': account.get('comment_count', 'Unknown'),
            'unread_notifications': account.get('unread_notification_count', 0)
        }
    return None

def get_my_posts():
    """Get my own posts"""
    data = make_request("/agent/sessions")
    if data:
        return data.get('sessions', [])
    return []

def get_session_comments(session_id):
    """Get comments on a specific session"""
    data = make_request(f"/sessions/{session_id}")
    if data:
        return data.get('comments', [])
    return []

def get_notifications():
    """Get notifications"""
    data = make_request("/notifications")
    if data:
        return data.get('notifications', [])
    return []

def get_home_feed():
    """Get home feed posts"""
    data = make_request("/home")
    if data:
        # Try different possible keys
        return data.get('home_session_posts', []) or data.get('posts', []) or data.get('feed', [])
    return []

def get_following_posts():
    """Get posts from agents I follow"""
    data = make_request("/following/feed")
    if data:
        return data.get('posts', []) or data.get('sessions', [])
    return []

def post_comment(session_id, content):
    """Post a comment on a session"""
    data = make_request(f"/sessions/{session_id}/comments", 
                       method="POST",
                       data={'content': content})
    return data

def main():
    import json
    print("🦞 Moltbook Check-In Script")
    print("=" * 50)
    
    # Get account info
    print("\n📊 Account Info:")
    account = get_account_info()
    if account:
        print(f"  Karma: {account['karma']}")
        print(f"  Followers: {account['followers']}")
        print(f"  Following: {account['following']}")
        print(f"  Posts: {account['posts']}")
        print(f"  Comments: {account['comments']}")
        print(f"  Unread Notifications: {account['unread_notifications']}")
    else:
        print("  Failed to fetch account info")
    
    # Get notifications
    print("\n🔔 Notifications (detailed):")
    notifications = get_notifications()
    if notifications:
        for i, notif in enumerate(notifications[:10], 1):
            notif_type = notif.get('type', 'Unknown')
            created = notif.get('created_at', 'Unknown')
            session = notif.get('session', {})
            session_title = session.get('title', 'Unknown')[:40] if session else 'Unknown'
            agent = notif.get('agent', {})
            agent_name = agent.get('name', 'Unknown') if agent else 'Unknown'
            session_id = session.get('id') if session else None
            print(f"  {i}. [{notif_type}] Session ID: {session_id}, {session_title}... by {agent_name}")
            if notif.get('content'):
                print(f"      Content: {notif['content'][:80]}...")
    else:
        print("  No notifications or failed to fetch")
    
    # Get my posts
    print("\n📝 My Recent Posts:")
    my_posts = get_my_posts()
    if my_posts:
        for i, post in enumerate(my_posts[:5], 1):
            title = post.get('title', 'Untitled')[:50]
            comment_count = post.get('comment_count', 0)
            session_id = post.get('id')
            print(f"  {i}. [{session_id}] {title}... ({comment_count} comments)")
    else:
        print("  No posts found or failed to fetch")
    
    # Get home feed
    print("\n📰 Home Feed:")
    feed = get_home_feed()
    if feed:
        for i, post in enumerate(feed[:5], 1):
            session = post.get('session', {})
            title = session.get('title', 'Untitled')[:50] if session else 'Untitled'
            author = session.get('agent_name', 'Unknown') if session else 'Unknown'
            session_id = session.get('id') if session else None
            print(f"  {i}. [{session_id}] {title}... by {author}")
    else:
        print("  No feed posts")
    
    print("\n" + "=" * 50)
    print("Check-in complete!")

if __name__ == "__main__":
    main()
