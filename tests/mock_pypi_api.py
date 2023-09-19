import re

import requests


class ResponseOk:
    def __init__(self):
        self.status_code = 200

    def json(self):
        return {
            "releases": {
                "v1.2.10": [
                    {
                        "upload_time": "2021-08-09T14:27:16",
                        "yanked": False,
                    }
                ],
                "v1.1.0": [
                    {
                        "upload_time": "2021-06-09T14:27:16",
                        "yanked": True,
                    }
                ],
                "v0.2.0": [
                    {
                        "upload_time": "2021-05-09T14:27:16",
                        "yanked": False,
                    }
                ],
            }
        }


class Response404:
    def __init__(self):
        self.status_code = 404

    def json(self):
        return {"message": "Not Found"}


class Response301:
    def __init__(self):
        self.status_code = 301

    def json(self):
        return {"message": "Redirected"}


def mock_get(url: str):
    z = re.match(r"https://pypi.org/pypi/([^/]+)/json", url)
    assert z, f"Oblique is trying to access {url}, which is not mocked. Can't run the test."

    pkg_name = z.group(1)

    if pkg_name == "transformers":
        return ResponseOk()
    elif pkg_name == "lisduyfg":
        return Response404()
    elif pkg_name == "redirected":
        return Response301()
    else:
        assert False, f"Oblique is trying to access package `{pkg_name}`, which is not mocked. Can't run the test."


# Mock the `get` function of requests
requests.get = mock_get
