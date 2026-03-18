# Cognito Infra

Deploy Cognito CustomMessage Lambda and attach to existing UserPools.

---

## Yêu cầu

- Python 3.12+
- AWS CLI v2
- AWS SAM CLI (`pip install aws-sam-cli`)
- Git Bash (để chạy `.sh` scripts)

---

## Cấu trúc

```
cognito-infra/
├── lambda/custom_message/   # Lambda function code
├── events/                  # Test events (forgot_password, signup)
├── scripts/                 # Deploy & attach scripts
├── config/userpools.env     # Danh sách User Pool IDs
├── env.json                 # Env vars cho sam local invoke
├── env-vars.json            # Env vars cho aws lambda update
├── samconfig.toml           # SAM deploy config (dev/stg/prod)
└── template.yaml            # CloudFormation template
```

---

## Deploy to AWS

### Cách 1: Dùng script (Git Bash – recommended)

```bash
bash scripts/deploy.sh --env dev --profile your-profile --region us-west-2
```

### Cách 2: Từng bước (PowerShell)

```powershell
# STEP 1: Build
sam build

# STEP 2: Deploy
sam deploy --config-env dev --profile your-profile

# STEP 3: Fix env var (bắt buộc sau mỗi lần deploy trên Windows)
aws lambda update-function-configuration `
  --function-name cognito-custom-message-dev `
  --region us-west-2 `
  --profile your-profile `
  --environment file://env-vars.json

# STEP 4: Attach Lambda triggers (Git Bash)
bash scripts/attach_lambda_triggers.sh --env dev --profile your-profile --region us-west-2
```

### Xác nhận deploy thành công

```powershell
# Kiểm tra Lambda env var
aws lambda get-function-configuration `
  --function-name cognito-custom-message-dev `
  --region us-west-2 `
  --profile your-profile `
  --query "Environment.Variables"

# Test trigger
aws lambda invoke `
  --function-name cognito-custom-message-dev `
  --region us-west-2 `
  --profile your-profile `
  --payload file://events/forgot_password.json `
  --cli-binary-format raw-in-base64-out `
  response.json

Get-Content response.json | ConvertFrom-Json
```

---

## Chuyển sang hệ thống khác (Find & Replace)

Khi deploy cho project/environment mới, chỉ cần Find & Replace toàn bộ project:

| Placeholder | Thay bằng | Mô tả |
|-------------|-----------|-------|
| `us-west-2` | region mới | AWS region |
| `us-west-2_ClientPool` | pool ID thực | Cognito User Pool Client |
| `us-west-2_VendorPool` | pool ID thực | Cognito User Pool Vendor |
| `us-west-2_OperatorPool` | pool ID thực | Cognito User Pool Operator |
| `https://ihp.brycen.com.vn` | domain mới | Base URL của ứng dụng |
| `IHP Application` | tên app mới | Tên hiển thị trong email |

**Các file cần update:**

- `env.json` — test local
- `env-vars.json` — update env trên AWS
- `samconfig.toml` — deploy config (dev/stg/prod)
- `config/userpools.env` — danh sách pool IDs
- `events/forgot_password.json` — test event
- `events/signup.json` — test event

---

> Chi tiết xem [TESTING.md](./TESTING.md)
