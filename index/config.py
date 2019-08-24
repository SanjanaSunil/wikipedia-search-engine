import resource

OUTPUT_DIR = ''
MAX_OPEN_FILES = resource.getrlimit(resource.RLIMIT_NOFILE)[0]