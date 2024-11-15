# DenKr_workoutScheduler


- Instructions are printed by the Tool itself on Start-up.

It calculates a progressing schedule for your resistance-training workout, i.e. tells you in which order you may train your muscle-groups.

In the defined class "workout" you may define your demands. That is, how many workouts you intend to do per week and how often per week individual muscles shall be attacked. The default should provide a solid setup for most people up to advanced. However, if you are very advanced you may need to adjust the volume and for sure your total workouts per week.

The tool stores the calculated schedule as a history in text-files (.json) and loads them during a run, to maintain a consistant suitable flow. After startup you are first told (again) the last loaded workouts, then the new ones are presented on the terminal. If using the GUI, these two parts arise simultaneously (directly after start-up) but in different areas.

Before writing the history (i.e. appending the newly computed workouts), you are prompted a query on the console - or (clickable) at the bottom of the GUI in bright yellow - whether the persistent history files shall be updated or not. You can use this to just lookup the last preceding computation without creating a new one and unintentionally messing with the history files.


## GUI vs. Terminal

The Tool comes equipped with a GUI to operate it. But it is also capable to work fully on Terminal.

If you want to do so, look into the configuration Files and change the Value "UsageMethodology" to Terminal instead of GUI (which is the default setting).

Values:

```
"UsageMethodology": "useMeth.GUI"
"UsageMethodology": "useMeth.Terminal"
```


## Configuration

The tool can be configured to compute a workout schedule tailored to specific demands (e.g. adjusted to number of workouts per week, or which exercises are included).

In the case of working with the source files, i.e. running the Python script manually: For this, consolidate the files in the directories "./_1cfg/" & "./0history/".

The .py-Files (in ./_1cfg/) serve as Default-Values (and can of course only be changed when working with the source-Scripts, not when using the .exe). But after first start, .json-Files (in ./0history/) are created (initialized with the values from the .py-Files). Afterwards you can work with the .json-Files (both when working with Script or bundled-exe).

But anyways, since by now the Tool has a GUI that allows to change the configuration, you might just want to use that method :).

Some Instruction on that is printed by the tool itself at the start of a run.


##  Non-deterministic computation aka Random Component

Don't be puzzled, because the tool can create (partly) different results on consecutive runs without updating the history.
Where *Math* dictates it, results are produced indeed deterministic. Muscles or Exercises that are more urgent to train are favored; in other words, the longer one did not make it into a workout, the more likely it is picked for an upcoming.
But cases can occur, where the score for certain muscles or exercises is equal. Then, among these a random component is introduced.



## Cmd-Line Arguments

Pass these as Command-Line Arguments to let it perform special functions

### History Trimming Functionality

> *Upfront-Notice*: There's actually no necessity to call this explicity. The tool checks the size of history-logs and in case they become too long, automatically trims the files after creating a backup of the prior.

Trims the History-Files down to the number of entries that are required for the Script to compute the schedule, that is, to derive the weight from the historical previous workouts, which decides about the upcoming order.
(Respectively keeps the existing entries, i.e. changes nothing, in case the history files do not contain more than these.)

```
history trim
```