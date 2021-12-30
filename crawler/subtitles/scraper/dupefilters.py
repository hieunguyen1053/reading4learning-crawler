from scrapy.dupefilters import BaseDupeFilter

from ..models import Subtitles


class CustomDupeFilter(BaseDupeFilter):
    def __init__(self):
        self.seen_urls = set()

    def request_seen(self, request):
        if Subtitles.objects.filter(referer=request.url).exists():
            return True
        if request.url in self.seen_urls:
            return True
        self.seen_urls.add(request.url)
        return False
