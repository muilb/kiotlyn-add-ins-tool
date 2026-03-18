#!/usr/bin/env bash
# ============================================================
# deploy.sh
# Full deployment pipeline for Cognito Custom Message infra
#
# Flow:
#   1. sam build
#   2. sam deploy  (Lambda + IAM Role + LogGroup)
#   3. attach_lambda_triggers.sh  (CustomMessage trigger per pool)
#   4. add_custom_attributes.sh   (12 custom string attributes per pool)
#
# Usage:
#   cd scripts
#   bash deploy.sh [--env dev|stg|prod] [--region us-west-2] [--profile default]
# ============================================================

set -euo pipefail

# ── defaults ─────────────────────────────────────────────
ENV="dev"
REGION="us-west-2"
PROFILE="default"

# ── parse args ───────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --env)     ENV="$2";     shift 2 ;;
    --region)  REGION="$2";  shift 2 ;;
    --profile) PROFILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── helpers ───────────────────────────────────────────────
step() { echo ""; echo "══════════════════════════════════════════════════"; echo "  STEP $1: $2"; echo "══════════════════════════════════════════════════"; }
ok()   { echo "  ✔ $*"; }
fail() { echo "  ✘ $*"; exit 1; }

# ── print config ─────────────────────────────────────────
echo "══════════════════════════════════════════════════"
echo "  Cognito Custom Message – Deploy Pipeline"
echo "  Env     : $ENV"
echo "  Region  : $REGION"
echo "  Profile : $PROFILE"
echo "══════════════════════════════════════════════════"

# ─────────────────────────────────────────────────────────
# STEP 1 – SAM Build
# ─────────────────────────────────────────────────────────
step 1 "SAM Build"

cd "$ROOT_DIR"
sam build
ok "sam build completed"

# ─────────────────────────────────────────────────────────
# STEP 2 – SAM Deploy
# ─────────────────────────────────────────────────────────
step 2 "SAM Deploy (env=$ENV)"

sam deploy \
  --config-env "$ENV" \
  --region "$REGION" \
  --profile "$PROFILE" \
  --no-confirm-changeset

ok "sam deploy completed"

# ─────────────────────────────────────────────────────────
# STEP 2b – Fix USER_POOL_CONFIGS env var (Windows SAM CLI truncation workaround)
# ─────────────────────────────────────────────────────────
ENV_VARS_FILE="$ROOT_DIR/env-vars.json"
if [[ -f "$ENV_VARS_FILE" ]]; then
  FUNCTION_NAME="cognito-custom-message-${ENV}"
  echo ">> Updating Lambda env vars from env-vars.json ..."
  aws lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --region "$REGION" \
    --profile "$PROFILE" \
    --environment "file://$ENV_VARS_FILE" > /dev/null
  ok "Lambda env vars updated"
fi

# ─────────────────────────────────────────────────────────
# STEP 3 – Attach Lambda triggers to User Pools
# ─────────────────────────────────────────────────────────
step 3 "Attach Lambda triggers to User Pools"

bash "$SCRIPT_DIR/attach_lambda_triggers.sh" \
  --env "$ENV" \
  --region "$REGION" \
  --profile "$PROFILE"

ok "Lambda triggers attached"

# ─────────────────────────────────────────────────────────
# STEP 4 – Add custom attributes to User Pools
# ─────────────────────────────────────────────────────────
step 4 "Add custom attributes to User Pools"

bash "$SCRIPT_DIR/add_custom_attributes.sh" \
  --region "$REGION" \
  --profile "$PROFILE"

ok "Custom attributes added"

# ─────────────────────────────────────────────────────────
# Done
# ─────────────────────────────────────────────────────────
echo ""
echo "══════════════════════════════════════════════════"
echo "  Deploy pipeline completed successfully!"
echo "  Env    : $ENV"
echo "  Region : $REGION"
echo "══════════════════════════════════════════════════"
