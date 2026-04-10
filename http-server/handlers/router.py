import re
from http.response import HttpResponse


class Route:
    def __init__(self, path, handler):
        self.path = path
        self.handler = handler
        self.param_names = []

        # Convert /user/{id} → regex
        pattern = self._convert_path_to_regex(path)
        self.regex = re.compile(f"^{pattern}$")

    def _convert_path_to_regex(self, path):
        parts = path.strip("/").split("/")
        regex_parts = []

        for part in parts:
            if part.startswith("{") and part.endswith("}"):
                param_name = part[1:-1]
                self.param_names.append(param_name)
                regex_parts.append(r"([^/]+)")
            else:
                regex_parts.append(part)

        return "/" + "/".join(regex_parts)

    def match(self, request_path):
        match = self.regex.match(request_path)
        if not match:
            return None

        values = match.groups()
        params = dict(zip(self.param_names, values))
        return params


class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, handler):
        self.routes.append(Route(path, handler))

    def resolve(self, request):
        for route in self.routes:
            params = route.match(request.path)
            if params is not None:
                request.path_params = params
                return route.handler

        return self.default_404

    def default_404(self, request):
        return HttpResponse("<h1>404 Not Found</h1>", status=404)