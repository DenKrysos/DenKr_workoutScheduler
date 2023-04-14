# DenKr_workoutScheduler


It calculates a progressing schedule for your resistance-training workout, i.e. tells you in which order you may train your muscle-groups.

In the defined class "workout" you may define your demands. That is, how many workouts you intend to do per week and how often per week individual muscles shall be attacked. The default should provide a solid setup for most people up to advanced. However, if you are very advanced you may need to adjust the volume and for sure your total workouts per week.

The tool stores the calculated schedule as a history in text-files and loads them during a run, to maintain a consistant suitable flow. After startup you are first told (again) the last loaded workouts, then the new ones are presented on the terminal.

Before writing the history (i.e. appending the newly computed workouts), you are prompted a query on the console whether the persistent history files shall be updated or not. You can use this to just lookup the last preceding computation without creating a new one and unintentionally messing with the history files.


## Configuration

The tool can be configured to compute a workout schedule tailored to specific demands (e.g. adjusted to number of workouts per week, or which exercises are included).

For that, consolidate the files in the directory "./_1cfg/".

Some Instruction on that is printed by the tools itself at the start of a run.


##  Non-deterministic computation aka Random Component

Don't be puzzled, because the tool can create (partly) different results on consecutive runs without updating the history.
Where math dictates it, results are produced indeed deterministic. Muscles or Exercises that are more urgent to train are favored; in other words, the longer one did not make it into a workout, the more likely it is picked for an upcoming.
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