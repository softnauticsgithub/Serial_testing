
"""Module for handling serial communication with logging."""

import serial
import logging  # pylint: disable=unused-import

# pylint: disable=invalid-name


class MySerial:
    """Class to manage serial communication."""

    def __init__(self, port, baudrate=9600):
        """Initialize the MySerial instance.

        Args:
            port (str): The serial port to connect to.
            baudrate (int): The baud rate for the connection.
        """
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.log_file = "COM_test_Log.txt"
        self.logger = self.setup_logger()

    def connect(self):
        """Establish a connection to the serial port."""
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate)
            self.logger.info(f"Connected to {self.port} at {self.baudrate} baudrate")
        except serial.SerialException as e:
            self.logger.error(f"Failed to connect to {self.port}: {e}")

    def read(self, num_bytes=1)
        """Read bytes from the serial connection.

        Args:
            num_bytes (int): The number of bytes to read.

        Returns:
            bytes: The bytes read from the serial connection.
        """
        if self.serial_connection:
            try:
                return self.serial_connection.read(num_bytes)
            except serial.SerialException as e:
                self.logger.error(f"Error while reading from {self.port}: {e}")
        else:
            self.logger.error("Serial connection not established.")
            return b''

    def write(self, data):
        """Write bytes to the serial connection.

        Args:
            data (bytes): The data to write to the serial connection.
        """
        if self.serial_connection:
            try:
                self.serial_connection.write(data
                self.logger.info(f"{data.decode()}")
            except serial.SerialException as e:
                self.logger.error(f"Error while writing to {self.port}: {e}")
        else:
            self.logger.error("Serial connection not established.")

    def flush(self):
        """Flush the serial buffer."""
        if self.serial_connection:
            try:
                self.serial_connection.flush()
                self.logger.info("Serial buffer flushed.")
            except serial.SerialException as e:
                self.logger.error(f"Error while flushing {self.port}: {e}")
        else:
            self.logger.error("Serial connection not established.")

    def setup_logger(self):
        """Set up the logger for the serial communication.

        Returns:
            logging.Logger: Configured logger instance.
        """
        logger = logging.getLogger('MySerialLogger')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
