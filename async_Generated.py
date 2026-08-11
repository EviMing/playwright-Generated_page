#作者：伊茗(微信：EviMing, QQ：2368199809, 邮箱：2368199809@qq.com)
#[伊茗的GitHub仓库] = 'https://github.com/EviMing/'
    #此文件所处项目 = 'https://github.com/EviMing/playwright-Main_Lib'

'链式操作 = await (await (await (async_Generated_Browser()).run(**参数)).get_Context(**参数)).get_Page()'

from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Locator, JSHandle
from playwright_stealth import Stealth
import asyncio
from typing import Literal, Any
from random import uniform
import traceback
import sys

#[变量] 指定全局的 timeout(单位=秒)
global_timeout = 30

#[定义标识类] 函数运行时有报错被拦截则返回此类, 用于判断是否存在报错
class IsError(Exception):
    pass

#[定义接口类] 让主类有更方便的生成上下文方法, 并提供更生成异步 page 的方法
class async_Generated_Context:

    #[定义属性] 无
    def __init__(self):
        pass

    #[定义方法] 主逻辑
    async def run(self,
        #[参数] 已有的浏览器实例
        browser:Browser,
        #[参数] 是否从文件获取登录态
        LogIn_state_FilePath:None|str=None,
    ):
        #创建上下文实例
        self.context :BrowserContext =  None
        #判断是否从文件获取登录态
        if type(LogIn_state_FilePath) == str:
            self.context = await browser.new_context(storage_state=LogIn_state_FilePath)
        else:
            self.context = await browser.new_context()

        #创建 Stealth 实例
        stealth = Stealth(
            #设置语言偏好
            navigator_languages_override=("zh-CN", "zh"),
            #是否(仅通过初始化脚本注入 stealth 代码，而不使用其他注入方式)
            init_scripts_only=False
        )
        #手动伪装上下文
        stealth.apply_stealth_async(self.context)

        #为了方便链式调用, 返回 self
        return self

    #[定义方法] 返回一个接口类(浏览器上下文)实例
    async def get_Page(self,
    ) -> Page:
        '每个异步 page 允许 \'await 函数(page对象, 参数)\' 或 \'await page对象.原生方法\' 直接运行, 或使用库提供的 \'`(async_){0,1}eval_pages`\' 方法批量运行'
        return await self.context.new_page()

#[定义类] 生成安全的浏览器实例并调用接口类达到链式操作
class async_Generated_Browser:

    #[定义属性] 无
    def __init__(self):
        pass

    #[定义方法] 主逻辑
    async def run(self,
        #[参数] 是否显示浏览器窗口
        look_window=False,
        #[参数]指定浏览器路径
        browser_path=r"D:\Quark\quark.exe",
        proxy:None|dict[str,str]=None,
        #[参数] 全局每一步行动后应 sleep 的毫秒数
        sleep_ms:int=100
    ):
        #代理字典
        proxy_ = {}
        #代理字典不为空时提取键
        if proxy:
            #核心键不存在则报错
            if not proxy.get('proxy'):
                raise KeyError('proxy[\'proxy\'] 键不存在')
            #存在则提取核心键
            else:
                proxy_['server'] = proxy['proxy']
            #提取配置键
            if proxy.get('user'):
                proxy_['user'] = proxy['user']
            if proxy.get('password'):
                proxy_['password'] = proxy['password']
            if proxy.get('not_proxy'):
                proxy_['bypass'] = ",".join(proxy['not_proxy'])

        #启动 Playwright
        p = async_playwright()
        #启动浏览器内核
        self.playwright = await p.start()
        #创建浏览器实例
        self.browser = await self.playwright.chromium.launch(
            executable_path=browser_path,
            headless= not look_window,
            slow_mo=sleep_ms,
            proxy= proxy_ if proxy else None
        )

        #为了方便链式调用, 返回 self
        return self

    #[定义方法] 生成并返回一个 接口类(浏览器上下文) 实例
    async def get_Context(self,
        #[参数] 是否从文件获取登录态
        LogIn_state_FilePath:None|str=None
    ) -> async_Generated_Context:
        return await (async_Generated_Context()).run(self.browser, LogIn_state_FilePath)

    #[定义方法] 关闭实例
    async def close(self):
        for context in self.browser.contexts:
            for page in context.pages:
                await page.close()
            await context.close()
        await self.browser.close()
        await self.playwright.stop()

"""[定义运行方法] 第一个参数必须是一个异步 page 对象, 会使用 await 运行"""
#[定义函数] 获取当前 page 的 URL
def page_get_url(
    page:Page
) -> None|str:
    return (x if (x:= page.url) else None)

