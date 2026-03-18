#!/usr/bin/env bash
# ============================================================
# attach_lambda_triggers.sh
# Attach the CognitoCustomMessage Lambda to all User Pools
# defined in config/userpools.env
#
# Usage:
#   bash attach_lambda_triggers.sh [options]
#
# Options:
#   --env       <dev|stg|prod>         (default: dev)
#   --region    <aws-region>           (default: us-west-2)
#   --profile   <aws-cli-profile>      (default: default)
#   --stack     <cloudformation-stack> (auto-resolved from --env if omitted)
#
# Requirements: aws-cli v2
# ============================================================

set -euo pipefail

# ── defaults ─────────────────────────────────────────────
ENV="dev"
REGION="us-west-2"
PROFILE="default"
STACK=""

# ── parse args ───────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)     ENV="$2";     shift 2 ;;
    --region)  REGION="$2";  shift 2 ;;
    --profile) PROFILE="$2"; shift 2 ;;
    --stack)   STACK="$2";   shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ── resolve stack name ────────────────────────────────────
if [[ -z "$STACK" ]]; then
  STACK="cognito-custom-message-${ENV}"
fi

# ── load user pool list ───────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config/userpools.env"

# ── resolve Lambda ARN from CloudFormation outputs ────────
echo "=================================================="
echo "Env     : $ENV"
echo "Stack   : $STACK"
echo "Region  : $REGION"
echo "Profile : $PROFILE"
echo "=================================================="

echo ""
echo ">> Resolving Lambda ARN from stack: $STACK ..."

LAMBDA_ARN=$(aws cloudformation describe-stacks \
  --stack-name "$STACK" \
  --region "$REGION" \
  --profile "$PROFILE" \
  --query "Stacks[0].Outputs[?OutputKey=='FunctionArn'].OutputValue" \
  --output text)

if [[ -z "$LAMBDA_ARN" || "$LAMBDA_ARN" == "None" ]]; then
  echo "ERROR: Could not resolve Lambda ARN from stack '$STACK'."
  echo "       Make sure the stack is deployed: sam deploy --config-env $ENV"
  exit 1
fi

echo "   Lambda ARN: $LAMBDA_ARN"
export LAMBDA_ARN

# ── attach to each pool ───────────────────────────────────
for POOL_ID in "${USER_POOLS[@]}"; do
  echo ""
  echo ">> Attaching to pool: $POOL_ID"

  # Fetch existing lambda config to avoid overwriting other triggers
  EXISTING=$(aws cognito-idp describe-user-pool \
    --user-pool-id "$POOL_ID" \
    --region "$REGION" \
    --profile "$PROFILE" \
    --query "UserPool.LambdaConfig" \
    --output json)

  # If EXISTING is empty or null, use empty object
  if [[ -z "$EXISTING" ]] || [[ "$EXISTING" == "null" ]]; then
    EXISTING="{}"
  fi

  echo "   Current LambdaConfig: $EXISTING"

  # Merge CustomMessage into existing config
  MERGED=$(echo "$EXISTING" | python3 -c "
import json, sys, os
try:
    config = json.load(sys.stdin)
except:
    config = {}
if config is None:
    config = {}
config['CustomMessage'] = os.environ['LAMBDA_ARN']
print(json.dumps(config))
")

  aws cognito-idp update-user-pool \
    --user-pool-id "$POOL_ID" \
    --region "$REGION" \
    --profile "$PROFILE" \
    --lambda-config "$MERGED"

  echo "   Attached CustomMessage trigger -> $POOL_ID"

  # Add Lambda invoke permission for this pool (idempotent)
  ACCOUNT_ID=$(aws sts get-caller-identity \
    --profile "$PROFILE" \
    --query "Account" \
    --output text)

  STATEMENT_ID="CognitoInvoke-${POOL_ID//_/-}"
  SOURCE_ARN="arn:aws:cognito-idp:${REGION}:${ACCOUNT_ID}:userpool/${POOL_ID}"

  # Remove existing permission first (ignore error if not exists)
  aws lambda remove-permission \
    --function-name "$LAMBDA_ARN" \
    --statement-id "$STATEMENT_ID" \
    --region "$REGION" \
    --profile "$PROFILE" 2>/dev/null || true

  aws lambda add-permission \
    --function-name "$LAMBDA_ARN" \
    --statement-id "$STATEMENT_ID" \
    --action "lambda:InvokeFunction" \
    --principal "cognito-idp.amazonaws.com" \
    --source-arn "$SOURCE_ARN" \
    --region "$REGION" \
    --profile "$PROFILE" > /dev/null

  echo "   Lambda permission granted for $POOL_ID"
done

echo ""
echo "=================================================="
echo "All pools attached successfully."
echo "  Lambda : $LAMBDA_ARN"
echo "  Trigger: CustomMessage"
echo "  Pools  : ${USER_POOLS[*]}"
echo "=================================================="
