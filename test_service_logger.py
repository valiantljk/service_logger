from service_logger import * 


#For local test on mac
#redis-server /usr/local/etc/redis.conf
#redis-cli shutdown
#redis-cli  -h localhost -p 6379 -a sunmiai2020 lrange  -3 -1 humanalarm
import os
class Test_Redis():
    def __init__(self):
        self.r = None
    def test_connect(self):
        #setting up Redis connection
        host = os.getenv('RedisHost', default = 'localhost')
        port = os.getenv('RedisPort', default = '6379')
        password = os.getenv('RedisPass', default = 'idontknow')
        r = Redis(host, port, password)
        self.r = r
    def test_put_onelog(self):
        #Test inserting a single log
        rlog0 = RedisLog(sname = 'humanalarm', 
                         fname = 'detection',
                         status = 0,
                         error = 'single log error',
                         uuid = 1000)
        key = 'humanalarm'
        l = self.r.put(key, rlog0)
        assert(l == 1)
    def test_put_logs(self):
        #Test inserting a list of logs
        RLogs=[]
        rlog1 = RedisLog(sname = 'humanalarm', 
                         fname = 'detection',
                         status = 1,
                         error = '',
                         uuid = 1000133)
        RLogs.append(rlog1)
        time.sleep(1)

        rlog2 = RedisLog(sname = 'humanalarm', 
                         fname = 'detection',
                         status = 0,
                         error = 'some expection',
                         uuid = 1000133)
        RLogs.append(rlog2)
        #Add logs into redis
        key = 'humanalarm'
        l = self.r.put(key, RLogs)
        assert(l==len(RLogs)) 
    def test_get_latest(self):
        #Test retrieving latest #num logs
        key = 'humanalarm'
        num = 3 # retrieve latest 3 logs for service 'humanalarm'
        logs = self.r.get(key,num)
        for log in logs:
            log.print()
    def test_get_all(self):
        #Test retrieving all logs for service 
        key = 'humanalarm'
        logs = self.r.get(key) 
        if logs:
            for log in logs:
                log.print()
        print('Total Logs:%d'%len(logs))
    def test_set_expire(self):
        #Test setting expiration time for a service
        key = 'humanalarm'
        ts = 30 # set it expire after 60 seconds
        self.r.set_expire(key,ts)
        print('TTL for service:%s = %f'%(key,ts))
        time.sleep(10)
        ttl = self.r.get_ttl(key)
        print('TTL for service:%s = %f'%(key,ttl))
        time.sleep(20)
        ttl = self.r.get_ttl(key)
        print('TTL for service:%s = %f'%(key,ttl))
        time.sleep(5)
        ttl = self.r.get_ttl(key)
        print('TTL for service:%s = %f'%(key,ttl))
        time.sleep(5)
        ttl = self.r.get_ttl(key)
        print('TTL for service:%s = %f'%(key,ttl))


test = Test_Redis()
test.test_connect()
test.test_put_onelog()
test.test_put_logs()
test.test_get_latest()
test.test_get_all()
test.test_set_expire()
test.test_get_latest()
test.test_get_latest()