# motified version of http://oschub.asia/

from __future__ import print_function

import time
import logging

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(levelname)s] (%(threadName)-10s) %(message)s',
)


# TODO: generate from sc source code
SC_COMMANDS = set([
    "/quit", "/notify", "/cmd", "/dumpOSC", "/sync", "/clearSched", "/error",
    "/d_recv", "/d_load", "/d_loadDir", "/d_free",
    "/n_free", "/n_run", "/n_set", "/n_setn", "/n_fill",
    "/n_map", "/n_mapn", "/n_mapa", "/n_mapan", "/n_before",
    "/n_after", "/n_query", "/n_trace", "/n_order",
    "/s_new", "/s_get", "/s_getn", "/s_noid",
    "/g_new", "/p_new", "/g_head", "/g_tail", "/g_freeAll",
    "/g_deepFree", "/g_dumpTree", "/g_queryTree",
    "/u_cmd", "/b_alloc", "/b_allocRead", "/b_allocReadChannel",
    "/b_read", "/b_readChannel", "/b_write", "/b_free",
    "/b_zero", "/b_set", "/b_setn", "/b_fill", "/b_gen",
    "/b_close", "/b_query", "/b_get", "/b_getn",
    "/c_set", "/c_setn", "/c_fill", "/c_get", "/c_getn",
    "/nrt_end",
    "/late",
    "/n_go", "/n_end", "/n_off", "/n_on", "/n_move", "/n_info",
    "/tr",
    "/chat",
    "/done",
    "/keepAlive", "/h_comm",
    "/pauseHUB", "/quitHUB", "/dumpHUB"
])


class OscHubServer(DatagramProtocol):

    """server for forwarding oschub msg to multiple clients"""

    def __init__(self):
        super(OscHubServer, self).__init__()
        self._clients = {}
        self._l = logging.info

    def _refresh_client(self, addr):
        if addr not in self._clients:
            self._l("new client connected", addr)
        self._clients[addr] = time.time()

    def _is_osc_command(self, data):
        return True

    def datagramReceived(self, data, addr):
        self._l("received %r from %s", data, addr)
        for client in self._clients:
            self.transport.write(data, client)
        self._refresh_client(addr)

reactor.listenUDP(9999, OscHubServer())
reactor.run()
