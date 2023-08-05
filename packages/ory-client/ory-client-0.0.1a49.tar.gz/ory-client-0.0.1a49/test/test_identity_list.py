"""
    Ory APIs

    Documentation for all public and administrative Ory APIs. Administrative APIs can only be accessed with a valid Personal Access Token. Public APIs are mostly used in browsers.   # noqa: E501

    The version of the OpenAPI document: v0.0.1-alpha.49
    Contact: support@ory.sh
    Generated by: https://openapi-generator.tech
"""


import sys
import unittest

import ory_client
from ory_client.model.identity import Identity
globals()['Identity'] = Identity
from ory_client.model.identity_list import IdentityList


class TestIdentityList(unittest.TestCase):
    """IdentityList unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testIdentityList(self):
        """Test IdentityList"""
        # FIXME: construct object with mandatory attributes with example values
        # model = IdentityList()  # noqa: E501
        pass


if __name__ == '__main__':
    unittest.main()
