#!/usr/bin/env bash
# Deploy anupreetwalia.com to AWS S3 + CloudFront.
# Prereqs: AWS CLI v2 installed and `aws configure` already run with your credentials.
# Usage:  ./deploy.sh
set -euo pipefail

# ---- CONFIG ----
AWS_PROFILE="personal"               # named AWS CLI profile to use for ALL calls
export AWS_PROFILE
REGION="us-east-1"
DOMAIN="anupreetwalia.com"

# Derive the same bucket name provision_aws.sh created (globally-unique, account-suffixed),
# and auto-find the CloudFront distribution by its domain alias. Nothing to hand-edit.
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
BUCKET="anupreetwalia-com-site-${ACCOUNT_ID}"
DIST_ID="$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?Aliases.Items && contains(Aliases.Items, '${DOMAIN}')].Id | [0]" \
  --output text 2>/dev/null || true)"

# Files to upload = everything except the generator + scripts
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "==> Account $ACCOUNT_ID · bucket $BUCKET · distribution ${DIST_ID:-none}"
echo "==> Syncing site to s3://$BUCKET ..."
aws s3 sync "$SRC_DIR" "s3://$BUCKET" \
  --region "$REGION" \
  --delete \
  --exclude "*.py" \
  --exclude "*.sh" \
  --exclude "README.md" \
  --exclude "*.bak" \
  --exclude ".DS_Store" \
  --exclude "Screenshot*" \
  --exclude "assets/gh-*.svg" \
  --exclude "*.docx"

# Force correct Content-Types (browsers ignore CSS served as the wrong type).
aws s3 cp "s3://$BUCKET" "s3://$BUCKET" --recursive --region "$REGION" \
  --exclude "*" --include "*.html" \
  --content-type "text/html; charset=utf-8" \
  --cache-control "max-age=300" --metadata-directive REPLACE

aws s3 cp "s3://$BUCKET" "s3://$BUCKET" --recursive --region "$REGION" \
  --exclude "*" --include "*.css" \
  --content-type "text/css; charset=utf-8" \
  --cache-control "max-age=300" --metadata-directive REPLACE

aws s3 cp "s3://$BUCKET" "s3://$BUCKET" --recursive --region "$REGION" \
  --exclude "*" --include "*.svg" \
  --content-type "image/svg+xml" --metadata-directive REPLACE

if [ -n "$DIST_ID" ] && [ "$DIST_ID" != "None" ]; then
  echo "==> Invalidating CloudFront cache ..."
  aws cloudfront create-invalidation --distribution-id "$DIST_ID" --paths "/*" >/dev/null
fi

echo "==> Done. https://$DOMAIN"
