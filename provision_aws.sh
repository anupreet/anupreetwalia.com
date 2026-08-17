#!/usr/bin/env bash
###############################################################################
# provision_aws.sh
# One-time, turnkey provisioning for anupreetwalia.com on AWS:
#   - Private S3 bucket (NOT public) for the site files
#   - CloudFront distribution with Origin Access Control (OAC) -> only
#     CloudFront can read the bucket. This is the secure pattern: the bucket
#     is never publicly exposed.
#   - ACM TLS certificate (us-east-1) with DNS validation, auto-validated
#     through Route 53.
#   - Route 53 A + AAAA alias records pointing the apex domain at CloudFront.
#   - Initial upload of the site.
#
# REQUIREMENTS (on your machine):
#   - AWS CLI v2 installed:        aws --version
#   - Credentials configured:      aws configure   (or SSO)  with rights to
#                                  S3, CloudFront, ACM, and Route 53.
#   - jq installed:                brew install jq
#   - You already own the domain's hosted zone in Route 53.
#
# USAGE:
#   chmod +x provision_aws.sh
#   ./provision_aws.sh
#
# Safe to read top-to-bottom before running. It prints each step and waits
# on the slow AWS operations (cert validation, CloudFront deploy).
###############################################################################
set -euo pipefail

# -------- CONFIG (edit if needed) --------
AWS_PROFILE="personal"             # named AWS CLI profile to use for ALL calls
export AWS_PROFILE
DOMAIN="anupreetwalia.com"
INCLUDE_WWW="yes"                  # also serve www.anupreetwalia.com -> redirected by CloudFront alias
REGION="us-east-1"                 # bucket region; us-east-1 keeps ACM+CF simple
SRC_DIR="$(cd "$(dirname "$0")" && pwd)"
CERT_REGION="us-east-1"            # ACM certs for CloudFront MUST be in us-east-1
# With CloudFront + OAC the bucket name does NOT need to match the domain, so we
# use a globally-unique name (the bare domain is already taken by another account).
# -----------------------------------------

command -v aws >/dev/null || { echo "ERROR: aws CLI not found."; exit 1; }
command -v jq  >/dev/null || { echo "ERROR: jq not found (brew install jq)."; exit 1; }
ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
BUCKET="anupreetwalia-com-site-${ACCOUNT_ID}"   # unique private bucket (not public, not the domain)
echo "==> AWS account: $ACCOUNT_ID   domain: $DOMAIN   bucket: $BUCKET"

ALIASES=("$DOMAIN")
[ "$INCLUDE_WWW" = "yes" ] && ALIASES+=("www.$DOMAIN")

############################# 1. S3 bucket (private) ##########################
echo "==> [1/6] Creating private S3 bucket: $BUCKET"
if aws s3api head-bucket --bucket "$BUCKET" 2>/dev/null; then
  echo "    bucket already exists, reusing."
else
  if [ "$REGION" = "us-east-1" ]; then
    aws s3api create-bucket --bucket "$BUCKET" --region "$REGION"
  else
    aws s3api create-bucket --bucket "$BUCKET" --region "$REGION" \
      --create-bucket-configuration LocationConstraint="$REGION"
  fi
fi
# Block ALL public access — security: bucket is reachable only via CloudFront OAC.
aws s3api put-public-access-block --bucket "$BUCKET" \
  --public-access-block-configuration \
  BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true

############################# 2. ACM certificate #############################
echo "==> [2/6] Requesting/locating ACM cert in $CERT_REGION (account $ACCOUNT_ID)"
SAN_ARGS=()
[ "$INCLUDE_WWW" = "yes" ] && SAN_ARGS=(--subject-alternative-names "www.$DOMAIN")
# Prefer an already-ISSUED cert in THIS account; then a pending one; else request new.
CERT_ARN="$(aws acm list-certificates --region "$CERT_REGION" --certificate-statuses ISSUED \
  --query "CertificateSummaryList[?DomainName=='$DOMAIN'].CertificateArn | [0]" --output text)"
if [ "$CERT_ARN" = "None" ] || [ -z "$CERT_ARN" ]; then
  CERT_ARN="$(aws acm list-certificates --region "$CERT_REGION" --certificate-statuses PENDING_VALIDATION \
    --query "CertificateSummaryList[?DomainName=='$DOMAIN'].CertificateArn | [0]" --output text)"
fi
if [ "$CERT_ARN" = "None" ] || [ -z "$CERT_ARN" ]; then
  CERT_ARN="$(aws acm request-certificate --region "$CERT_REGION" \
    --domain-name "$DOMAIN" "${SAN_ARGS[@]}" \
    --validation-method DNS --query CertificateArn --output text)"
  echo "    requested: $CERT_ARN"
  sleep 8
