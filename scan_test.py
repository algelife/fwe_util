import unittest
from scan import validate_hostname, determine_protocol, check_service_status

class ServiceStatusTest(unittest.TestCase):
    def test_valid_hostname(self):
        hostname = "www.google.com"
        ip_address = validate_hostname(hostname)
        self.assertIsNotNone(ip_address)

    def test_invalid_hostname(self):
        hostname = "none_existing_web.com"
        ip_address = validate_hostname(hostname)
        self.assertIsNone(ip_address)

    def test_determine_protocol(self):
        hostname = "www.google.com"
        port = 80
        protocol = determine_protocol(hostname, port)
        self.assertIn(protocol, ["TCP", "UDP"])

    def test_check_service_status(self):
        hostname = "www.google.com"
        port = 80
        ip_address, protocol = check_service_status(hostname, port)
        self.assertIsNotNone(ip_address)
        self.assertIsNotNone(protocol)

if __name__ == '__main__':
    unittest.main()