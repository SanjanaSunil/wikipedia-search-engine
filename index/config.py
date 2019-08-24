import resource

TEMP_INDICES_DIR = 'indices'
MAX_OPEN_FILES = resource.getrlimit(resource.RLIMIT_NOFILE)[0]