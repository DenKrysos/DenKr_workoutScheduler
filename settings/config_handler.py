#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-15

@author: Dennis Krummacker
'''


import _1cfg.configuration as configuration
import _1cfg.setup as setup


keyUseMeth='UsageMethodology'
keyOutRev='OutputReverse'
keyWOpW='WorkoutsPerWeek'
keyNumComp='NumberWorkoutsToCompute'
keyVolScal='VolumeScaling'
keyExeEquip='ExercisesToInclude'

cfg_handle={
    keyUseMeth: configuration.usageMethodology,
    keyOutRev: configuration.upcomingOutput_Reverse,
    keyWOpW: configuration.workouts_perWeek,
    keyNumComp: configuration.num_workout_toCompute,
    keyVolScal: configuration.volumeScaling,
    keyExeEquip: configuration.exercisesToInclude
}


keySetupMuscle='SetupMuscle'
keySetupExe='SetupExercise'

cfgSetup_handle_inherent={
    keySetupMuscle:setup.muscle_setup,
    keySetupExe:setup.exercise_setup
}
cfgSetup_handle={}



#Double-Write Strategy. On Config-Read, the cfg_handle is updated and a deepcopy of it is created to cfgh_rt ('rt' for "Runtime-Copy")
# During runtime actually the _rt is used to read values and make changes for runtime-operations.
# When written to disk, the cfg_handle is written down
# Certain cfg-changes directly alter cfg_handle (and _rt simultaneously), other shall only change the runtime behavior and not the persistent storage config, hence do only alter _rt
# If desired, on certain operations, the _rt can be written to cfg_handle, to then dump the current runtime status to persistent storage.
cfgh_rt={}
cfgSetup_rt={}