#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2023-04-09

@author: Dennis Krummacker
'''


from enum import Enum



#-----------------------------------------------------
# Muscle-Identifier
class muscleID(Enum):
    undef=[0,"<undefined>"]
    chest=[1,"Chest"]
    back=[2,"Back"]
    rotator_cuff=[3,"Rotator-Cuff"]
    delt_front=[4,"Delt-Front"]
    delt_rear=[5,"Delt-Rear"]
    delt_side=[6,"Delt-Side"]
    quads_n_glutes=[7,"Quads-&-Glutes"]
    biceps=[8,"Biceps"]
    triceps=[9,"Triceps"]
    hamstrings=[10,"Hamstrings"]
    abs=[11,"Abs"]
    calves=[12,"Calves"]
    trapez=[13,"Trapez"]
    lower_back=[14,"Lower-Back"]
    serratus_ant=[15,"Serratus-Anterior"]#Currently not really explicitly included in calculation
#-----------------------------------------------------
# Equipment-Identifier
class equipID(Enum):
    undef=[0,"<undefined>"]
    Bodyweight=[1,"Bodyweight"]
    Sling=[2,"Sling"]
    ResistanceBand=[3,"Resistance-Band"]
    Dumbbell=[4,"Dumbbell"]
    Barbell=[5,"Barbell"]
    PullUpBar=[6,"Pull-Up-Bar"]
    SimpleBench=[7,"Simple-Bench"]# A simple Bench/Step, something where you can lie on to elevate your body and have your arms free to go deeper than your body
    MountBench=[8,"Mount-Bench"]# A sophisticated Bench with a mount attached for a barbell
    CablePull=[9,"Cable-Pull"]
    Gym=[10,"Gym"]
#-----------------------------------------------------
#=====================================================
#=====================================================
#-----------------------------------------------------
class SetupExeIdx:
    NAME=0
    INHERENT=1
    ENABLED=2
    PRECEDENCE=3
    EQUIPMENT=4
    INTENSITY=5


class BOILERPLATE:
    @classmethod
    def empty_exercise(cls):
        empty_exercise=[
            "<new>", 0, True,
            1.0,
            [
                equipID.undef
            ],
            [
                [
                    muscleID.undef,
                    1
                ]
            ]
        ]
        return empty_exercise











#-----------------------------------------------------
class useMeth(Enum):
    Terminal=[1,"Terminal"]
    GUI=[2,"GUI"]
#-----------------------------------------------------