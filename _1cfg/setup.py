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
    ("Uni-lateral Butterfly", True,
        1.0,
        [equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("UCV-Raise -> Cavaliere-Crossover", True,
        1.0,
        [equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],0.9)]
    ),
    ("Bench-Press", True,
        1.5,
        [equipmentIdentifier.Barbell.value[0],equipmentIdentifier.MountBench.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Dumbbell-Press", True,
        1.0,
        [equipmentIdentifier.SimpleBench.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Low Rotation Push-Up (e.g. on Dumbbell)", True,
        0.75,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("High Rotation Push-Up (e.g. on Dumbbell)", True,
        0.75,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Dips", True,
        0.6,# Only seldom as primary exercise. Include it as Intensity-Finisher with other exercises
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.chest.value[0],85),(muscleIdentifier.serratus_ant.value[0],0.7)]
    ),
    ("Reverse Dips / Raising Butterfly (Sling/CablePull)", True,
        0.9,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Butterfly (Sling/Dumbbell/CablePull)", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Positive Push-Up", True,
        0.5,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.chest.value[0],0.6)]
    ),
    ("Negative Push-Up", True,
        0.5,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.chest.value[0],0.6)]
    ),
    ("Sling, Push-Up w/ Reach-out", True,
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Sling, Superman Push-Up", True,
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Push-Up (Sling/Bodyweight)", False,
        0.5,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],0.9)]
    ),
    ("Sling Push-Up (Grip-Variation: over/under, parallel-inner/outer)", True,
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],0.9)]
    ),
    ("Push-Up (Feet in Sling)", True,
        0.4,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Push-Up w/ Roll-out", True,
        0.55,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Power-Push", True,
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Reverse Archer / Push into Cross", True,
        0.6,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    ("Fall-Out", True,
        0.4,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.chest.value[0],1)]
    ),
    #########################
    ###  Back            ####
    #########################
    ("Row", True,
        0.7,#Lowered, because I often times use Row as Intensity-Finisher after other exercises. So I don't include it that often as primary exercise.
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1.0)]
    ),
    ("Inverted Row", True,
        0.7,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1.0)]
    ),
    ("Single-Arm-Row", True,
        0.6,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1)]
    ),
    ("Sling, Single-Arm-Row w/ Rotation", True,
        0.85,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.back.value[0],1)]
    ),
    ("Long-Arm Pull-down", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1)]
    ),
    ("Pull-Up", True,
        1.2,
        [equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.back.value[0],1)]
    ),
    ("Rev-Grip Pull-Up", True,
        1.2,
        [equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.back.value[0],1)]
    ),
    ("Human Pull-Over", True,
        0.65,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.back.value[0],0.6)]
    ),
    ("Sling, Archer-Row / Row into Cross", True,
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.back.value[0],0.8),(muscleIdentifier.trapez.value[0],0.3)]
    ),
    ("Power-Pull", True,
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.back.value[0],1)]
    ),
    #Latziehen
    ("Cable Pull-Down", True,
        1.0,
        [equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.back.value[0],1)]
    ),
    #########################
    ###  Rotator-Cuff    ####
    #########################
    ("Facepull", True,
        1.5,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],1),(muscleIdentifier.delt_rear.value[0],0.1)]
    ),
    ("External-Rotation", True,
        1.0,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],1),(muscleIdentifier.trapez.value[0],0.1)]
    ),
    ("Scarecrow -> Y-Pull", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],1)]
    ),
    ("W-Pull", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],0.8)]
    ),
    #########################
    ###  Delt-Front      ####
    #########################
    ("Urlacher", True,
        1.0,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)]
    ),
    ("Scoop-Press", True,
        1.1,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.chest.value[0],0.05),(muscleIdentifier.delt_front.value[0],1),(muscleIdentifier.serratus_ant.value[0],0.6)]
    ),
    ("Handstand Push-Up", True,
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)]
    ),
    ("Reach-out Y-Pull", True,
        0.7,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)]
    ),
    # Carefull when doing this. Do it right or you risk impingement
    ("High-Pull", True,
        0.7,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.delt_front.value[0],1)]
    ),
    ("Dumbbell Clean & Press", True,
        0.9,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.delt_front.value[0],1),(muscleIdentifier.lower_back.value[0],0.15)]
    ),
    #########################
    ###  Delt-Rear       ####
    #########################
    ("Rear-Delt Row (prior with Dumbbell)", True,
        1.0,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)]
    ),
    ("Rotating Reverse-Butterfly", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)]
    ),
    ("Back Widow", True,
        0.8,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1.0)]
    ),
    ("Pull-Back (similar to Facepull)", True,
        0.6,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)]
    ),
    ("Crab-Row (\"Rear-Delt Row\")", True,
        0.8,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)]
    ),
    ("Sling, Ext.-rotated Pull-to-Cross", True,
        0.5,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.delt_rear.value[0],1)]
    ),
    #########################
    ###  Delt-Side       ####
    #########################
    ("Reach-out Rev-Butterfly", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],0.1),(muscleIdentifier.delt_side.value[0],0.8),(muscleIdentifier.serratus_ant.value[0],0.6)]
    ),
    ("Uni-lateral Lateral-Raise", True,
        1.0,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_side.value[0],1)]
    ),
    ("Bi-lateral Lateral-Raise", True,
        0.85,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_side.value[0],1)]
    ),
    ("Reverse Butterfly", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.delt_side.value[0],0.75),(muscleIdentifier.trapez.value[0],0.4)]#,(muscleIdentifier.rotator_cuff.value[0],0.4)
    ),
    ("Delta-Fly", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.delt_side.value[0],1)]
    ),
    #########################
    ###  Quads-&-Glutes  ####
    #########################
    ("Romanian Split Squat", True,
        1.1,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Sling, Single-Leg Squat", True,
        1.2,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Sling, Single-Leg Pistol-Squat", True,
        0.9,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Single-Leg Box-Squat", True,
        1.1,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Single-Leg-Box-Squat -> 1 1/2 Squat -> Slight Jump Squat", True,
        0.7,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Alt. Heel-touch Squat -> Alt. Sprint-Start Lunge -> Plyo Sprinter Lunge", True,
        0.7,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Alt Crossover Step-Up -> Alt. Reverse Lunge -> Split Squat Jump", True,
        0.7,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Crab-Walk (Resist-Band)", True,
        0.8,
        [equipmentIdentifier.ResistanceBand.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Sling, Alpine-Row", True,
        0.5,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Lateral Lunge (Dumbbell/BW/Sling)", True,
        1.0,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Sling.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Lunge to High-Knee / Reverse Version", True,
        0.4,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    ("Weighted Squats", True,
        1.1,
        [equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],1)]
    ),
    #########################
    ###  Biceps          ####
    #########################
    # NOTE: One does not need ordinary "Dumbbell Curls" or "Hammer Curls". Just do the 3-Variation Curls
    ("3-Variation Curls (underhand inwards -> overhand inwards -> underhand outwards)", True,
        1.4,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.biceps.value[0],1)]
    ),
    ("Sling, w/ Shoulder-Raise", True,
        1.0,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1),(muscleIdentifier.delt_front.value[0],0.15)]
    ),
    ("Sling, Cross-Chest", True,
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1)]
    ),
    ("Sling, Chest-Tap", True,
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1)]
    ),
    ("Chin-Curl", True,
        0.8,
        [equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.back.value[0],0.51),(muscleIdentifier.biceps.value[0],0.8)]
    ),
    ("Bent-forward inwards Curl", True,
        1.0,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.biceps.value[0],1)]
    ),
    ("Sling, Hercules Curl", True,
        0.2,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.biceps.value[0],1)]
    ),
    #########################
    ###  Triceps         ####
    #########################
    ("Kick-Back / Back-Extension", True,
        0.75,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    ("3-Var Push-Up (inefficient Back-Extension -> Cobra Push-Up -> Diamond Push-Up)", True,
        1.3,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    ("Parallel-Grip Pull", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    ("Pull-Down (Undergrip)", True,
        0.75,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    ("Push-Down (Overgrip)", True,
        0.8,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.ResistanceBand.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    ("Backside Dips", False,
        0.45,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    ("Triceps Bench-Press", True,
        1.0,
        [equipmentIdentifier.MountBench.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    ("Bench Triceps-Stretch (Bench & SZ-Barbell)", True,
        1.0,
        [equipmentIdentifier.Barbell.value[0]],
        [(muscleIdentifier.triceps.value[0],1)]
    ),
    #########################
    ###  Hamstrings      ####
    #########################
    ("Hip-Thrust", True,
        1.5,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.Barbell.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.25),(muscleIdentifier.hamstrings.value[0],0.75)]# (muscleIdentifier.lower_back.value[0],0.55)
    ),
    ("Hamstring-Curls", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.hamstrings.value[0],1)]
    ),
    ("Long Leg March", True,
        0.8,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.1),(muscleIdentifier.hamstrings.value[0],0.75)]
    ),
    ("High Hip Bucks", True,
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.25),(muscleIdentifier.hamstrings.value[0],0.9),(muscleIdentifier.lower_back.value[0],0.2)]
    ),
    #########################
    ###  Abs             ####
    #########################
    ("BW Side Lateral Raise", True,
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.rotator_cuff.value[0],0.2),(muscleIdentifier.quads_n_glutes.value[0],0.2),(muscleIdentifier.abs.value[0],0.46),(muscleIdentifier.lower_back.value[0],0.1)]
    ),
    ("Hanging Leg-Raise (Legs straight or drawn)", True,
        0.65,#Because there are two slightly distinct exercises
        [equipmentIdentifier.PullUpBar.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Hanging Leg-Raise edgeways (Legs straight or drawn)", True,
        0.75,#Because there are two slightly distinct exercises
        [equipmentIdentifier.PullUpBar.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Floor, 3-Compund from (Cross-Ellbow-Knee, Hip-Up-Crunch, Diagonal-Ellbow-Thrust)", True,
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Floor, 3-Compund from (Candle, Levitation Sit-Up, Hand crossed past leg)", True,
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Rev Corkscrew -> Black Widow Knee Slide -> Levitation Crunch", True,
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Ab Halo -> V-Up Tuck -> Sit-Up Ellbow-Thrust", True,
        0.4,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Sit-Up -> Candle -> Crunch", True,
        0.3,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Sling, Crunch", True,
        0.8,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Sling sideways", True,
        1.0,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Sling Candle", True,
        0.7,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Core-Rotation -> Sit-Up", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    ("Corkscrew (Hanging/Feet-in-Sling)", True,
        0.6,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.PullUpBar.value[0]],
        [(muscleIdentifier.abs.value[0],1)]
    ),
    #########################
    ###  Calves          ####
    #########################
    ("Calf Press (Uni- or Bi-lateral)", True,
        1.0,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.calves.value[0],1)]
    ),
    ("Sprinting Calf Press (Uni- or Bi-lateral)", True,
        1.0,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.calves.value[0],1)]
    ),
    #########################
    ###  Trapez          ####
    #########################
    ("Dumbbell Full-Motion", True,
        1.0,
        [equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.trapez.value[0],1)]
    ),
    ("Pull-back, roll-downwards", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.trapez.value[0],1)]
    ),
    ("Uni-lateral Pull-back", True,
        1.0,
        [equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.trapez.value[0],1)]
    ),
    ("Neck Pull-Up, rotate down", True,
        0.6,
        [equipmentIdentifier.Dumbbell.value[0],equipmentIdentifier.Sling.value[0],equipmentIdentifier.CablePull.value[0]],
        [(muscleIdentifier.trapez.value[0],1)]
    ),
    #########################
    ###  Lower-Back      ####
    #########################
    ("Deadlift", True,
        1.4,
        [equipmentIdentifier.Barbell.value[0],equipmentIdentifier.Gym.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.46),(muscleIdentifier.lower_back.value[0],1)]
    ),
    ("Rev Hyper-Extension", True,
        1.0,
        [equipmentIdentifier.Bodyweight.value[0]],
        [(muscleIdentifier.lower_back.value[0],1)]
    ),
    ("Sling, Hanging L-Sit to Hip-Thrust", True,
        1.2,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.lower_back.value[0],1)]
    ),
    ("Sling Leg-March (side- or backwards)", True,
        0.9,
        [equipmentIdentifier.Sling.value[0]],
        [(muscleIdentifier.lower_back.value[0],1)]
    ),
    ("Angels & Devils", True,
        0.9,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.1),(muscleIdentifier.lower_back.value[0],1)]
    ),
    ("Raise Hand-&-Foot diagonal", True,
        0.3,
        [equipmentIdentifier.Bodyweight.value[0],equipmentIdentifier.Dumbbell.value[0]],
        [(muscleIdentifier.quads_n_glutes.value[0],0.1),(muscleIdentifier.lower_back.value[0],0.8),(muscleIdentifier.delt_side.value[0],0.5)]
    )
]





#Warmup-Exercises
# Delt-Front/Side: Prowler Push-Up, Bodyweight
#                  Frog Push-Up