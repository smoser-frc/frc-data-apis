import base64
import hashlib
import json
import os
import requests
import sys
import time

from urllib.parse import quote_plus
from http import HTTPStatus

class client(object):
    endpoint = None
    user = None
    key = None
    tok = None
    cachepath = None

    def __init__(self, user, key, cachepath=None, endpoint="https://frc-api.firstinspires.org/v3.0", tok=None):
        self.endpoint = endpoint
        self.user = user
        self.key = key
        if cachepath == None:
            self.cachepath = ".cache"

        if (self.tok and self.user != ""):
            raise TypeError("Can't give uuser and tok")
        if self.user != "":
            self.tok = base64.b64encode(("%s:%s\n" % (user, key)).encode()).decode()
        else:
            self.tok = tok

    def get_single(self, path, **kwargs):
        headers = {'Authorization': 'Basic ' + self.tok}
        args = '&'.join("%s=%s" % (k, v) for k, v in kwargs.items())
        if not path.startswith("/"):
            path = "/" + path
        url = self.endpoint + path + "?" + args
        ret = requests.get(url, headers=headers)
        if ret.status_code != HTTPStatus.OK:
            raise Exception("status_code = %d from %s" % (ret.status_code, url))
        return ret

    def get(self, path, **kwargs):
        data = {}
        n = 1
        args = kwargs
        limit = args.pop('limit', None)
        while True:
            kwargs["page"] = n
            ret = self.get_single(path, **kwargs)
            rdata = ret.json()
            for k, v in rdata.items():
                if isinstance(v, dict):
                    if k not in data:
                        data[k] = {}
                    data[k].update(v)
                elif isinstance(v, (list, tuple)):
                    if k not in data:
                        data[k] = []
                    data[k].extend(v)
                elif k.endswith("CountTotal") or k.endswith("CountPage"):
                    pass
                elif k in ("eventCount",):
                    pass
                elif k in ("pageTotal", "pageCurrent"):
                    pass
                else:
                    print(json.dumps(rdata, indent=" "))
                    raise TypeError("path %s: %s is not dict or list: %s" % (path, k, v))

            #result = rdata[name]
            #data.extend(result)
            if "pageTotal" not in rdata:
                break
            tot = rdata["pageTotal"]
            #print("got %d in page %d tot=%d" % (len(result), n, tot))
            if n == tot or (limit and n == limit):
                break
            n = n + 1
        return data

    def cache(self, path, **kwargs):
        result = {'path': path, 'args': kwargs}
        key = hashlib.sha256(json.dumps(result, sort_keys=True).encode()).hexdigest()
        cachepath = os.path.join(self.cachepath, key)
        if os.path.exists(cachepath):
            with open(cachepath) as fp:
                result = json.loads(fp.read())
            return result['result']

        result['result'] = self.get(path, **kwargs)
        result['time'] = time.time()
        os.makedirs(os.path.dirname(cachepath), exist_ok=True)
        with open(cachepath, "w") as fp:
            fp.write(json.dumps(result, sort_keys=True, indent=" "))
        return result['result']
