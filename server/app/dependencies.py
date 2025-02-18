import pathlib
import os
from config.settings import settings


def model_path(name, model_id):
    return os.path.join(settings.data_dir, "models", name, model_id)

def model_base_path(name):
    return os.path.join(settings.data_dir, "models", name)