glevel = 'debug'
bind = "0.0.0.0:80"
pidfile = "log/gunicorn.pid"
accesslog = "log/access.log"
errorlog = "log/debug.log"
daemon = True
workers = 1

