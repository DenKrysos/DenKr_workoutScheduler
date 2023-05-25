#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

'''
Created on 2020-11-18
Last modified: 2023-04-09

@author: Dennis Krummacker
'''


from settings.values import muscleID, equipID


#Here, you can safely change the numeric values per muscle.
# But! Leave the names alone, they are internally used by some functions
# - - - - - - - - -
#INSTRUCTIONS:
#Tuple-Values: (Muscle-Name, Muscle-Type, Workouts-per-Week, Sets-per-Week)
#- Muscle-Name: Name of the Muscle, just leave alone, is used internally
#- Muscle-Type: Big-or-Small-Muscle. 1: Big, 2: Small.
#- Workouts-per-Week: How often, in terms of workouts the muscle is approached per week.
#- Sets-per-Week: How many Sets in one week shall be exercised for this muscle.
# - - - - - 
# You should make sure that the sum of the Workouts-per-Week is not significantly higher than
#    "Muskles-you-want-per-Workout" * Total-Workouts-per-Week
# - - - - -
# This profile here works reasonably well for having 3.5 Workouts-per-Week with 4 Muscles per Workout.
#   (But actually, this is a little too low Volume. The Profile in "muscle.py" called "muscle_setup_default" would be more like the optimum volume. But this would require about 5-6 Muscles per Workout or 4-5 Workouts-per-Week, which would be most likely too much a dedication for most people.)
#   (So you might very well work with this profile here and still live on with a good and calm conscience.)
#   (Now you can consider using the "Volume Scaling" Option, which allows the computation to include an additional muscle every now and then.)
#   (I would assess that leaving the values like here works well with deactivated Volume-Scaling)
#   (Active Volume-Scaling might add a fifth muscle too often for many people. So, when using this option, you might want to lower Chest&Back to 1.55, Lower-back to 0.75, Quads&Glutes to 1.4)
# - - - - -
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
# - - - - -
# This forst profile serves for setting the initial values, when no .json-Config-Files are existent yet.
#   The ones below are always kept as additional immutable profiles
muscle_setup__preset=[
    (muscleID.chest,1,1.7,10),
    (muscleID.back,1,1.7,10),
    (muscleID.rotator_cuff,2,1.25,6),
    (muscleID.delt_front,2,0.75,5),
    (muscleID.delt_rear,2,1,5),
    (muscleID.delt_side,2,1,5),
    (muscleID.quads_n_glutes,1,1.5,10),
    (muscleID.biceps,2,1,5),
    (muscleID.triceps,2,1,5),
    (muscleID.hamstrings,2,0.9,5),
    (muscleID.abs,1,1.5,8),
    (muscleID.calves,2,0.9,6),
    (muscleID.trapez,2,1,5),
    (muscleID.lower_back,2,0.8,5)
]
# - - - - -
#Leave the Profiles below just alone. They essentially serves as a templates.
# -> If you want to change muscle's values, adjust the one above or create more custom profiles via the GUI
muscle_setup__default=[
    (muscleID.chest,1,1.7,10),
    (muscleID.back,1,1.7,10),
    (muscleID.rotator_cuff,2,1.25,6),
    (muscleID.delt_front,2,0.75,5),
    (muscleID.delt_rear,2,1,5),
    (muscleID.delt_side,2,1,5),
    (muscleID.quads_n_glutes,1,1.5,10),
    (muscleID.biceps,2,1,5),
    (muscleID.triceps,2,1,5),
    (muscleID.hamstrings,2,0.9,5),
    (muscleID.abs,1,1.5,8),
    (muscleID.calves,2,0.9,6),
    (muscleID.trapez,2,1,5),
    (muscleID.lower_back,2,0.8,5)
]
muscle_setup__appropriate=[
    (muscleID.chest,1,1.8,10),
    (muscleID.back,1,1.8,10),
    (muscleID.rotator_cuff,2,1.25,6),
    (muscleID.delt_front,2,0.75,5),
    (muscleID.delt_rear,2,1,5),
    (muscleID.delt_side,2,1,5),
    (muscleID.quads_n_glutes,1,1.5,10),
    (muscleID.biceps,2,1,5),
    (muscleID.triceps,2,1,5),
    (muscleID.hamstrings,2,0.9,5),
    (muscleID.abs,1,1.5,8),
    (muscleID.calves,2,0.9,6),
    (muscleID.trapez,2,1,5),
    (muscleID.lower_back,2,0.8,5)
]
muscle_setup__optimum=[
    (muscleID.chest,1,2,10),
    (muscleID.back,1,2,10),
    (muscleID.rotator_cuff,2,1.25,6),
    (muscleID.delt_front,2,0.75,5),
    (muscleID.delt_rear,2,1,5),
    (muscleID.delt_side,2,1,5),
    (muscleID.quads_n_glutes,1,2,10),
    (muscleID.biceps,2,1,5),
    (muscleID.triceps,2,1,5),
    (muscleID.hamstrings,2,1,5),
    (muscleID.abs,1,1.5,8),
    (muscleID.calves,2,1.25,6),
    (muscleID.trapez,2,1,5),
    (muscleID.lower_back,2,1,5)
]
#-----------------------------------------------------


