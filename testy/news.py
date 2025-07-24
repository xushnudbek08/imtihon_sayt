import feedparser
from .models import news
from datetime import datetime
import pytz


def fetch_kunuz():
    fedd_url = 'https://kun.uz/news/rss'
    fedd = feedparser.parse(fedd_url)


    for entry in fedd.entries:
        if not news.objects.filter(link=entry.link).exists():
            # Agar published_parsed yo'q bo'lsa, hozirgi vaqtni ishlatamiz
            if entry.get("published_parsed"):
                published_date = datetime(*entry.published_parsed[:6], tzinfo=pytz.UTC)
            else:
                published_date = datetime.now(tz=pytz.UTC)

            news.objects.create(
                title=entry.title,
                link=entry.link,
                published=published_date,
                summary=entry.summary or ""
            )
           