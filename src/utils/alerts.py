import os
import logging

import requests


class AlertHandler(logging.Handler):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.url = kwargs['url']

    def emit(self, record):
        message = self.format(record)
        priority = int(logging.getLevelNamesMapping()[record.levelname]//10)
        title = "Advent Of Code Handler"
        try:
            requests.post(self.url,
                          data=message,
                          headers={"Priority": str(priority), "Title": str(title)})
        except Exception:
            pass
