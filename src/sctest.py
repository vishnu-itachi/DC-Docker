from server import Server
from client import Client

s = Server("localhost", 50007)
c = Client("localhost", 50007)


c.send("hello world")
obj = s.recieve()
print(obj)

c.close()
s.close()