#[定义函数] 跳转页面
async def async_goto(
    page:Page,
    #[参数] 跳转的目标 URL
    url,
    #[参数] 等待什么事件触发时停止跳转行为
    wait_until:Literal['commit','domcontentloaded','load','networkidle']='domcontentloaded',
    #[参数] 指定来源 URL, 默认为跳转前的 URL
    referer:None|str|Literal['page.url']='page.url',
    #[参数] timeout(单位=秒)，默认使用全局 timeout
    timeout:int|Literal['global_timeout']='global_timeout'
):
    await page.goto(url, wait_until=wait_until, referer=(page_get_url(page) if referer == 'page.url' else (referer if type(referer) == str else None)), timeout=int((global_timeout if timeout == 'global_timeout' else timeout)*1000))

#[定义函数] 执行JS代码
async def async_eval_js(
    page:Page,
    #[参数] JavaScript 代码
    js_code,
    #[参数] JavaScript 参数字典
    parameter:None|dict=None
) -> Any:
    return await page.evaluate(js_code, parameter)

#[定义函数] 执行JS代码并返回JSHandle对象
async def async_eval_js_handle(
    page:Page,
    #[参数] JavaScript 代码
    js_code,
    #[参数] JavaScript 参数字典 -> dict['参数名', 参数值]
    parameter:None|dict=None
) -> JSHandle:
    return await page.evaluate_handle(js_code, parameter)

#[定义函数] 等待元素出现
async def async_waiting_DOM(
    page:Page,
    #[参数] selector=选择器, text=元素文本, not_text=元素不允许存在的文本
    selector:str, text:None|str=None, not_text:None|str=None,
    #[参数] 元素存在的最小个数
    min_number:int=1,
    #[参数] timeout(单位=秒), 默认使用全局 timeout
    timeout:int|Literal['global_timeout']='global_timeout'
):
    await page.locator(selector, has_text=text, has_not_text=not_text).nth(min_number-1).wait_for(timeout=int((global_timeout if timeout == 'global_timeout' else timeout)*1000))

#[定义函数] 利用CSS选择器获取 DOM元素 或 元素的属性值
async def async_get_DOM(
    page:Page,
    #[参数] selector=选择器, text=元素文本, not_text=元素不允许存在的文本
    selector:str, text:None|str=None, not_text:None|str=None,
    #[参数] 指定第 index 个元素, 默认'all'返回所有元素
    index:Literal['all']|int='all',
    #[参数] 不为 None 时返回数据由 元素本身 变为 元素指定属性名的值
    get_attribute_name:None|str=None
) -> (list[Locator]|Locator) | (list[str]|str):

    list_or_locator :list[Locator]|Locator = None
    #已知索引值时返回第 index 个
    if type(index) == int:
        list_or_locator = await page.locator(selector, has_text=text, has_not_text=not_text).nth(index)
    #否则返回 所有:list
    elif index == 'all':
        list_or_locator = await page.locator(selector, has_text=text, has_not_text=not_text).all()
    else:
        raise ValueError('#-> \'index\' 参数值错误')

    #已知属性名时返回属性值
    if type(get_attribute_name) == str:
        return (
            [
                i.get_attribute(get_attribute_name)
                for i in list_or_locator
            ]
            if type(list_or_locator) == list
            else list_or_locator.get_attribute(get_attribute_name)
        )
    #否则返回元素本身
    else:
        return (list_or_locator if type(list_or_locator) == list else list_or_locator[index])

#[定义函数] 获取元素坐标
async def async_get_DOM_coordinate(
    page:Page,
    #[参数] selector=选择器, text=元素文本, not_text=元素不允许存在的文本
    selector, text:None|str=None, not_text:None|str=None,
    #[参数] 指定第 index 个元素, 默认选中第一个, 未指定 index 且元素数量大于 1 则报错
    index:None|int=None,
) -> tuple[float, float]:

    DOM :Locator = None
    if type(index) == int:
        DOM = await page.locator(selector, has_text=text, has_not_text=not_text).nth(index)
    elif index in None:
        DOM = await page.locator(selector, has_text=text, has_not_text=not_text)
    else:
        raise ValueError('#-> \'index\' 参数值错误')
    box = await DOM.bounding_box()
    x = float(box['x'] + box['width'] / 2)
    y = float(box['y'] + box['height'] / 2)
    return (x,y)

#[定义函数] 点击元素
async def async_click(
    page:Page,
    #[参数] selector=选择器, text=元素文本, not_text=元素不允许存在的文本
    selector, text:None|str=None, not_text:None|str=None,
    #[参数] 指定第 index 个元素, 默认选中第一个, 未指定 index 且元素数量大于 1 则报错
    index:None|int=None,
    #[参数] 指定要触发的键名, ['left','right','middle']=[左,中,右]
    key:Literal['left','right','middle']='left'
):
    DOM :Locator = None
    if type(index) == int:
        DOM = await page.locator(selector, has_text=text, has_not_text=not_text).nth(index)
    elif index in None:
        DOM = await page.locator(selector, has_text=text, has_not_text=not_text)
    else:
        raise ValueError('#-> \'index\' 参数值错误')

    #手动移动到元素中心点击，防止出现遮罩阻挡点击事件
    await DOM.hover()
    await page.mouse.down(button=key)
    await asyncio.sleep(uniform(0.1, 0.2))
    page.mouse.up(button=key)

