"""
    Copyright 2017 Inmanta

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Contact: code@inmanta.com
"""


def test_rest_base(project):
    """ test using the postman echo service """
    testurl = "https://postman-echo.com/get"
    project.compile(
        """
import rest
rest::RESTCall(url="%(testurl)s", body={"a":"test", "b":{"c":3}}, headers={"h":"x"})
        """
        % {"testurl": testurl}
    )

    e = project.deploy_resource("rest::RESTCall")
    project.deploy(e)
