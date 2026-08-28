#作者：伊茗(微信：EviMing, QQ：2368199809, 邮箱：2368199809@qq.com)
#[伊茗的GitHub仓库] = 'https://github.com/EviMing/'
    #此文件所处项目 = 'https://github.com/EviMing/playwright-Main_Lib'

(
"""
链式操作 = `await (await (await (async_Generated_Browser_MainClass()).run(**参数)).get_Context(**参数)).get_Page()`\n\n
非链式操作 = \n\n
```
    browser = await (async_Generated_Browser_MainClass()).run(**参数)
    context = await browser.get_Context(**参数)
    page = await context.get_Page()
```

[运行方法们]
    第一个参数必须是一个异步 page 对象, 会使用 await 运行,
    第一个参数可以是已有的 Locator 对象, 作用对象则变为 Locator 对象本身, 所以标有特殊注释的函数本身就可以直接作为重载函数
        特殊注释=形参(info=True)

[eval_pages 方法们]
    直接异步运行大量 page 操作
"""
)

from playwright.async_api import (
    async_playwright, Browser, BrowserContext, Page, Locator, JSHandle,
    TimeoutError as pl_TimeoutError
)
from playwright_stealth import Stealth
import asyncio
from typing import Literal, Any
from random import uniform
import traceback
import sys

#[变量] 指定全局的 timeout(单位=秒)
global_timeout = 30

#[变量] 键盘按键名的缩写->映射为键名全称
key_map = {

    #常用修饰键
    "Ctrl": "Control",
    "Cmd": "Meta",
    "Win": "Meta",
    "Opt": "Alt",

    #方向键
    "Up": "ArrowUp",
    "Down": "ArrowDown",
    "Left": "ArrowLeft",
    "Right": "ArrowRight",

    #功能键
    "Esc": "Escape",
    "Ins": "Insert",
    "Del": "Delete",
    "PgUp": "PageUp",
    "PgDn": "PageDown",

    #回车与退格
    "Enter": "Enter",
    "Return": "Enter",
    "Bksp": "Backspace",

    #空格
    "Space": " ",

}

#[定义标识类] 用于类型注释时表示对象应为一个可调用函数或方法
class IsFunction:
    pass

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
        if isinstance(LogIn_state_FilePath, str):
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
        await stealth.apply_stealth_async(self.context)

        #为了方便链式调用, 返回 self
        return self

    #[定义方法] 返回一个异步 page 对象
    async def get_Page(self,
    ) -> Page:
        '每个异步 page 允许 \'await 函数(page对象, 参数)\' 或 \'await page对象.原生方法\' 直接运行, 或使用库提供的 \'`(async_){0,1}eval_pages`\' 方法批量运行'
        return await self.context.new_page()

#[定义类] 生成安全的浏览器实例并调用接口类达到链式操作
class async_Generated_Browser_MainClass:

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
        if proxy is not None:
            #核心键不存在则报错
            if not proxy.get('proxy'):
                raise KeyError('#-> proxy[\'proxy\'] 键不存在')
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
            proxy=(proxy_ if proxy else None),
        )

        #为了方便链式调用, 返回 self
        return self

    #[定义方法] 生成并返回一个 接口类(生成浏览器上下文) 的实例
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

"""[定义辅助方法]"""
#[定义函数] 异步 sleep
async def sleep(
    #[参数] sleep 时间, 单位=秒
    sleep_time:float
):
    await asyncio.sleep(sleep_time)

"""[定义运行方法]
    第一个参数必须是一个异步 page 对象, 会使用 await 运行,
    第一个参数可以是已有的 Locator 对象, 作用对象则变为 Locator 对象本身, 所以标有特殊注释的函数本身就可以直接作为重载函数
        特殊注释=形参(info=True)
"""
#[定义函数] 获取当前 page 的 URL
def get_url(
    #[参数] 作用的 Page 对象
    page:Page
) -> None|str:
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')
    return (x if (x:= page.url) else None)

