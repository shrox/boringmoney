# Boring Money - News Sitemap

This repository automatically generates and hosts a Google News sitemap for [boringmoney.in](https://boringmoney.in) using GitHub Pages.

## How it works

1. **Automatic Generation**: Every time code is pushed to the `main` branch, GitHub Actions runs a Python script that fetches the latest articles from the Substack RSS feed.

2. **Google News Format**: The script generates a properly formatted `news-sitemap.xml` file that follows Google News sitemap standards.

3. **GitHub Pages Hosting**: The sitemap is hosted at `boringmoney.in/news-sitemap.xml` via GitHub Pages.

## Files

- `generate-sitemap.py` - Python script that fetches RSS feed and generates the sitemap
- `requirements.txt` - Python dependencies
- `.github/workflows/static.yml` - GitHub Actions workflow for automatic deployment
- `index.html` - Simple landing page for the sitemap
- `news-sitemap.xml` - Auto-generated news sitemap (created by the workflow)

## Setup

The sitemap is automatically updated whenever:
- New commits are pushed to the `main` branch
- The workflow can be manually triggered from the GitHub Actions tab

## DNS Configuration

To make this available at `boringmoney.in/news-sitemap.xml`, you'll need to configure your DNS to point to GitHub Pages. This typically involves setting up a CNAME record or configuring your web server to proxy requests to GitHub Pages.

## Manual Updates

You can manually trigger a sitemap update by going to the "Actions" tab in this GitHub repository and running the "Deploy static content to Pages" workflow. 