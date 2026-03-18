import json
import os
from datetime import datetime
from urllib.parse import quote

import boto3

_cognito_client = None


def _get_cognito_client():
    global _cognito_client
    if _cognito_client is None:
        _cognito_client = boto3.client("cognito-idp")
    return _cognito_client


def _get_pool_name(user_pool_id):
    """Fetch the UserPoolName for the given pool ID (cached per Lambda container)."""
    try:
        resp = _get_cognito_client().describe_user_pool(UserPoolId=user_pool_id)
        return resp["UserPool"]["Name"]
    except Exception as e:
        print(f"Warning: could not describe user pool {user_pool_id}: {e}")
        return ""


def _detect_pool_type(pool_name):
    """
    Detect pool type by checking if keyword exists anywhere in the pool name.
    Returns 'vendor', 'operator', or 'client' (default).
    """
    name = pool_name.lower()
    if "vendor" in name:
        return "vendor"
    if "operator" in name:
        return "operator"
    return "client"


def _resolve_config(user_pool_id):
    """
    Map a pool to its config by matching the pool name prefix.
    Pool names are expected to start with 'client-', 'vendor-', or 'operator-'.
    Falls back to client config if no match found.
    """
    pool_name = _get_pool_name(user_pool_id).lower()

    if pool_name.startswith("vendor"):
        return {
            "app_name": os.environ.get("VENDOR_APP_NAME", "Application"),
            "reset_path": os.environ.get("VENDOR_RESET_PASSWORD_PATH", ""),
            "login_path": os.environ.get("VENDOR_LOGIN_PATH", ""),
        }
    elif pool_name.startswith("operator"):
        return {
            "app_name": os.environ.get("OPERATOR_APP_NAME", "Application"),
            "reset_path": os.environ.get("OPERATOR_RESET_PASSWORD_PATH", ""),
            "login_path": os.environ.get("OPERATOR_LOGIN_PATH", ""),
        }
    else:
        # default to client
        return {
            "app_name": os.environ.get("CLIENT_APP_NAME", "Application"),
            "reset_path": os.environ.get("CLIENT_RESET_PASSWORD_PATH", ""),
            "login_path": os.environ.get("CLIENT_LOGIN_PATH", ""),
        }


def format_date_yyyymmdd():
    now = datetime.now()
    return f"{now.year}{now.month:02d}{now.day:02d}"


def lambda_handler(event, context):
    """
    Lambda handler for Cognito Custom Message trigger.

    Supported trigger sources:
    - CustomMessage_ForgotPassword
    - CustomMessage_SignUp (email verification)
    """
    try:
        print(f"Event: {json.dumps(event, indent=2)}")

        trigger_source = event.get("triggerSource", "")
        user_pool_id = event.get("userPoolId", "")
        request = event.get("request", {})
        code_parameter = request.get("codeParameter", "{####}")
        user_attributes = request.get("userAttributes", {})
        username = event.get("userName", "")
        user_email = user_attributes.get("email", username)

        pool_config = _resolve_config(user_pool_id)
        print(f"DEBUG pool_config: {json.dumps(pool_config)}")

        app_name = pool_config["app_name"]
        reset_path = pool_config["reset_path"]
        login_path = pool_config["login_path"]
        current_date = format_date_yyyymmdd()

        if trigger_source == "CustomMessage_ForgotPassword":
            reset_link = f"{reset_path}?code={code_parameter}&email={quote(user_email, safe='')}"
            subject = f"[{current_date}]password reset - {app_name}"
            message = _build_forgot_password_email(
                user_email, app_name, code_parameter, reset_link, login_path
            )
            event["response"]["emailSubject"] = subject
            event["response"]["emailMessage"] = message
            print(f"ForgotPassword email built for {user_email}")

        elif trigger_source == "CustomMessage_SignUp":
            subject = f"[{current_date}]email verification - {app_name}"
            message = _build_signup_email(user_email, app_name, code_parameter, login_path)
            event["response"]["emailSubject"] = subject
            event["response"]["emailMessage"] = message
            print(f"SignUp verification email built for {user_email}")

        else:
            print(f"Unhandled trigger source: {trigger_source}. Returning event unchanged.")

        return event

    except Exception as e:
        print(f"Error in lambda_handler: {e}")
        return event


def _build_forgot_password_email(user_email, app_name, code_parameter, reset_link, login_path):
    login_section = f'<p>Login: <a href="{login_path}">{login_path}</a></p>' if login_path else ""
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: sans-serif; line-height: 1.6; color: #333;">
<div style="max-width: 600px; margin: 0 auto; padding: 20px;">
  <h3>Password Reset</h3>
  <p>Dear {user_email},</p>
  <p>Your password reset code for {app_name}:</p>
  <div style="background: #f5f5f5; padding: 15px; margin: 20px 0; text-align: center;">
    <strong style="font-size: 24px; letter-spacing: 2px;">{code_parameter}</strong>
  </div>
  <p>Or reset your password via the link below:</p>
  <p><a href="{reset_link}">{reset_link}</a></p>
  {login_section}
  <p style="color: #666; font-size: 12px; margin-top: 30px;">This code expires in 15 minutes.</p>
  <p style="color: #666; font-size: 12px;">If you did not request this, please ignore this email.</p>
</div>
</body>
</html>"""


def _build_signup_email(user_email, app_name, code_parameter, login_path):
    login_section = f'<p>Login: <a href="{login_path}">{login_path}</a></p>' if login_path else ""
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body style="font-family: sans-serif; line-height: 1.6; color: #333;">
<div style="max-width: 600px; margin: 0 auto; padding: 20px;">
  <h3>Email Verification</h3>
  <p>Dear {user_email},</p>
  <p>Thank you for registering with {app_name}. Please enter the verification code below:</p>
  <div style="background: #f5f5f5; padding: 15px; margin: 20px 0; text-align: center;">
    <strong style="font-size: 24px; letter-spacing: 2px;">{code_parameter}</strong>
  </div>
  {login_section}
  <p style="color: #666; font-size: 12px; margin-top: 30px;">This code expires in 24 hours.</p>
</div>
</body>
</html>"""
