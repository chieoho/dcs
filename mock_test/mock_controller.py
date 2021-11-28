import serial
import time
import thread
from modbus_crc import modbus_crc16


port = serial.Serial(port='COM2', baudrate=9600, bytesize=8,
                     parity='N', stopbits=1, timeout=0.05,
                     writeTimeout=0.2)

ctrller_status = ['00']
detector_value_list = ['00','00','00',  '00','01','70',  '00','05','00'] * 85
detector_status_list = ['00', '00', '02'] * 85
detector_unit_list = ['00', '01', '02'] * 85
detector_decimal_list = ['00', '01', '02'] * 85
detector_material_list = ['00', '01', '02'] * 85

reg_dict = {'1': ctrller_status,
            '2': detector_value_list,
            '3': detector_status_list,
            '4': detector_unit_list,
            '5': detector_decimal_list,
            '6': detector_material_list}

var_dict = {
    'cs': 'ctrller_status',
    'dv': 'detector_value_list',
    'ds': 'detector_status_list',
    'du': 'detector_unit_list',
    'dd': 'detector_decimal_list',
    'dm': 'detector_material_list'
}


class Exit:
    fg = 0


def listening():
    while True:
        data = ''
        try:
            while 1:
                receive = port.read(1).encode('hex').upper()
                if receive == '':
                    break
                data += receive
        except Exception as e:
            print e
        else:
            if data:
		print(data)
		reg_addr = data[4: 8]
		length = int(data[8: 12], 16)
		print(length)
                head = '0103'
                start = int(reg_addr, 16) - int(reg_addr[0], 16) * (16**3)
                ret_data = ''.join(reg_dict.get(reg_addr[0])[start: start + length])
                ret_data_length = len(ret_data) / 2
                ret_data_length = '%02x' % ret_data_length
                ret_body = head + ret_data_length + ret_data
                crc_code = modbus_crc16(ret_body)
                ret_frame = ret_body + crc_code
                port.write(ret_frame.decode('hex'))
        if Exit.fg:
            break


if __name__ == '__main__':
    thread.start_new_thread(listening, ())
    while True:
        cmd = raw_input('>')
        if cmd == 'exit':
            Exit.fg = 1
            time.sleep(0.5)
            break
        elif cmd.startswith('dis'):
            var = cmd.split()[-1]
            if var not in var_dict.keys():
                print 'invalid input'
                continue
            print eval(var_dict.get(cmd.split()[-1]))
        elif cmd.startswith('ch'):
            _, var, num, value = cmd.split()
            if var not in var_dict.keys() or len(value) != 2:
                print 'invalid input'
                continue
            eval(var_dict[var])[int(num)] = value
            print eval(var_dict[var])
        elif cmd == 'help':
            print 'dis var, display variate. example: disp cs'
            print 'ch var num value, change variate. example: ch ds 1 02'
            from pprint import pprint
            print
            pprint(var_dict)
            print
        elif cmd == '':
            pass
        else:
            print 'invalid input'