#[定义函数] 跳转页面
async def async_goto(
    #[参数] 作用的 Page 对象
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
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')
    await page.goto(url, wait_until=wait_until, referer=(get_url(page) if referer == 'page.url' else (referer if isinstance(referer, str) else None)), timeout=int((global_timeout if timeout == 'global_timeout' else timeout)*1000))

#[定义函数] 执行JS代码
async def async_eval_js(
    #[参数] 作用的 Page 对象
    page:Page,
    #[参数] JavaScript 代码
    js_code,
    #[参数] JavaScript 参数字典 | 无参数(None)
    parameter:None|dict=None
) -> Any:
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')
    if parameter is not None:
        if not isinstance(parameter, dict):
            raise ValueError('#-> \'parameter\' 参数值应当是字典')
    return await page.evaluate(js_code, parameter)

#[定义函数] 执行JS代码并返回JSHandle对象
async def async_eval_js_handle(
    #[参数] 作用的 Page 对象
    page:Page,
    #[参数] JavaScript 代码
    js_code,
    #[参数] JavaScript 参数字典 | 无参数(None)
    parameter:None|dict=None
) -> JSHandle:
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')
    if parameter is not None:
        if not isinstance(parameter, dict):
            raise ValueError('#-> \'parameter\' 参数值应当是字典')
    return await page.evaluate_handle(js_code, parameter)

#[定义函数] 利用CSS选择器获取 (Locator 对象(建立搜索规则)) 或 元素的属性值
async def async_get_DOM(
    #[参数] 作用的 Page 对象, 或直接进行操作的 Locator 对象
    page_or_locator:Page|Locator,
    #[参数] selector=选择器 (page 为 Page 实例时提供), text=元素文本, not_text=元素不允许存在的文本
    selector:str=None, text:None|str=None, not_text:None|str=None,
    #[参数] 指定第 index 个元素, 默认 None 直接搜索元素
    index:None|Literal['all']|int=None,
    #[参数] 不为 None 时返回数据由 元素本身 变为 元素指定属性名的值 (text只要手动指定)
    get_attribute_name:None|str|Literal['text']=None,
    *,info=True
) -> (list[Locator]|Locator) | (list[str]|str):

    if not isinstance(page_or_locator, (Page, Locator)):
        raise TypeError('#-> 参数 \'page_or_locator\' 类型错误, 应当为 (playwright-Page, playwright-Locator) 之一')

    list_or_locator :list[Locator]|Locator = None
    #默认直接建立搜索规则
    if index is None:
        list_or_locator = page_or_locator.locator(selector, has_text=text, has_not_text=not_text)
    #已知索引值时对第 index 个标签建立搜索规则
    elif isinstance(index, int):
        list_or_locator = page_or_locator.locator(selector, has_text=text, has_not_text=not_text).nth(index)
    #否则返回 所有:list
    elif index == 'all':
        list_or_locator = await (page_or_locator.locator(selector, has_text=text, has_not_text=not_text)).all()
    else:
        raise ValueError('#-> \'index\' 参数值错误')

    #已知属性名时返回属性值
    if isinstance(get_attribute_name, str):
        if get_attribute_name == 'text':
            return (
            [
                (await i.text_content())
                for i in list_or_locator
            ]
            if isinstance(list_or_locator, list)
            else (await list_or_locator.text_content())
        )
        else:
            return (
                [
                    (await i.get_attribute(get_attribute_name))
                    for i in list_or_locator
                ]
                if isinstance(list_or_locator, list)
                else (await list_or_locator.get_attribute(get_attribute_name))
            )
    #否则返回元素本身
    else:
        return list_or_locator

#[定义函数] 等待元素出现
async def async_waiting_DOM(
    #[参数] 作用的 Locator 对象
    locator:Locator,
    #[参数] 元素存在的最小个数
    min_number:int=1,
    #[参数] timeout(单位=秒), 默认使用全局 timeout
    timeout:int|Literal['global_timeout']='global_timeout'
):
    if not isinstance(locator, Locator):
        raise TypeError('#-> 参数 \'Locator\' 类型错误, 应当为 \'playwright-Locator\'')
    if min_number < 1:
        raise ValueError('#-> 参数 \'min_number\' 值不应小于1')
    try:
        await locator.nth(min_number-1).wait_for(timeout=int((global_timeout if timeout == 'global_timeout' else timeout)*1000))
    except pl_TimeoutError as e:
        raise TimeoutError('#-> 函数 \'waiting_DOM\' 等待标签出现超时') from e

#[定义函数] 获取元素坐标
async def async_get_DOM_coordinate(
    #[参数] 被作用的 Locator 对象
    locator:Locator
) -> tuple[float, float]:

    if not isinstance(locator, Locator):
        raise TypeError('#-> 参数 \'Locator\' 类型错误, 应当为 \'playwright-Locator\'')
    box = await locator.bounding_box()
    x = float(box['x'] + box['width'] / 2)
    y = float(box['y'] + box['height'] / 2)
    return (x, y)

#[定义函数] 点击元素
async def async_click(
    #[参数] 被作用的 Locator 对象
    locator:Locator,
    #[参数] 指定要触发的键名, ['left','right','middle']=[左,中,右]
    button:Literal['left','right','middle']='left',
    #[参数] 坐标偏移量, 以元素中心为起点, 偏移 (x, y) 个坐标, 偏移方向=[(tuple[0]->[± x]=[+右,-左]), [± y]=[+下,-上]]
    position:None|tuple[float,float]=None
):
    if not isinstance(locator, Locator):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当为 \'playwright-Locator\'')
    await locator.hover()
    await locator.click(button=button, delay=uniform(0.080, 0.120), force=True, position=({'x': position[0], 'y': position[1]} if isinstance(position, tuple) else None))

