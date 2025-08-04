#!/bin/bash
# GitHub Secrets一括設定スクリプト

echo "=== GitHub Secrets Setup Script ==="
echo "This script helps you set multiple GitHub secrets at once."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "Error: GitHub CLI (gh) is not installed."
    echo "Please install it from: https://cli.github.com/"
    exit 1
fi

# Check if authenticated
if ! gh auth status &> /dev/null; then
    echo "Error: Not authenticated with GitHub CLI."
    echo "Please run: gh auth login"
    exit 1
fi

# Create template file if it doesn't exist
if [ ! -f ".env.secrets.template" ]; then
    cat > .env.secrets.template << 'EOF'
# GitHub Secrets Template
# Copy this file to .env.secrets and fill in your actual values
# DO NOT commit .env.secrets to version control!

# OpenAI
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# YouTube
YOUTUBE_API_KEY=AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Slack
SLACK_BOT_TOKEN=xoxb-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SLACK_SIGNING_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Twitter/X
TWITTER_BEARER_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWITTER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWITTER_API_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Google Services
GOOGLE_SHEETS_CREDENTIALS={"type":"service_account","project_id":"xxx"}
GOOGLE_NEWS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# News & Weather
NEWSAPI_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WEATHER_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Financial
FINNHUB_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# GitHub (for API operations)
GITHUB_TOKEN=ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# AI/ML Services
ELEVENLABS_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
HUGGINGFACE_API_KEY=hf_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Communication
DISCORD_BOT_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TELEGRAM_BOT_TOKEN=xxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Productivity
NOTION_API_KEY=secret_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Payment
STRIPE_SECRET_KEY=sk_test_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Email
SENDGRID_API_KEY=SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

# Reddit
REDDIT_CLIENT_ID=xxxxxxxxxxxxxxxx
REDDIT_CLIENT_SECRET=xxxxxxxxxxxxxxxxxxxxxxxx
EOF
    echo "Created .env.secrets.template"
fi

# Check if .env.secrets exists
if [ ! -f ".env.secrets" ]; then
    echo ""
    echo "Please copy .env.secrets.template to .env.secrets and fill in your API keys:"
    echo "  cp .env.secrets.template .env.secrets"
    echo "  Then edit .env.secrets with your actual API keys"
    exit 1
fi

# Add to .gitignore
if ! grep -q "^\.env\.secrets$" .gitignore 2>/dev/null; then
    echo ".env.secrets" >> .gitignore
    echo "Added .env.secrets to .gitignore"
fi

# Confirm before proceeding
echo ""
echo "This will set GitHub secrets for the current repository."
echo "Repository: $(gh repo view --json nameWithOwner -q .nameWithOwner)"
echo ""
read -p "Continue? (y/N) " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Cancelled."
    exit 0
fi

# Set secrets from .env.secrets
echo ""
echo "Setting secrets..."

SUCCESS_COUNT=0
SKIP_COUNT=0
ERROR_COUNT=0

while IFS='=' read -r key value; do
    # Skip comments and empty lines
    if [[ "$key" =~ ^#.*$ ]] || [ -z "$key" ]; then
        continue
    fi
    
    # Skip template values
    if [[ "$value" =~ ^(xxx|sk-xxx|AIzaxxx|xoxb-xxx|hf_xxx|ghp_xxx|SG\.xxx|secret_xxx).*$ ]]; then
        echo "⚠️  Skipping $key (template value not updated)"
        ((SKIP_COUNT++))
        continue
    fi
    
    # Set the secret
    if gh secret set "$key" -b "$value" 2>/dev/null; then
        echo "✓ Set $key"
        ((SUCCESS_COUNT++))
    else
        echo "✗ Failed to set $key"
        ((ERROR_COUNT++))
    fi
done < .env.secrets

# Summary
echo ""
echo "=== Summary ==="
echo "✓ Successfully set: $SUCCESS_COUNT secrets"
echo "⚠️  Skipped (template): $SKIP_COUNT secrets"
echo "✗ Failed: $ERROR_COUNT secrets"

# List current secrets
echo ""
echo "=== Current GitHub Secrets ==="
gh secret list

echo ""
echo "Done! Remember to delete .env.secrets if you no longer need it."
echo "IMPORTANT: Never commit .env.secrets to version control!"