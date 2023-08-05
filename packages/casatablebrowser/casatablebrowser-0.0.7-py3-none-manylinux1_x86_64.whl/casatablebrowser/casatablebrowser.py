##########################################################################
#
# Copyright (C) 2021
# Associated Universities, Inc. Washington DC, USA.
#
# This script is free software; you can redistribute it and/or modify it
# under the terms of the GNU Library General Public License as published by
# the Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Library General Public
# License for more details.
#
# You should have received a copy of the GNU Library General Public License
# along with this library; if not, write to the Free Software Foundation,
# Inc., 675 Massachusetts Ave, Cambridge, MA 02139, USA.
#
# Correspondence concerning AIPS++ should be adressed as follows:
#        Internet email: aips2-request@nrao.edu.
#        Postal address: AIPS++ Project Office
#                        National Radio Astronomy Observatory
#                        520 Edgemont Road
#                        Charlottesville, VA 22903-2475 USA
###########################################################################
import os as __os
import subprocess
import atexit
import platform


def casatablebrowser( tab=None, cleanup=True ):
    app_path = __os.path.abspath(__os.path.dirname(__file__))
    flavor = platform.system( )
    if flavor == 'Linux':
        app_path = __os.path.join( app_path, "__bin__","casatablebrowser-x86_64.AppImage" )
    elif flavor == 'Darwin':
        app_path = __os.path.join( app_path, '__bin__', 'casatablebrowser.app', 'Contents', 'MacOS', 'casatablebrowser' )
    else:
        raise Exception('unsupported platform')

    args = [ app_path ]
    if tab is not None:
        if __os.path.isdir(tab):
            args.append( tab )
        else:
            raise RuntimeError( '"tab" parameter is not a directory' )
    
    try:
        p = subprocess.Popen(args)
        if cleanup:

            @atexit.register
            def stop_casatablebrowser():
                p.kill()

    except FileNotFoundError as error:
        print(f"Error: {error.strerror}")


if __name__ == "__main__":
    casatablebrowser(False)
