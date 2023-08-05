from amino.lib.util import device
import hmac
import base64
from hashlib import sha1
from uuid import uuid4
sid = None
def sigg(data):
        key=' fbf98eb3a07a9042ee5593b10ce9f3286a69d4e2'
        mac = hmac.new(bytes.fromhex(key), data.encode("utf-8"), sha1)
        digest = bytes.fromhex("32") + mac.digest()
        return base64.b64encode(digest).decode("utf-8")

class Headers:
    def __init__(self, data = None, type = None, deviceId: str = None, sig: str = None):
        if deviceId:
            dev = device.DeviceGenerator(deviceId=deviceId)
        else:
            dev = device.DeviceGenerator()

        headers = {
            "NDCDEVICEID": dev.device_id,
            #"NDC-MSG-SIG": dev.device_id_sig,
            "Accept-Language": "en-US",
            "Content-Type": "application/json; charset=utf-8",
            "User-Agent": dev.user_agent,
            "Host": "service.narvii.com",
            "Accept-Encoding": "gzip",
            "Connection": "Keep-Alive"
        }

        if data:
            #print(data)
            headers["Content-Length"] = str(len(data))
            signature=None
            try: signature=sigg(data)
            except: pass
            headers["NDC-MSG-SIG"] = signature
        if sid: headers["NDCAUTH"] = f"sid={sid}"
        if type: headers["Content-Type"] = type
        #if sig: headers["NDC-MSG-SIG"] = sig
        self.headers = headers
 
 
