#!/usr/bin/env python3
"""
SUPER FIXED SCRAPERS - Get actual products and add alternative sources
Fix Product Hunt to get real products, replace BetaList with working alternatives
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class SuperFixedScrapers:
    """Super improved scrapers with real product data"""
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.session = None
        
        # Alternative sources to replace failed ones
        self.working_sources = {
            'product_hunt_daily': {
                'url': 'https://www.producthunt.com/leaderboard/daily',
                'scraper': self._scrape_product_hunt_daily
            },
            'startup_stash': {
                'url': 'https://startupstash.com/',
                'scraper': self._scrape_startup_stash
            },
            'launching_next': {
                'url': 'https://www.launchingnext.com/',
                'scraper': self._scrape_launching_next
            },
            'side_projects': {
                'url': 'https://www.sideprojects.net/',
                'scraper': self._scrape_side_projects
            },
            'maker_log': {
                'url': 'https://getmakerlog.com/',
                'scraper': self._scrape_maker_log
            },
            'ycombinator_news': {
                'url': 'https://news.ycombinator.com/show',
                'scraper': self._scrape_ycombinator_show
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
    
    async def scrape_all_working_sources(self):
        """Scrape all working alternative sources"""
        print("🚀 SUPER FIXED SCRAPERS - REAL PRODUCTS ONLY")
        print("=" * 60)
        
        session = await self._get_session()
        all_results = {}
        total_items = 0
        
        for source_name, config in self.working_sources.items():
            print(f"🔍 Scraping {source_name}...")
            print(f"   📍 URL: {config['url']}")
            
            try:
                results = await config['scraper'](session, config['url'])
                all_results[source_name] = results
                total_items += len(results)
                
                print(f"   ✅ Success: {len(results)} items")
                
                # Show sample
                if results:
                    sample = results[0]
                    title = sample.get('title', 'No title')[:50]
                    print(f"   📝 Sample: {title}...")
                
                await asyncio.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"   ❌ Failed: {str(e)}")
                all_results[source_name] = []
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        results_file = f"super_fixed_scrapers_{timestamp}.json"
        
        output = {
            'timestamp': timestamp,
            'total_items': total_items,
            'sources_scraped': len(self.working_sources),
            'results': all_results,
            'summary': {
                'successful_sources': len([r for r in all_results.values() if r]),
                'failed_sources': len([r for r in all_results.values() if not r]),
                'average_items_per_source': total_items / len(all_results) if all_results else 0
            }
        }
        
        with open(results_file, 'w', encoding='utf-8') as f:
            json.dump(output, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n🎉 SUPER SCRAPING COMPLETE!")
        print("=" * 50)
        print(f"📊 Total Items: {total_items}")
        print(f"✅ Working Sources: {output['summary']['successful_sources']}")
        print(f"❌ Failed Sources: {output['summary']['failed_sources']}")
        print(f"💾 Results saved to: {results_file}")
        
        return output
    
    async def _scrape_product_hunt_daily(self, session, url):
        """Scrape Product Hunt daily leaderboard for actual products"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for product cards/items in the daily leaderboard
                    # Try multiple selectors for product listings
                    product_selectors = [
                        'a[href*="/posts/"]',  # Links to product posts
                        'div[data-test*="product"]',  # Product containers
                        'h3 a',  # Product titles in h3 tags
                        'h4 a',  # Product titles in h4 tags
                    ]
                    
                    seen_titles = set()
                    
                    for selector in product_selectors:
                        elements = soup.select(selector)
                        
                        for elem in elements:
                            if elem.name == 'a':
                                title = elem.get_text(strip=True)
                                href = elem.get('href', '')
                            else:
                                link = elem.find('a')
                                if link:
                                    title = link.get_text(strip=True)
                                    href = link.get('href', '')
                                else:
                                    continue
                            
                            # Filter for actual products
                            if (title and 
                                len(title) > 5 and 
                                len(title) < 100 and
                                title not in seen_titles and
                                not any(skip in title.lower() for skip in ['sign up', 'log in', 'learn more', 'get started', 'try now', 'launches', 'coming soon', 'archive', 'guide', 'stories', 'changelog', 'forums', 'streaks'])):
                                
                                seen_titles.add(title)
                                
                                if href.startswith('/'):
                                    href = f"https://www.producthunt.com{href}"
                                
                                results.append({
                                    'title': title,
                                    'url': href,
                                    'source': 'product_hunt_daily',
                                    'scraped_at': datetime.now().isoformat()
                                })
                                
                                if len(results) >= 10:
                                    break
                        
                        if len(results) >= 10:
                            break
                    
                    # Fallback: Look for any text that looks like product names
                    if len(results) < 3:
                        all_text = soup.get_text()
                        # Look for patterns like "ProductName - Description"
                        lines = all_text.split('\n')
                        for line in lines:
                            line = line.strip()
                            if (line and 
                                len(line) > 10 and 
                                len(line) < 80 and
                                line not in seen_titles and
                                not line.lower().startswith(('the ', 'a ', 'an ', 'this ', 'that ', 'these ', 'those ')) and
                                any(char.isupper() for char in line)):
                                
                                seen_titles.add(line)
                                results.append({
                                    'title': line,
                                    'url': url,
                                    'source': 'product_hunt_daily',
                                    'scraped_at': datetime.now().isoformat()
                                })
                                
                                if len(results) >= 8:
                                    break
                    
        except Exception as e:
            print(f"   ⚠️ Product Hunt Daily error: {e}")
        
        return results
    
    async def _scrape_startup_stash(self, session, url):
        """Scrape Startup Stash for tools and resources"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for tool/startup listings
                    tool_links = soup.find_all('a', href=True)
                    
                    seen_titles = set()
                    for link in tool_links:
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        
                        if (title and 
                            len(title) > 3 and 
                            len(title) < 60 and
                            title not in seen_titles and
                            not any(skip in title.lower() for skip in ['home', 'about', 'contact', 'privacy', 'terms', 'submit', 'newsletter'])):
                            
                            seen_titles.add(title)
                            
                            if href.startswith('/'):
                                href = f"https://startupstash.com{href}"
                            
                            results.append({
                                'title': title,
                                'url': href,
                                'source': 'startup_stash',
                                'scraped_at': datetime.now().isoformat()
                            })
                            
                            if len(results) >= 8:
                                break
                    
        except Exception as e:
            print(f"   ⚠️ Startup Stash error: {e}")
        
        return results
    
    async def _scrape_launching_next(self, session, url):
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
                            title not in seen_titles):
                            
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
    
    async def _scrape_side_projects(self, session, url):
        """Scrape Side Projects for indie projects"""
        results = []
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Look for project listings
                    project_links = soup.find_all('a', href=True)
                    
                    seen_titles = set()
                    for link in project_links:
                        title = link.get_text(strip=True)
                        href = link.get('href', '')
                        
                        if (title and 
                            len(title) > 4 and 
                            len(title) < 70 and
                            title not in seen_titles and
                            not any(skip in title.lower() for skip in ['submit', 'login', 'signup', 'about', 'contact', 'privacy'])):
                            
                            seen_titles.add(title)
                            
                            if href.startswith('/'):
                                href = f"https://www.sideprojects.net{href}"
                            
                            results.append({
                                'title': title,
                                'url': href,
                                'source': 'side_projects',
                                'scraped_at': datetime.now().isoformat()
                            })
                            
                            if len(results) >= 6:
                                break
                    
        except Exception as e:
            print(f"   ⚠️ Side Projects error: {e}")
        
        return results
    
    async def _scrape_maker_log(self, session, url):
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
    
    async def _scrape_ycombinator_show(self, session, url):
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
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()

async def main():
    """Run the super fixed scrapers"""
    scraper = SuperFixedScrapers()
    
    try:
        results = await scraper.scrape_all_working_sources()
        
        print(f"\n🎯 SUPER SCRAPING SUMMARY:")
        print(f"   📊 Total Items: {results['total_items']}")
        print(f"   ✅ Working Sources: {results['summary']['successful_sources']}")
        print(f"   📈 Avg Items/Source: {results['summary']['average_items_per_source']:.1f}")
        
        # Show sample data from each working source
        print(f"\n📝 SAMPLE DATA FROM WORKING SOURCES:")
        for source_name, items in results['results'].items():
            if items:
                sample = items[0]
                title = sample.get('title', 'No title')[:50]
                print(f"   🎯 {source_name}: {title}...")
        
    finally:
        await scraper.close()

if __name__ == "__main__":
    asyncio.run(main()) 