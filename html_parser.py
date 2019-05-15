# [解析器]
# 负责对下载器下载下来的网页内容进行解析，解析规则就是我们自己定义的感兴趣的内容，
# 这里我们只分析网页后解析出 url、title、content，其他的不关心，解析好的数据通过字典返回。
import re
from urllib.parse import urljoin
from bs4 import BeautifulSoup


class HtmlParser(object):
    def parse(self, url, content, html_encode="utf-8"):
        if url is None or content is None:
            return
        soup = BeautifulSoup(content, "html.parser", from_encoding=html_encode)
        new_urls = self._get_new_urls(url, soup)  # 解析url
        new_data = self._get_new_data(url, soup)  # 解析title 和 content
        return new_urls, new_data

    def _get_new_urls(self, url, soup):
        new_urls = set()
        links = soup.find_all("a", href=re.compile(r"/item/\w+"))
        for link in links:
            url_path = link["href"]
            new_url = urljoin(url, url_path)
            new_urls.add(new_url)
        return new_urls

    def _get_new_data(self, url, soup):
        data = {"url": url}
        title_node = soup.find("dd", class_="lemmaWgt-lemmaTitle-title").find("h1")
        data["title"] = title_node.get_text()
        summary_node = soup.find("div", class_="lemma-summary")
        data["summary"] = summary_node.get_text()
        return data