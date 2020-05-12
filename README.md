# Install service_logger
* Install from pypi with pip3
```
pip3 install -i https://test.pypi.org/simple/ service-logger==0.0.1
```
* Install from source code
```
python3 setup.py install 
```

# Local test
* Start the redis server:
```
redis-server /usr/local/etc/redis.conf
```
* Run some tests
```
python3 test_service_logger.py
```