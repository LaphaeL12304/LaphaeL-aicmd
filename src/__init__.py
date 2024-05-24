#!/usr/bin/env python3
import os
from . import main

def cli():
    # 切换到 home 目录 - switch to home directory
    os.chdir(os.path.expanduser('~'))
    main.main()

if __name__ == "__main__":
    cli()
