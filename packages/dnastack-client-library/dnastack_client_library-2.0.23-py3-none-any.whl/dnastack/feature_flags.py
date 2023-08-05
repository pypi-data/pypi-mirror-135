import os

__boolean_flag = lambda k: str(os.getenv(k) or '').lower() in ['1', 'true']

in_global_debug_mode = __boolean_flag('DNASTACK_CLI_DEBUG')
