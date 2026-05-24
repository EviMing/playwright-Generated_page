作者：伊茗(QQ：2368199809，邮箱：__2368199809@qq.com__)

注释：由于我懒得一个个对方法进行排序，所以MD源代码里有序列表统一用'`1.`'，转HTML时交给库来渲染

# 注释：
1. 该项目是一套基于'playwright'库的方法集，定义了常用的操作，可以用更方便的语句操作page
1. **`实例.page`** 可以访问playwright的原page对象，当方法集里的方法不足以构成程序的全部逻辑时，可以通过 __实例.page__ 调用原page对象的方法

### 遇到奇奇怪怪的bug时：
1. 当 鼠标按下或抬起按键 不执行时：可以 在需要抬起的地方重新执行一遍 按下再抬起，或 在需要按下的地方重新执行一遍 抬起再按下，第一个步骤可以重置鼠标或键盘状态，第二个步骤就能正常执行了，原因：#库的bug，滑动时不会保留'鼠标按键按下'的状态，会导致抬起或按下按键失效，需要手动重新补全一次操作
# 核心类的使用说明
1. **Generated_page.py** 核心库，里面定义了一个核心类 **Generated_page**

    **Generated_page** 类的方法：

    1. **__init__** 初始化方法，参数：
        - **LogIn_state_FilePath** 登录状态文件路径，为 __None__ 时表示不进行自动登录，为 __字符串__ 时表示从传参的路径中读取登录态
        - **look_window** 是否显示浏览器窗口，为 __True__ 时显示，为 __False__ 时不显示
        - **browser_path** 指定 __浏览器.exe__ 可执行文件路径
        - **proxy** 字典，结构：{
                'proxy': '代理地址',
                'user': '提供账号，默认为 None',
                'password': '提供密码，默认为 None',
                'bypass': '不走代理的地址，每个用逗号分隔'
            }

    1. **goto** 跳转页面，参数：
        - **url** 跳转的页面
            //跳转时默认等待页面 __DOMContentLoaded__ 事件触发时停止

    1. **eval_js** 执行JavaScript代码，参数：
        - **js_code** 执行的JavaScript代码，如果要有返回给 Python 的返回值，则必须是一个 __箭头函数__
        - **parameter** 当箭头函数需要参数时传参，除第一个参数以外的位置参数都会视为 __parameter__ 参数的一部分

    1. **eval_js_handle** 执行JavaScript代码，但返回的是一个JavaScript对象，且可以被再次传入给执行方法
        **参数和 eval_js 一样**

    1. **get_DOM** 获取页面 DOM，参数：
        - **css_selector** CSS选择器，用于查找页面元素
        - **get_attribute_name** 获取的属性名，为 __None__ 时表示获取元素本身，为 __字符串__ 时表示获取元素的属性值

    1. **click** 直接点击页面元素，先移动，再点击，参数：
        - **css_selector** CSS选择器，用于查找页面元素
        - **文本**元素的文本内容，为 __None__ 时直接用CSS查找元素，为__字符串__时表示指定元素的文本内容
        - **索引**元素的索引，默认为 __None__，当存在多个被选中元素时，需要提供 __整数__ 参数表示获取指定索引的元素

    1. **get_element_coordinate** 获取页面元素坐标，参数：
        - **css_selector** CSS选择器，用于查找页面元素
        - **文本**元素的文本内容，为 __None__ 时直接用CSS查找元素，为 __字符串__ 时表示指定元素的文本内容

    1. **mouse_move** 鼠标指针移动，参数：
        - **x** 目标X轴坐标
        - **y** 目标Y轴坐标
        - **steps** 将鼠标移动分为指定个步骤移动，默认为 __None__
            //if (steps>1){由playwright在移动过程中插入多个中间坐标点，并依次移动鼠标} 步骤越多，鼠标移动越平滑
            //if (steps<=1){鼠标会瞬间移动到目标坐标}

    1. **mose_wheel** 模拟鼠标滚轮，参数：
        - **delta_x** X轴滚动量，__正数__ 时向右滚动指定像素，__负数__ 时向左滚动指定像素
        - **delta_y** Y轴滚动量，__正数__ 时向下滚动指定像素，__负数__ 时向上滚动指定像素

    1. **mouse_key_down** 单个鼠标按键按下，参数：
        - **key** 按下的按键名，`['left', 'middle', 'right']` 分别表示 `['左键', '中键', '右键']`

    1. **mouse_key_up** 单个鼠标按键抬起，参数：
        - **key** 抬起的按键名，`['left', 'middle', 'right']` 分别表示 `['左键', '中键', '右键']`

    1. **key_press** 单个键盘按键按下，参数：
        **key** 按下的按键名

    1. **key_up** 单个键盘按键抬起，参数：
        **key** 抬起的按键名

    1. **save_LogIn_state** 保存登录态为 __JSON__ 文件，参数：
        - **FilePath** 保存登录态的文件路径

    1. **html** 返回当前的页面 __HTML__ 源代码，无参数

    1. **close** 关闭实例并卸载内存，无参数

# 基于核心类的子类
1. **exe_get_page** 通过端口接管已有的浏览器进程

    ```注释
        对于封装了浏览器的exe程序，一般可通过启动时给exe传参 '--remote-debugging-port=端口' 启动调试端口
            如果是 Electron 应用，有时会有两个调试端口(一个给主进程，一个给渲染进程/网页内容)
                如果连接后找不到页面，可以尝试访问 'http://localhost:端口/json'，查看具体的调试 WebSocket 地址
                    或 'http://localhost:端口/json/version'，webSocketDebuggerUrl 地址
                    对于DrissionPage库，大部分情况下直接连接 '127.0.0.1:调试端口' 即可
    ```
    ```Python
        import requests
        json = requests.get(f'{url}:{port}/version').json()
        debug_url = json['webSocketDebuggerUrl']
    ```

    **exe_get_page** 类的方法：

    1. **__init__** 初始化方法，参数：
        **url** 指定目标IP或URL，默认 __`http://localhost`==`http://127.0.0.1`__
        **port** 指定目标端口，默认 **9222**
        **context_index** 浏览器上下文索引，当存在多个 __浏览器上下文__ 时，即多个 __浏览器窗口__ 时，可主动选择
            //对于 __Electron__ 应用这种，exe 打开后的用户看到的上下文索引一般为 __0__
        **page_index** page页索引，当存在多个 __page页__，即 __浏览器标签__ 时，可主动选择
            //对于 __Electron__ 应用这种，exe 打开后的用户看到的page页索引一般为 __0__
