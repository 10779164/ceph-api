import json
from rados import Rados
from rados import Error as RadosError

config={'conffile': '/etc/ceph/ceph.conf', 'conf': {}}

class CephClusterCommand(dict):
    """
    cluster: connect ceph
    prefix: ceph command
    json: return a json format data
    """

    def __init__(self, cluster, **kwargs):
        dict.__init__(self)
        ret, buf, err = cluster.mon_command(json.dumps(kwargs), '', timeout=5)
        if ret != 0:
            self['err'] = err
            #logger
        else:
            self.update(json.loads(buf))


class CephCheck(object):
    def get_cephhealth(self):
        with Rados(**config) as cluster:
            cluster_status = CephClusterCommand(cluster, prefix='health', format='json')
            ceph_status = {}
            if cluster_status['status'] == "HEALTH_OK":
                ceph_status['ceph_status'] = "Normal"
                return ceph_status
            else:
                error_msg = ''
                for i in cluster_status['checks']:
                    error_msg = error_msg + cluster_status['checks'][i]['summary']['message']+';'
                ceph_status['status'] = "Abnormal"
                ceph_status['msg'] = error_msg
                return ceph_status

    
    def get_cephfsdata(self):
        with Rados(**config) as cluster:
            cluster_status = CephClusterCommand(cluster, prefix='df', format='json') 
            cephfs_data = {}
            for i in cluster_status['pools']:
                if i['name'] == "cephfs_data":
                    cephfs_data['name'] = i['name']
                    cephfs_data['used'] = i['stats']['bytes_used']
                    cephfs_data['max'] = i['stats']['max_avail']
                    return cephfs_data
            return cephfs_data


    def get_rbd(self):
        with Rados(**config) as cluster:
            cluster_status = CephClusterCommand(cluster, prefix='df', format='json')
            rbd = {}
            for i in cluster_status['pools']:
                if i['name'] == "rbd":
                    rbd['name'] = i['name']
                    rbd['used'] = i['stats']['bytes_used']
                    rbd['max'] = i['stats']['max_avail']
                    return rbd
            return rbd
                
    
    def get_osd(self):
        with Rados(**config) as cluster:
            cluster_status = CephClusterCommand(cluster, prefix='status', format='json')
            osd = {}
            osd_status = cluster_status['osdmap']
            osd['num_osds'] = osd_status['osdmap']['num_osds']
            osd['num_up_osds'] = osd_status['osdmap']['num_up_osds']
            osd['num_in_osds'] = osd_status['osdmap']['num_in_osds']
            if osd['num_up_osds'] == osd['num_osds'] and osd['num_in_osds'] == osd['num_osds']:
                osd['status'] = 'Normal'
            else:
                osd['status'] = 'Abnormal'
            return osd

    def get_pgs(self):
        with Rados(**config) as cluster:
            cluster_status = CephClusterCommand(cluster, prefix='status', format='json')
            pg = {}
            pg_status = cluster_status['pgmap']
            if 'write_bytes_sec' in pg_status:
                pg['write_bytes_sec'] = pg_status['write_bytes_sec']
            else:
                pg['write_bytes_sec'] = 0

            if 'read_bytes_sec' in pg_status:
                pg['read_bytes_sec'] = pg_status['read_bytes_sec']
            else:
                pg['read_bytes_sec'] = 0
            return pg

