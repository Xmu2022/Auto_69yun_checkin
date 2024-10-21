# -*- coding: utf-8 -*-

import os
import importlib.util

file_path = os.path.abspath("interface_main.cpython-38-x86_64-linux-gnu.so")
spec = importlib.util.spec_from_file_location("interface_main", file_path)
interface_main = importlib.util.module_from_spec(spec)
spec.loader.exec_module(interface_main)

if __name__ == "__main__":
    import asyncio
    asyncio.run(interface_main.main())