fi
echo "    cert: $CERT_ARN"

# Find the Route 53 hosted zone for the domain
ZONE_ID="$(aws route53 list-hosted-zones-by-name --dns-name "$DOMAIN." \
  --query "HostedZones[?Name=='$DOMAIN.'].Id | [0]" --output text | sed 's#/hostedzone/##')"
[ -z "$ZONE_ID" ] || [ "$ZONE_ID" = "None" ] && { echo "ERROR: no Route 53 hosted zone for $DOMAIN"; exit 1; }
echo "    hosted zone: $ZONE_ID"

echo "==> Writing DNS validation records to Route 53"
aws acm describe-certificate --region "$CERT_REGION" --certificate-arn "$CERT_ARN" \
  --query "Certificate.DomainValidationOptions[].ResourceRecord" --output json > /tmp/_acm_dns.json
jq -c '.[]' /tmp/_acm_dns.json | sort -u | while read -r rec; do
  NAME="$(echo "$rec" | jq -r .Name)"; VALUE="$(echo "$rec" | jq -r .Value)"
  cat > /tmp/_acm_change.json <<JSON
{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{"Name":"$NAME","Type":"CNAME","TTL":300,"ResourceRecords":[{"Value":"$VALUE"}]}}]}
JSON
  aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" --change-batch file:///tmp/_acm_change.json >/dev/null
  echo "    upserted validation CNAME: $NAME"
done

echo "==> Waiting for certificate to validate (can take a few minutes)..."
aws acm wait certificate-validated --region "$CERT_REGION" --certificate-arn "$CERT_ARN"
STATUS="$(aws acm describe-certificate --region "$CERT_REGION" --certificate-arn "$CERT_ARN" \
  --query Certificate.Status --output text)"
echo "    certificate status: $STATUS"
if [ "$STATUS" != "ISSUED" ]; then
  echo "ERROR: cert $CERT_ARN is $STATUS, not ISSUED. It may live in a different account"
  echo "       than profile '$AWS_PROFILE'. Re-run once it shows ISSUED in THIS account."
  exit 1
fi

############################# 3. CloudFront OAC ##############################
echo "==> [3/6] Creating CloudFront Origin Access Control"
OAC_ID="$(aws cloudfront list-origin-access-controls \
  --query "OriginAccessControlList.Items[?Name=='${DOMAIN}-oac'].Id | [0]" --output text 2>/dev/null || true)"
if [ "$OAC_ID" = "None" ] || [ -z "$OAC_ID" ]; then
  OAC_ID="$(aws cloudfront create-origin-access-control --origin-access-control-config \
    "Name=${DOMAIN}-oac,SigningProtocol=sigv4,SigningBehavior=always,OriginAccessControlOriginType=s3" \
    --query OriginAccessControl.Id --output text)"
fi
echo "    OAC: $OAC_ID"

############################# 4. CloudFront distribution #####################
echo "==> [4/6] Creating CloudFront distribution"
S3_DOMAIN="${BUCKET}.s3.${REGION}.amazonaws.com"
CALLER_REF="$DOMAIN-$(date +%s)"
ALIAS_ITEMS="$(printf '"%s",' "${ALIASES[@]}" | sed 's/,$//')"
ALIAS_COUNT="${#ALIASES[@]}"

cat > /tmp/_cf.json <<JSON
{
  "CallerReference": "$CALLER_REF",
  "Aliases": { "Quantity": $ALIAS_COUNT, "Items": [ $ALIAS_ITEMS ] },
  "DefaultRootObject": "index.html",
  "Origins": { "Quantity": 1, "Items": [ {
    "Id": "s3-$BUCKET",
    "DomainName": "$S3_DOMAIN",
    "OriginAccessControlId": "$OAC_ID",
    "S3OriginConfig": { "OriginAccessIdentity": "" }
  } ] },
  "DefaultCacheBehavior": {
    "TargetOriginId": "s3-$BUCKET",
    "ViewerProtocolPolicy": "redirect-to-https",
    "Compress": true,
    "CachePolicyId": "658327ea-f89d-4fab-a63d-7e88639e58f6",
    "AllowedMethods": { "Quantity": 2, "Items": ["GET","HEAD"],
      "CachedMethods": { "Quantity": 2, "Items": ["GET","HEAD"] } }
  },
  "CustomErrorResponses": { "Quantity": 2, "Items": [
    { "ErrorCode": 403, "ResponseCode": "404", "ResponsePagePath": "/index.html", "ErrorCachingMinTTL": 60, "ResponsePagePathQuantity": 1 },
    { "ErrorCode": 404, "ResponseCode": "404", "ResponsePagePath": "/index.html", "ErrorCachingMinTTL": 60, "ResponsePagePathQuantity": 1 }
  ] },
  "ViewerCertificate": {
    "ACMCertificateArn": "$CERT_ARN",
    "SSLSupportMethod": "sni-only",
    "MinimumProtocolVersion": "TLSv1.2_2021"
  },
  "Comment": "anupreetwalia.com static site",
  "Enabled": true,
  "HttpVersion": "http2and3"
}
JSON
# (CustomErrorResponses Items don't take ResponsePagePathQuantity; strip if your CLI complains.)
sed -i.bak 's/, "ResponsePagePathQuantity": 1//g' /tmp/_cf.json && rm -f /tmp/_cf.json.bak

