""" Clammy """

import contextlib
import re
import socket
import struct
import sys

from clammy import exceptions


class ClamAVDaemon:
    """
    Class for using clamd with a network socket
    """

    def __init__(self, host="127.0.0.1", port=3310, unix_socket=None, timeout=None):
        """
        Args:
            host (string): The hostname or IP address (if connecting to a network socket)
            port (int): TCP port (if connecting to a network socket)
            unix_socket (str):
            timeout (float or None) : socket timeout
        """

        self.host = host
        self.port = port
        self.unix_socket = unix_socket
        self.timeout = timeout

        if self.unix_socket:
            self.socket_type = socket.AF_UNIX
        else:
            self.socket_type = socket.AF_INET

        self.socket = self._init_socket()

    def _init_socket(self):

        try:
            clamd_socket = socket.socket(self.socket_type, socket.SOCK_STREAM)

            # Set timeout prior to connecting to ensure that an initial
            # connection timeout will respect the setting regardless of OS.
            # https://docs.python.org/3/library/socket.html#timeouts-and-the-connect-method
            clamd_socket.settimeout(self.timeout)

            if self.socket_type == socket.AF_INET:
                clamd_socket.connect((self.host, self.port))
            elif self.socket_type == socket.AF_UNIX:
                clamd_socket.connect(self.unix_socket)

        except socket.error as error:
            if self.socket_type == socket.AF_UNIX:
                error_message = f'Error connecting to Unix socket "{self.unix_socket}"'
            elif self.socket_type == socket.AF_INET:
                error_message = f'Error connecting to network socket with host "{self.host}" and port "{self.port}"'
            raise exceptions.ClamdConnectionError(error_message) from error

        return clamd_socket

    def ping(self):
        """Sends the ping command to the ClamAV daemon"""
        return self._basic_command("PING")

    def version(self):
        """Sends the version command to the ClamAV daemon"""
        return self._basic_command("VERSION")

    def reload(self):
        """Sends the reload command to the ClamAV daemon"""
        return self._basic_command("RELOAD")

    def shutdown(self):
        """
        Force Clamd to shutdown and exit

        return: nothing

        May raise:
          - ClamdConnectionError: in case of communication problem
        """
        try:
            self._init_socket()
            self._send_command("SHUTDOWN")
            # result = self._recv_response()
        finally:
            self._close_socket()

    def scan(self, filename):
        """Scan a file."""
        return self._file_system_scan("SCAN", filename)

    def cont_scan(self, filename):
        """Scan a file but don't stop if a virus is found."""
        return self._file_system_scan("CONTSCAN", filename)

    def multi_scan(self, filename):
        """Scan a file using multiple threads."""
        return self._file_system_scan("MULTISCAN", filename)

    def _basic_command(self, command):
        """Send a command to the clamav server, and return the reply."""
        self._init_socket()
        try:
            self._send_command(command)
            response = self._recv_response().rsplit("ERROR", 1)
            if len(response) > 1:
                raise exceptions.ClamdResponseError(response[0])
            return response[0]
        finally:
            self._close_socket()

    def _file_system_scan(self, command, filename):
        """
        Scan a file or directory given by filename using multiple threads (faster on SMP machines).
        Do not stop on error or virus found.
        Scan with archive support enabled.

        filename (string): filename or directory (MUST BE ABSOLUTE PATH !)

        return:
          - (dict): {filename1: ('FOUND', 'virusname'), filename2: ('ERROR', 'reason')}

        May raise:
          - ClamdConnectionError: in case of communication problem
        """

        try:
            self._init_socket()
            self._send_command(command, filename)

            directory = {}
            for result in self._recv_response_multiline().split("\n"):
                if result:
                    filename, reason, status = parse_response(result)
                    directory[filename] = (status, reason)

            return directory

        finally:
            self._close_socket()

    def instream(self, buff, max_chunk_size=1024):
        """
        Scan a buffer

        buff  filelikeobj: buffer to scan
        max_chunk_size int: Maximum size of chunk to send to clamd in bytes
          MUST be < StreamMaxLength in /etc/clamav/clamd.conf

        return:
          - (dict): {filename1: ("virusname", "status")}

        May raise :
          - ClamdBufferTooLongError: if the buffer size exceeds clamd limits
          - ClamdConnectionError: in case of communication problem
        """

        try:
            self._init_socket()
            self._send_command("INSTREAM")

            chunk = buff.read(max_chunk_size)
            while chunk:
                size = struct.pack(b"!L", len(chunk))
                self.socket.sendall(size + chunk)
                chunk = buff.read(max_chunk_size)

            self.socket.sendall(struct.pack(b"!L", 0))

            result = self._recv_response()

            if len(result) > 0:
                if result == "INSTREAM size limit exceeded. ERROR":
                    raise exceptions.ClamdBufferTooLongError(result)

                filename, reason, status = parse_response(result)
                return {filename: (status, reason)}
        finally:
            self._close_socket()

    def stats(self):
        """
        Get Clamscan stats

        return: (string) clamscan stats

        May raise:
          - ClamdConnectionError: in case of communication problem
        """
        self._init_socket()
        try:
            self._send_command("STATS")
            return self._recv_response_multiline()
        finally:
            self._close_socket()

    def _send_command(self, cmd, *args):
        """
        Sends a command to the ClamAV daemon.

        `man clamd` recommends to prefix commands with z, but we will use \n
        terminated strings, as python<->clamd has some problems with \0x00
        """
        concat_args = ""
        if args:
            concat_args = " " + " ".join(args)

        # cmd = 'n{cmd}{args}\n'.format(cmd=cmd, args=concat_args).encode('utf-8')
        cmd = f"n{cmd}{concat_args}\n".encode("utf-8")
        self.socket.sendall(cmd)

    def _recv_response(self):
        """Receive line from clamd"""
        try:
            with contextlib.closing(self.socket.makefile("rb")) as file_object:
                return file_object.readline().decode("utf-8").strip()
        except (socket.error, socket.timeout) as error:
            raise exceptions.ClamdConnectionError(
                f"Error while reading from socket: {sys.exc_info()[1].args}"
            ) from error

    def _recv_response_multiline(self):
        """Receive multiple line response from clamd and strip all whitespace characters"""
        try:
            with contextlib.closing(self.socket.makefile("rb")) as file_object:
                return file_object.read().decode("utf-8")
        except (socket.error, socket.timeout) as error:
            raise exceptions.ClamdConnectionError(
                f"Error while reading from socket: {sys.exc_info()[1]}"
            ) from error

    def _close_socket(self):
        """Close clamd socket"""
        self.socket.close()


def parse_response(msg):
    """Parses responses for SCAN, CONTSCAN, MULTISCAN and STREAM commands."""

    scan_response = re.compile(
        r"^(?P<path>.*): ((?P<virus>.+) )?(?P<status>(FOUND|OK|ERROR))$"
    )

    try:
        return scan_response.match(msg).group("path", "virus", "status")
    except AttributeError:
        raise exceptions.ClamdResponseError(
            msg.rsplit("ERROR", 1)[0]
        ) from AttributeError
