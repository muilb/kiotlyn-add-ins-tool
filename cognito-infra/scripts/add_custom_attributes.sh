#!/usr/bin/env bash
# ============================================================
# add_custom_attributes.sh
# Add 12 custom string attributes (mutable=false) to Cognito
# User Pools defined in userpools.env
#
# Usage:
#   bash add_custom_attributes.sh [--region us-west-2] [--profile default]
#
# Requirements: aws-cli v2
# ============================================================

set -euo pipefail

# ── defaults ─────────────────────────────────────────────
REGION="us-west-2"
PROFILE="default"

# ── parse args ───────────────────────────────────────────
while [[ $# -gt 0 ]]; do
  case "$1" in
    --region)  REGION="$2";  shift 2 ;;
    --profile) PROFILE="$2"; shift 2 ;;
    *) echo "Unknown option: $1"; exit 1 ;;
  esac
done

# ── load user pool list ───────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/../config/userpools.env"

# ── custom attributes (all String, mutable=false) ─────────
# Cognito prepends "custom:" automatically.
# Max 25 custom attributes per pool; max name length = 20 chars.
ATTRIBUTES_JSON='[
  {
    "Name": "tenant_id",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "organization",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "department",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "role1",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "employee_id",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "position",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "office_location",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "cost_center",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "contract_type",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "manager_id",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  },
  {
    "Name": "start_date",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "10"}
  },
  {
    "Name": "system_code",
    "AttributeDataType": "String",
    "Mutable": false,
    "Required": false,
    "StringAttributeConstraints": {"MinLength": "0", "MaxLength": "256"}
  }
]'

# ── main loop ─────────────────────────────────────────────
echo "=================================================="
echo "Region  : $REGION"
echo "Profile : $PROFILE"
echo "Pools   : ${USER_POOLS[*]}"
echo "=================================================="

for POOL_ID in "${USER_POOLS[@]}"; do
  echo ""
  echo ">> Processing pool: $POOL_ID"

  aws cognito-idp add-custom-attributes \
    --user-pool-id "$POOL_ID" \
    --region "$REGION" \
    --profile "$PROFILE" \
    --custom-attributes "$ATTRIBUTES_JSON"

  echo "   Done: 12 attributes added to $POOL_ID"
done

echo ""
echo "=================================================="
echo "All pools updated successfully."
echo ""
echo "Attributes added (prefix 'custom:' applied by Cognito):"
echo "  custom:tenant_id       custom:organization    custom:department"
echo "  custom:role            custom:employee_id     custom:position"
echo "  custom:office_location custom:cost_center     custom:contract_type"
echo "  custom:manager_id      custom:start_date      custom:system_code"
echo "=================================================="
