from Generated_page import Generated_page
from playwright.sync_api import sync_playwright
import requests

class exe_get_page(Generated_page):

    def __init__(self,
                 url='http://localhost', port=9222,
                 context_index=0, page_index=0):

        json_data = requests.get(f'{url}:{port}/json/version').json()
        debug_url = json_data['webSocketDebuggerUrl']

        #启动 Playwright
        p = sync_playwright()
        #启动浏览器内核
        self.playwright_ = p.start()

        #连接已有的调试端口控制exe里的浏览器实例
        self.browser = self.playwright_.chromium.connect_over_cdp(debug_url)

        #获取当前打开的上下文
        context = self.browser.contexts[context_index]

        #直接获取页面，而不用方法单独生成新建页面实例
        self.page = context.pages[page_index]

    def close(slef):
        super().close()