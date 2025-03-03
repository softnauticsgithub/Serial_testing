

import myserial

serial_connect = myserial.MySerial("COM1")


def main():
    serial_connect.connect()
    serial_connect.write(b"Hello")
    data = serial_connect.read()
    print("Read data:", data)
    serial_connect.flush()
    serial_connect.close()


if __name__ == "__main__":
    main()
