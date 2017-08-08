
"""
Copyright [2016] [Mark Hill, Matthew Waite]
          [2017] [Deniz Erbilgin]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import binascii
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import logging


# lifted from https://cryptography.io/en/latest/hazmat/primitives/symmetric-encryption/#cryptography.hazmat.primitives.ciphers.modes.GCM
# for test case to work, we need to comment out the next 2 lines!! ToDo Ill have to get my head around pyunit
#from datamodel.datamodelquery import SensorLocationQuery
#from datamodel.datamodelquery import SensorQuery

# AESGCM encoding 101
#--------------------

#     The algorithm has four inputs: a secret key, an initialisation vector (IV),  plain-text, and an input for additional authenticated data (AAD).
# It has two outputs, a cipher-text whose length is identical to the
# plain-text, and an authentication tag

#        where:

#        inputs
#        * The secret key is the 128bit preshared key
#        * The IV is as per this spec - http://www.earth.org.uk/OpenTRV/stds/network/20151203-DRAFT-SecureBasicFrame.txt
#        * The plain text is the message body, 0 padded to 32 bits
#        * AAD is the 8 header bytes of the frame (length, type, seqlen, 4xID bytes, bodyLength)
#
#        outputs
#        * The cipher text is the encrypted message body and is the same length as the plain text.
#        * The authentication tag, used to check the vaidity of the message originator.
#
#       The transmitted frame then contains:
#         The 8 byte header (unencrypted)
#         The 32 byte padded body (encrypted)
# The 23 byte trailer (which includes the 16byte authentication tag) as
# detailed in the spec (unencrypted)


# openTRVAesgcmPacket Class is initialised with and OpenTRV AESGCM encoded packet and the pre-shared LSBs of the
# leaf node address (ID). FRom that data, the class can extract the

class OpenTRVAesgcmPacket(object):
    """
    Open TRV packet format
    ----------------------
    | Authenticated Additional Data                                                   | Plain/cipher text    | Reset + message counters, tag and encryption type
    |length byte|type byte|Seq_num + id_len byte| variable length ID |body length byte| variable length body | variable length trailer (1 byte or 23 bytes)

    Class instance expects the encrypted packet, stored as a bytearray and the  6 bytes of
    The 6 byte leaf node ID required for the decrypt (the full ID is 8 c-bytes long) also stored as a byte array.
    """

    def __init__(self):
        pass


def prettyprint(data):
    line = ""
    for i in range(len(data)):
        # comma at EOL stops new line at every iteration.
        line += "%02x " % data[i]
    return line

INDEX_FRAME_LENGTH = 0 # First byte is frame length
INDEX_FRAME_TYPE = 1  # Frame Type
INDEX_SEQUENCE_NUMBER = 2  # Frame Sequence number = upper nibble byte 2
INDEX_ID_LENGTH = 2  # ID length = lower nibble of byte 2
INDEX_ID_START = 3      # the ID starts at byte 3 and is IDLEN bytes long


def additional_data(packet):
    """ Put additional authenticated data (ad) in its own buffer.

    The ad consists of the start of the packet up to but not including the start of the ciphertext.

    :param packet: Raw byte encoded secure frame.
    :return: Additional authenticated data as a bytes object.
    """

    # Packet length + secure O-frame type + (sequence number & ID length) + len(ID)
    # On a usual V0p2 secure frame (e.g. as in RC3-5 releases) this will be 8-bytes.
    ad_length = 4 + (packet[INDEX_ID_LENGTH] & 0x0f)
    log.debug("aesgcm:additional_date:ad_length: " + str(ad_length))
    ad = bytes(packet[:ad_length])
    total_length = len(packet)  # +1 for length
    log.debug("aesgcm:additional_data:total_length: " + str(total_length))
    return ad


def split_packet(packet):
    id_length = packet[INDEX_ID_LENGTH] & 0x0f
    index_text_start = INDEX_ID_START + id_length + 1
    text_length = packet[INDEX_ID_START + id_length]
    return id_length, index_text_start, text_length


def cipher_text(packet):
    (id_length, index_text_start, text_length) = split_packet(packet)
    return packet[index_text_start:index_text_start + text_length]


def hex_string_to_bytes(s):
    return binascii.unhexlify(s.replace(' ', '').lower())


def tag(packet):
    # The tag is 16 bytes long , and starts 17 bytes from the end of the packet (there is a 0x80 aes-gcm
    # identifier byte at the end of the end of the packet) hence the magic
    # numbers 17 and 16.
    index_tag_start = len(packet) - 17
    tg = packet[index_tag_start:-1]
    return bytes(tg)


def initialisation_vector(packet, node_id):
    (id_length, index_text_start, text_length) = split_packet(packet)

    index_trailer_start = index_text_start + text_length
    # Bytes 0-3 of trailer are the restart counter
    index_restart_counter = index_trailer_start
    # Bytes 4-6 of trailer are the Message Counter
    index_message_counter = index_restart_counter + 3
    # Bytes 7 - 21 are the Authentication tag
    index_authentication_tag = index_message_counter + 3

    nonce = bytearray()
    # copy 6 MSBs of ID contained in the sixByteID passed in at class
    # instantiation
    nonce.extend(hex_string_to_bytes(node_id[:12]))
    log.debug("iv:should be 6: " + str(len(nonce)))
    # copy the 3 bytes of restart counter
    nonce.extend(packet[index_restart_counter:index_message_counter])
    log.debug("iv:should be 9: " + str(len(nonce)))
    # copy the 3 bytes of the message counter
    nonce.extend(packet[index_message_counter:index_authentication_tag])
    log.debug("iv:should be 12: " + str(len(nonce)))
    return bytes(nonce)


def decrypt_message(data_packet, hex_key, node_id):
    retval = None
    log.debug("decrypting for node " + node_id)
    log.debug("aesgcm:eMFEP2:data_packet:pp (len) (" + str(len(data_packet)) + ") ")
    log.debug(prettyprint(data_packet))

    # key is from the csv file, 128 bits
    # aad is additional data, from (length, type, seqlen, 4xID bytes, bodyLength)
    # iv is initialisation vector, from
    # ciphertext is from packet
    # tag is from
    # data_packet is a handful of byte
    if data_packet[len(data_packet) - 1] == 0x80:
        log.debug("aesgcm encryption used")

        # packet contains the entire packet, except for the leading length byte
        # indices are reference as per normal Python from 0 - hence the frame type (cf) is at index 0

        log.debug("initialisation vector...")
        iv = initialisation_vector(data_packet, node_id)
        log.debug("cipher text...")
        ct = cipher_text(data_packet)
        log.debug("tag...")
        tg = tag(data_packet)
        log.debug("additional data...")
        ad = additional_data(data_packet)
        key = hex_string_to_bytes(hex_key)
        log.debug("preparation complete")
        debug_array = [iv, ct, tg, ad, key]
        log.debug("len | pp:iv,ct,tg,ad,key")
        [log.debug("{:>2} | {}".format(repr(len(x)), prettyprint(x))) for x in debug_array]

        log.debug("attempting decryption...")
        try:
            buf = ct + tg  # aesgcm.decrypt takes a buffer with the tag appended to the ciphertext.
            aesgcm = AESGCM(key)  # (DE20170807) Shiny new interface in cryptography v2.x
            retval = aesgcm.decrypt(iv, buf, ad)
            log.debug("decrypted")

        except Exception as e:
            log.error('decryption failed with exception: {}: {}'.format(e.__class__.__name__, e))

    return retval

log = logging.getLogger('root')
