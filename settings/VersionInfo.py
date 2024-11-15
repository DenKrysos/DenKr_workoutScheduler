#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-11

@author: Dennis Krummacker
'''

VERSION_DevStage="beta"
# VERSION_ReleaseTrack="Preview"
# VERSION_ReleaseTrackMAJOR=1
VERSION_MAJOR=0
VERSION_MINOR=5
VERSION_PATCH=2
VERSION_TWEAK=0

if 0<VERSION_TWEAK:
    VERSION_NUMBER="%s.%s.%s_%s"%(VERSION_MAJOR,VERSION_MINOR,VERSION_PATCH,VERSION_TWEAK)
else:
    VERSION_NUMBER="%s.%s.%s"%(VERSION_MAJOR,VERSION_MINOR,VERSION_PATCH)

VERSION_DESCRIPTION="%s"%(VERSION_NUMBER)

try: VERSION_DevStage
except NameError: VERSION_DevStage=None
if not VERSION_DevStage is None and 0<len(VERSION_DevStage):
    VERSION_DESCRIPTION="%s-%s"%(VERSION_DevStage,VERSION_DESCRIPTION)

try: VERSION_ReleaseTrack
except NameError: VERSION_ReleaseTrack=None
try: VERSION_ReleaseTrackMAJOR
except NameError: VERSION_ReleaseTrackMAJOR=None
if not VERSION_ReleaseTrack is None and 0<len(VERSION_ReleaseTrack) and not VERSION_ReleaseTrackMAJOR is None and 0<VERSION_ReleaseTrackMAJOR:
    VERSION_ReleaseTRACKDescription=f"{VERSION_ReleaseTrack}-{VERSION_ReleaseTrackMAJOR}"
else:
    VERSION_ReleaseTRACKDescription=None

if not VERSION_ReleaseTRACKDescription is None:
    VERSION_DESCRIPTION=f"{VERSION_DESCRIPTION}:{VERSION_ReleaseTRACKDescription}"