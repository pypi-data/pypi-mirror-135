from lark import Lark, Transformer
from catswalk.scraping.webdriver import CWWebDriver
from catswalk.scraping.types.type_webdriver import *
import os
import time


def execute(request: CWWebDriver, order_name: str, grammar_path: str, order_path: str, url:str, output_path:str, filename:str) -> str:
    class Main(Transformer):
        def __init__(self):
            self._functions = {}
        
        def open_call(self, token):
            print(f"open: {url}")
            if request:
                request.get(url=url)

        def transition(self, token):
            _url = token[0]
            if _url == "URL":
                _url = url
            print(f"open: {_url}")
            if request:
                request.get(url=_url)

        def move_by_class(self, token):
            class_name = token[0]
            print(f"move_by_class: {class_name}")
            if request:
                request.move_to_element_by_class_name(class_name=class_name)

        def click_by_class(self, token):
            class_name = token[0]
            print(f"click_by_class: {class_name}")
            if request:
                request.click_by_class_name(class_name=class_name)


        def click_by_class_when_exist(self, token):
            class_name = token[0]
            print(f"click_by_class_when_exist: {class_name}")
            if request:
                request.click_by_class_name(class_name=class_name, check_exist=True)


        def capture_by_screen(self, token):
            __output_path = f"{output_path}/{order_name}"
            print(f"capture_by_screen: {__output_path}, {filename}")
            if request:
                # mkdirs
                os.makedirs(__output_path, exist_ok=True)
                fullpath = request.print_screen_by_window(__output_path, filename)
                return fullpath
        
        def capture_by_hight(self, token):
            hight = token[0]
            __output_path = f"{output_path}/{order_name}"
            print(f"capture_by_screen: {__output_path}, {filename}, {hight}")
            if request:
                # mkdirs
                os.makedirs(__output_path, exist_ok=True)
                if request.execution_env == "local":
                    fullpath = request.print_screen_by_hight(hight, __output_path, filename)
                else:
                    fullpath = request.print_screen_by_hight(hight, __output_path, filename, 2)
                return fullpath

        def wait_by_class(self, token):
            class_name = token[0]
            print(f"wait_by_class: {class_name}")
            if request:
                request.get_elem_by_class(class_name)

        def wait_by_time(self, token):
            _time = int(token[0])
            print(f"wait_by_time: {_time}")
            time.sleep(_time)

        def symbol(self, token):
            return token[0].value

        def string(self, token):
            return token[0][1:-1]

    rule = open(grammar_path).read()
    parser = Lark(rule, parser='lalr', transformer=Main())
    program = open(order_path).read()
    r = parser.parse(program)
    fullpath = list(r.children)[-1]
    print(r)
    return fullpath