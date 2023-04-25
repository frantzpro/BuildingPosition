#!/usr/bin/env python
import signal
import sys
import time
from time import sleep

from AbstractVirtualCapability import AbstractVirtualCapability, VirtualCapabilityServer, formatPrint


class BuildingPosition(AbstractVirtualCapability):
    def __init__(self, server):
        super().__init__(server)
        self.functionality = {"GetBuildingPosition": None}

    def GetBuildingPosition(self, params: dict) -> dict:
        if self.functionality["GetBuildingPosition"] is not None:
            vicon_name = params["SimpleStringParameter"]
            if not isinstance(vicon_name, str):
                raise TypeError("Parameter of Function has to be a String")
            pos = self.functionality["GetBuildingPosition"](vicon_name)
            return {"Position3D": pos}
        else:
            return {"Position3D": [0., 0., 0.]}

    def loop(self):
        pass
        
if __name__ == '__main__':
    # Needed for properly closing when process is being stopped with SIGTERM signal
    def handler(signum, frame):
        print("[Main] Received SIGTERM signal")
        listener.kill()
        quit(1)


    try:
        port = None
        if len(sys.argv[1:]) > 0:
            port = int(sys.argv[1])
        server = VirtualCapabilityServer(port)
        listener = BuildingPosition(server)
        listener.start()
        signal.signal(signal.SIGTERM, handler)
        listener.join()
    # Needed for properly closing, when program is being stopped wit a Keyboard Interrupt
    except KeyboardInterrupt:
        print("[Main] Received KeyboardInterrupt")
        server.kill()
        listener.kill()
