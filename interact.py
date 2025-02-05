
"""Module for serial communication using myserial."""

# pylint: disable=invalid-name

import myserial

serial_connect = myserial.MySerial("COM1")


def main():
    """Establish a connection, send data, read response, and clean up."""
    serial_connect.connect()
    serial_connect.write(b"Hello")
    data = serial_connect.read()
    print("Read data:", data)
    serial_connect.flush()
    serial_connect.close()


if __name__ == "__main__":
    main()
