import serial
import logging


class MySerial:
    def __init__(self, port, baudrate=9600):
        self.port = port
        self.baudrate = baudrate
        self.serial_connection = None
        self.log_file = "COM_test_Log.txt"
        self.logger = self.setup_logger()

    def connect(self):
        try:
            self.serial_connection = serial.Serial(self.port, self.baudrate)
            self.logger.info(f"Connected to {self.port} at {self.baudrate} baudrate")
        except serial.SerialException as e:
            self.logger.error(f"Failed to connect to {self.port}: {e}")

    def read(self, num_bytes=1):
        if self.serial_connection:
            try:
                return self.serial_connection.read(num_bytes)
            except serial.SerialException as e:
                self.logger.error(f"Error while reading from {self.port}: {e}")
        else:
            self.logger.error("Serial connection not established.")
            return b''

    def write(self, data):
        if self.serial_connection:
            try:
                self.serial_connection.write(data)
                self.logger.info(f"{data.decode()}")
            except serial.SerialException as e:
                self.logger.error(f"Error while writing to {self.port}: {e}")
        else:
            self.logger.error("Serial connection not established.")

    def flush(self):
        if self.serial_connection:
            try:
                self.serial_connection.flush()
                self.logger.info("Serial buffer flushed.")
            except serial.SerialException as e:
                self.logger.error(f"Error while flushing {self.port}: {e}")
        else:
            self.logger.error("Serial connection not established.")

    def setup_logger(self):
        logger = logging.getLogger('MySerialLogger')
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler = logging.FileHandler(self.log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        return logger
