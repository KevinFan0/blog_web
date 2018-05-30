#! /usr/bin/env python
# coding=utf-8
from flask import Flask
import os
from flaskr import db,auth,blog
import logging.config
import logging

filepath = os.path.join(os.path.dirname(__file__), 'logging.conf')
# print(filepath)
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('root')

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path,'flaskr.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py',silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        logger.info("begin to hello")
        return 'Hello,fandong!'

    @app.route('/clear', methods=["get"])
    def clear_csv():
        file = open('blog_web.log', 'w+')
        f1 = file.readline()
        print(f1)
        file.truncate()
        print(file)
        return 'clear finished'

    db.init_app(app)
    
    app.register_blueprint(auth.bp)

    app.register_blueprint(blog.bp)
    app.add_url_rule('/',endpoint='index')

    return app

application = create_app()

if __name__ == '__main__':
    application.run()