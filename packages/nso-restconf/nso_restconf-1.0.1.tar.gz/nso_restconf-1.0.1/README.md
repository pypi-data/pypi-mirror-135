# nso_restconf
A wrapper of requests for managing the RestCONF API of NSO

# Installation
```
pip install nso-restconf
```

# Usage
For example we retrieve the NED ids in a json structure :
```python
from nso_restconf.restconf import RestConf

nso_api = RestConf(address="http://127.0.0.1", port=8080,
                   username="admin", password="admin")

res_ned_id = nso_api.get("tailf-ncs:devices/ned-ids/ned-id", content=None)

print(res_ned_id.json())

{
  'tailf-ncs:ned-id': [
    {
      'id': 'tailf-ncs-ned:lsa-netconf'
    },
    {
      'id': 'tailf-ncs-ned:netconf'
    },
    {
      'id': 'tailf-ncs-ned:snmp'
    },
    {
      'id': 'cisco-ios-cli-6.72:cisco-ios-cli-6.72',
      'module': [
        {
          'name': 'ietf-interfaces',
          'revision': '2014-05-08',
          'namespace': 'urn:ietf:params:xml:ns:yang:ietf-interfaces'
        },
...
```

## Methods

Supported methods are GET,POST,PUT,PATCH,DELETE.
There is others custom methods like action(), a wrapper of POST used to launch a NSO action.
See the RestConf object source code for supported methods at : https://github.com/rtrjl/nso_restconf/blob/master/nso_restconf/restconf.py

## License

This project is licensed to you under the terms of the [Cisco Sample Code License](https://raw.githubusercontent.com/rtrjl/nso_restconf/master/LICENSE).
