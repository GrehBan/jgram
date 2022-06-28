import logging

root_logger = logging.getLogger('jgram')
loader_logger = root_logger.getChild('loader')
registry_logger = root_logger.getChild('registry')
manager_logger = root_logger.getChild('manager')
context_logger = root_logger.getChild('context')
handler_logger = registry_logger.getChild('handler')
