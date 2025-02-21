
"""
This module contains unit tests for the MySerial class, which is assumed to handle
serial communication. The tests cover connection, reading, writing, flushing, and repetitive
read/write operations using unittest.mock for mocking serial.Serial.
"""

# pylint: disable=invalid-name

from unittest.mock import patch
import pytest
from myserial import MySerial


def test_connection_successful():
    """
    Test that a serial connection is successfully established.
    """
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value = True
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.serial_connection is True


def test_connection_failure():
    """
    Test that a serial connection fails to establish when the return value is None.
    """
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value = None
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.serial_connection is None


def test_read_successful():
    """
    Test that data is successfully read from the serial connection.
    """
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value.read.return_value = b'Test data'
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.read() == b'Test data'


def test_read_failure():
    """
    Test that reading from the serial connection returns an empty byte string on failure.
    """
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value.read.return_value = b''
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.read() == b''


def test_write_successful():
    """
    Test that data is successfully written to the serial connection and logged.
    """
    with patch('serial.Serial') as mock_serial:
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        serial_instance.serial_connection.write = lambda data: None
        test_data = b'Test data'

        serial_instance.write(test_data)
        with open("serial_log.txt", "r") as log_file:
            log_content = log_file.read()
            assert f"{test_data.decode()}" in log_content


def test_write_failure():
    """
    Test that writing to the serial connection fails when a SerialException is raised.
    """
    with patch('serial.Serial') as mock_serial:
        mock_serial.side_effect = serial.SerialException(
            "Serial connection not established.")
        serial_instance = MySerial('COM10')
        assert serial_instance.write(b'') is None


def test_flush_successful():
    """
    Test that the serial connection is successfully flushed.
    """
    with patch('serial.Serial') as mock_serial:
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        serial_instance.flush()


def test_repetitive_read_write():
    """
    Test repetitive read/write operations to ensure reliability over multiple iterations.
    """
    with patch('serial.Serial') as mock_serial:
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        mock_serial.return_value.read.side_effect = [b'Test'] * 10
        serial_instance.serial_connection.write = lambda data: None
        for _ in range(10):
            assert serial_instance.read(4) == b'Test'
            serial_instance.write(b'Test')
