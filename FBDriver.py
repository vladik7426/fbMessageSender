from selenium.webdriver import Proxy
from selenium.webdriver.common.proxy import ProxyType
from undetected_chromedriver import Chrome, ChromeOptions

from config import facebook_config
from utils.fb_accounts import next_account_cookies


class FBDriver(Chrome):
    """
    Ready driver with user authorized with cookies.
    """

    def __init__(self, **kwargs):
        """
        Creates new driver with user authorized with cookies.
        """
        self.options = ChromeOptions()

        self.options.proxy = Proxy({
            'proxyType': ProxyType.MANUAL,
            'httpProxy': facebook_config.proxy,
            'ftpProxy': facebook_config.proxy,
            'sslProxy': facebook_config.proxy,
            'noProxy': '',
        })

        self.options.add_argument("--headless")
        self.options.add_argument("start-maximized")
        self.options.add_argument("--disable-extensions")
        self.options.add_argument("--disable-gpu")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--no-sandbox")

        super().__init__(options=self.options, **kwargs)

        self.get('https://facebook.com')

        for cookie in next_account_cookies():
            self.add_cookie(cookie)
