#作者：伊茗(微信：EviMing，QQ：2368199809，邮箱：2368199809@qq.com)
#[伊茗的GitHub仓库] = 'https://github.com/EviMing/'
    #此文件所处项目 = https://github.com/EviMing/playwright-Generated_page

from Generated_page import Generated_page
from playwright.sync_api import sync_playwright

class exe_get_page(Generated_page):

    def __init__(self,
                 url='http://localhost', port=9222,
                 context_index=0, page_index=0):

        debug_url = f'{url}:{port}'

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

    def close(self):
        super().close()
