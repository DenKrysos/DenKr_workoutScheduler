# DenKr_workoutScheduler


It calculates a progressing schedule for your resistance-training workout, i.e. tells you in which order you may train your muscle-groups.

In the defined class "workout" you may define your demands. That is, how many workouts you intend to do per week and how often per week individual muscles shall be attacked. The default should provide a solid setup for most people up to advanced. However, if you are very advanced you may need to adjust the volume and for sure your total workouts per week.

The tool stores the calculated schedule as a history in text-files and loads them during a run, to maintain a consistant suitable flow. After startup you are first told (again) the last loaded workouts, then the new ones are presented on the terminal.

Before writing the history (i.e. appending the newly computed workouts), you are prompted a query on the console whether the persistent history files shall be updated or not. You can use this to just lookup the last preceding computation without creating a new one and unintentionally messing with the history files.