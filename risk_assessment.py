import logging
from collections import Counter

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SecurityRiskAssessment:
    """Assess security risk level based on news articles"""
    
    # Crime-related keywords in Indonesian for scoring
    CRIME_KEYWORDS = {
        'terrorist': ['teroris', 'teror', 'bom', 'pengeboman', 'jihadis', 'ekstremis'],
        'corruption': ['korupsi', 'suap', 'penyuapan', 'korup', 'mark up', 'penggelapan', 'kpk'],
        'crime': ['kejahatan', 'kriminal', 'membunuh', 'pembunuhan', 'pencurian', 'perampokan', 
                 'penculikan', 'perkosaan', 'narkoba', 'narkotika', 'obat terlarang', 'pelecehan'],
        'violence': ['kekerasan', 'baku tembak', 'pemukulan', 'pembaresan', 'bentrok', 'tawuran'],
        'theft': ['curi', 'pencuri', 'maling', 'perampokan', 'rampok'],
        'war': ['israel', 'perang', 'iran', 'weapon', 'weapons'],
        'fraud': ['penipuan', 'tipuan', 'fraud', 'palsuan', 'manipulasi']
    }
    
    # Risk level descriptions
    RISK_LEVELS = {
        0: {'level': 'Sangat Aman', 'color': '#4CAF50', 'description': 'Tidak ada laporan kejahatan'},
        1: {'level': 'Aman', 'color': '#8BC34A', 'description': 'Risiko sangat rendah'},
        2: {'level': 'Cukup Aman', 'color': '#FFC107', 'description': 'Risiko sedang-rendah'},
        3: {'level': 'Rawan', 'color': '#FF9800', 'description': 'Risiko sedang-tinggi'},
        4: {'level': 'Rawan Tinggi', 'color': '#FF5722', 'description': 'Risiko tinggi'},
        5: {'level': 'Sangat Berbahaya', 'color': '#F44336', 'description': 'Risiko sangat tinggi'}
    }
    
    def __init__(self):
        pass
    
    def calculate_risk_score(self, articles):
        """
        Calculate security risk score from 0-5 based on articles
        
        Args:
            articles (list): List of article dictionaries with 'title' key
            
        Returns:
            dict: Contains risk_score, level, description, and details
        """
        
        if not articles or len(articles) == 0:
            return {
                'risk_score': 0,
                'level_info': self.RISK_LEVELS[0],
                'keyword_count': 0,
                'articles_analyzed': 0,
                'keyword_breakdown': {},
                'details': 'Tidak ada artikel untuk dianalisis'
            }
        
        # Count keyword occurrences
        keyword_count = 0
        keyword_breakdown = {}
        
        # Combine all article titles to lowercase for analysis
        all_text = ' '.join([article.get('title', '').lower() for article in articles])
        
        # Count keywords
        for category, keywords in self.CRIME_KEYWORDS.items():
            category_count = 0
            for keyword in keywords:
                count = all_text.count(keyword)
                if count > 0:
                    category_count += count
                    keyword_count += count
            
            if category_count > 0:
                keyword_breakdown[category] = category_count
        
        # Calculate risk score (scale 0-5)
        # Based on keyword frequency and number of articles
        articles_count = len(articles)
        
        # Risk calculation formula
        if keyword_count == 0:
            risk_score = 0
        else:
            # Average keywords per article
            avg_keywords_per_article = keyword_count / articles_count
            
            # Scale formula: higher keywords increase risk
            # 0-0.5 avg keywords = low risk (0-1)
            # 0.5-1.0 = moderate (1-2)
            # 1.0-1.5 = high (2-3)
            # 1.5-2.0 = very high (3-4)
            # 2.0+ = critical (4-5)
            
            if avg_keywords_per_article <= 0.2:
                risk_score = 0
            elif avg_keywords_per_article <= 0.5:
                risk_score = 1
            elif avg_keywords_per_article <= 1.0:
                risk_score = 2
            elif avg_keywords_per_article <= 1.5:
                risk_score = 3
            elif avg_keywords_per_article <= 2.0:
                risk_score = 4
            else:
                risk_score = 5
        
        # Ensure score is within 0-5 range
        risk_score = min(5, max(0, int(risk_score)))
        
        level_info = self.RISK_LEVELS[risk_score]
        
        return {
            'risk_score': risk_score,
            'level_info': level_info,
            'keyword_count': keyword_count,
            'articles_analyzed': articles_count,
            'keyword_breakdown': keyword_breakdown,
            'details': f"Ditemukan {keyword_count} kata kunci terkait kejahatan dalam {articles_count} artikel"
        }
    
    def get_risk_level_display(self, risk_score):
        """Get display information for risk level"""
        return self.RISK_LEVELS.get(risk_score, self.RISK_LEVELS[0])
    
    def analyze_articles_with_risk(self, articles):
        """
        Analyze articles and return articles with risk indicators
        
        Args:
            articles (list): List of article dictionaries
            
        Returns:
            dict: Risk assessment result with articles marked by risk level
        """
        risk_assessment = self.calculate_risk_score(articles)
        
        # Mark articles with risk level
        marked_articles = []
        for article in articles:
            article_text = article.get('title', '').lower()
            article_risk_keywords = []
            
            # Find which keywords appear in this article
            for category, keywords in self.CRIME_KEYWORDS.items():
                for keyword in keywords:
                    if keyword in article_text:
                        article_risk_keywords.append((category, keyword))
            
            article['risk_keywords'] = article_risk_keywords
            article['has_risk_keywords'] = len(article_risk_keywords) > 0
            marked_articles.append(article)
        
        risk_assessment['articles'] = marked_articles
        return risk_assessment


if __name__ == "__main__":
    # Test the risk assessment
    assessor = SecurityRiskAssessment()
    
    # Sample articles for testing
    test_articles = [
        {'title': 'Polisi mengungkap kejahatan pencurian motor', 'source': 'Detik'},
        {'title': 'Teroris tertangkap di kota besar', 'source': 'BBC'},
        {'title': 'Korupsi dalam proyek infrastruktur terbongkar', 'source': 'CNN'},
        {'title': 'Pembunuhan di gang sempit ditangani polisi', 'source': 'Detik'},
    ]
    
    result = assessor.analyze_articles_with_risk(test_articles)
    print(f"Risk Score: {result['risk_score']}/5")
    print(f"Level: {result['level_info']['level']}")
    print(f"Keywords found: {result['keyword_count']}")
    print(f"Breakdown: {result['keyword_breakdown']}")
