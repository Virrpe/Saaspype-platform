#!/usr/bin/env python3
"""
DEBUG FAILED SOURCES - Fix Product Hunt and BetaList scrapers
Investigate why they returned 0 items and fix the selectors
"""

import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json
from datetime import datetime

class SourceDebugger:
    """Debug and fix failed web scrapers"""
    
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
    
    async def debug_product_hunt(self):
        """Debug Product Hunt scraping"""
        print("🔍 DEBUGGING PRODUCT HUNT")
        print("=" * 50)
        
        session = await self._get_session()
        url = "https://www.producthunt.com/"
        
        try:
            async with session.get(url) as response:
                print(f"📊 Status Code: {response.status}")
                print(f"📊 Content Type: {response.headers.get('content-type', 'unknown')}")
                
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    print(f"📊 HTML Length: {len(html)} characters")
                    
                    # Save HTML for inspection
                    with open('product_hunt_debug.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    print("💾 HTML saved to: product_hunt_debug.html")
                    
                    # Try different selectors
                    print(f"\n🔍 TESTING DIFFERENT SELECTORS:")
                    
                    # Test 1: Look for any links with "posts" in href
                    posts_links = soup.find_all('a', href=lambda x: x and 'posts' in x)
                    print(f"   📝 Links with 'posts': {len(posts_links)}")
                    if posts_links:
                        for i, link in enumerate(posts_links[:3]):
                            text = link.get_text(strip=True)[:50]
                            href = link.get('href', '')[:50]
                            print(f"      {i+1}. Text: '{text}' | Href: '{href}'")
                    
                    # Test 2: Look for any links with product names
                    all_links = soup.find_all('a', href=True)
                    product_links = [link for link in all_links if link.get_text(strip=True) and len(link.get_text(strip=True)) > 5]
                    print(f"   📝 All meaningful links: {len(product_links)}")
                    if product_links:
                        for i, link in enumerate(product_links[:5]):
                            text = link.get_text(strip=True)[:50]
                            href = link.get('href', '')[:50]
                            print(f"      {i+1}. Text: '{text}' | Href: '{href}'")
                    
                    # Test 3: Look for specific Product Hunt patterns
                    ph_patterns = [
                        soup.find_all('h3'),
                        soup.find_all('h2'),
                        soup.find_all('div', class_=lambda x: x and 'product' in x.lower()),
                        soup.find_all('div', class_=lambda x: x and 'post' in x.lower()),
                        soup.find_all('a', class_=lambda x: x and 'product' in x.lower())
                    ]
                    
                    for i, pattern in enumerate(ph_patterns):
                        print(f"   📝 Pattern {i+1}: {len(pattern)} elements")
                        if pattern:
                            for j, elem in enumerate(pattern[:2]):
                                text = elem.get_text(strip=True)[:50]
                                print(f"      {j+1}. '{text}'")
                    
                    # Test 4: Look for data attributes
                    data_elements = soup.find_all(attrs=lambda x: any(k.startswith('data-') for k in x.keys()) if x else False)
                    print(f"   📝 Elements with data attributes: {len(data_elements)}")
                    
                    # Test 5: Check for JavaScript-rendered content
                    scripts = soup.find_all('script')
                    print(f"   📝 Script tags: {len(scripts)}")
                    
                    # Look for JSON data in scripts
                    json_scripts = []
                    for script in scripts:
                        if script.string and ('product' in script.string.lower() or 'post' in script.string.lower()):
                            json_scripts.append(script.string[:100])
                    
                    print(f"   📝 Scripts with product/post data: {len(json_scripts)}")
                    for i, script_content in enumerate(json_scripts[:2]):
                        print(f"      {i+1}. {script_content}...")
                
                else:
                    print(f"❌ Failed to load Product Hunt: {response.status}")
                    
        except Exception as e:
            print(f"❌ Product Hunt debug error: {e}")
    
    async def debug_betalist(self):
        """Debug BetaList scraping"""
        print(f"\n🔍 DEBUGGING BETALIST")
        print("=" * 50)
        
        session = await self._get_session()
        url = "https://betalist.com/"
        
        try:
            async with session.get(url) as response:
                print(f"📊 Status Code: {response.status}")
                print(f"📊 Content Type: {response.headers.get('content-type', 'unknown')}")
                
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    print(f"📊 HTML Length: {len(html)} characters")
                    
                    # Save HTML for inspection
                    with open('betalist_debug.html', 'w', encoding='utf-8') as f:
                        f.write(html)
                    print("💾 HTML saved to: betalist_debug.html")
                    
                    # Try different selectors
                    print(f"\n🔍 TESTING DIFFERENT SELECTORS:")
                    
                    # Test 1: Look for startup links
                    startup_links = soup.find_all('a', href=lambda x: x and 'startup' in x)
                    print(f"   📝 Links with 'startup': {len(startup_links)}")
                    if startup_links:
                        for i, link in enumerate(startup_links[:3]):
                            text = link.get_text(strip=True)[:50]
                            href = link.get('href', '')[:50]
                            print(f"      {i+1}. Text: '{text}' | Href: '{href}'")
                    
                    # Test 2: Look for company/product names
                    all_links = soup.find_all('a', href=True)
                    meaningful_links = [link for link in all_links if link.get_text(strip=True) and len(link.get_text(strip=True)) > 3]
                    print(f"   📝 All meaningful links: {len(meaningful_links)}")
                    if meaningful_links:
                        for i, link in enumerate(meaningful_links[:5]):
                            text = link.get_text(strip=True)[:50]
                            href = link.get('href', '')[:50]
                            print(f"      {i+1}. Text: '{text}' | Href: '{href}'")
                    
                    # Test 3: Look for specific BetaList patterns
                    bl_patterns = [
                        soup.find_all('h1'),
                        soup.find_all('h2'),
                        soup.find_all('h3'),
                        soup.find_all('div', class_=lambda x: x and 'startup' in x.lower()),
                        soup.find_all('div', class_=lambda x: x and 'company' in x.lower()),
                        soup.find_all('div', class_=lambda x: x and 'product' in x.lower())
                    ]
                    
                    for i, pattern in enumerate(bl_patterns):
                        print(f"   📝 Pattern {i+1}: {len(pattern)} elements")
                        if pattern:
                            for j, elem in enumerate(pattern[:2]):
                                text = elem.get_text(strip=True)[:50]
                                print(f"      {j+1}. '{text}'")
                    
                    # Test 4: Look for class patterns
                    all_divs = soup.find_all('div', class_=True)
                    class_names = set()
                    for div in all_divs:
                        classes = div.get('class', [])
                        class_names.update(classes)
                    
                    relevant_classes = [cls for cls in class_names if any(keyword in cls.lower() for keyword in ['startup', 'company', 'product', 'item', 'card', 'list'])]
                    print(f"   📝 Relevant CSS classes: {relevant_classes[:10]}")
                    
                    # Test 5: Look for specific content patterns
                    text_content = soup.get_text()
                    startup_mentions = text_content.lower().count('startup')
                    company_mentions = text_content.lower().count('company')
                    print(f"   📝 'startup' mentions: {startup_mentions}")
                    print(f"   📝 'company' mentions: {company_mentions}")
                
                else:
                    print(f"❌ Failed to load BetaList: {response.status}")
                    
        except Exception as e:
            print(f"❌ BetaList debug error: {e}")
    
    async def test_fixed_scrapers(self):
        """Test improved scrapers based on debug findings"""
        print(f"\n🔧 TESTING FIXED SCRAPERS")
        print("=" * 50)
        
        session = await self._get_session()
        
        # Fixed Product Hunt scraper
        print("🔍 Testing fixed Product Hunt scraper...")
        ph_results = await self._fixed_product_hunt_scraper(session)
        print(f"   ✅ Product Hunt: {len(ph_results)} items")
        for i, item in enumerate(ph_results[:3]):
            print(f"      {i+1}. {item.get('title', 'No title')[:50]}...")
        
        # Fixed BetaList scraper
        print(f"\n🔍 Testing fixed BetaList scraper...")
        bl_results = await self._fixed_betalist_scraper(session)
        print(f"   ✅ BetaList: {len(bl_results)} items")
        for i, item in enumerate(bl_results[:3]):
            print(f"      {i+1}. {item.get('title', 'No title')[:50]}...")
        
        return ph_results, bl_results
    
    async def _fixed_product_hunt_scraper(self, session) -> list:
        """Improved Product Hunt scraper"""
        results = []
        url = "https://www.producthunt.com/"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Strategy 1: Look for any meaningful links
                    all_links = soup.find_all('a', href=True)
                    
                    seen_titles = set()
                    for link in all_links:
                        text = link.get_text(strip=True)
                        href = link.get('href', '')
                        
                        # Filter for product-like content
                        if (text and 
                            len(text) > 5 and 
                            len(text) < 100 and
                            text not in seen_titles and
                            not text.lower().startswith(('sign', 'log', 'get', 'try', 'learn', 'about', 'contact', 'privacy', 'terms')) and
                            not any(skip in text.lower() for skip in ['cookie', 'policy', 'newsletter', 'subscribe', 'follow'])):
                            
                            seen_titles.add(text)
                            
                            # Clean up href
                            if href.startswith('/'):
                                href = f"https://www.producthunt.com{href}"
                            
                            results.append({
                                'title': text,
                                'url': href,
                                'source': 'product_hunt_fixed',
                                'scraped_at': datetime.now().isoformat()
                            })
                            
                            if len(results) >= 10:  # Limit results
                                break
                    
                    # Strategy 2: Look for headings
                    if len(results) < 5:
                        headings = soup.find_all(['h1', 'h2', 'h3', 'h4'])
                        for heading in headings:
                            text = heading.get_text(strip=True)
                            if text and len(text) > 5 and text not in seen_titles:
                                seen_titles.add(text)
                                results.append({
                                    'title': text,
                                    'url': url,
                                    'source': 'product_hunt_fixed',
                                    'scraped_at': datetime.now().isoformat()
                                })
                                
                                if len(results) >= 10:
                                    break
                    
        except Exception as e:
            print(f"   ⚠️ Fixed Product Hunt error: {e}")
        
        return results
    
    async def _fixed_betalist_scraper(self, session) -> list:
        """Improved BetaList scraper"""
        results = []
        url = "https://betalist.com/"
        
        try:
            async with session.get(url) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    
                    # Strategy 1: Look for any meaningful links
                    all_links = soup.find_all('a', href=True)
                    
                    seen_titles = set()
                    for link in all_links:
                        text = link.get_text(strip=True)
                        href = link.get('href', '')
                        
                        # Filter for startup-like content
                        if (text and 
                            len(text) > 3 and 
                            len(text) < 80 and
                            text not in seen_titles and
                            not text.lower().startswith(('sign', 'log', 'get', 'try', 'learn', 'about', 'contact', 'privacy', 'terms', 'submit')) and
                            not any(skip in text.lower() for skip in ['cookie', 'policy', 'newsletter', 'subscribe', 'follow', 'twitter', 'facebook'])):
                            
                            seen_titles.add(text)
                            
                            # Clean up href
                            if href.startswith('/'):
                                href = f"https://betalist.com{href}"
                            
                            results.append({
                                'title': text,
                                'url': href,
                                'source': 'betalist_fixed',
                                'scraped_at': datetime.now().isoformat()
                            })
                            
                            if len(results) >= 8:  # Limit results
                                break
                    
                    # Strategy 2: Look for headings and strong text
                    if len(results) < 3:
                        elements = soup.find_all(['h1', 'h2', 'h3', 'h4', 'strong', 'b'])
                        for elem in elements:
                            text = elem.get_text(strip=True)
                            if text and len(text) > 3 and text not in seen_titles:
                                seen_titles.add(text)
                                results.append({
                                    'title': text,
                                    'url': url,
                                    'source': 'betalist_fixed',
                                    'scraped_at': datetime.now().isoformat()
                                })
                                
                                if len(results) >= 8:
                                    break
                    
        except Exception as e:
            print(f"   ⚠️ Fixed BetaList error: {e}")
        
        return results
    
    async def save_fixed_results(self, ph_results, bl_results):
        """Save the fixed scraping results"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        fixed_results = {
            'timestamp': timestamp,
            'product_hunt_fixed': ph_results,
            'betalist_fixed': bl_results,
            'total_items': len(ph_results) + len(bl_results),
            'debug_info': {
                'product_hunt_items': len(ph_results),
                'betalist_items': len(bl_results),
                'status': 'fixed_scrapers_tested'
            }
        }
        
        filename = f"fixed_sources_results_{timestamp}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fixed_results, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"\n💾 Fixed results saved to: {filename}")
        return fixed_results
    
    async def close(self):
        """Clean up resources"""
        if self.session:
            await self.session.close()

async def main():
    """Run the source debugger"""
    debugger = SourceDebugger()
    
    try:
        # Debug failed sources
        await debugger.debug_product_hunt()
        await debugger.debug_betalist()
        
        # Test fixed scrapers
        ph_results, bl_results = await debugger.test_fixed_scrapers()
        
        # Save results
        results = await debugger.save_fixed_results(ph_results, bl_results)
        
        print(f"\n🎯 DEBUG SUMMARY:")
        print(f"   📊 Product Hunt Fixed: {len(ph_results)} items")
        print(f"   📊 BetaList Fixed: {len(bl_results)} items")
        print(f"   📊 Total Fixed Items: {results['total_items']}")
        
        if results['total_items'] > 0:
            print(f"\n✅ SUCCESS: Fixed scrapers are working!")
        else:
            print(f"\n⚠️ STILL ISSUES: Need further investigation")
        
    finally:
        await debugger.close()

if __name__ == "__main__":
    asyncio.run(main()) 