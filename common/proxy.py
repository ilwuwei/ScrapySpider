from fake_useragent.fake import UserAgent
import httpx


class Proxy:
    """爬虫代理类"""

    @staticmethod
    def getProxyIpPool():
        """https代理ip池"""
        resp = httpx.get(
            "http://http.tiqu.letecs.com/getip3?num=3&type=2&pro=&city=0&yys=0&port=11&pack=266987&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4"
        )
        ip_pools = []
        if resp.status_code != 200:
            # 如果响应状态码不等于200, 则手动抛出异常
            raise Exception("代理ip获取失败, 请检查该代理是否可用!")
        data = resp.json()["data"]
        for item in data:
            ip_pools.append(f"https://{item['ip']}:{item['port']}")
        return ip_pools

    @staticmethod
    def getUaPool():
        """UA池"""
        ua_pools = [UserAgent().random for i in range(100)]
        return ua_pools
