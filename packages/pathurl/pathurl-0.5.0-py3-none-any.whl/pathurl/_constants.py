from enum import Enum


class Port(Enum):
    ftp = 21
    sftp = 22
    ssh = 22
    telnet = 23
    dns = 53
    gopher = 70
    http = 80
    ws = 80
    https = 443
    wss = 443
    ipp = 631
    ipps = 631
    mariadb = 3306
    mysql = 3306
    postgres = 5432
    postgresql = 5432
    redshift = 5439
    redis = 6379
    git = 9418
    mongodb = 27017
