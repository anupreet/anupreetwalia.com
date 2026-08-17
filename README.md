# anupreetwalia.com

Static personal site — technical work, writing, research, and patents in one place.
No build step required to view: every page is plain HTML + one CSS file.

## Structure

```
site/
├── index.html              Home (bio, work timeline, highlights, external links)
├── research.html           BatchDAG paper page (abstract + PDF)
├── patents.html            Patents listing
├── writing/
│   ├── index.html          Blog index
│   └── *.html              Individual reposted Brevian posts
├── assets/
│   ├── styles.css          All styling
│   ├── BatchDAG_Walia.pdf  The paper
│   └── Anupreet_Walia_Resume_2026.docx
├── build.py                Generator (regenerates HTML from content; needs `pip install markdown`)
└── deploy.sh               One-command deploy to S3 + CloudFront
```

To preview locally: `cd site && python3 -m http.server` → open http://localhost:8000

## Deploying to anupreetwalia.com (S3 + CloudFront + Route 53)

You already own the domain in Route 53. Run this **on your own machine** (it needs
your AWS credentials — it cannot be run from the assistant's sandbox).

### One command: `provision_aws.sh`

```
brew install jq                 # if you don't have it
aws configure                   # if not already set up (needs S3, CloudFront, ACM, Route 53 perms)
chmod +x provision_aws.sh
./provision_aws.sh
```

This provisions the whole stack the **secure** way and requires no clicking in the console:

- Creates a **private** S3 bucket with **all public access blocked**. The bucket is
  never exposed to the internet.
- Creates a CloudFront distribution using **Origin Access Control (OAC)** — only
  CloudFront can read the bucket, and it serves everything over **HTTPS**
  (`redirect-to-https`, TLS 1.2+).
- Requests an **ACM certificate** (us-east-1), and auto-validates it by writing the
  DNS records into your Route 53 hosted zone.
- Points the apex domain (and `www`) at CloudFront via Route 53 **A/AAAA alias** records.
- Uploads the site.

CloudFront takes ~5–15 min to finish deploying the first time. The script prints the
distribution ID at the end.

### Redeploying content later

After provisioning once, put the printed `DIST_ID` into `deploy.sh` and run `./deploy.sh`
to sync new files and invalidate the CloudFront cache.

### Why not just a public S3 website bucket?

A public website bucket works but exposes the bucket directly and serves over plain
HTTP. The OAC + CloudFront setup above keeps the bucket private, adds HTTPS, and is the
current AWS-recommended pattern — which is what avoids the "security issues" you
mentioned.

## Editing content

Content lives in `build.py` (posts as Markdown, roles/patents as Python lists). Edit there and run:

```
pip install markdown
python3 build.py
```

…to regenerate all HTML, then redeploy.
