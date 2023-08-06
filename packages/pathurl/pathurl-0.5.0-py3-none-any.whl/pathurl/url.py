from typing import Union
from urllib.parse import urljoin, urlsplit, urlunsplit

from pathurl._constants import Port
from pathurl.path import Path
from pathurl.query import Query


class URL:
    __slots__ = [
        "_string",
        "_netloc",
        "_scheme",
        "_username",
        "_password",
        "_hostname",
        "_port",
        "_path",
        "_query",
        "_fragment",
    ]

    def __init__(self, string: str = ""):
        parsed_url = urlsplit(string)
        self._string = string
        self._netloc = parsed_url.netloc
        self._scheme = parsed_url.scheme
        self._username = parsed_url.username
        self._hostname = parsed_url.hostname
        self._password = parsed_url.password
        self._port = parsed_url.port or self._infer_port(self._scheme)
        self._path = Path(parsed_url.path)
        self._query = Query(parsed_url.query)
        self._fragment = parsed_url.fragment

    def __str__(self):
        return self._string

    def __hash__(self) -> int:
        return hash(self._string)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self._string == other._string

    def __repr__(self):
        return f"URL('{self}')"

    def __bool__(self) -> bool:
        return bool(self._string)

    @property
    def string(self) -> str:
        return self._string

    @property
    def netloc(self) -> str:
        return self._netloc

    @property
    def scheme(self) -> str:
        return self._scheme

    @property
    def username(self) -> str:
        return self._username

    @property
    def hostname(self) -> str:
        return self._hostname

    @property
    def password(self) -> str:
        return self._password

    @property
    def port(self) -> int:
        return self._port

    @property
    def path(self) -> Path:
        return self._path

    @property
    def query(self) -> Query:
        return self._query

    @property
    def fragment(self) -> str:
        return self._fragment

    @staticmethod
    def _infer_port(scheme: str) -> int:
        try:
            port = Port[scheme]
        except KeyError:
            return None

        return port.value

    @classmethod
    def _create_netloc(
        cls, scheme: str, username: str, password: str, hostname: str, port: int
    ) -> str:
        parts = []
        if username or password:
            if username:
                parts.append(username)
            if password:
                parts.append(f":{password}")
            parts.append("@")
        parts.append(hostname)
        if port and port != cls._infer_port(scheme):
            parts.append(f":{port}")
        return "".join(parts)

    @classmethod
    def _from_parts(
        cls,
        scheme: str,
        username: str,
        password: str,
        hostname: str,
        port: int,
        path: Union[str, Path],
        query: Union[str, Query],
        fragment: str,
    ) -> "URL":
        netloc = cls._create_netloc(scheme, username, password, hostname, port)
        return cls(urlunsplit((scheme, netloc, str(path), str(query), fragment)))

    def replace(self, **kwargs) -> "URL":
        parts = {
            "scheme",
            "username",
            "password",
            "hostname",
            "port",
            "path",
            "query",
            "fragment",
        }
        for part in parts:
            kwargs.setdefault(part, getattr(self, part))
        return self._from_parts(**kwargs)

    def join(self, path: Union[str, Path]) -> "URL":
        return self.__class__(urljoin(str(self), str(path)))
