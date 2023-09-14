import requests


def get_package_info(pkg_name: str):
    r = requests.get(f"https://pypi.org/pypi/{pkg_name}/json")
    print(r.status_code)
    data = r.json()

    # Retrieve the list of (non-yanked) versions released
    versions = [version for version, info in data["releases"].items()]
    print(len(versions))
    versions = [version for version, info in data["releases"].items() if not info[0]["yanked"]]
    print(len(versions))