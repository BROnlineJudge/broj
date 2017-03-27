# -*- coding: utf-8 -*-
from mock import MagicMock, patch
from ej import connections
from ej import exceptions
import unittest


class TestConnections(unittest.TestCase):
    def test_compress_decompress(self):
        compressions = [
            ({'key': 'value'}, b'x\x9c\xabV\xcaN\xadT\xb2RP*K\xcc)MU\xaa\x05\x00+\xaf\x05A'),  # noqa: E501
            ({'language': 'cpp', 'code': 'int main() { return 0; }', 'problem': 1, 'user': 1}, b'x\x9c\xabV\xcaI\xccK/MLOU\xb2RPJ.(P\xd2\x01R\xf9)`nf^\x89Bnbf\x9e\x86\xa6B\xb5BQjIiQ\x9e\x82\x81\xb5B-HMAQ~RNj.P\x99!\x90WZ\x9cZ\x04b\xd6\x02\x00\xe4+\x17\xf5')  # noqa: E501
        ]

        for k, v in compressions:
            c = connections._compress(k)
            self.assertEqual(c, v)
            d = connections.decompress(c)
            self.assertEqual(d, k)


class TestJudgeConnection(unittest.TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.lang = 'cpp'
        self.judge_conn = connections.JudgeConnection(host=self.host,
                                                      language=self.lang)

    def test_init(self):
        self.assertEqual(self.judge_conn.host, self.host)
        self.assertEqual(self.judge_conn.language, self.lang)
        self.assertIsNone(self.judge_conn.connection)
        self.assertIsNone(self.judge_conn.channel)

    @patch('ej.connections.JudgeConnection.connect')
    def test_enter_and_exit(self, mock_connect):
        self.judge_conn.connection = MagicMock()
        self.judge_conn.channel = MagicMock()
        with self.judge_conn:
            pass
        mock_connect.assert_called_once()
        self.assertTrue(self.judge_conn.channel.close.called)
        self.assertTrue(self.judge_conn.connection.close.called)

    def test_connect_unsupported_language(self):
        self.judge_conn.language = 'XxXxX'
        with self.assertRaises(exceptions.JudgeConnectionError):
            self.judge_conn.connect()

    @patch('pika.ConnectionParameters')
    def test_connect_raises_on_issue(self, mock_cp):
        with self.assertRaises(exceptions.JudgeConnectionError):
            self.judge_conn.connect()

    def test_send_before_connect_raises(self):
        with self.assertRaises(exceptions.JudgeConnectionError):
            self.judge_conn.send(None)

    def test_consume_before_connect_raises(self):
        with self.assertRaises(exceptions.JudgeConnectionError):
            self.judge_conn.consume(None)


class TestCourierConnection(unittest.TestCase):
    def setUp(self):
        self.host = 'localhost'
        self.courier_conn = connections.CourierConnection(host=self.host)

    def test_init(self):
        self.assertEqual(self.courier_conn.host, self.host)
        self.assertIsNone(self.courier_conn.connection)
        self.assertIsNone(self.courier_conn.channel)

    @patch('ej.connections.CourierConnection.connect')
    def test_enter_and_exit(self, mock_connect):
        self.courier_conn.connection = MagicMock()
        self.courier_conn.channel = MagicMock()
        with self.courier_conn:
            pass
        mock_connect.assert_called_once()
        self.assertTrue(self.courier_conn.channel.close.called)
        self.assertTrue(self.courier_conn.connection.close.called)

    @patch('pika.ConnectionParameters')
    def test_connect_raises_on_issue(self, mock_cp):
        with self.assertRaises(exceptions.CourierConnectionError):
            self.courier_conn.connect()

    def test_send_before_connect_raises(self):
        with self.assertRaises(exceptions.CourierConnectionError):
            self.courier_conn.send(None)

    def test_consume_before_connect_raises(self):
        with self.assertRaises(exceptions.CourierConnectionError):
            self.courier_conn.consume(None)


if __name__ == '__main__':
    unittest.main()
