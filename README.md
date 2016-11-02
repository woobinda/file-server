Python implementation of File Server for Radioteria. Flask framework. 

Server provides POST, GET, and DELETE methods for work with audio files.
Provides client authentication using a token systems.
All files are placed in a tree structure of folders on the disc.

Server supports the exact configuration from the console and may be configurated in settings.py file.

To install all dependencies and runn App may use Makefile with sudo console command:

$make start
