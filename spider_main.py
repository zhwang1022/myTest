# from PythonSpider import url_manager, html_downloader, html_parser, html_output
import PythonSpider.url_manager as url_manager
import PythonSpider.html_downloader as html_downloader
import PythonSpider.html_parser as html_parser
import PythonSpider.html_output as html_output
import sys
'''
爬取百度百科 Python 关键词相关词及简介并输出为一个HTML tab网页
Extra module:
BeautifulSoup
'''


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownLoader()
        self.parser = html_parser.HtmlParser()
        self.out_put = html_output.HtmlOutput()

    def craw(self, root_url):
        count = 1
        self.urls.add_new_url(root_url)
        while self.urls.has_new_url():
            try:
                # print(new_url)
                new_url = self.urls.get_new_url()
                print("craw %d : %s" % (count, new_url))
                headers = {
                    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.100 Safari/537.36"
                }
                html_content = self.downloader.download(new_url, retry_count=2, headers=headers)
                new_urls, new_data = self.parser.parse(new_url, html_content, "utf-8")
                self.urls.add_new_urls(new_urls)
                self.out_put.collect_data(new_data)
                if count >= 30:
                    break
                count = count + 1
            except Exception as e:
                print("craw failed!\n"+str(e))
        self.out_put.output_html()


if __name__ == "__main__":
    # rootUrl = "https://baike.baidu.com/item/%E7%8B%97/85474#hotspotmining"
    # a = sys
    # rootUrl = sys.argv[1]  # 获取命令行参数
    # count_limit = int(sys.argv[2])
    # objSpider = SpiderMain()
    # objSpider.craw(rootUrl)
    rootUrl = "https://baike.baidu.com/item/Python/407313?fr=aladdin"
    objSpider = SpiderMain()
    objSpider.craw(rootUrl)
