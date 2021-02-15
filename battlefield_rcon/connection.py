import binascii
import socket


from battlefield_rcon.utils import (
    generate_password_hash,
    create_packet,
    contains_complete_packet,
    decode_packet,
    encode_packet,
)
from battlefield_rcon.exceptions import RCONLoginRequiredException, RCONAuthException


class RCONConnection(object):
    def __init__(self, remote_addr, port, password=None):
        self._remote_addr = remote_addr
        self._port = port
        self._password = password
        self._conn = None
        self._authenticated = False
        self._seq = 0

    def _read_response(self):
        data_buffer = bytes()
        while not contains_complete_packet(data_buffer):
            data_buffer += self._conn.recv(1024)

        return decode_packet(data_buffer)

    def send(self, words):
        packet_to_send = encode_packet(
            create_packet(self._seq, False, False, words=words)
        )
        self._seq += 1

        self._conn.send(packet_to_send)

        data = self._read_response()

        if "LogInRequired" in data["words"]:
            raise RCONLoginRequiredException

        return data["words"]

    def connect(self):
        if not self._conn:
            self._conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self._conn.settimeout(1)
            self._conn.connect((self._remote_addr, self._port))
            self._conn.setblocking(True)
            self._seq = 0

        if not self._password:
            return

        password_salt_response = self.send(words=["login.hashed"])

        if "OK" not in password_salt_response:
            raise RCONAuthException

        salt_bytes = binascii.unhexlify(password_salt_response[1])

        pwd_hash = generate_password_hash(password=self._password, salt=salt_bytes)
        pwd_hash_final = pwd_hash.upper()

        response = self.send(words=["login.hashed", pwd_hash_final])

        if "OK" not in response:
            raise RCONAuthException

        self._authenticated = True

        return response

    def disconnect(self):
        if self._conn:
            self._conn.close()
            self._conn = None
            self._authenticated = False

    def read_events(self):
        self.send(words=["admin.eventsEnabled", "true"])

        while True:
            raw = self._read_response()
            yield raw["words"]
