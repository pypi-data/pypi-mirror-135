# -*-coding:utf-8 -*-

import base64
import imp
from sqlite3 import connect
import jaydebeapi
import json
import pandas as pd
import datetime
from datacenter_datasdk.settings import td_columns, td_type_map
import datacenter_datasdk.settings as settings
from datacenter_datasdk.verify import verify_args, format_date_param
import os


def jdbc_read(db, sql):
    td_token_str = base64.b64decode(bytes(settings.td_token, encoding="utf8")).decode('utf8')
    (user, password) = td_token_str.split(':')
    jdbc_url = f"jdbc:TAOS-RS://10.50.1.236:6052/{db}?user={user}&password={password}"
    driver = "com.taosdata.jdbc.rs.RestfulDriver"
    rp = os.path.abspath(os.path.dirname(__file__))
    jar_file = os.path.join(rp, 'taos-jdbcdriver-2.0.32-dist.jar')
    conn = jaydebeapi.connect(driver, jdbc_url, jars=jar_file)
    curs = conn.cursor()
    curs.execute(sql)
    d = curs.fetchall()
    curs.close()
    return d

def get_int_code(code, region):
    if region == 'cn':
        if 'XSHG' in code:
            code_int = int(code.strip('.XSHG')) + 1000000
        else:
            code_int = int(code.strip('.XSHE')) + 2000000
    elif region == 'us':
        code_int = int(code)
    else:
        code_int = int(code)
    return code_int


def get_str_code(code_int, region):
    if region == 'cn':
        if 2000000 > code_int > 1000000:
            code = '{:06d}.XSHG'.format(code_int-1000000)
        else:
            code = '{:06d}.XSHE'.format(code_int-2000000)
    elif region == 'us':
        code = str(code_int)
    else:
        code = str(code_int)
    return code


@verify_args(check={'code': (str, list),
                    'region': str,
                    'frequency': str,
                    'start_date': (datetime.datetime, datetime.date, str),
                    'end_date': (datetime.datetime, datetime.date, str)
                    }
             )
def get_price(code: str or list,
              region: str,
              frequency: str,
              start_date: datetime.datetime or datetime.date or str = datetime.datetime(2005, 1, 1),
              end_date: datetime.datetime or datetime.date or str = datetime.datetime.today(
              ).replace(hour=0, minute=0, second=0, microsecond=0)
              ):
    """
    get kline data, include daily, minute and tick

    code: str or list, single code or multi code as list
    region: str, 'cn' or 'us'
    frequency: str, represent frequency of kline, 'd1', 'm1', 'm5', 'm15', 'm30', 'm60' and 'tick'(only in cn)
    start_date, datetime.datetime or datetime.date or str, start time of data, default '2005-01-01'
    end_date, datetime.datetime or datetime.date or str, end time of data, default 0 o'clock of today 
    """
    if not settings.td_token or not settings.td_url:
        raise Exception('auth failed')
    
    if f'{region}_{frequency}' not in td_columns.keys():
        raise Exception(f'{frequency} of {region} not support')
        
    if start_date > end_date:
        raise Exception(f'start_date({start_date}) > end_date({end_date}) on code({code})')
    if isinstance(code, list):
        codes = tuple([get_int_code(c, region) for c in code])
        code_sql = f'code in {codes}'
    else:
        code_int = get_int_code(code, region)
        code_sql = f'code={code_int}'
    
    start_date = format_date_param(start_date)
    end_date = format_date_param(end_date)
    sql = f"select * from {region}_{frequency}.{region}_st_{frequency} where ({code_sql}) and (time >= '{start_date}' and time <='{end_date}');"
    
    data = jdbc_read(f'{region}_{frequency}', sql)
    columns = settings.td_columns_types[f'{region}_{frequency}']['columns']
    df = pd.DataFrame(data,columns=columns)
    df.sort_values(by='time', inplace=True)
    if frequency != 'tick':
        df = df[df.open != 0]
    
    types = settings.td_columns_types[f'{region}_{frequency}']['types']
    
    for t, c in zip(types, columns):
        df[c] = df[c].astype(t)
    df['code'] = df['code'].apply(lambda x: get_str_code(x, region))
    df = df[td_columns.get(f'{region}_{frequency}')]
    return df

