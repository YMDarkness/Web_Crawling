from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 공통 크롤러 클래스

class BaseCrawler:
    '''
    requests 기반

    def __init__(self, name):
        self.name = name
        self.data = {}

    def fetch_data(self):
        raise NotImplementedError
    
    def parse_data(self):
        raise NotImplementedError
    
    def prometheus_format(self):
        output = ""

        for k, v in self.data.items():
            output += f'# HELP {k} AUTO-Collected metric\n'
            output += f'# TYPE {k} gauge\n'
            outpur += f'{k} {v}\n'
        return output
    '''

    # Seleium 기반
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.driver = self._init_driver()

    def _init_driver(self):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        return webdriver.Chrome(options=options)
    
    def fetch_data(self, url, wait_selector=None):
        self.driver.get(url)
        if wait_selector:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located(wait_selector)
            )
        self.html = self.driver.page_source

    def prometheus_format(self):
        lines = []
        for key, value in self.data.items():
            metrics = f'{self.name}_{key}'.replace('.', '')
            lines.append(f'{metrics} {value}')
        return '\n'.join(lines) + '\n'
    
    def quit(self):
        self.driver.quit()
        