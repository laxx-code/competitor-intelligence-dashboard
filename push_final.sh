#!/bin/bash

echo "🚀 Pushing to GitHub"
echo "===================="

# Remove existing remote
echo "Removing existing remote..."
git remote remove origin 2>/dev/null

# Add correct remote
echo "Adding remote: https://github.com/teamworklax-maker/competitor-intelligence-dashboard.git"
git remote add origin https://github.com/teamworklax-maker/competitor-intelligence-dashboard.git

# Verify remote
echo ""
echo "✅ Remote set to:"
git remote -v

# Add files
echo ""
echo "📁 Adding files..."
git add .

# Commit
echo ""
echo "📝 Committing..."
git commit -m "Initial commit: Competitor Intelligence Dashboard

- Multi-agent system (Scraper, Cleaner, Analyzer, Comparison agents)
- Company discovery with DuckDuckGo
- Competitor comparison (V2)
- PostgreSQL database integration
- Professional React dashboard with 15+ sections
- All FREE and open-source tools"

# Push
echo ""
echo "🚀 Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Successfully pushed to GitHub!"
echo "📊 Repository: https://github.com/teamworklax-maker/competitor-intelligence-dashboard"
