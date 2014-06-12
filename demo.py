'''class Service(BASE, NovaBase):
    """Represents a running service on a host."""

    __tablename__ = 'services'
    id = Column(Integer, primary_key=True)
    host = Column(String(255))  # , ForeignKey('hosts.id'))
    host_ip = Column(String(255))
    binary = Column(String(255))
    topic = Column(String(255))
    report_count = Column(Integer, nullable=False, default=0)
    disabled = Column(Boolean, default=False)
    availability_zone = Column(String(255), default='nova')
'''

import commands
import sqlite3


from oslo.config import cfg

commands.getstatusoutput('rm -f nova.sqlite')
CONF = cfg.CONF

# NOTE(hzrandd): Configure the filename to use with sqlite
sql_connection_nova_opt = [cfg.StrOpt('nova_sqlite',
                                      default='nova.sqlite',
                                      help='A valid SQLAlchemy connection')]
CONF.register_opts(sql_connection_nova_opt)


def my_function(name):
    return name.upper()


def do_my_dask(conn, name, num_params, func):
    # create_function("my_function", 1, my_function)
    conn.create_function(name, num_params, func)
    return conn.execute("select func(title), foo, bar from somtable")


def dump_database(conn):
    # dump all memory info to query for store disk
    return conn.iterdump()


def delete(conn, model, col, var):
    conn.execute("delete from %s where %s=?" % (model, col), var)


def get_connection():
    conn = sqlite3.connect(CONF.nova_sqlite)
    return conn


def get_fake_service_datas():
    # connect(database=':memory:', timeout=5, isolattion_level='')
    # isolattion_level: IMMEDIATE--- others can read but cannot wirte.
    con = sqlite3.connect(CONF.nova_sqlite)

    cur = con.cursor()
    cur.execute('CREATE TABLE Service (id Integer PRIMARY KEY, \
                host String(255),\
                host_ip String(255), binary String(255), topic String(255),\
                report_count Integer ,\
                disabled Boolean , availability_zone String(255) )')
    con.commit()
    fake_services = [
        (1, "114-113-199-12", "10.120.120.11",
         "nova-consoleauth", "consoleauth", 2155, 0, "beta11"),
        (2, "114-113-199-11", "10.120.120.12",
         "nova-consoleauth", "console", 1255, 1, "beta12"),
        (3, "114-113-199-13", "10.120.120.13",
         "nova-consoleauth", "consoleauth", 13, 0, "beta13")
    ]

    # cur.executemany("insert into Service values (?,?,?,?,?,?,?,?)",
    # fake_services)
    for service in fake_services:
        cur.execute("insert into Service values (?,?,?,?,?,?,?,?)", service)
        con.commit()

    cur.execute('SELECT * FROM Service')
    services_datas = cur.fetchall()
    return services_datas


def model_query(conn=None, model='Service', detail=True, col=None, var=None):
    if not conn:
        conn = get_connection()
    cur = conn.cursor()
    if col and var:
        cur.execute("select * from %s where %s=%s" % (model, col, var))
    else:
        cur.execute("select * from %s" % model)
    if detail:
        return cur.fetchall()
    else:
        return cur


def update(conn, model, col, var, col2, var2):
    import ipdb; ipdb.set_trace() ### XXX BREAKPOINT
    conn.execute("update %s set %s= ? where %s=?" % (model, col, col2), (var, var2))


def main():
    conn = get_connection()
    print get_fake_service_datas()
    update(conn, "Service", "availability_zone", "updated", "availability_zone", "beta13")
    print model_query(conn)

main()

