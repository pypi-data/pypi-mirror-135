import unittest

from client.common.variables import RESPONSE, ERROR, ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME
from server import create_response


class TestServer(unittest.TestCase):

    bad_response = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    good_response = {
        RESPONSE: 200
    }

    def test_no_action(self):
        self.assertEqual(create_response(
            {
                TIME: '1.1',
                USER: {
                    ACCOUNT_NAME: 'User'
                }
            }
        ), self.bad_response)

    def test_bad_action(self):
        self.assertEqual(create_response(
            {
                ACTION: 'BAD ACTION',
                TIME: '1.1',
                USER: {
                    ACCOUNT_NAME: 'User'
                }
            }
        ), self.bad_response)

    def test_no_time(self):
        self.assertEqual(create_response(
            {
                ACTION: PRESENCE,
                USER: {
                    ACCOUNT_NAME: 'User'
                }
            }
        ), self.bad_response)

    def test_no_user(self):
        self.assertEqual(create_response(
            {
                ACTION: PRESENCE,
                TIME: '1.1',
            }
        ), self.bad_response)

    def test_bad_user(self):
        self.assertEqual(create_response(
            {
                ACTION: PRESENCE,
                TIME: '1.1',
                USER: {
                    ACCOUNT_NAME: 'BAD USER'
                }
            }
        ), self.bad_response)

    def test_good_response(self):
        self.assertEqual(create_response(
            {
                ACTION: PRESENCE,
                TIME: '1.1',
                USER: {
                    ACCOUNT_NAME: 'User'
                }
            }
        ), self.good_response)


if __name__ == '__main__':
    unittest.main()