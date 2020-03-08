# pr-burn
Weightlifting training aid for predicting maximal lifts and planning workouts around RPEs & RIRs. Uses the following max prediction formulas / methods:
  * Lombardi
  * Brzycki
  * Epley
  * Mayhew
  * O'Conner
  * Wathan
  * Lander
  * Average

Included modules:
* intensity_table_gen.py - Generates intensity tables using a PR weight and a selected maximum prediction method
* rm_est.py - Predicts N rep max (NRM) given a PR set (weight x reps) where N is the number of reps to be completed

Planned usage: integrate into web application for easy NRM prediction and working planning.

Example usage:
See "rm_via_intensity_sample.xlsx" for example usage in Excel.
