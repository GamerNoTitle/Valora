import os

session_type = os.environ.get('SESSION_TYPE')
redis_host = os.environ.get('REDIS_HOST')
redis_port = os.environ.get('REDIS_PORT')
redis_pass = os.environ.get('REDIS_PASSWORD')
redis_ssl = os.environ.get('REDIS_SSL', False)
redisurl = os.environ.get('REDIS_URL')
