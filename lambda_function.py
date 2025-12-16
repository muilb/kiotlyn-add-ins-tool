import json
from datetime import datetime

# User pool configurations
USER_POOL_CONFIGS = {
    'us-west-2_KPanuv1zg': {
        'reset_path': 'https://ihp.brycen.com.vn/reset-password',
        'app_name': 'IHP Application'
    },
    'us-east-1_XXXXX2': {
        'reset_path': 'https://app2.example.com/reset-password',
        'app_name': 'Application 2'
    }
}

def format_japanese_date():
    """Format current date: yyyymmdd"""
    now = datetime.now()
    return f"{now.year}{now.month:02d}{now.day:02d}"

def lambda_handler(event, context):
    """
    Lambda handler for Cognito Custom Message trigger
    
    Event structure:
    {
        "triggerSource": "CustomMessage_ForgotPassword",
        "userPoolId": "us-east-1_XXXXX",
        "userName": "user@example.com",
        "request": {
            "codeParameter": "{####}",
            "usernameParameter": "{username}",
            "userAttributes": {
                "sub": "xxx-xxx-xxx",
                "email": "user@example.com"
            }
        },
        "response": {
            "emailSubject": "",
            "emailMessage": ""
        }
    }
    """
    
    try:
        # Log full event for debugging
        print(f"=== Lambda Triggered ===")
        print(f"Event: {json.dumps(event, indent=2)}")
        
        trigger_source = event.get('triggerSource')
        print(f"Trigger Source: {trigger_source}")
        
        # Only handle ForgotPassword trigger
        if trigger_source != 'CustomMessage_ForgotPassword':
            print(f"Skipping trigger: {trigger_source}")
            return event
        
        # Get event details
        user_pool_id = event.get('userPoolId')
        username = event.get('userName')
        code_parameter = event['request'].get('codeParameter', '{####}')
        user_attributes = event['request'].get('userAttributes', {})
        user_email = user_attributes.get('email', username)
        
        # Get configuration for this user pool
        pool_config = USER_POOL_CONFIGS.get(user_pool_id)
        if not pool_config:
            print(f"Warning: No configuration found for user pool {user_pool_id}")
            print(f"Available pools: {list(USER_POOL_CONFIGS.keys())}")
            return event
        
        print(f"Using config: {pool_config['app_name']}")
        
        # Format current date (yyyymmdd)
        current_date = format_japanese_date()
        
        # Build reset link
        reset_link = f"{pool_config['reset_path']}?code={code_parameter}&email={user_email}"
        app_name = pool_config['app_name']
        
        # Email subject
        email_subject = f"[{current_date}]パスワード再設定 - {app_name}"
        
        # Simple HTML email
        email_message = f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: sans-serif; line-height: 1.6; color: #333;">
<div style="max-width: 600px; margin: 0 auto; padding: 20px;">
  <h3>パスワード再設定</h3>
  <p>{user_email} 様</p>
  <p>Hi {username} </p>
  <p>{app_name}のパスワード再設定コード:</p>
  <div style="background: #f5f5f5; padding: 15px; margin: 20px 0; text-align: center;">
    <strong style="font-size: 24px; letter-spacing: 2px;">{code_parameter}</strong>
  </div>
  <p>リンク: <a href="{reset_link}">{reset_link}</a></p>
  <p style="color: #666; font-size: 12px; margin-top: 30px;">※ 15分間有効</p>
</div>
</body>
</html>"""
        
        # Update response
        event['response']['emailSubject'] = email_subject
        event['response']['emailMessage'] = email_message
        
        print(f"✅ Custom message generated successfully!")
        print(f"Subject: {email_subject}")
        print(f"Message length: {len(email_message)} chars")
        
        return event
        
    except Exception as e:
        print(f"Error in lambda_handler: {str(e)}")
        # Return original event to avoid breaking Cognito flow
        return event