#INSTRUCTIONS:
#Tuple-Values: (Exercise-Name, Precedence, Equipment-Requirement, muscleIntensity, EnableDisable)
#- Exercise-Name: Name of the Exercise.
#- Inherent: To state, that this exercise is built-in the Apps exercise database itself. E.g. changing its name shall not be done and deleting it is of no use.
#            Set to '1' for pre-shipped exercises. Ones added via the GUI during executions are initialized with '0'
#- Precedence: Assigns some kind of "weight/importance" to an exercise. Gives the possibility to have certain exercise occur more often (or less) over continious computations. Base-Value: 1. Don't let it deviate too much from 1. 2 is fine to roughly double its frequence, 0.5 to roughly halve it.
#- Equipment-Requirement: What is required to perform the exercise. Gym-Equipment, simple Dumbbells, only own Body. With setting the appropriate values in _1cfg/configuration.py, entire sets of exercises can be deactivated for computation. (When an exercise only has equipment capabilities that are set to False, it won't be proposed in your training plan.
#- muscleIntensity: To which intensity the exercise trains individual muscles. 0< & <=1. Can attack multiple muscles.
#- EnableDisable. Can be used to Enable or Disable single Exercises for your schedule computation. True: Exercise will be included. False: Exercise is excluded.
exercise_setup=[
    #########################
    ###  Chest           ####
    #########################
    ("Uni-lateral Butterfly", 1, True,
        1.0,
        [equipID.ResistanceBand,equipID.CablePull],
        [(muscleID.chest,1)]
    ),
    ("UCV-Raise -> Cavaliere-Crossover", 1, True,
        1.0,
        [equipID.ResistanceBand,equipID.Dumbbell,equipID.CablePull],
        [(muscleID.chest,0.9)]
    ),
    ("Bench-Press", 1, True,
        1.5,
        [equipID.Barbell,equipID.MountBench,equipID.Gym],
        [(muscleID.chest,1)]
    ),
    ("Dumbbell-Press", 1, True,
        1.0,
        [equipID.SimpleBench,equipID.Gym],
        [(muscleID.chest,1)]
    ),
    ("Low Rotation Push-Up (e.g. on Dumbbell)", 1, True,
        0.75,
        [equipID.Bodyweight,equipID.Dumbbell],
        [(muscleID.chest,1)]
    ),
    ("High Rotation Push-Up (e.g. on Dumbbell)", 1, True,
        0.75,
        [equipID.Bodyweight,equipID.Dumbbell],
        [(muscleID.chest,1)]
    ),
    ("Dips", 1, True,
        0.6,# Only seldom as primary exercise. Include it as Intensity-Finisher with other exercises
        [equipID.Sling,equipID.Gym],
        [(muscleID.chest,0.85),(muscleID.serratus_ant,0.7)]
    ),
    ("Reverse Dips / Raising Butterfly (Sling/CablePull)", 1, True,
        0.9,
        [equipID.Sling,equipID.CablePull],
        [(muscleID.chest,1)]
    ),
    ("Butterfly (Sling/Dumbbell/CablePull)", 1, True,
        1.0,
        [equipID.Sling,equipID.Dumbbell,equipID.CablePull],
        [(muscleID.chest,1)]
    ),
    ("Positive Push-Up", 1, True,
        0.5,
        [equipID.Bodyweight],
        [(muscleID.chest,0.6)]
    ),
    ("Negative Push-Up", 1, True,
        0.5,
        [equipID.Bodyweight],
        [(muscleID.chest,0.6)]
    ),
    ("Sling, Push-Up w/ Reach-out", 1, True,
        0.7,
        [equipID.Sling],
        [(muscleID.chest,1)]
    ),
    ("Sling, Superman Push-Up", 1, True,
        0.7,
        [equipID.Sling],
        [(muscleID.chest,1)]
    ),
    ("Push-Up (Sling/Bodyweight)", 1, False,
        0.5,
        [equipID.Bodyweight,equipID.Sling],
        [(muscleID.chest,0.9)]
    ),
    ("Sling Push-Up (Grip-Variation: over/under, parallel-inner/outer)", 1, True,
        0.7,
        [equipID.Sling],
        [(muscleID.chest,0.9)]
    ),
    ("Push-Up (Feet in Sling)", 1, True,
        0.4,
        [equipID.Sling],
        [(muscleID.chest,1)]
    ),
    ("Push-Up w/ Roll-out", 1, True,
        0.55,
        [equipID.Sling],
        [(muscleID.chest,1)]
    ),
    ("Power-Push (Sling)", 1, True,
        0.8,
        [equipID.Sling],
        [(muscleID.chest,1)]
    ),
    ("Reverse Archer / Push into Cross", 1, True,
        0.6,
        [equipID.Sling],
        [(muscleID.chest,1)]
    ),
    ("Fall-Out", 1, True,
        0.4,
        [equipID.Sling],
        [(muscleID.chest,1)]
    ),
    #########################
    ###  Back            ####
    #########################
    ("Row", 1, True,
        0.7,#Lowered, because I often times use Row as Intensity-Finisher after other exercises. So I don't include it that often as primary exercise.
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.back,1.0)]
    ),
    ("Inverted Row", 1, True,
        0.7,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.back,1.0)]
    ),
    ("Single-Arm-Row", 1, True,
        0.6,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.back,1)]
    ),
    ("Sling, Single-Arm-Row w/ Rotation", 1, True,
        0.85,
        [equipID.Sling],
        [(muscleID.back,1)]
    ),
    ("Long-Arm Pull-down", 1, True,
        1.0,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.back,1)]
    ),
    ("Pull-Up", 1, True,
        1.2,
        [equipID.PullUpBar],
        [(muscleID.back,1)]
    ),
    ("Rev-Grip Pull-Up", 1, True,
        1.2,
        [equipID.PullUpBar],
        [(muscleID.back,1)]
    ),
    ("Human Pull-Over", 1, True,
        0.65,
        [equipID.Bodyweight],
        [(muscleID.back,0.6)]
    ),
    ("Sling, Archer-Row / Row into Cross", 1, True,
        0.8,
        [equipID.Sling],
        [(muscleID.back,0.8),(muscleID.trapez,0.3)]
    ),
    ("Power-Pull (Sling)", 1, True,
        0.8,
        [equipID.Sling],
        [(muscleID.back,1)]
    ),
    #Latziehen
    ("Cable Pull-Down", 1, True,
        1.0,
        [equipID.Gym],
        [(muscleID.back,1)]
    ),
    #########################
    ###  Rotator-Cuff    ####
    #########################
    ("Facepull", 1, True,
        1.5,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.rotator_cuff,1),(muscleID.delt_rear,0.1)]
    ),
    ("External-Rotation", 1, True,
        1.0,
        [equipID.Dumbbell,equipID.Sling,equipID.CablePull,equipID.Gym],
        [(muscleID.rotator_cuff,1),(muscleID.trapez,0.1)]
    ),
    ("Scarecrow -> Y-Pull", 1, True,
        1.0,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.rotator_cuff,1)]
    ),
    ("W-Pull", 1, True,
        1.0,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.rotator_cuff,0.8)]
    ),
    #########################
    ###  Delt-Front      ####
    #########################
    ("Urlacher", 1, True,
        1.0,
        [equipID.Dumbbell],
        [(muscleID.delt_front,1)]
    ),
    ("Scoop-Press", 1, True,
        1.1,
        [equipID.Dumbbell],
        [(muscleID.chest,0.05),(muscleID.delt_front,1),(muscleID.serratus_ant,0.6)]
    ),
    ("Handstand Push-Up", 1, True,
        1.0,
        [equipID.Bodyweight],
        [(muscleID.delt_front,1)]
    ),
    ("Reach-out Y-Pull", 1, True,
        0.7,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.delt_front,1)]
    ),
    # Carefull when doing this. Do it right or you risk impingement
    ("High-Pull", 1, True,
        0.7,
        [equipID.Dumbbell],
        [(muscleID.delt_front,1)]
    ),
    ("Dumbbell Clean & Press", 1, True,
        0.9,
        [equipID.Dumbbell],
        [(muscleID.delt_front,1),(muscleID.lower_back,0.15)]
    ),
    #########################
    ###  Delt-Rear       ####
    #########################
    ("Rear-Delt Row (prior with Dumbbell)", 1, True,
        1.0,
        [equipID.Dumbbell,equipID.ResistanceBand,equipID.CablePull],
        [(muscleID.delt_rear,1)]
    ),
    ("Rotating Reverse-Butterfly", 1, True,
        1.0,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.delt_rear,1)]
    ),
    ("Back Widow", 1, True,
        0.8,
        [equipID.Bodyweight],
        [(muscleID.delt_rear,1.0)]
    ),
    ("Pull-Back (similar to Facepull)", 1, True,
        0.6,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull,equipID.Gym],
        [(muscleID.delt_rear,1)]
    ),
    ("Crab-Row (\"Rear-Delt Row\") (Sling)", 1, True,
        0.8,
        [equipID.Sling,equipID.Gym],
        [(muscleID.delt_rear,1)]
    ),
    ("Dumbbell Crab-Row", 1, False,
        0.5,
        [equipID.Dumbbell,equipID.Gym],
        [(muscleID.delt_rear,1)]
    ),
    ("Sling, Ext.-rotated Pull-to-Cross", 1, True,
        0.5,
        [equipID.Sling],
        [(muscleID.delt_rear,1)]
    ),
    #########################
    ###  Delt-Side       ####
    #########################
    ("Reach-out Rev-Butterfly", 1, True,
        1.0,
        [equipID.Sling,equipID.CablePull,equipID.Gym],
        [(muscleID.rotator_cuff,0.1),(muscleID.delt_side,0.8),(muscleID.serratus_ant,0.6)]
    ),
    ("Uni-lateral Lateral-Raise", 1, True,
        1.0,
        [equipID.Dumbbell,equipID.CablePull],
        [(muscleID.delt_side,1)]
    ),
    ("Bi-lateral Lateral-Raise", 1, True,
        0.85,
        [equipID.Dumbbell,equipID.CablePull],
        [(muscleID.delt_side,1)]
    ),
    ("Reverse Butterfly", 1, True,
        1.0,
        [equipID.Sling,equipID.CablePull,equipID.Gym],
        [(muscleID.delt_side,0.75),(muscleID.trapez,0.4)]#,(muscleID.rotator_cuff,0.4)
    ),
    ("Delta-Fly", 1, True,
        1.0,
        [equipID.Sling,equipID.CablePull],
        [(muscleID.delt_side,1)]
    ),
    #########################
    ###  Quads-&-Glutes  ####
    #########################
    ("Romanian Split Squat", 1, True,
        1.1,
        [equipID.Bodyweight],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Sling, Single-Leg Squat", 1, True,
        1.2,
        [equipID.Sling],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Sling, Single-Leg Pistol-Squat", 1, True,
        0.9,
        [equipID.Sling],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Single-Leg Box-Squat", 1, True,
        1.1,
        [equipID.Bodyweight],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Single-Leg-Box-Squat -> 1 1/2 Squat -> Slight Jump Squat", 1, True,
        0.7,
        [equipID.Bodyweight],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Alt. Heel-touch Squat -> Alt. Sprint-Start Lunge -> Plyo Sprinter Lunge", 1, True,
        0.7,
        [equipID.Bodyweight],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Alt Crossover Step-Up -> Alt. Reverse Lunge -> Split Squat Jump", 1, True,
        0.7,
        [equipID.Bodyweight],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Crab-Walk (Resist-Band)", 1, True,
        0.8,
        [equipID.ResistanceBand],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Sling, Alpine-Row", 1, True,
        0.5,
        [equipID.Sling],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Lateral Lunge (Dumbbell/BW/Sling)", 1, True,
        1.0,
        [equipID.Bodyweight,equipID.Sling,equipID.Dumbbell],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Lunge to High-Knee / Reverse Version", 1, True,
        0.4,
        [equipID.Bodyweight,equipID.Sling],
        [(muscleID.quads_n_glutes,1)]
    ),
    ("Weighted Squats", 1, True,
        1.1,
        [equipID.Gym],
        [(muscleID.quads_n_glutes,1)]
    ),
    #########################
    ###  Biceps          ####
    #########################
    # NOTE: One does not need ordinary "Dumbbell Curls" or "Hammer Curls". Just do the 3-Variation Curls
    ("3-Variation Curls (underhand inwards -> overhand inwards -> underhand outwards)", 1, True,
        1.4,
        [equipID.Dumbbell],
        [(muscleID.biceps,1)]
    ),
    ("Sling, w/ Shoulder-Raise", 1, True,
        1.0,
        [equipID.Sling],
        [(muscleID.biceps,1),(muscleID.delt_front,0.15)]
    ),
    ("Sling, Cross-Chest", 1, True,
        0.7,
        [equipID.Sling],
        [(muscleID.biceps,1)]
    ),
    ("Sling, Chest-Tap", 1, True,
        0.7,
        [equipID.Sling],
        [(muscleID.biceps,1)]
    ),
    ("Chin-Curl", 1, True,
        0.8,
        [equipID.PullUpBar],
        [(muscleID.back,0.51),(muscleID.biceps,0.8)]
    ),
    ("Bent-forward inwards Curl", 1, True,
        1.0,
        [equipID.Dumbbell],
        [(muscleID.biceps,1)]
    ),
    ("Sling, Hercules Curl", 1, True,
        0.2,
        [equipID.Sling],
        [(muscleID.biceps,1)]
    ),
    #########################
    ###  Triceps         ####
    #########################
    ("Kick-Back / Back-Extension", 1, True,
        0.75,
        [equipID.Dumbbell,equipID.ResistanceBand,equipID.CablePull],
        [(muscleID.triceps,1)]
    ),
    ("3-Var Push-Up (inefficient Back-Extension -> Cobra Push-Up -> Diamond Push-Up)", 1, True,
        1.3,
        [equipID.Bodyweight],
        [(muscleID.triceps,1)]
    ),
    ("Parallel-Grip Pull", 1, True,
        1.0,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull],
        [(muscleID.triceps,1)]
    ),
    ("Pull-Down (Undergrip)", 1, True,
        0.75,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull],
        [(muscleID.triceps,1)]
    ),
    ("Push-Down (Overgrip)", 1, True,
        0.8,
        [equipID.Sling,equipID.ResistanceBand,equipID.CablePull],
        [(muscleID.triceps,1)]
    ),
    ("Backside Dips", 1, False,
        0.45,
        [equipID.Bodyweight],
        [(muscleID.triceps,1)]
    ),
    ("Triceps Bench-Press", 1, True,
        1.0,
        [equipID.MountBench],
        [(muscleID.triceps,1)]
    ),
    ("Bench Triceps-Stretch (Bench & SZ-Barbell)", 1, True,
        1.0,
        [equipID.Barbell],
        [(muscleID.triceps,1)]
    ),
    #########################
    ###  Hamstrings      ####
    #########################
    ("Hip-Thrust", 1, True,
        1.5,
        [equipID.Bodyweight,equipID.Dumbbell,equipID.Barbell,equipID.Gym],
        [(muscleID.quads_n_glutes,0.25),(muscleID.hamstrings,0.75)]# (muscleID.lower_back,0.55)
    ),
    ("Hamstring-Curls", 1, True,
        1.0,
        [equipID.Sling,equipID.Gym],
        [(muscleID.hamstrings,1)]
    ),
    ("Long Leg March", 1, True,
        0.8,
        [equipID.Bodyweight],
        [(muscleID.quads_n_glutes,0.1),(muscleID.hamstrings,0.75)]
    ),
    ("High Hip Bucks", 1, True,
        1.0,
        [equipID.Bodyweight],
        [(muscleID.quads_n_glutes,0.25),(muscleID.hamstrings,0.9),(muscleID.lower_back,0.2)]
    ),
    #########################
    ###  Abs             ####
    #########################
    ("BW Side Lateral Raise", 1, True,
        1.0,
        [equipID.Bodyweight],
        [(muscleID.rotator_cuff,0.2),(muscleID.quads_n_glutes,0.2),(muscleID.abs,0.46),(muscleID.lower_back,0.1)]
    ),
    ("Hanging Leg-Raise (Legs straight or drawn)", 1, True,
        0.65,#Because there are two slightly distinct exercises
        [equipID.PullUpBar,equipID.Gym],
        [(muscleID.abs,1)]
    ),
    ("Hanging Leg-Raise edgeways (Legs straight or drawn)", 1, True,
        0.75,#Because there are two slightly distinct exercises
        [equipID.PullUpBar,equipID.Gym],
        [(muscleID.abs,1)]
    ),
    ("Floor, 3-Compund from (Cross-Ellbow-Knee, Hip-Up-Crunch, Diagonal-Ellbow-Thrust)", 1, True,
        0.4,
        [equipID.Bodyweight],
        [(muscleID.abs,1)]
    ),
    ("Floor, 3-Compund from (Candle, Levitation Sit-Up, Hand crossed past leg)", 1, True,
        0.4,
        [equipID.Bodyweight],
        [(muscleID.abs,1)]
    ),
    ("Rev Corkscrew -> Black Widow Knee Slide -> Levitation Crunch", 1, True,
        0.4,
        [equipID.Bodyweight],
        [(muscleID.abs,1)]
    ),
    ("Ab Halo -> V-Up Tuck -> Sit-Up Ellbow-Thrust", 1, True,
        0.4,
        [equipID.Bodyweight],
        [(muscleID.abs,1)]
    ),
    ("Sit-Up -> Candle -> Crunch", 1, True,
        0.3,
        [equipID.Bodyweight],
        [(muscleID.abs,1)]
    ),
    ("Sling, Crunch", 1, True,
        0.8,
        [equipID.Sling],
        [(muscleID.abs,1)]
    ),
    ("Sling sideways", 1, True,
        1.0,
        [equipID.Sling],
        [(muscleID.abs,1)]
    ),
    ("Sling Candle", 1, True,
        0.7,
        [equipID.Sling],
        [(muscleID.abs,1)]
    ),
    ("Core-Rotation -> Sit-Up", 1, True,
        1.0,
        [equipID.Sling,equipID.CablePull],
        [(muscleID.abs,1)]
    ),
    ("Corkscrew (Hanging/Feet-in-Sling)", 1, True,
        0.6,
        [equipID.Sling,equipID.PullUpBar],
        [(muscleID.abs,1)]
    ),
    #########################
    ###  Calves          ####
    #########################
    ("Calf Press (Uni- or Bi-lateral)", 1, True,
        1.0,
        [equipID.Bodyweight,equipID.Gym],
        [(muscleID.calves,1)]
    ),
    ("Sling, Sprinting Calf Press (Uni- or Bi-lateral)", 1, True,
        1.0,
        [equipID.Sling],
        [(muscleID.calves,1)]
    ),
    #########################
    ###  Trapez          ####
    #########################
    ("Dumbbell Full-Motion", 1, True,
        1.0,
        [equipID.Dumbbell],
        [(muscleID.trapez,1)]
    ),
    ("Pull-back, roll-downwards", 1, True,
        1.0,
        [equipID.Sling,equipID.CablePull],
        [(muscleID.trapez,1)]
    ),
    ("Uni-lateral Pull-back", 1, True,
        1.0,
        [equipID.Sling,equipID.CablePull],
        [(muscleID.trapez,1)]
    ),
    ("Neck Pull-Up, rotate down", 1, True,
        0.6,
        [equipID.Dumbbell,equipID.Sling,equipID.CablePull],
        [(muscleID.trapez,1)]
    ),
    #########################
    ###  Lower-Back      ####
    #########################
    ("Deadlift", 1, True,
        1.4,
        [equipID.Barbell,equipID.Gym],
        [(muscleID.quads_n_glutes,0.46),(muscleID.lower_back,1)]
    ),
    ("Rev Hyper-Extension", 1, True,
        1.0,
        [equipID.Bodyweight],
        [(muscleID.lower_back,1)]
    ),
    ("Sling, Hanging L-Sit to Hip-Thrust", 1, True,
        1.2,
        [equipID.Sling],
        [(muscleID.lower_back,1)]
    ),
    ("Sling Leg-March (side- or backwards)", 1, True,
        0.9,
        [equipID.Sling],
        [(muscleID.lower_back,1)]
    ),
    ("Angels & Devils", 1, True,
        0.9,
        [equipID.Bodyweight,equipID.Dumbbell],
        [(muscleID.quads_n_glutes,0.1),(muscleID.lower_back,1)]
    ),
    ("Raise Hand-&-Foot diagonal", 1, True,
        0.3,
        [equipID.Bodyweight,equipID.Dumbbell],
        [(muscleID.quads_n_glutes,0.1),(muscleID.lower_back,0.8),(muscleID.delt_side,0.5)]
    )
]





#Warmup-Exercises
# Delt-Front/Side: Prowler Push-Up, Bodyweight
#                  Frog Push-Up