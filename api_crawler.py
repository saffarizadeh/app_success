import requests

class ApiCrawler(object):
    def __init__(self):
        self.crawled_apps = []
        self.crawled_data = {}
        self.to_crawl_list = []
        self.chart_types =  ['top-free', 'top-grossing', 'top-paid']

    def create_crawl_list_from_rss(self):
        for chart_type in self.chart_types:
            url = 'https://rss.itunes.apple.com/api/v1/us/ios-apps/%s/all/200/explicit.json' % chart_type
            chart_json = self.download_json_from_url(url, 'chart')
            if chart_json:
                app_ids = self.app_ids_from_chart(chart_json)
                self.to_crawl_list.extend(app_ids)

    def app_ids_from_chart(self, chart_json):
        app_ids = []
        for app in chart_json:
            app_ids.append(app['id'])
        return app_ids

    def crawl(self):
        self.to_crawl_list = list(set(self.to_crawl_list))
        while self.to_crawl_list:
            app_id = self.to_crawl_list.pop(0)
            url = 'https://itunes.apple.com/lookup?id=%s' % app_id
            try:
                self.crawled_data[app_id] = self.download_json_from_url(url, 'app')
                self.crawled_apps.append(app_id)
            except:
                print('Something went wrong with %s.' % app_id)

    def download_json_from_url(self, url, type):
        data = None
        u = requests.get(url)
        #u.raise_for_status()
        page = u.json()
        try:
            if type == 'app':
                data = page['results'][0]
            elif type == 'chart':
                data = page['feed']['results']
        except:
            pass
        return data


c = ApiCrawler()
c.create_crawl_list_from_rss()
c.crawl()
