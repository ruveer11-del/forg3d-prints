#!/bin/bash
# Simple Prints - Auto Deploy Script
# Just run this file to update the website!

cd "$(dirname "$0")"

echo "🚀 Deploying to Netlify..."
echo ""

# Add all files
git add .

# Commit with timestamp
git commit -m "Update $(date '+%Y-%m-%d %H:%M')"

# Push to GitHub
git push origin main

echo ""
echo "✅ Deployed! Check https://simpleprints.netlify.app in ~30 seconds"
echo ""
echo "Press any key to close..."
read