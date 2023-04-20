import redis

r = redis.Redis(host='localhost', port=6379)

if r.ping():
    print('Redis is ready')
else:
    print('Redis is not ready')