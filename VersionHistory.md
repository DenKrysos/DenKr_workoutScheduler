# DenKr_workoutScheduler -- Version-History


## beta-0.5.1
* One minor adjustment:
    * Increased the len of the "history_shortened" for exercises to account for better variety with big exercise selections



## beta-0.5.0

* Support for maintaining multiple Profiles
    * Stored per Profile:
        * Muscle-Config
        * Exercise-Config
    * Independent of Profiles (Global):
        * Basic-Cfg Values
* Adjusting GUI to Managing Profiles
* Improved Computation:
    * The Sub-Functionality "assure_rest" now works better with allowing muscles that are set to crazy high volumes in relation to Workouts-per-Week

### Commissioning Version

If you worked with one of the beta-0.4.x Versions, you have to delete your old Config-File "0history/1_2-config_setup.json". A new one, with the new format will be created.
You can carry over your values from before. Within a profile, the format is identical to the former single-profile-file.




## beta-0.4.1

* Just some minor enhancements for the GUI
* Memorizing and restoring of Window Geometry, if desired
* Some more help-button
* Some feature to ease my life as developer



## beta-0.4.0

* GUI
* Sophisticated means for configuration
* Schedules the muscles to train
* And furnishes with concrete exercises
* Allows finetuning via "Volume-Scaling" to reach the configured training amount vs. normalizing to weekly volume
* Configuration possible in three ways: Default in .py-Modules, Operating cfg in .json-Files, adjusting comfortable via GUI
* GUI newly introduced in this version
* First time also available as bundled .exe