# Retry: a freshly ISSUED cert can take 1-2 min to be usable by CloudFront.
DIST_JSON=""
for attempt in 1 2 3 4 5 6; do
  if DIST_JSON="$(aws cloudfront create-distribution --distribution-config file:///tmp/_cf.json 2>/tmp/_cf_err)"; then
    break
  fi
  if grep -q InvalidViewerCertificate /tmp/_cf_err; then
    echo "    attempt $attempt: cert not yet visible to CloudFront, waiting 30s..."
    sleep 30
  else
    echo "ERROR creating distribution:"; cat /tmp/_cf_err; exit 1
  fi
  [ "$attempt" = "6" ] && { echo "ERROR: cert still not accepted by CloudFront after retries."; cat /tmp/_cf_err; exit 1; }
done
DIST_ID="$(echo "$DIST_JSON" | jq -r .Distribution.Id)"
DIST_DOMAIN="$(echo "$DIST_JSON" | jq -r .Distribution.DomainName)"
echo "    distribution: $DIST_ID  ($DIST_DOMAIN)"

############################# 5. Bucket policy for OAC #######################
echo "==> [5/6] Attaching bucket policy allowing only this CloudFront distribution"
cat > /tmp/_bucketpolicy.json <<JSON
{
  "Version": "2012-10-17",
  "Statement": [{
    "Sid": "AllowCloudFrontServicePrincipal",
    "Effect": "Allow",
    "Principal": { "Service": "cloudfront.amazonaws.com" },
    "Action": "s3:GetObject",
    "Resource": "arn:aws:s3:::$BUCKET/*",
    "Condition": { "StringEquals": {
      "AWS:SourceArn": "arn:aws:cloudfront::$ACCOUNT_ID:distribution/$DIST_ID" } }
  }]
}
JSON
aws s3api put-bucket-policy --bucket "$BUCKET" --policy file:///tmp/_bucketpolicy.json

############################# 6. Upload + Route 53 alias #####################
echo "==> [6/6] Uploading site and pointing Route 53 at CloudFront"
aws s3 sync "$SRC_DIR" "s3://$BUCKET" --delete \
  --exclude "*.sh" --exclude "build.py" --exclude "README.md" --exclude ".DS_Store" --exclude "*.bak"
aws s3 cp "s3://$BUCKET" "s3://$BUCKET" --recursive \
  --exclude "*" --include "*.html" --content-type "text/html; charset=utf-8" \
  --cache-control "max-age=300" --metadata-directive REPLACE

# CloudFront's fixed hosted zone ID for alias records is Z2FDTNDATAQYW2 (global).
CF_HOSTED_ZONE="Z2FDTNDATAQYW2"
for NAME in "${ALIASES[@]}"; do
  for TYPE in A AAAA; do
    cat > /tmp/_alias.json <<JSON
{"Changes":[{"Action":"UPSERT","ResourceRecordSet":{
  "Name":"$NAME.","Type":"$TYPE",
  "AliasTarget":{"HostedZoneId":"$CF_HOSTED_ZONE","DNSName":"$DIST_DOMAIN.","EvaluateTargetHealth":false}}}]}
JSON
    aws route53 change-resource-record-sets --hosted-zone-id "$ZONE_ID" --change-batch file:///tmp/_alias.json >/dev/null
    echo "    alias $TYPE -> $NAME"
  done
done

cat <<DONE

============================================================
 DONE. Provisioned:
   Bucket (private):  $BUCKET
   CloudFront:        $DIST_ID  ($DIST_DOMAIN)
   Certificate:       $CERT_ARN
   DNS:               https://$DOMAIN  (and www if enabled)

 CloudFront takes ~5-15 min to finish deploying the first time.
 After that: https://$DOMAIN

 To redeploy content later, edit deploy.sh and set:
   DIST_ID="$DIST_ID"
 then run ./deploy.sh
============================================================
DONE
