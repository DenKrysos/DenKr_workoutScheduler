# DenKr_workoutScheduler -- Version-History


## beta-0.5.2
* Algorithm Enhancement:
    * It was possible that through an unlucky roll of compound-exercises that a Muscle of a Superset was removed due to insufficient rest before a workout, causing its counterpart to be schedule as incomplete Superset
    * Improved the Algorithm to make this process smoother. Supersets should no longer be ripped apart.
* Improved User-Experience:
    * The Output of a computed Schedule is now more orderly.
    * Superset-Muscles are always grouped together
    * Supersets always lead the Output-Group of a workout (Non-Superset-Muscles come afterward)
       * That does not really mean anything. I.e. it does recommend that you start a workout with Superset-Muscles. It is just, I guess, visually more appealing as it now follows a re-ocurring pattern?



## beta-0.5.1
* Three minor adjustments:
    * Increased the len of the "history_shortened" for exercises to account for better variety with big exercise selections
	* Slight Change in naming of some exercises
	* Changed the day-of-the-week abbreviation to English (as opposed to German)



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
