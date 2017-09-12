"""
This file is responsible for running application server.
"""

from api import app

if __name__ == '__main__':
    app.config.from_object('config.DevConfig')
    app.run(host='0.0.0.0', port=5000)
