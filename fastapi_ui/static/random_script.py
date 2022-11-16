import os, random
import logging

logger = logging.getLogger(__name__)



def list_random_files():
    package_dir = os.path.dirname(os.path.abspath(__file__))
    radom_dir = os.path.join(package_dir,'images/inference_images/')
    # radom_dir = package_dir
    random_file = random.choice(os.listdir(radom_dir))
    logger.info(radom_dir)

    return random_file
