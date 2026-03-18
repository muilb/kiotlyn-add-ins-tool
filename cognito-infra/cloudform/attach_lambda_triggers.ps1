# attach_lambda_triggers.ps1
# Run after sam deploy completes.
# Usage: .\attach_lambda_triggers.ps1 -Env dev -Profile lb_mui

param(
    [string]$Env     = "dev",
    [string]$Profile = "default",
    [string]$Region  = "us-west-2"
)

$StackName = "cognito-infra-$Env"

# --- Get Lambda ARN and Pool IDs from single stack ---
$LambdaArn = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --profile $Profile --region $Region `
    --query "Stacks[0].Outputs[?OutputKey=='LambdaFunctionArn'].OutputValue" `
    --output text

$ClientPoolId = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --profile $Profile --region $Region `
    --query "Stacks[0].Outputs[?OutputKey=='ClientUserPoolId'].OutputValue" `
    --output text

$VendorPoolId = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --profile $Profile --region $Region `
    --query "Stacks[0].Outputs[?OutputKey=='VendorUserPoolId'].OutputValue" `
    --output text

$OperatorPoolId = aws cloudformation describe-stacks `
    --stack-name $StackName `
    --profile $Profile --region $Region `
    --query "Stacks[0].Outputs[?OutputKey=='OperatorUserPoolId'].OutputValue" `
    --output text

Write-Host "Lambda ARN   : $LambdaArn"
Write-Host "Client Pool  : $ClientPoolId"
Write-Host "Vendor Pool  : $VendorPoolId"
Write-Host "Operator Pool: $OperatorPoolId"
Write-Host ""

$AccountId = aws sts get-caller-identity --profile $Profile --query Account --output text

$Pools = @(
    @{ Id = $ClientPoolId;   Name = "Client"   }
    @{ Id = $VendorPoolId;   Name = "Vendor"   }
    @{ Id = $OperatorPoolId; Name = "Operator" }
)

foreach ($Pool in $Pools) {
    $PoolId  = $Pool.Id
    $PoolArn = "arn:aws:cognito-idp:${Region}:${AccountId}:userpool/$PoolId"

    Write-Host "[$($Pool.Name)] Adding Lambda invoke permission..."
    aws lambda add-permission `
        --function-name $LambdaArn `
        --statement-id  "cognito-$($Pool.Name.ToLower())-$Env" `
        --action        lambda:InvokeFunction `
        --principal     cognito-idp.amazonaws.com `
        --source-arn    $PoolArn `
        --profile $Profile --region $Region 2>&1 | Out-Null

    Write-Host "[$($Pool.Name)] Attaching CustomMessage trigger..."
    aws cognito-idp update-user-pool `
        --user-pool-id $PoolId `
        --lambda-config "CustomMessage=$LambdaArn" `
        --profile $Profile --region $Region

    Write-Host "[$($Pool.Name)] Done."
    Write-Host ""
}

Write-Host "All triggers attached successfully."
