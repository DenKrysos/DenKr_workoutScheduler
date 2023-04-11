#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-09

@author: Dennis Krummacker
'''


from settings.values import muscleIdentifier, equipmentIdentifier


#Here, you can safely change the numeric values per muscle.
# But! Leave the names alone, they are internally used by some functions
# - - - - - - - - -
#INSTRUCTIONS:
#Tuple-Values: (Muscle-Name, Muscle-Type, Workouts-per-Week, Sets-per-Week)
#- Muscle-Name: Name of the Muscle, just leave alone, is used internally
#- Muscle-Type: Big-or-Small-Muscle. 1: Big, 2: Small.
#- Workouts-per-Week: How often, in terms of workouts the muscle is approached per week.
#- Sets-per-Week: How many Sets in one week shall be exercised for this muscle.
muscle_setup=[
    (muscleIdentifier.chest.value,1,2,10),
    (muscleIdentifier.back.value,1,2,10),
    (muscleIdentifier.rotator_cuff.value,2,1.25,6),
    (muscleIdentifier.delt_front.value,2,0.75,5),
    (muscleIdentifier.delt_rear.value,2,1,5),
    (muscleIdentifier.delt_side.value,2,1,5),
    (muscleIdentifier.quads_n_glutes.value,1,1.5,10),#1.75 per Week
    (muscleIdentifier.biceps.value,2,1,5),
    (muscleIdentifier.triceps.value,2,1,5),
    (muscleIdentifier.hamstrings.value,2,1,5),
    (muscleIdentifier.abs.value,1,1.5,8),
    (muscleIdentifier.calves.value,2,1,6),
    (muscleIdentifier.trapez.value,2,1,5),
    (muscleIdentifier.lower_back.value,2,0.75,5)
]
    #Chest -- Brust
    #Back -- Rücken
    #Quads -- Quadrizeps (Oberschenkel)
    #Glutes -- Pobacken (Gluteus Maximus)
    #Hamstrings -- Beinbizeps
    #Abs/Calves -- Bauch & Waden | Liegen mehr zwischen Groß&Klein. Teilen sich miteinander ein 3-Mal innerhalb von 2 Wochen (Werden gern zusammengefasst, haben aber nichts groß miteinander zu tun)
    #Abs/Calves -- Bauch & Waden | Liegen mehr zwischen Groß&Klein. Teilen sich miteinander ein 3-Mal innerhalb von 2 Wochen (Werden gern zusammengefasst, haben aber nichts groß miteinander zu tun)
    #Bizeps
    #Trizeps
    #Rear-Delts / Back-Delts (Hinterer (oberer) Schulter-Muskel)
    #Side-Delts (Seitlicher (oberer) Schulter-Muskel)
    #Front-Delts (Forderer (oberer) Schulter-Muskel)
    #Trapezius
#-----------------------------------------------------


#INSTRUCTIONS:
#Tuple-Values: (Exercise-Name, Precedence, Equipment-Requirement, muscleIntensity, EnableDisable)
#- Exercise-Name: Name of the Exercise.
#- Precedence: Assigns some kind of "weight/importance" to an exercise. Gives the possibility to have certain exercise occur more often (or less) over continious computations. Base-Value: 1. Don't let it deviate too much from 1. 2 is fine to roughly double its frequence, 0.5 to roughly halve it.
#- Equipment-Requirement: What is required to perform the exercise. Gym-Equipment, simple Dumbbells, only own Body. With setting the appropriate values in _1cfg/configuration.py, entire sets of exercises can be deactivated for computation. (When an exercise only has equipment capabilities that are set to False, it won't be proposed in your training plan.
#- muscleIntensity: To which intensity the exercise trains individual muscles. 0< & <=1. Can attack multiple muscles.
#- EnableDisable. Can be used to Enable or Disable single Exercises for your schedule computation. True: Exercise will be included. False: Exercise is excluded.
exercise_setup=[
    #########################
    ###  Chest           ####
    #########################
    ("Uni-lateral Butterfly",
        1.0,
        [equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("UCV-Raise -> Cavaliere-Crossover",
        1.0,
        [equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],0.9)],
        True
    ),
    ("Bench-Press",
        1.5,
        [equipmentIdentifier.Barbell.value[0],equipmentIdentifier.MountBench.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Dumbbell-Press",
        1.0,
        [equipmentIdentifier.SimpleBench.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Low Rotation Push-Up (e.g. on Dumbbell)",
        0.75,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("High Rotation Push-Up (e.g. on Dumbbell)",
        0.75,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Dips",
        0.6,# Only seldom as primary exercise. Include it as Intensity-Finisher with other exercises
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.chest.value[0],85),(muscleIdentifier.serratus_ant.value[0],0.7)],
        True
    ),
    ("Reverse Dips / Raising Butterfly (Sling/CablePull)",
        0.9,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Butterfly (Sling/Dumbbell/CablePull)",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Positive Push-Up",
        0.5,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.chest.value[0],0.6)],
        True
    ),
    ("Negative Push-Up",
        0.5,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.chest.value[0],0.6)],
        True
    ),
    ("Sling, Push-Up w/ Reach-out",
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Sling, Superman Push-Up",
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Push-Up (Sling/Bodyweight)",
        0.5,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],0.9)],
        False
    ),
    ("Sling Push-Up (Grip-Variation: over/under, parallel-inner/outer)",
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],0.9)],
        True
    ),
    ("Push-Up (Feet in Sling)",
        0.4,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Push-Up w/ Roll-out",
        0.55,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Power-Push",
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Reverse Archer / Push into Cross",
        0.6,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    ("Fall-Out",
        0.4,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)],
        True
    ),
    #########################
    ###  Back            ####
    #########################
    ("Row",
        0.7,#Lowered, because I often times use Row as Intensity-Finisher after other exercises. So I don't include it that often as primary exercise.
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1.0)],
        True
    ),
    ("Inverted Row",
        0.7,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1.0)],
        True
    ),
    ("Single-Arm-Row",
        0.6,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1)],
        True
    ),
    ("Sling, Single-Arm-Row w/ Rotation",
        0.85,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.back.value[0],1)],
        True
    ),
    ("Long-Arm Pull-down",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1)],
        True
    ),
    ("Pull-Up",
        1.2,
        [equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.back.value[0],1)],
        True
    ),
    ("Rev-Grip Pull-Up",
        1.2,
        [equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.back.value[0],1)],
        True
    ),
    ("Human Pull-Over",
        0.65,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.back.value[0],0.6)],
        True
    ),
    ("Sling, Archer-Row / Row into Cross",
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.back.value[0],0.8),(muscleIdentifier.trapez.value[0],0.3)],
        True
    ),
    ("Power-Pull",
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.back.value[0],1)],
        True
    ),
    ("Cable Pull-Down",#Latziehen
        1.0,
        [equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1)],
        True
    ),
    #########################
    ###  Rotator-Cuff    ####
    #########################
    ("Facepull",
        1.5,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],1),(muscleIdentifier.delt_rear.value[0],0.1)],
        True
    ),
    ("External-Rotation",
        1.0,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],1),(muscleIdentifier.trapez.value[0],0.1)],
        True
    ),
    ("Scarecrow -> Y-Pull",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],1)],
        True
    ),
    ("W-Pull",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],0.8)],
        True
    ),
    #########################
    ###  Delt-Front      ####
    #########################
    ("Urlacher",
        1.0,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)],
        True
    ),
    ("Scoop-Press",
        1.1,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.chest.value[0],0.05),(muscleIdentifier.delt_front.value[0],1),(muscleIdentifier.serratus_ant.value[0],0.6)],
        True
    ),
    ("Handstand Push-Up",
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)],
        True
    ),
    ("Reach-out Y-Pull",
        0.7,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)],
        True
    ),
    ("High-Pull",# Carefull when doing this. Do it right or you risk impingement
        0.7,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)],
        True
    ),
    ("Dumbbell Clean & Press",
        0.9,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.delt_front.value[0],1),(muscleIdentifier.lower_back.value[0],0.15)],
        True
    ),
    #########################
    ###  Delt-Rear       ####
    #########################
    ("Rear-Delt Row (prior with Dumbbell)",
        1.0,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)],
        True
    ),
    ("Rotating Reverse-Butterfly",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)],
        True
    ),
    ("Back Widow",
        0.8,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1.0)],
        True
    ),
    ("Pull-Back (similar to Facepull)",
        0.6,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)],
        True
    ),
    ("Crab-Row (\"Rear-Delt Row\")",
        0.8,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)],
        True
    ),
    ("Sling, Ext.-rotated Pull-to-Cross",
        0.5,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)],
        True
    ),
    #########################
    ###  Delt-Side       ####
    #########################
    ("Reach-out Rev-Butterfly",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],0.1),(muscleIdentifier.delt_side.value[0],0.8),(muscleIdentifier.serratus_ant.value[0],0.6)],
        True
    ),
    ("Uni-lateral Lateral-Raise",
        1.0,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_side.value[0],1)],
        True
    ),
    ("Bi-lateral Lateral-Raise",
        0.85,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_side.value[0],1)],
        True
    ),
    ("Reverse Butterfly",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_side.value[0],0.75),(muscleIdentifier.trapez.value[0],0.4)],#,(muscleIdentifier.rotator_cuff.value[0],0.4)
        True
    ),
    ("Delta-Fly",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_side.value[0],1)],
        True
    ),
    #########################
    ###  Quads-&-Glutes  ####
    #########################
    ("Romanian Split Squat",
        1.1,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Sling, Single-Leg Squat",
        1.2,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Sling, Single-Leg Pistol-Squat",
        0.9,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Single-Leg Box-Squat",
        1.1,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Single-Leg-Box-Squat -> 1 1/2 Squat -> Slight Jump Squat",
        0.7,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Alt. Heel-touch Squat -> Alt. Sprint-Start Lunge -> Plyo Sprinter Lunge",
        0.7,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Alt Crossover Step-Up -> Alt. Reverse Lunge -> Split Squat Jump",
        0.7,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Crab-Walk (Resist-Band)",
        0.8,
        [equipmentIdentifier.ResistanceBand.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Sling, Alpine-Row",
        0.5,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Lateral Lunge (Dumbbell/BW/Sling)",
        1.0,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Sling.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Lunge to High-Knee / Reverse Version",
        0.4,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    ("Weighted Squats",
        1.1,
        [equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)],
        True
    ),
    #########################
    ###  Biceps          ####
    #########################
    # NOTE: One does not need ordinary "Dumbbell Curls" or "Hammer Curls". Just do the 3-Variation Curls
    ("3-Variation Curls (underhand inwards -> overhand inwards -> underhand outwards)",
        1.4,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.biceps.value[0],1)],
        True
    ),
    ("Sling, w/ Shoulder-Raise",
        1.0,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1),(muscleIdentifier.delt_front.value[0],0.15)],
        True
    ),
    ("Sling, Cross-Chest",
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1)],
        True
    ),
    ("Sling, Chest-Tap",
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1)],
        True
    ),
    ("Chin-Curl",
        0.8,
        [equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.back.value[0],0.51),(muscleIdentifier.biceps.value[0],0.8)],
        True
    ),
    ("Bent-forward inwards Curl",
        1.0,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.biceps.value[0],1)],
        True
    ),
    ("Sling, Hercules Curl",
        0.2,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1)],
        True
    ),
    #########################
    ###  Triceps         ####
    #########################
    ("Kick-Back / Back-Extension",
        0.75,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        True
    ),
    ("3-Var Push-Up (inefficient Back-Extension -> Cobra Push-Up -> Diamond Push-Up)",
        1.3,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        True
    ),
    ("Parallel-Grip Pull",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        True
    ),
    ("Pull-Down (Undergrip)",
        0.75,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        True
    ),
    ("Push-Down (Overgrip)",
        0.8,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        True
    ),
    ("Backside Dips",
        0.45,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        False
    ),
    ("Triceps Bench-Press",
        1.0,
        [equipmentIdentifier.MountBench.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        True
    ),
    ("Bench Triceps-Stretch (Bench & SZ-Barbell)",
        1.0,
        [equipmentIdentifier.Barbell.value[0]],
        [(muscleIdentifier.triceps.value[0],1)],
        True
    ),
    #########################
    ###  Hamstrings      ####
    #########################
    ("Hip-Thrust",
        1.5,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.Barbell.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.25),(muscleIdentifier.hamstrings.value[0],0.75)],# (muscleIdentifier.lower_back.value[0],0.55)
        True
    ),
    ("Hamstring-Curls",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.hamstrings.value[0],1)],
        True
    ),
    ("Long Leg March",
        0.8,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.1),(muscleIdentifier.hamstrings.value[0],0.75)],
        True
    ),
    ("High Hip Bucks",
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.25),(muscleIdentifier.hamstrings.value[0],0.9),(muscleIdentifier.lower_back.value[0],0.2)],
        True
    ),
    #########################
    ###  Abs             ####
    #########################
    ("BW Side Lateral Raise",
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],0.2),(muscleIdentifier.quads_n_glutes.value[0],0.2),(muscleIdentifier.abs.value[0],0.46),(muscleIdentifier.lower_back.value[0],0.1)],
        True
    ),
    ("Hanging Leg-Raise (Legs straight or drawn)",
        0.65,#Because there are two slightly distinct exercises
        [equipmentIdentifier.PullUpBar.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Hanging Leg-Raise edgeways (Legs straight or drawn)",
        0.75,#Because there are two slightly distinct exercises
        [equipmentIdentifier.PullUpBar.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Floor, 3-Compund from (Cross-Ellbow-Knee, Hip-Up-Crunch, Diagonal-Ellbow-Thrust)",
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Floor, 3-Compund from (Candle, Levitation Sit-Up, Hand crossed past leg)",
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Rev Corkscrew -> Black Widow Knee Slide -> Levitation Crunch",
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Ab Halo -> V-Up Tuck -> Sit-Up Ellbow-Thrust",
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Sit-Up -> Candle -> Crunch",
        0.3,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Sling, Crunch",
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Sling sideways",
        1.0,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Sling Candle",
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Core-Rotation -> Sit-Up",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    ("Corkscrew (Hanging/Feet-in-Sling)",
        0.6,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.abs.value[0],1)],
        True
    ),
    #########################
    ###  Calves          ####
    #########################
    ("Calf Press (Uni- or Bi-lateral)",
        1.0,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.calves.value[0],1)],
        True
    ),
    ("Sprinting Calf Press (Uni- or Bi-lateral)",
        1.0,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.calves.value[0],1)],
        True
    ),
    #########################
    ###  Trapez          ####
    #########################
    ("Dumbbell Full-Motion",
        1.0,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.trapez.value[0],1)],
        True
    ),
    ("Pull-back, roll-downwards",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.trapez.value[0],1)],
        True
    ),
    ("Uni-lateral Pull-back",
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.trapez.value[0],1)],
        True
    ),
    ("Neck Pull-Up, rotate down",
        0.6,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.trapez.value[0],1)],
        True
    ),
    #########################
    ###  Lower-Back      ####
    #########################
    ("Deadlift",
        1.4,
        [equipmentIdentifier.Barbell.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.46),(muscleIdentifier.lower_back.value[0],1)],
        True
    ),
    ("Rev Hyper-Extension",
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.lower_back.value[0],1)],
        True
    ),
    ("Sling, Hanging L-Sit to Hip-Thrust",
        1.2,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.lower_back.value[0],1)],
        True
    ),
    ("Sling Leg-March (side- or backwards)",
        0.9,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.lower_back.value[0],1)],
        True
    ),
    ("Angels & Devils",
        0.9,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.1),(muscleIdentifier.lower_back.value[0],1)],
        True
    ),
    ("Raise Hand-&-Foot diagonal",
        0.3,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.1),(muscleIdentifier.lower_back.value[0],0.8),(muscleIdentifier.delt_side.value[0],0.5)],
        True
    )
]





#Warmup-Exercises
# Delt-Front/Side: Prowler Push-Up, Bodyweight
#                  Frog Push-Up