import requests


class GetIPAddressError(Exception):
    pass


class SomeClass(object):
    def __init__(self, name):
        self.name = name
        self.session = None

    def add_numbers(self, a, b):
        for k, v in {'a': a, 'b': b}.items():
            if isinstance(v, (int, float)):
                continue

            raise TypeError('expected {} to be {} or {} but was {}'.format(
                k, type(1), type(1.337), type(v)
            ))

        return 'Hi {}, {} + {} = {}'.format(
            self.name, a, b, a + b
        )

    def get_ip_address(self):
        if self.session is None:
            self.session = requests.Session()

        response = self.session.get('http://ifconfig.co/json')
        if response.status_code not in [200, 201]:
            raise GetIPAddressError('expected status code of 200 or 201, instead got {}'.format(
                response.status_code
            ))

        return response.json().get('ip')
