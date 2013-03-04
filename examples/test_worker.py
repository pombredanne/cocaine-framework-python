#! /usr/bin/env python

from cocaine.worker import Worker
from cocaine.decorators import *
from cocaine.services import Log

from hashlib import sha512

l = Log()
l.info("INFO")
l.debug("DEBUG")
l.error("ERROR")
l.warn("WARN")

@ProxyHTTP
def http_ok(response):
    headers = yield
    result = "<html><head>Hash</head>%s</html>\r\n" % sha512(str(headers)).hexdigest()
    l.info(result)
    response.write_head( 200, {'Content-Type' : 'text/plain'})
    response.write(result)
    response.close()


W = Worker()
W.on("hash",http_ok)
W.on("fs",http_ok)
W.run()