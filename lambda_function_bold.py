import json
from datetime import datetime
from typing import Dict, Optional

# User pool configurations
USER_POOL_CONFIGS = {
    'us-west-2_KPanuv1zg': {
        'reset_path': 'https://ihp.brycen.com.vn/reset-password',
        'login_path': 'https://ihp.brycen.com.vn/login',
        'app_name': 'IHP Application'
    },
    'us-east-1_XXXXX2': {
        'reset_path': 'https://app2.example.com/reset-password',
        'login_path': 'https://app2.example.com/login',
        'app_name': 'Application 2'
    }
}

# Role-based message templates
ROLE_MESSAGES = {
    'CLIENT': {
        'ja': '発注者としてPUBDISシステムにアクセスできます。',
        'en': 'You can access the PUBDIS system as a Client.'
    },
    'CONTRACTOR': {
        'ja': '受注者としてPUBDISシステムにアクセスできます。',
        'en': 'You can access the PUBDIS system as a Contractor.'
    },
    'OPERATOR': {
        'ja': 'オペレーターとしてPUBDISシステムを管理できます。',
        'en': 'You can manage the PUBDIS system as an Operator.'
    }
}

def format_japanese_date() -> str:
    """Format current date as yyyymmdd"""
    now = datetime.now()
    return f"{now.year}{now.month:02d}{now.day:02d}"

def get_user_role(user_attributes: Dict) -> str:
    """Extract user role from custom:role attribute"""
    return user_attributes.get('custom:role', 'CLIENT')

def get_user_test_value(user_attributes: Dict) -> Optional[str]:
    """Extract custom:test attribute value"""
    return user_attributes.get('custom:test')

def get_email_subject(trigger_source: str, app_name: str, user_role: str = None) -> str:
    current_date = format_japanese_date()
    
    subject_templates = {
        'CustomMessage_ForgotPassword': f"[{current_date}]パスワード再設定 - {app_name}",
        'CustomMessage_AdminCreateUser': f"[{current_date}]{user_role}アカウント作成通知 - {app_name}"
    }
    
    return subject_templates.get(
        trigger_source, 
        f"[{current_date}]通知 - {app_name}"
    )

def get_forgot_password_message(
    code_parameter: str,
    username: str,
    user_email: str,
    reset_link: str,
    app_name: str,
    test_value: Optional[str]
) -> str:
    test_section = ""
    if test_value:
        test_section = f"<p>テスト値: {test_value}</p>"
    
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body>
<p>パスワード再設定</p>
<p>Password Reset</p>

<p>こんにちは、{user_email} 様</p>
<p>Hello, {username}</p>

<p>{app_name}のパスワード再設定リクエストを受け付けました。</p>
<p>We have received your password reset request for {app_name}.</p>

<p>確認コード / Verification Code:</p>
<p>{code_parameter}</p>

{test_section}

<p>パスワード再設定リンク:</p>
<p><a href="{reset_link}">パスワードを再設定する</a></p>

<p>⚠️ このコードは15分間のみ有効です。</p>
<p>⚠️ This code is valid for 15 minutes only.</p>

<p>このメールは自動送信されています。返信しないでください。</p>
<p>This is an automated email. Please do not reply.</p>
<p>&copy; 2026 {app_name}</p>
</body>
</html>"""

def get_admin_create_user_message(
    code_parameter: str,
    username: str,
    user_email: str,
    user_name: str,
    user_role: str,
    login_link: str,
    app_name: str,
    test_value: Optional[str]
) -> str:
    role_message = ROLE_MESSAGES.get(user_role, ROLE_MESSAGES['CLIENT'])
    
    test_section = ""
    if test_value:
        test_section = f"""<p>テスト値: {test_value}</p>
<p>Test Value: {test_value}</p>"""
    
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body>
<p>{user_role} アカウント作成のお知らせ</p>
<p>{app_name}</p>

<p>こんにちは、{user_name or username} 様</p>
<p>Hello, {user_name or username}</p>

<p>{app_name}の{user_role}アカウントが作成されました。</p>
<p>Your {user_role} account has been created for {app_name}.</p>

<p>{role_message['ja']}</p>
<p>{role_message['en']}</p>

{test_section}

<p>ログイン情報 / Login Credentials</p>

<p>ログインURL / Login URL:</p>
<p><a href="{login_link}">{login_link}</a></p>

<p>ユーザー名 / Username:</p>
<p>{username}</p>

<p>仮パスワード / Temporary Password:</p>
<p>{code_parameter}</p>

<p>⚠️ 初回ログイン時に、パスワードの変更が必要です。</p>
<p>⚠️ You will be required to change your password on first login.</p>

<p><a href="{login_link}">ログインページへ / Go to Login</a></p>

<p>サポート / Support:</p>
<p>ご不明な点がございましたら、システム管理者までお問い合わせください。</p>
<p>If you have any questions, please contact your system administrator.</p>

<p>このメールは自動送信されています。返信しないでください。</p>
<p>This is an automated email. Please do not reply.</p>
<p>&copy; 2026 {app_name}</p>
</body>
</html>"""

def lambda_handler(event, context):
    """
    Lambda handler for Cognito Custom Message triggers
    
    Supported triggers:
    - CustomMessage_ForgotPassword: Password reset
    - CustomMessage_AdminCreateUser: Admin creates new user
    
    Event structure documented in AWS Cognito docs:
    https://docs.aws.amazon.com/cognito/latest/developerguide/user-pool-lambda-custom-message.html
    """
    
    try:
        trigger_source = event.get('triggerSource')
        user_pool_id = event.get('userPoolId')
        username = event.get('userName')
        
        pool_config = USER_POOL_CONFIGS.get(user_pool_id)
        if not pool_config:
            return event
        
        app_name = pool_config['app_name']
        
        request = event.get('request', {})
        code_parameter = request.get('codeParameter', '{####}')
        user_attributes = request.get('userAttributes', {})
        user_email = user_attributes.get('email', username)
        user_name = user_attributes.get('name', '')
        user_role = get_user_role(user_attributes)
        test_value = get_user_test_value(user_attributes)
        
        email_subject = get_email_subject(trigger_source, app_name, user_role)
        email_message = None
        
        if trigger_source == 'CustomMessage_ForgotPassword':
            reset_link = f"{pool_config['reset_path']}?code={code_parameter}&email={user_email}"
            email_message = get_forgot_password_message(
                code_parameter=code_parameter,
                username=username,
                user_email=user_email,
                reset_link=reset_link,
                app_name=app_name,
                test_value=test_value
            )
            
        elif trigger_source == 'CustomMessage_AdminCreateUser':
            login_link = pool_config['login_path']
            email_message = get_admin_create_user_message(
                code_parameter=code_parameter,
                username=username,
                user_email=user_email,
                user_name=user_name,
                user_role=user_role,
                login_link=login_link,
                app_name=app_name,
                test_value=test_value
            )
            
        else:
            return event
        
        if email_message:
            event['response']['emailSubject'] = email_subject
            event['response']['emailMessage'] = email_message
        
        return event
        
    except Exception:
        return event