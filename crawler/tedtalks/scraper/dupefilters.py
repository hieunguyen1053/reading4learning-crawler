from scrapy.dupefilters import BaseDupeFilter

from ..models import TedTalks


class CustomDupeFilter(BaseDupeFilter):
    def __init__(self):
        self.seen_urls = set()

    def request_seen(self, request):
        if TedTalks.objects.filter(url=request.url).exists():
            return True
        if request.url in self.seen_urls:
            return True
        self.seen_urls.add(request.url)
        return False
