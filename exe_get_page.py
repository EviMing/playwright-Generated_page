从生成页面导入生成页面
从playwright.
导入requests

类exe_get_page(生成的页面):

     __init__(self,
url='http://localhost', 端口=9222,
上下文索引=0, 页面索引=0):

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

    定义 关闭(自我):
        超级().关闭()
