
# 공통 크롤러 클래스

class BaseCollector:
    def __init__(self, name):
        self.name = name
        self.data = {}

    def fetch(self):
        raise NotImplementedError
    
    def parse(self):
        raise NotImplementedError
    
    def to_prometheus_format(self):
        output = ""

        for k,v in self.data.items():
            output += f"# HELP {k} AUTO-Collected metric\n"
            output += f"# TYPE {k} gauge\n"
            output += f"{k} {v}\n"
        return output
