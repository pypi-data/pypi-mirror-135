# -*- encoding=utf-8 *-*
"""
    author: Li Junxian
    function: cookie
"""
from urllib.parse import urlparse


class CookiesUtils(object):

    @staticmethod
    def __is_match(url, domain):
        """
        判断domain是否匹配host
        :param domain:
        :return:
        """
        parse_ret = urlparse(url)
        hostname = parse_ret.hostname
        if hostname is None:
            return False
        if hostname.endswith(domain):
            return True
        return False

    @staticmethod
    def merge_requests_to_selenium(session, driver):
        if session is None or driver is None:
            return driver
        url = driver.current_url
        for cookie in session.cookies:
            cookie_ = {"name": cookie.name, "value": cookie.value}
            if cookie.path is not None:
                cookie_["path"] = cookie.path
            if cookie.domain is not None:
                domain = cookie.domain
                if not CookiesUtils.__is_match(url, domain):
                    continue
                cookie_["domain"] = cookie.domain
            if cookie.secure is not None:
                cookie_["secure"] = cookie.secure
            if cookie.expires is not None:
                cookie_["expiry"] = cookie.expires
            driver.delete_cookie(cookie.name)
            driver.add_cookie(cookie_)
        return driver

    @staticmethod
    def merge_selenium_to_requests(driver, session):
        if driver is None or session is None:
            return session
        cookies = driver.get_cookies()
        for cookie in cookies:
            name = cookie.get("name")
            value = cookie.get("value")
            optional = {}
            if cookie.get("domain") is not None:
                optional['domain'] = cookie.get("domain")
            if cookie.get("expiry") is not None:
                optional['expires'] = cookie.get("expiry")
            if cookie.get("path") is not None:
                optional['path'] = cookie.get("path")
            if cookie.get("secure") is not None:
                optional['secure'] = cookie.get("secure")
            if cookie.get("httpOnly") is not None:
                optional['rest'] = {'HttpOnly': cookie.get("httpOnly")},
            session.cookies.set(name, value, **optional)
        return session
