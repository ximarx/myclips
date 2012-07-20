import logging

FORMAT = '[%(levelname).3s %(module)s::%(funcName)s:%(lineno)d] %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger('myclips')
logger.setLevel(logging.DEBUG)

#
#logger.debug("Logger enabled")
#logger.info("Logger enabled")
#logger.warn("Logger enabled")
#logger.error("Logger enabled")
#logger.critical("Logger enabled")
