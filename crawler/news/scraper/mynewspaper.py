from dateutil.parser import parse as date_parser
from newspaper import Article


class MyArticle(Article):
    def __init__(self, url, title='', source_url='', config=None, **kwargs):
        super().__init__(url, title, source_url, config, **kwargs)
        self.categories = []
        self.config.MIN_SENT_COUNT = 30

    def set_categories(self, categories):
        self.categories = categories

    def extract_category(self):
        def iter_to_leaf(meta_data, result={}):
            if isinstance(meta_data, dict):
                for key, value in meta_data.items():
                    if isinstance(value, str):
                        result[key] = value
                    else:
                        iter_to_leaf(value, result)
            elif isinstance(meta_data, list):
                for item in meta_data:
                    iter_to_leaf(item, result)
            return result

        categories = []
        keywords = ['topic', 'category', 'categories', 'section']
        for key, value in iter_to_leaf(dict(self.meta_data)).items():
            for k in keywords:
                if k in key:
                    categories.append(value)
        return list(set(categories))

    def extract_publish_date(self):
        def iter_to_leaf(meta_data, result={}):
            if isinstance(meta_data, dict):
                for key, value in meta_data.items():
                    if isinstance(value, str):
                        result[key] = value
                    else:
                        iter_to_leaf(value, result)
            elif isinstance(meta_data, list):
                for item in meta_data:
                    iter_to_leaf(item, result)
            return result

        def parse_date_str(date_str):
            if date_str:
                try:
                    return date_parser(date_str)
                except (ValueError, OverflowError, AttributeError, TypeError):
                    # near all parse failures are due to URL dates without a day
                    # specifier, e.g. /2014/04/
                    return None

        keywords = ['date', 'created']
        for key, value in iter_to_leaf(dict(self.meta_data)).items():
            for k in keywords:
                if k in key:
                    datetime_obj = parse_date_str(value)
                    if datetime_obj:
                        return datetime_obj

    def parse(self):
        super().parse()

        categories = self.extract_category()
        self.set_categories(categories)

        if not self.publish_date:
            publish_date = self.extract_publish_date()
            self.publish_date = publish_date
