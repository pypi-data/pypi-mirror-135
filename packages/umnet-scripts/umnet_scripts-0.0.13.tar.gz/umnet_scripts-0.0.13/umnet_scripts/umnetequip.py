from sqlalchemy import create_engine
from .utils import get_env_vars
from .umnetdb import UMnetdb
import logging

logger = logging.getLogger(__name__)

class UMnetequip(UMnetdb):
    '''
    This class wraps helpful equip db queries in python.
    The API is lame.
    '''
    def __init__(self, host='equipdb-prod.umnet.umich.edu', port=1521):

        eqdb_creds = get_env_vars(['EQUIP_DB_USERNAME','EQUIP_DB_PASSWORD'])
        self._url = f"oracle://{eqdb_creds['EQUIP_DB_USERNAME']}:{eqdb_creds['EQUIP_DB_PASSWORD']}@(DESCRIPTION=(ADDRESS=(PROTOCOL=TCP)(HOST={host})(PORT={port}))(CONNECT_DATA=(SID=KANNADA)))"
        self._e = create_engine(self._url)
        
        logger.debug(f"Created DB engine {self._url}")


    def get_devices_by_category(self, category, active_only=False):
        '''
        Queries equip db for devices by category. You can also
        specify if you only want active devices.
        '''

        select = [ 'eq.monitored_device', 
                   'eq.rancid',
                   'eq.off_line',
                   'eq.dns_name',
                   'eq.ip_address',
                 ]
        table = 'ARADMIN1.UMNET_EQUIPMENT eq'

        where = [f"eq.category = '{category}'"]

        # Equipshim status numbers (see ARADMIN1.UMNET_EQUIPMENT_STATUS)
        # 1: RESERVE, 2:ACTIVE, 3:RETIRED
        if active_only:
            where.append("eq.status = 2")
        
        sql = self._build_select(select, table, where=where, distinct=True)
        return self._execute(sql)

    def get_device_location(self, ip):
        '''
        Queries equip db for a device by ip. Returns the location of the device
        '''
        select = [ 'bldg as building_name',
                   'address as building_address',
                   'room as room_no',
                   'bldg_code__ as building_no',
                 ]
        table = 'ARADMIN1.UMNET_EQUIPMENT'
        where = [f"ip_address='{ip}'"]

        sql = self._build_select(select, table, where=where)
        return self._execute(sql)


    def get_device_type(self, ip):
        '''
        Queries equip db for a device by ip, returns the 'type' of the device.
        By type we mean the UMNET_EQUIPMENT_TYPE: ACCESS LAYER, DISTRIBUTION LAYER, UMD, etc
        '''
        select = [ 'types as type' ]
        table = 'ARADMIN1.UMNET_EQUIPMENT'
        where = [f"ip_address='{ip}'"]

        sql = self._build_select(select, table, where=where)
        return self._execute(sql)
 
