import logging

from pokete import release

logger = logging.getLogger("startup")


def init_logger(do_logging: bool) -> None:
    # logging config
    log_file = (release.SAVEPATH / "pokete.log") if do_logging else None
    logging.basicConfig(
        filename=log_file,
        format="[%(asctime)s][%(levelname)s][%(name)s]: %(message)s",
        level=logging.DEBUG if do_logging else logging.ERROR,
    )
    logger.info("=== Startup Pokete %s v%s ===", release.CODENAME, release.VERSION)
