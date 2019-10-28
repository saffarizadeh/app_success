import requests
import json
import shutil


class ApiCrawler(object):
    def __init__(self):
        self.crawled_apps = []
        self.crawled_data = {}
        self.to_crawl_list = []
        self.chart_types = ['top-free', 'top-grossing', 'top-paid']

    def create_crawl_list_from_rss(self):
        for chart_type in self.chart_types:
            url = 'https://rss.itunes.apple.com/api/v1/us/ios-apps/%s/all/200/explicit.json' % chart_type
            chart_json = self.download_json_from_url(url, 'chart')
            if chart_json:
                app_ids = self.app_ids_from_chart(chart_json)
                self.to_crawl_list.extend(app_ids)

    @staticmethod
    def app_ids_from_chart(chart_json):
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

    def download_icons(self):
        for app_id, data in self.crawled_data.items():
            try:
                icon100_url = data['artworkUrl100']
                self.download_image(app_id, icon100_url, 'jpg')
            except:
                print('Failed to find the icon for app_id: ' + app_id)

    @staticmethod
    def download_image(app_id, url, file_type):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open('icons/' + app_id + '.' + file_type, 'wb') as f:
                r.raw.decode_content = True
                shutil.copyfileobj(r.raw, f)

    @staticmethod
    def download_json_from_url(url, type):
        data = None
        u = requests.get(url)
        # u.raise_for_status()
        page = u.json()
        try:
            if type == 'app':
                data = page['results'][0]
            elif type == 'chart':
                data = page['feed']['results']
        except:
            pass
        return data

    def save_data_as_json(self):
        with open('crawled_data.json', 'w') as fp:
            json.dump(self.crawled_data, fp)

    def read_json_as_dict(self):
        with open('crawled_data.json', 'r') as f:
            self.crawled_data = json.load(f)


c = ApiCrawler()
# c.create_crawl_list_from_rss()
# c.crawl()
# c.save_data_as_json()
c.read_json_as_dict()
c.download_icons()