#[定义函数] 按下单个鼠标按键
async def async_mouse_down(
    page:Page,
    #[参数] 指定要按下的键名, ['left','right','middle']=[左,中,右]
    button:Literal['left','right','middle']='left'
):
    if not isinstance(page, Page):
        raise TypeError('#-> \'page\' 参数类型错误, 应当为 \'playwright-Page\'')
    await page.mouse.down(button=button)
#[定义函数] 抬起单个鼠标按键
async def async_mouse_up(
    page:Page,
    #[参数] 指定要按下的键名, ['left','right','middle']=[左,中,右]
    button:Literal['left','right','middle']='left'
):
    if not isinstance(page, Page):
        raise TypeError('#-> \'page\' 参数类型错误, 应当为 \'playwright-Page\'')
    await page.mouse.up(button=button)
#[定义函数] 鼠标平面移动
async def async_mouse_move(
    page:Page,
    #[参数] x,y=屏幕坐标(像素值:float)
    px_tuple:tuple[float,float],
    #[参数] 移动步数, 值越大移动越慢, (1 为瞬间移动), (None 为 playwright 自己判断移动)
    steps:None|int=None
):
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 \'playwright-Page\'')
    await page.mouse.move(*px_tuple, steps=steps)
#[定义函数] 鼠标滚轮上下滚动
async def async_mouse_wheel(
    page:Page,
    #[参数] 滚动方向=[(tuple[0]->[± x]=[+右,-左]), [± y]=[+下,-上]]
    wheel_px_tuple:tuple[float,float]=(0,500)
):
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 \'playwright-Page\'')
    await page.mouse.wheel(*wheel_px_tuple)

#[定义函数] 按下单个键盘按键
async def async_key_down(
    page:Page,
    #[参数] 指定抬起的键名, 允许'+'符拼接为组合键
    key:str
):
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')

    #多键时不应当瞬间按下
    if '+' in key:
        keys = key.split('+')
        for k in keys:
            if k in key_map.keys():
                await page.keyboard.down(key_map[k])
                #键按下时, 应当滞留较长时间, 用于 视觉查找下一个键 并 手指移动按下
                await asyncio.sleep(uniform(0.100, 0.200))
            else:
                await page.keyboard.down(k)
                await asyncio.sleep(uniform(0.100, 0.200))
    #单键时应当自己控制延迟
    else:
        if key in key_map.keys():
            await page.keyboard.down(key_map[key])
        else:
            await page.keyboard.down(key)
#[定义函数] 抬起单个键盘按键
async def async_key_up(
    page:Page,
    #[参数] 指定抬起的键名, 允许'+'符拼接为组合键
    key:str
):
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')

    if '+' in key:
        keys = key.split('+')
        for k in keys:
            if k in key_map.keys():
                await page.keyboard.up(key_map[k])
                #键抬起时, 应当快速的抬起键, 以模拟人手的单指瞬间抬起
                await asyncio.sleep(uniform(0.070, 0.100))
            else:
                await page.keyboard.up(k)
                await asyncio.sleep(uniform(0.070, 0.100))
    else:
        if key in key_map.keys():
            await page.keyboard.up(key_map[key])
        else:
            await page.keyboard.up(key)

