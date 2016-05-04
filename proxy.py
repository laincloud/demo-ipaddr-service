#!/usr/bin/env python
# -*- coding: utf-8

from os import environ
import requests
import random
from flask import Flask
app = Flask(__name__)


def get_upstreams():
    upstreams = []
    try:
        service_appname = environ.get("LAIN_APPNAME")
        service_procname = environ.get("LAIN_SERVICE_NAME")
        print "service_appname: {}".format(service_appname)
        url = 'http://lainlet.lain:9001/v2/proxywatcher?appname={}'.format(service_appname)
        r = requests.get(url)
        print 'r.status_code: {}'.format(r.status_code)
        print 'r.content: {}'.format(r.content)
        procs = r.json()
        for k, v in procs.iteritems():
            procname = k.split('.')[-1]
            if procname == service_procname:
                containers = v['containers']
                upstreams = ["{}:{}".format(x['container_ip'], x['container_port']) for x in containers]
    except Exception as e:
        print e
    return upstreams


@app.route("/")
def proxy():
    upstreams = get_upstreams()
    print 'upstreams: {}'.format(upstreams)
    if len(upstreams) == 0:
        return 'no service upstreams'
    upstream = random.choice(upstreams)
    print 'upstream: {}'.format(upstream)
    r = requests.get('http://{}/'.format(upstream))
    print 'sr.status_code: {}'.format(r.status_code)
    print 'sr.content: {}'.format(r.content)
    return r.content


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='10000')
