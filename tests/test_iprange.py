import unittest
from iprange import IPRange
from mock import patch


class IPRangeTest(unittest.TestCase):
    def setUp(self):
        self.iprange = IPRange(redis_key='IPRangeTest')

    def tearDown(self):
        self.iprange.remove('0.0.0.0/0')
        self.iprange.remove('192.168.0.1/24')
        self.iprange.remove('router1:192.168.0.1/24')

    @patch('redis.StrictRedis')
    def test_simple_redis_connection(self, mocked_redis):
        IPRange()
        mocked_redis.assert_called_with(encoding='utf-8', decode_responses=True)

    @patch('redis.StrictRedis')
    def test_redis_connection_with_args(self, mocked_redis):
        redis_key = 'another_redis_key'
        host, port, db = ['127.0.0.1', 63790, 5]
        iprange = IPRange(redis_key, host=host, port=port, db=db)
        self.assertEqual(redis_key, iprange.redis_key)
        mocked_redis.assert_called_with(host=host, port=port, db=5, encoding='utf-8', decode_responses=True)

    @patch('rediscluster.RedisCluster')
    def test_redis_cluster_connection(self, mocked_redis_cluster):
        IPRange(redis_cluster=True)
        mocked_redis_cluster.assert_called_with(encoding='utf-8', decode_responses=True)

    @patch('rediscluster.RedisCluster')
    def test_redis_cluster_connection_with_args(self, mocked_redis_cluster):
        redis_key = 'another_redis_key'
        startup_nodes = [{'host': '127.0.0.1', 'port': 16379}]
        iprange = IPRange(redis_key, redis_cluster=True, startup_nodes=startup_nodes)
        self.assertEqual(redis_key, iprange.redis_key)
        mocked_redis_cluster.assert_called_with(startup_nodes=startup_nodes, encoding='utf-8', decode_responses=True)

    # should find it back
    def test_successful_find(self):
        self.iprange.add('192.168.0.1/24', {'some': 'data', 'more': 'metadata'})
        response = self.iprange.find('192.168.0.20')
        self.assertEqual('192.168.0.1/24', response['range'])
        self.assertEqual('data', response['some'])
        self.assertEqual('metadata', response['more'])

    # should return None for a smaller ip that is not in range
    def test_return_none_for_smaller_ip(self):
        response = self.iprange.find('192.167.255.255')
        self.assertIsNone(response)

    # should return None for greater ip that is not in range
    def test_return_none_for_greater_ip(self):
        response = self.iprange.find('192.169.0.1')
        self.assertIsNone(response)

    # when a range is added with extra key, should find it with that key
    def test_find_with_other_key(self):
        self.iprange.add('192.168.0.1/24', {'key': 'router1'})
        response = self.iprange.find('192.168.0.20')
        self.assertEqual('router1:192.168.0.1/24', response['range'])

    # when there is multiple ranges with overlap, it should find the most specific range
    def test_find_most_specific(self):
        self.iprange.add('0.0.0.0/0')
        self.iprange.add('192.168.0.1/24')
        response = self.iprange.find('192.168.0.20')
        self.assertEqual('192.168.0.1/24', response['range'])

    # when there is multiple ranges with overlap, it should find all the ranges
    def test_find_all_ranges(self):
        self.iprange.add('0.0.0.0/0')
        self.iprange.add('192.168.0.1/24')
        response = self.iprange.find_all('192.168.0.20')
        expected = [
            {'range': '192.168.0.1/24'},
            {'range': '0.0.0.0/0'}
        ]
        self.assertListEqual(expected, response)
