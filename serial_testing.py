
"""Module for testing MySerial class functionality."""

import pytest
from unittest.mock import patch
from myserial import MySerial  # pylint: disable=invalid-name


def test_connection_successful():
    """Test successful connection to the serial port."""
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value = True
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.serial_connection is True


def test_connection_failure():
    """Test failure to connect to the serial port."""
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value = None
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.serial_connection is None


def test_read_successful():
    """Test successful read from the serial port."""
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value.read.return_value = b'Test data'
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.read() == b'Test data'


def test_read_failure():
    """Test failure to read from the serial port."""
    with patch('serial.Serial') as mock_serial:
        mock_serial.return_value.read.return_value = b''
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        assert serial_instance.read() == b''


def test_write_successful():
    """Test successful write to the serial port."""
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
    """Test failure to write to the serial port."""
    with patch('serial.Serial') as mock_serial:
        mock_serial.side_effect = serial.SerialException("Serial connection not established.")
        serial_instance = MySerial('COM10')
        assert serial_instance.write(b'') is None


def test_flush_successful():
    """Test successful flush of the serial port."""
    with patch('serial.Serial') as mock_serial:
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        serial_instance.flush()


def test_repetitive_read_write():
    """Test repetitive read and write operations on the serial port."""
    with patch('serial.Serial') as mock_serial:
        serial_instance = MySerial('COM10')
        serial_instance.connect()
        mock_serial.return_value.read.side_effect = [b'Test'] * 10
        serial_instance.serial_connection.write = lambda data: None
        for _ in range(10):
            assert serial_instance.read(4) == b'Test'
            serial_instance.write(b'Test')
