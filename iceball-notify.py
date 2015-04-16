# Copyright (c) 2013 Marco Schlumpp
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import notify2
import json
import urllib2
import time

if __name__ == "__main__":
    notify2.init("iceball-notify")
    lastlist = {"servers": []}
    while True:
        # Download server list
        jsn = {}
        fobj = urllib2.urlopen("http://magicannon.com:27790/master.json")
        jsn = json.load(fobj)
        fobj.close()

        for server in jsn[u"servers"]:
            if server["name"] in [s["name"] for s in lastlist["servers"]]: # Generate list of all names
                # Known server
                previousentry = None
                for s in lastlist["servers"]:
                    if s["name"] == server["name"]:
                        previousentry = s
                        break

                # Are there more players than before?
                if previousentry["players_current"] < server["players_current"]:
                    notify2.Notification("Iceball", "A player joined '" + server["name"] + "'").show()
            # New server
            else:
                # Any players online?
                if server["players_current"] > 0:
                    notify2.Notification("Iceball", "The server '" + server["name"] + "' with " + server["players_current"] + "players appeared").show()

        lastlist = jsn
        time.sleep(10)
