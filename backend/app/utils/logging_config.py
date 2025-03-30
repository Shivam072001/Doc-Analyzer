import logging
import os

def setup_logging(app):
    log_level = logging.INFO if app.debug else logging.WARNING
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s',
        filename=os.path.join(app.config.get('LOGS_DIR', '.'), 'app.log'),
        filemode='a'
    )
    if app.debug:
        logging.getLogger().addHandler(logging.StreamHandler())