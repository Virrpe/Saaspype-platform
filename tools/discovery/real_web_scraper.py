#!/usr/bin/env python3
"""
REAL WEB SCRAPER - NO MOCK DATA (UPDATED WITH WORKING SOURCES)
Actually scrapes live websites for real business intelligence
Updated with working alternatives to replace failed sources
"""

import sys
import os
sys.path.append('src')

import asyncio
import aiohttp
import json
import re
from datetime import datetime
from bs4 import BeautifulSoup
from typing import List, Dict, Any
import time

class RealWebScraper:
    """Real web scraper that actually scrapes live websites"""
    
    def __init__(self):
        self.session = None
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        
        # Updated real sources with working alternatives
        self.real_sources = {
            'hacker_news': {
                'url': 'https://news.ycombinator.com/',
                'enabled': True,
                'scraper': self._scrape_hacker_news
            },
            'ycombinator_show': {
                'url': 'https://news.ycombinator.com/show',
                'enabled': True,
                'scraper': self._scrape_ycombinator_show
            },
            'indie_hackers': {
                'url': 'https://www.indiehackers.com/',
                'enabled': True,
                'scraper': self._scrape_indie_hackers
            },
            'github_trending': {
                'url': 'https://github.com/trending',
                'enabled': True,
                'scraper': self._scrape_github_trending
            },
            'dev_to': {
                'url': 'https://dev.to/',
                'enabled': True,
                'scraper': self._scrape_dev_to
            },
            'medium_startup': {
                'url': 'https://medium.com/tag/startup',
                'enabled': True,
                'scraper': self._scrape_medium_startup
            },
            'reddit_entrepreneur': {
                'url': 'https://www.reddit.com/r/entrepreneur.json',
                'enabled': True,
                'scraper': self._scrape_reddit_json
            },
            'launching_next': {
                'url': 'https://www.launchingnext.com/',
                'enabled': True,
                'scraper': self._scrape_launching_next
            },
            'maker_log': {
                'url': 'https://getmakerlog.com/',
                'enabled': True,
                'scraper': self._scrape_maker_log
            }
        }
    
    async def _get_session(self):
        """Get or create aiohttp session"""
        if self.session is None:
            connector = aiohttp.TCPConnector(limit=10, limit_per_host=5)
            timeout = aiohttp.ClientTimeout(total=30, connect=10)
            self.session = aiohttp.ClientSession(
                connector=connector,
                timeout=timeout,
                headers=self.headers
            )
        return self.session
    
    async def scrape_all_real_sources(self) -> Dict[str, Any]:
        """Scrape all real sources for actual business intelligence"""
        
        print("🔥 REAL WEB SCRAPER - NO MOCK DATA (UPDATED)")
        print("=" * 70)
        print("🎯 Scraping LIVE websites for REAL business intelligence")
        print("✅ Updated with working alternatives to failed sources")
        print()
        
        start_time = datetime.now()
        all_results = {}
        total_items = 0
        
        session = await self._get_session()
        
        for source_name, config in self.real_sources.items():
            if not config['enabled']:
                continue
                
            print(f"🔍 Scraping {source_name}...")
            print(f"   📍 URL: {config['url']}")
            
            try:
                start_source = time.time()
                results = await config['scraper'](session, config['url'])
                duration = time.time() - start_source
                
                all_results[source_name] = results
                total_items += len(results)
                
                print(f"   ✅ Success: {len(results)} items in {duration:.1f}s")
                
                # Show sample results
                if results:
                    sample = results[0]
                    title = sample.get('title', 'No title')[:50]
                    print(f"   📝 Sample: {title}...")
                
                # Rate limiting
                await asyncio.sleep(1)
                
            except Exception as e:
                print(f"   ❌ Failed: {str(e)}")
                all_results[source_name] = []
        
        duration = (datetime.now() - start_time).total_seconds()
        
        # Analysis
        print(f"\n🎉 REAL SCRAPING COMPLETE!")
        print("=" * 50)
        print(f"⏱️ Total Duration: {duration:.1f} seconds")
        print(f"🔍 Sources Scraped: {len([s for s in self.real_sources.values() if s['enabled']])}")
        print(f"📊 Total Items: {total_items}")
        print(f"🚀 Items per Second: {total_items/duration:.1f}")
        
        # Show results by source
        print(f"\n📊 RESULTS BY SOURCE:")
        for source_name, results in all_results.items():
            print(f"   🎯 {source_name}: {len(results)} items")
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"real_web_scraping_updated_{timestamp}.json"
        
        output = {
            'timestamp': timestamp,
            'duration_seconds': duration,
            'total_items': total_items,
            'sources_scraped': len(all_results),
            'results': all_results,
            'summary': {
                'successful_sources': len([r for r in all_results.values() if r]),
                'failed_sources': len([r for r in all_results.values() if not r]),
                'average_items_per_source': total_items / len(all_results) if all_results else 0
            }
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"💾 Results saved to: {results_file}")
        
        return output
    
    async def _scrape_hacker_news(self, session, url: str) -> List[Dict]:
        """Scrape real Hacker News stories"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Find story rows
                    story_rows = soup.find_all('tr', class_='athing')
                    
                    for row in story_rows[:10]:  # Top 10 stories
                        try:
                            title_cell = row.find('span', class_='titleline')
                            if title_cell:
                                title_link = title_cell.find('a')
                                if title_link:
                                    title = title_link.get_text(strip=True)
                                    link = title_link.get('href', '')
                                    
                                    # Get score from next row
                                    next_row = row.find_next_sibling('tr')
                                    score = 0
                                    if next_row:
                                        score_span = next_row.find('span', class_='score')
                                        if score_span:
                                            score_text = score_span.get_text()
                                            score = int(re.findall(r'\d+', score_text)[0]) if re.findall(r'\d+', score_text) else 0
                                    
                                    results.append({
                                        'title': title,
                                        'url': link,
                                        'score': score,
                                        'source': 'hacker_news',
                                        'scraped_at': datetime.now().isoformat()
                                    })
                        except Exception as e:
                            continue
                            
        except Exception as e:
            print(f"   ⚠️ Hacker News error: {e}")
        
        return results
    
    async def _scrape_ycombinator_show(self, session, url: str) -> List[Dict]:
        """Scrape Y Combinator Show HN for projects"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for Show HN posts
                    story_rows = soup.find_all('tr', class_='athing')
                    
                    for row in story_rows[:8]:  # Top 8 Show HN posts
                        try:
                            title_cell = row.find('span', class_='titleline')
                            if title_cell:
                                title_link = title_cell.find('a')
                                if title_link:
                                    title = title_link.get_text(strip=True)
                                    link = title_link.get('href', '')
                                    
                                    # Only include "Show HN" posts
                                    if title.startswith('Show HN:'):
                                        # Clean up title
                                        clean_title = title.replace('Show HN:', '').strip()
                                        
                                        results.append({
                                            'title': clean_title,
                                            'url': link,
                                            'source': 'ycombinator_show',
                                            'scraped_at': datetime.now().isoformat()
                                        })
                        except Exception as e:
                            continue
                    
        except Exception as e:
            print(f"   ⚠️ Y Combinator Show error: {e}")
        
        return results
    
    async def _scrape_launching_next(self, session, url: str) -> List[Dict]:
        """Scrape Launching Next for upcoming products"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for product listings
                    product_elements = soup.find_all(['h1', 'h2', 'h3', 'h4'])
                    
                    seen_titles = set()
                    for elem in product_elements:
                        title = elem.get_text(strip=True)
                        
                        if (title and 
                            len(title) > 5 and 
                            len(title) < 80 and
                            title not in seen_titles and
                            not any(skip in title.lower() for skip in ['new startups', 'newest startups', 'side projects'])):
                            
                            seen_titles.add(title)
                            
                            # Try to find associated link
                            link = elem.find('a') or elem.find_parent('a')
                            href = link.get('href', url) if link else url
                            
                            if href.startswith('/'):
                                href = f"https://www.launchingnext.com{href}"
                            
                            results.append({
                                'title': title,
                                'url': href,
                                'source': 'launching_next',
                                'scraped_at': datetime.now().isoformat()
                            })
                            
                            if len(results) >= 6:
                                break
                    
        except Exception as e:
            print(f"   ⚠️ Launching Next error: {e}")
        
        return results
    
    async def _scrape_maker_log(self, session, url: str) -> List[Dict]:
        """Scrape Maker Log for maker projects"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for maker projects
                    project_elements = soup.find_all(['h1', 'h2', 'h3', 'a'])
                    
                    seen_titles = set()
                    for elem in project_elements:
                        title = elem.get_text(strip=True)
                        
                        if (title and 
                            len(title) > 5 and 
                            len(title) < 60 and
                            title not in seen_titles and
                            not any(skip in title.lower() for skip in ['login', 'signup', 'about', 'contact', 'privacy', 'terms'])):
                            
                            seen_titles.add(title)
                            
                            # Get link if available
                            if elem.name == 'a':
                                href = elem.get('href', url)
                            else:
                                link = elem.find('a') or elem.find_parent('a')
                                href = link.get('href', url) if link else url
                            
                            if href.startswith('/'):
                                href = f"https://getmakerlog.com{href}"
                            
                            results.append({
                                'title': title,
                                'url': href,
                                'source': 'maker_log',
                                'scraped_at': datetime.now().isoformat()
                            })
                            
                            if len(results) >= 5:
                                break
                    
        except Exception as e:
            print(f"   ⚠️ Maker Log error: {e}")
        
        return results
    
    async def _scrape_indie_hackers(self, session, url: str) -> List[Dict]:
        """Scrape real Indie Hackers posts"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for post titles and links
                    post_links = soup.find_all('a', href=re.compile(r'/post/'))
                    
                    seen_titles = set()
                    for link in post_links[:10]:  # Top 10 posts
                        try:
                            title = link.get_text(strip=True)
                            if title and title not in seen_titles and len(title) > 10:
                                seen_titles.add(title)
                                href = link.get('href', '')
                                
                                results.append({
                                    'title': title,
                                    'url': f"https://www.indiehackers.com{href}" if href.startswith('/') else href,
                                    'source': 'indie_hackers',
                                    'scraped_at': datetime.now().isoformat()
                                })
                        except Exception as e:
                            continue
                            
        except Exception as e:
            print(f"   ⚠️ Indie Hackers error: {e}")
        
        return results
    
    async def _scrape_github_trending(self, session, url: str) -> List[Dict]:
        """Scrape real GitHub trending repositories"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for repository links
                    repo_links = soup.find_all('h2', class_='h3')
                    
                    for repo_header in repo_links[:10]:  # Top 10 repos
                        try:
                            link = repo_header.find('a')
                            if link:
                                title = link.get_text(strip=True)
                                href = link.get('href', '')
                                
                                # Get description
                                description = ""
                                desc_elem = repo_header.find_next('p')
                                if desc_elem:
                                    description = desc_elem.get_text(strip=True)
                                
                                results.append({
                                    'title': title,
                                    'description': description,
                                    'url': f"https://github.com{href}" if href.startswith('/') else href,
                                    'source': 'github_trending',
                                    'scraped_at': datetime.now().isoformat()
                                })
                        except Exception as e:
                            continue
                            
        except Exception as e:
            print(f"   ⚠️ GitHub Trending error: {e}")
        
        return results
    
    async def _scrape_dev_to(self, session, url: str) -> List[Dict]:
        """Scrape real Dev.to articles"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for article links
                    article_links = soup.find_all('a', class_=re.compile(r'crayons-story__hidden-navigation-link'))
                    
                    seen_titles = set()
                    for link in article_links[:8]:  # Top 8 articles
                        try:
                            # Get title from the link or nearby elements
                            title_elem = link.find_next('h3') or link.find_next('h2') or link.find_next('h1')
                            if title_elem:
                                title = title_elem.get_text(strip=True)
                                if title and title not in seen_titles and len(title) > 10:
                                    seen_titles.add(title)
                                    href = link.get('href', '')
                                    
                                    results.append({
                                        'title': title,
                                        'url': f"https://dev.to{href}" if href.startswith('/') else href,
                                        'source': 'dev_to',
                                        'scraped_at': datetime.now().isoformat()
                                    })
                        except Exception as e:
                            continue
                            
        except Exception as e:
            print(f"   ⚠️ Dev.to error: {e}")
        
        return results
    
    async def _scrape_medium_startup(self, session, url: str) -> List[Dict]:
        """Scrape real Medium startup articles"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for article titles
                    article_links = soup.find_all('a', href=re.compile(r'/@'))
                    
                    seen_titles = set()
                    for link in article_links[:8]:  # Top 8 articles
                        try:
                            title = link.get_text(strip=True)
                            if title and title not in seen_titles and len(title) > 15:
                                seen_titles.add(title)
                                href = link.get('href', '')
                                
                                results.append({
                                    'title': title,
                                    'url': href,
                                    'source': 'medium_startup',
                                    'scraped_at': datetime.now().isoformat()
                                })
                        except Exception as e:
                            continue
                            
        except Exception as e:
            print(f"   ⚠️ Medium error: {e}")
        
        return results
    
    async def _scrape_reddit_json(self, session, url: str) -> List[Dict]:
        """Scrape real Reddit JSON API"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    posts = data.get('data', {}).get('children', [])
                    
                    for post in posts[:10]:  # Top 10 posts
                        try:
                            post_data = post.get('data', {})
                            title = post_data.get('title', '')
                            score = post_data.get('score', 0)
                            url = post_data.get('url', '')
                            
                            if title:
                                results.append({
                                    'title': title,
                                    'score': score,
                                    'url': url,
                                    'source': 'reddit_entrepreneur',
                                    'scraped_at': datetime.now().isoformat()
                                })
                        except Exception as e:
                            continue
                            
        except Exception as e:
            print(f"   ⚠️ Reddit JSON error: {e}")
        
        return results
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()

async def main():
    """Run the updated real web scraper"""
    scraper = RealWebScraper()
    
    try:
        results = await scraper.scrape_all_real_sources()
        
        print(f"\n🎯 UPDATED REAL SCRAPING SUMMARY:")
        print(f"   📊 Total Items: {results['total_items']}")
        print(f"   ⏱️ Duration: {results['duration_seconds']:.1f}s")
        print(f"   🚀 Items/Second: {results['total_items']/results['duration_seconds']:.1f}")
        print(f"   ✅ Successful Sources: {results['summary']['successful_sources']}")
        print(f"   ❌ Failed Sources: {results['summary']['failed_sources']}")
        
        # Show sample real data
        print(f"\n📝 SAMPLE REAL DATA:")
        for source_name, items in results['results'].items():
            if items:
                sample = items[0]
                title = sample.get('title', 'No title')[:60]
                print(f"   🎯 {source_name}: {title}...")
        
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main()) 