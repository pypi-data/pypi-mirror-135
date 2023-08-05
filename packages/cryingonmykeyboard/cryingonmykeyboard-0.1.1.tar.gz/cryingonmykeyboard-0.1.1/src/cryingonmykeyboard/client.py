base_url="https://cryingonmykeyboard.com"

class ExceptionHandler:
    def __init__(self, project_id: str, api_version=None):
        self.project_id = project_id
        self.api_version = api_version

    def exception(self, exception_type: type, error_id: str, exception_args: object):
        path = f"/{self.project_id}/{error_id}"
        if self.api_version:
            path += f"?api_version={self.api_version}"
        url = base_url + path
        print(f"\n")
        print(f"An error occurred. More info here: {url}")
        print(f"\n")
        raise exception_type(exception_args)