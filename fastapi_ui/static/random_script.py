import os, random
import logging

logger = logging.getLogger(__name__)



def list_random_files(static_images_folder):
    package_dir = os.path.dirname(os.path.abspath(__file__))
    radom_dir = os.path.join(package_dir,'images/' + static_images_folder)
    random_file = random.choice(os.listdir(radom_dir))
    logger.info(radom_dir)

    return random_file
