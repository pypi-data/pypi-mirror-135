import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["common", "project_logs", "gui", 'main'],
}
setup(
    name="mess_server",
    version="0.0.1",
    description="mess_server",
    options={
        "build_exe": build_exe_options
    },
    executables=[Executable('main/server_start.py',
                            # base='Win32GUI',
                            targetName='server_start.exe',
                            )]
)
