#  (C) Copyright IBM Corp. 2021.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import unittest
from ibm_watson_machine_learning.tests.utils import is_cp4d
from ibm_watson_machine_learning.tests.autoai.abstract_tests_classes import\
    AbstractTestAutoAIDatabaseConnection


@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
class TestAutoAIMSSQLServer(AbstractTestAutoAIDatabaseConnection, unittest.TestCase):
    database_name = "sqlserver"
    schema_name = "connections"
    max_connection_nb = None


@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
class TestAutoAIDB2(AbstractTestAutoAIDatabaseConnection, unittest.TestCase):
    database_name = "db2cloud"
    schema_name = "VDH94923"
    table_name = "IRIS"
    prediction_column = "SPECIES"
    max_connection_nb = 2


@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
class TestAutoAIPostgresSQL(AbstractTestAutoAIDatabaseConnection, unittest.TestCase):
    database_name = "postgresql"
    schema_name = "public"
    max_connection_nb = None


@unittest.skipIf(not is_cp4d(), "Not supported on Cloud")
@unittest.skip("The writing of training data is broken for now.")
class TestAutoAIMySQL(AbstractTestAutoAIDatabaseConnection, unittest.TestCase):
    database_name = "mysql"
    schema_name = "mysql"
    max_connection_nb = 15

if __name__ == "__main__":
    unittest.main()
