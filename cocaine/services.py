# encoding: utf-8
#
#    Copyright (c) 2011-2013 Anton Tyurin <noxiouz@yandex.ru>
#    Copyright (c) 2011-2013 Other contributors as noted in the AUTHORS file.
#
#    This file is part of Cocaine.
#
#    Cocaine is free software; you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#
#    Cocaine is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>. 
#

import sys

from asio_worker import ev
from asio_worker.pipe import ServicePipe
from asio_worker.stream import ReadableStream
from asio_worker.stream import WritableStream
from asio_worker.stream import Decoder
from asio_worker.log_message import PROTOCOL_LIST
from asio_worker.log_message import Message

class _BaseService(object):

    def __init__(self, endpoint):
        self.m_service = ev.Service()
        self.m_pipe = ServicePipe(endpoint)
        self.m_app_name = sys.argv[sys.argv.index("--app") + 1]

        self.m_decoder = Decoder()
        self.m_decoder.bind(self.on_message)

        self.m_w_stream = WritableStream(self.m_service, self.m_pipe)
        self.m_r_stream = ReadableStream(self.m_service, self.m_pipe)
        self.m_r_stream.bind(self.m_decoder.decode)

        self.m_service.register_callback(self.m_r_stream._on_event, self.m_pipe.fileno(), self.m_service.READ)
        self.m_service.register_callback(self.m_w_stream._on_event, self.m_pipe.fileno(), self.m_service.WRITE)
        self.m_service.bind_on_fd(self.m_pipe.fileno())

    def on_message(self, *args):
        pass

class Log(_BaseService):

    def __init__(self):
        super(Log, self).__init__(('localhost', 12501))
        self.m_target = "app/%s" % self.m_app_name

    def debug(self, data):
        self.m_w_stream.write(Message("Message", 4, self.m_target, data).pack())

    def info(self, data):
        self.m_w_stream.write(Message("Message", 3, self.m_target, data).pack())

    def warn(self, data):
        self.m_w_stream.write(Message("Message", 2, self.m_target, data).pack())

    def error(self, data):
        self.m_w_stream.write(Message("Message", 1, self.m_target, data).pack())