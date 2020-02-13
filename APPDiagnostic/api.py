from flask import Flask
from flask_restful import Resource, Api
import ceph_check

app = Flask(__name__)
api = Api(app)

class CephCheck(Resource):
    def get(self):
        agent = ceph_check.CephCheck()
        msg = {}
        msg['health'] = agent.get_cephhealth()
        msg['cephfsdata'] = agent.get_cephfsdata()
        msg['rbd'] = agent.get_rbd()
        msg['osd'] = agent.get_osd()
        msg['pg'] = agent.get_pgs()
        return {"ceph": msg}

api.add_resource(CephCheck, '/')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=8090,threaded='True')