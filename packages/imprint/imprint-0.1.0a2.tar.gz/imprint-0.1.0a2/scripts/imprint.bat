@ECHO off

REM imprint: a program for creating documents from data and content templates

REM Copyright (C) 2019  Joseph R. Fox-Rabinovitz <jfoxrabinovitz at gmail dot com>

REM This program is free software: you can redistribute it and/or modify
REM it under the terms of the GNU Affero General Public License as
REM published by the Free Software Foundation, either version 3 of the
REM License, or (at your option) any later version.

REM This program is distributed in the hope that it will be useful,
REM but WITHOUT ANY WARRANTY; without even the implied warranty of
REM MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
REM GNU Affero General Public License for more details.

REM You should have received a copy of the GNU Affero General Public License
REM along with this program.  If not, see <https://www.gnu.org/licenses/>.

REM Author: Joseph Fox-Rabinovitz <jfoxrabinovitz at gmail dot com>
REM Version: 13 Apr 2019: Initial Coding


REM Runs imprint in the same directory as as this batch file.

setlocal

set "script_path=%~dp0\imprint"

python "%script_path%" %*
endlocal
