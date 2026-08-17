#!/usr/bin/env bash
###############################################################################
# verify_gsc.sh
# Adds the Google Search Console DNS TXT verification record to Route 53 for
# anupreetwalia.com, merging with any existing apex TXT records (so nothing
# already there gets clobbered). Idempotent: safe to run more than once.
###############################################################################
set -euo pipefail

export AWS_PROFILE="personal"
DOMAIN="anupreetwalia.com"
TOKEN="google-site-verification=2LDBzJoF4lu5rRbzuyqBlKiaf1zqJyqzzK6J66pALPM"

command -v aws >/dev/null || { echo "ERROR: aws CLI not found."; exit 1; }
command -v jq  >/dev/null || { echo "ERROR: jq not found (brew install jq)."; exit 1; }

ZONE="$(aws route53 list-hosted-zones-by-name --dns-name "${DOMAIN}." \
  --query "HostedZones[?Name=='${DOMAIN}.'].Id | [0]" --output text | sed 's#/hostedzone/##')"
[ -z "$ZONE" ] || [ "$ZONE" = "None" ] && { echo "ERROR: no Route 53 hosted zone for ${DOMAIN}"; exit 1; }
echo "==> Hosted zone: $ZONE"

# Existing apex TXT records (array of {Value:...}); defaults to [] if none.
EXIST="$(aws route53 list-resource-record-sets --hosted-zone-id "$ZONE" \
  --query "ResourceRecordSets[?Name=='${DOMAIN}.' && Type=='TXT'].ResourceRecords[]" --output json)"
[ -z "$EXIST" ] && EXIST="[]"

jq -n --argjson exist "$EXIST" --arg tok "\"$TOKEN\"" \
  '{Changes:[{Action:"UPSERT",ResourceRecordSet:{
     Name:"'"$DOMAIN"'.",Type:"TXT",TTL:300,
     ResourceRecords:(($exist // []) + [{"Value":$tok}] | unique)}}]}' > /tmp/gsc-txt.json

echo "==> Applying TXT record..."
aws route53 change-resource-record-sets --hosted-zone-id "$ZONE" --change-batch file:///tmp/gsc-txt.json >/dev/null

echo "==> Done. Current apex TXT values:"
aws route53 list-resource-record-sets --hosted-zone-id "$ZONE" \
  --query "ResourceRecordSets[?Name=='${DOMAIN}.' && Type=='TXT'].ResourceRecords[].Value" --output text

cat <<NOTE

Next:
  1. Wait ~2-5 min for DNS to propagate. Check with:  dig +short TXT ${DOMAIN}
  2. Click "Verify" in Google Search Console.
NOTE
