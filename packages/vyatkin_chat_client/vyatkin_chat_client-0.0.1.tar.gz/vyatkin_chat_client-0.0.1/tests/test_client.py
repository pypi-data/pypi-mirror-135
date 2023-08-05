import unittest

from client import get_answer_server, create_send_message
from client.common.variables import RESPONSE, ERROR, TIME, ACTION, PRESENCE, USER, ACCOUNT_NAME


class TestClient(unittest.TestCase):
    message1 = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    message2 = {
        RESPONSE: 200
    }

    bad_response = "400 : Bad Request"
    good_response = '200 : OK'

    def test_bad_response(self):
        self.assertEqual(get_answer_server(self.message1), self.bad_response)

    def test_good_response(self):
        self.assertEqual(get_answer_server(self.message2), self.good_response)

    def test_no_response(self):
        self.assertEqual(get_answer_server({
            ERROR: 'Bad Request'
        }), f'Bad message')

    def test_create_message(self):
        test_message = create_send_message()
        test_message[TIME] = '1.1'
        self.assertEqual(test_message, {
            ACTION: PRESENCE,
            TIME: '1.1',
            USER: {
                ACCOUNT_NAME: 'User'
            }
        })

if __name__ == '__main__':
    unittest.main()
