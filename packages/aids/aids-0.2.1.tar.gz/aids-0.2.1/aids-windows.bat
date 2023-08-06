@echo off & python -x "%~f0" %* & goto :eof
from aids.manage import get_command

get_command()