#[定义函数] 按下单个鼠标按键
async def async_mouse_down(
    page:Page,
    #[参数] 指定要按下的键名, ['left','right','middle']=[左,中,右]
    button:Literal['left','right','middle']='left'
):
    await page.mouse.down(button=button)
#[定义函数] 抬起单个鼠标按键
async def async_mouse_up(
    page:Page,
    #[参数] 指定要按下的键名, ['left','right','middle']=[左,中,右]
    button:Literal['left','right','middle']='left'
):
    await page.mouse.up(button=button)
#[定义函数] 鼠标平面移动
async def async_mouse_move(
    page:Page,
    #[参数] x,y=屏幕坐标(像素值:float)
    px_tuple:tuple[float,float],
    #[参数] 移动步数, 值越大移动越慢, (1 为瞬间移动), (None 为 playwright 自己判断移动)
    steps:None|int=None
):
    await page.mouse.move(*px_tuple, steps=steps)
#[定义函数] 模拟鼠标滚轮上下滚动
async def async_mouse_wheel(
    page:Page,
    #[参数] 横向滚动的像素距离, [正,负]=[右,左], 横向滚动的像素距离, [正,负]=[下,上]
    wheel_px_tuple:tuple[float,float]=(0,500)
):
    await page.mouse.wheel(*wheel_px_tuple)

#[定义函数] 按下单个键盘按键
async def async_key_down(
    page:Page,
    #[参数] 指定按下的键名
    key:str
):
    await page.keyboard.press(key)
#[定义函数] 抬起单个键盘按键
async def async_key_up(
    page:Page,
    #[参数] 指定抬起的键名
    key:str
):
    await page.keyboard.up(key)

#[定义函数] 保存登录态为 JSON 文件
async def async_save_LogIn_state(
    page:Page,
    #[参数] 指定文件的写入路径
    file_path:str
):
    await page.context.storage_state(path=file_path)

#[定义函数] 返回页面 HTML 源代码
async def async_html(
    page:Page
) -> str:
    return await page.content()

"""[定义函数] 异步运行大量 page 操作"""
#[定义函数] 异步运行多个 page 操作
async def async_eval_pages(
    #[参数] 存储每一个任务元组的列表 -> [(page对象, (调用对象, (None(无参数)|{'参数名': 参数值,}))),]
    run_list: list[tuple[Page, tuple[function|type, dict[str,Any]|None]]]
) -> list[dict[Any, None] | dict[IsError,tuple[type,str,str]]]:
    ':return list[dict[执行结果, None] | dict[IsError(类本身), tuple[报错类本身, 报错字符串, 报错链字符串]]]'
    #包装单个任务
    async def _run(page:Page, func:function, kwargs:None|dict[str,Any]) -> dict[Any,None] | dict[IsError,tuple[type,str,str]]:
        try:
            #判断传入的 func 是否为异步函数
            if asyncio.iscoroutinefunction(func):
                #异步函数使用 await 执行
                if kwargs:
                    return {await func(page, **kwargs): None}
                else:
                    return {await func(page): None}
            else:
                #同步函数直接调用执行
                if kwargs:
                    return {func(page, **kwargs): None}
                else:
                    return {func(page): None}
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except SystemExit:
            raise SystemExit
        #捕捉非安全的报错 并 以报错字典形式返回
        except:
            error_class, error_str, all_error = sys.exc_info()
            #打印报错并返回报错字典
            return {IsError: (error_class, str(error_str), traceback.format_exc())}
    #构建并发任务列表
    tasks = [ 
        (_run(page, func, run_data) if run_data else _run(page, func))
        for (page, (func, run_data)) in run_list
    ]
    #并发调度所有任务并返回结果
    return await asyncio.gather(*tasks)
#[定义函数] 同步模式下直接运行 async_eval_pages 方法
def eval_pages(
    #[参数] 存储每一个任务元组的列表 -> [(page对象, (调用对象, (None(无参数)|{'参数名': 参数值,}))),]
    run_list: list[tuple[Page, tuple[function|type, dict[str,Any]|None]]]
) -> list[dict[Any, None] | dict[IsError,tuple[type,str,str]]]:
    ':return list[dict[执行结果, None] | dict[IsError(类本身), tuple[报错类本身, 报错字符串, 报错链字符串]]]'
    #直接使用 asyncio.run() 运行异步评估函数 (run 函数会自动处理事件循环的创建和销毁)
    return asyncio.run(async_eval_pages(run_list))
