import feedparser
import pandas as pd
import requests
from datetime import datetime
from textblob import TextBlob

class NewsEngine:
    def __init__(self):
        # Seleção estratégica de fontes para o mercado brasileiro e global
        self.sources = {
            "InfoMoney": "https://www.infomoney.com.br/feed/",
            "Investing.com": "https://br.investing.com/rss/news.rss",
            "CNBC Markets": "https://search.cnbc.com/rs/search/combinedfeed.view?articlePubDate=0&output=rss&searchterm=markets",
            "Valor Econômico": "https://valor.globo.com/rss/valor/"
        }

    def _analyze_sentiment(self, text):
        """Analisa o tom da manchete para indicar viés de mercado."""
        analysis = TextBlob(text)
        score = analysis.sentiment.polarity
        
        # Léxico financeiro para ajuste fino do sentimento
        bullish = ['alta', 'lucro', 'sobe', 'cresce', 'dividendo', 'supera', 'bull']
        bearish = ['queda', 'prejuízo', 'cai', 'recessão', 'venda', 'crise', 'bear']
        
        t_lower = text.lower()
        for w in bullish:
            if w in t_lower: score += 0.25
        for w in bearish:
            if w in t_lower: score -= 0.25

        if score > 0.05: return "BULLISH 🟢"
        if score < -0.05: return "BEARISH 🔴"
        return "NEUTRAL ⚪"

    def fetch(self):
        """Coleta e consolida as notícias mais relevantes (Top 7)."""
        all_news = []
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}

        for name, url in self.sources.items():
            try:
                response = requests.get(url, headers=headers, timeout=10)
                feed = feedparser.parse(response.content)
                
                # Coleta as 5 mais recentes de cada fonte para triagem
                for entry in feed.entries[:5]:
                    all_news.append({
                        "title": entry.title,
                        "link": entry.link,
                        "source": name,
                        "sentiment": self._analyze_sentiment(entry.title),
                        "published": entry.get("published", datetime.now().strftime("%H:%M"))
                    })
            except Exception:
                continue
        
        if not all_news:
            return pd.DataFrame()

        df = pd.DataFrame(all_news).drop_duplicates(subset=['title'])
        
        # Lógica de Diversidade: Garante uma notícia de cada fonte antes de repetir
        diverse_df = df.groupby('source').first().reset_index()
        if len(diverse_df) < 7:
            remaining = df[~df['title'].isin(diverse_df['title'])]
            diverse_df = pd.concat([diverse_df, remaining.head(7 - len(diverse_df))])
            
        return diverse_df.head(7)