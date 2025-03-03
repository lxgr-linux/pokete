import logging
from pokete.release import SAVEPATH, CODENAME, VERSION


def init_logger(do_logging: bool):
    # logging config
    log_file = (SAVEPATH / "pokete.log") if do_logging else None
    logging.basicConfig(filename=log_file,
                        format='[%(asctime)s][%(levelname)s]: %(message)s',
                        level=logging.DEBUG if do_logging else logging.ERROR)
    logging.info("=== Startup Pokete %s v%s ===", CODENAME, VERSION)
