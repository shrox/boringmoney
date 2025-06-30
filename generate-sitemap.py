#!/usr/bin/env python3
"""
Generate news sitemap for boringmoney.in Substack
"""

import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import json
import re
import os

def fetch_substack_posts():
    """Fetch posts from Substack RSS feed using requests and manual parsing"""
    rss_url = "https://boringmoney.substack.com/feed"
    
    try:
        response = requests.get(rss_url, timeout=30)
        response.raise_for_status()
        
        # Parse RSS XML manually
        import xml.etree.ElementTree as ET
        root = ET.fromstring(response.content)
        
        posts = []
        
        # Find all item elements
        for item in root.findall('.//item'):
            post = {}
            
            # Extract title
            title_elem = item.find('title')
            post['title'] = title_elem.text if title_elem is not None else "No Title"
            
            # Extract link
            link_elem = item.find('link')
            post['link'] = link_elem.text if link_elem is not None else ""
            
            # Extract publication date
            pub_date_elem = item.find('pubDate')
            if pub_date_elem is not None:
                # Parse RFC 2822 date format to datetime
                from email.utils import parsedate_to_datetime
                try:
                    post['published_parsed'] = parsedate_to_datetime(pub_date_elem.text).timetuple()
                except:
                    post['published_parsed'] = datetime.now().timetuple()
            else:
                post['published_parsed'] = datetime.now().timetuple()
            
            posts.append(post)
        
        return posts
        
    except Exception as e:
        print(f"Error fetching RSS feed: {e}")
        return []

def generate_news_sitemap():
    """Generate Google News sitemap XML"""
    posts = fetch_substack_posts()
    
    if not posts:
        print("No posts found, creating empty sitemap")
        posts = []
    
    # Create the root element
    root = ET.Element("urlset")
    root.set("xmlns", "http://www.sitemaps.org/schemas/sitemap/0.9")
    root.set("xmlns:news", "http://www.google.com/schemas/sitemap-news/0.9")
    
    # Add each post to the sitemap
    for post in posts:
        url_elem = ET.SubElement(root, "url")
        
        # Location
        loc_elem = ET.SubElement(url_elem, "loc")
        loc_elem.text = post['link']
        
        # News element
        news_elem = ET.SubElement(url_elem, "news:news")
        
        # Publication
        publication_elem = ET.SubElement(news_elem, "news:publication")
        name_elem = ET.SubElement(publication_elem, "news:name")
        name_elem.text = "Boring Money"
        language_elem = ET.SubElement(publication_elem, "news:language")
        language_elem.text = "en"
        
        # Publication date
        pub_date_elem = ET.SubElement(news_elem, "news:publication_date")
        
        # Parse the published date and format it for Google News
        try:
            # Use the parsed date from our manual parsing
            pub_date = datetime(*post['published_parsed'][:6])
            pub_date_elem.text = pub_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        except:
            # Fallback to current time if parsing fails
            pub_date_elem.text = datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")
        
        # Title
        title_elem = ET.SubElement(news_elem, "news:title")
        title_elem.text = post['title']
    
    # Create the XML tree and write to file
    tree = ET.ElementTree(root)
    ET.indent(tree, space="  ", level=0)
    
    with open("news-sitemap.xml", "wb") as f:
        tree.write(f, encoding="utf-8", xml_declaration=True)
    
    print(f"Generated news sitemap with {len(posts)} articles")

if __name__ == "__main__":
    generate_news_sitemap() 