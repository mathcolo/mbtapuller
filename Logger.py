import sys
import logging

log = logging.getLogger('mbtapuller')

handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(logging.Formatter('%(asctime)s [%(module)s]: %(message)s'))
handler.setLevel(logging.INFO)

log.addHandler(handler)
log.setLevel(logging.INFO)

def info(message):
    log.info(message)