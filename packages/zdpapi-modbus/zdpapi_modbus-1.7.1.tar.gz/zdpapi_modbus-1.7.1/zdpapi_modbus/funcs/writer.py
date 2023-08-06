from ..libs.modbus_tk import  modbus_tcp

def write(address,values,slave=1,func=16,host="127.0.0.1",port=8888):
    """
    写入数据
    """
    # 创建master
    master = modbus_tcp.TcpMaster(host=host, port=port)
    master.execute(slave, func, address, output_value=values)
