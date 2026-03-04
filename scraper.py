import requests
from bs4 import BeautifulSoup
from datetime import datetime
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class NewsScraperConfig:
    """Configuration for news scrapers"""
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    TIMEOUT = 10
    REQUEST_DELAY = 1  


class NewsScraper:
    """Scraper for news headlines from BBC, CNN, and Detik"""
    
    def __init__(self):
        self.config = NewsScraperConfig()
        self.articles = []
    
    def scrape_bbc_news(self):
        """Scrape headlines from BBC News"""
        try:
            url = "https://www.bbc.com/news"
            response = requests.get(url, headers=self.config.HEADERS, timeout=self.config.TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find all headline elements from BBC
            headlines = soup.find_all(['h2', 'h3'], limit=15)
            
            for headline in headlines:
                title = headline.get_text(strip=True)
                if title and len(title) > 5:  
                    articles.append({
                        'title': title,
                        'source': 'BBC News',
                        'category': 'General News',
                        'url': url,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            return articles[:10]  # Return top 10
        except requests.RequestException as e:
            logger.error(f"Error scraping BBC News: {e}")
            return []
    
    def scrape_cnn_news(self):
        """Scrape headlines from CNN"""
        try:
            url = "https://www.cnn.com"
            response = requests.get(url, headers=self.config.HEADERS, timeout=self.config.TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find CNN headlines - look for various heading tags and links
            links = soup.find_all('span', class_='container__headline-text', limit=15)
            if not links:
                links = soup.find_all(['h3'], limit=15)
            
            for link in links:
                title = link.get_text(strip=True)
                if title and len(title) > 5:
                    articles.append({
                        'title': title,
                        'source': 'CNN News',
                        'category': 'International News',
                        'url': url,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            return articles[:10]  # Return top 10
        except requests.RequestException as e:
            logger.error(f"Error scraping CNN News: {e}")
            return []
    
    def scrape_detik_news(self):
        """Scrape headlines from Detik.com (Indonesian news)"""
        try:
            url = "https://www.detik.com"
            response = requests.get(url, headers=self.config.HEADERS, timeout=self.config.TIMEOUT)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = []
            
            # Find Detik headlines - look for article links
            article_links = soup.find_all('a', class_='media__link', limit=15)
            if not article_links:
                article_links = soup.find_all('h3', limit=15)
            
            for link in article_links:
                title_elem = link.find(['h2', 'h3', 'span']) if link.name != 'h3' else link
                title = title_elem.get_text(strip=True) if title_elem else link.get_text(strip=True)
                
                if title and len(title) > 5:
                    articles.append({
                        'title': title,
                        'source': 'Detik.com',
                        'category': 'Berita Indonesia',
                        'url': url,
                        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    })
            
            return articles[:10]  # Return top 10
        except requests.RequestException as e:
            logger.error(f"Error scraping Detik.com: {e}")
            return []
    
    def get_all_headlines(self):
        """Get headlines from all sources (BBC, CNN, Detik)"""
        all_articles = []
        
        logger.info("Fetching BBC News...")
        all_articles.extend(self.scrape_bbc_news())
        time.sleep(self.config.REQUEST_DELAY)
        
        logger.info("Fetching CNN News...")
        all_articles.extend(self.scrape_cnn_news())
        time.sleep(self.config.REQUEST_DELAY)
        
        logger.info("Fetching Detik.com...")
        all_articles.extend(self.scrape_detik_news())
        
        # Return article
        return all_articles[:30]


if __name__ == "__main__":
    scraper = NewsScraper()
    print("Starting news scraper for BBC, CNN, and Detik...\n")
    
    headlines = scraper.get_all_headlines()
    
    print(f"Found {len(headlines)} headlines:\n")
    for idx, article in enumerate(headlines, 1):
        print(f"{idx}. {article['title']}")
        print(f"   Source: {article['source']} | Category: {article['category']}")
        print(f"   Time: {article['timestamp']}\n")
