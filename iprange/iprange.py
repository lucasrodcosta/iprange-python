import redis
from netaddr import IPNetwork


class IPRange:
    def __init__(self, redis_key='ip_table', **kwargs):
        self.redis_key = redis_key
        self.redis = redis.StrictRedis(**kwargs)

    def remove(self, range):
        self.redis.execute_command('irem', self.redis_key, range)
        self.redis.delete(self.metadata_key(range))

    def add(self, range, metadata={}):
        ips = IPNetwork(range)

        if 'key' in metadata:
            range = "{}:{}".format(metadata['key'], range)

        self.redis.execute_command('iadd', self.redis_key, ips.first, ips.last, range)
        hash = self.metadata_key(range)
        if metadata:
            self.redis.hmset(hash, metadata)

    def find(self, ip):
        all = self.find_all(ip)
        return all[0] if all else None

    def find_all(self, ip):
        ipaddr = IPNetwork(ip)
        ranges = self.redis.execute_command('istab', self.redis_key, ipaddr.value)
        all = []
        for range in ranges:
            metadata = self.redis.hgetall(self.metadata_key(range))
            result = {'range': range}
            result.update(metadata)
            all.append(result)
        return all

    def metadata_key(self, range):
        return "{}:{}".format(self.redis_key, range)
