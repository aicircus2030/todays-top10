name: 📰 Auto Update News

on:
  schedule:
    - cron: '0 3 * * *'  # 每天 UTC 3 点（北京时间 11 点）
  workflow_dispatch:      # 允许手动运行

jobs:
  update-news:
    runs-on: ubuntu-latest

    steps:
      - name: 🔁 Checkout repo
        uses: actions/checkout@v3

      - name: 🐍 Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: 3.x

      - name: 📦 Install dependencies
        run: pip install requests beautifulsoup4 openai

      - name: 📰 Run news update script
        run: python newsbot/update.py

      - name: ✅ Commit and push changes
        run: |
          git config --global user.name "news-bot"
          git config --global user.email "bot@example.com"
          git add news.json summary.json
          git commit -m "🔁 Update daily news" || echo "No changes to commit"
          git push