#[定义函数] 返回页面 HTML 源代码
async def async_get_html(
    page:Page
) -> str:
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')
    return await page.content()

#[定义函数] 保存登录态为 JSON 文件
async def async_save_LogIn_state(
    page:Page,
    #[参数] 指定文件的写入路径
    file_path:str
):
    if not isinstance(page, Page):
        raise TypeError('#-> 参数 \'page\' 类型错误, 应当是 playwright-Page')
    await page.context.storage_state(path=file_path)

"""[定义函数] 异步运行大量 page 操作"""
#[定义函数] 异步运行多个 page 操作
async def async_eval_pages(
    #[参数] 存储任务元组的列表 -> [(page对象|自定义参数, (调用对象, {'参数名': 参数值,} | None(无参数))),]
    run_list: list[tuple[Page|Any, tuple[IsFunction, dict[str,Any]|None]]]
) -> list[tuple[Any,] | tuple[type[IsError], tuple[type, str, str]]]:
    '''
:input `list[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`tuple[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`(Page对象 | 自定义参数),`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`tuple[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`可调用函数(第一个位置参数由 \'eval_pages\' 方法固定传参为 input 的 \'(page对象 | 自定义参数)\'),`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`dict['参数名', 参数值]`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`]`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`]`\n\n`]`\n\n
:output `list[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`[done] tuple[执行结果,]`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`[error] tuple[type[IsError], tuple[type[报错类本身], 报错字符串, 报错链字符串]]`\n\n`]`
    '''
    #包装单个任务
    async def _run(page:Page|Any, func:IsFunction, kwargs:None|dict[str, Any]) -> tuple[Any,] | tuple[type[IsError], tuple[type, str, str]]:
        try:
            #判断传入的 func 是否为异步函数
            if asyncio.iscoroutinefunction(func):
                #异步函数使用 await 执行
                if kwargs:
                    return (await func(page, **kwargs),)
                else:
                    return (await func(page),)
            else:
                #同步函数直接调用执行
                if kwargs:
                    return (func(page, **kwargs),)
                else:
                    return (func(page),)
        except KeyboardInterrupt:
            raise KeyboardInterrupt
        except SystemExit:
            raise SystemExit
        #捕捉非安全的报错 并 以报错字典形式返回
        except:
            error_class, error_str, all_error = sys.exc_info()
            #打印报错并返回报错字典
            return (IsError, (error_class, str(error_str), traceback.format_exc()))
    #构建并发任务列表
    tasks = [ 
        (_run(page, func, run_data) if run_data else _run(page, func))
        for (page, (func, run_data)) in run_list
    ]
    #并发调度所有任务并返回结果
    return await asyncio.gather(*tasks)
#[定义函数] 同步模式下直接运行 async_eval_pages 方法
def eval_pages(
    #[参数] 存储任务元组的列表 -> [(page对象|自定义参数, (调用对象, (None(无参数)|{'参数名': 参数值,}))),]
    run_list: list[tuple[Page|Any, tuple[IsFunction, dict[str,Any]|None]]]
) -> list[tuple[Any,] | tuple[type[IsError], tuple[type, str, str]]]:
    '''
:input `list[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`tuple[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`(Page对象 | 自定义参数),`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`tuple[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`可调用函数(第一个位置参数由 \'eval_pages\' 方法固定传参为 input 的 \'(page对象 | 自定义参数)\'),`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`dict['参数名', 参数值]`\n\n&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;`]`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`]`\n\n`]`\n\n
:output `list[`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`[done] tuple[执行结果,]`\n\n&nbsp;&nbsp;&nbsp;&nbsp;`[error] tuple[type[IsError], tuple[type[报错类本身], 报错字符串, 报错链字符串]]`\n\n`]`
    '''
    #直接使用 asyncio.run() 运行异步评估函数 (run 函数会自动处理事件循环的创建和销毁)
    return asyncio.run(async_eval_pages(run_list))
