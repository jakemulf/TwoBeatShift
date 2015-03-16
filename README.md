#Problem to solve

This script determines the ideal transition between 2 songs while ignoring tempo.  This is useful for transitioning between 2 songs by shifting the tempo of 1 to match the other one.

#Inspiration

My previous report (BeatShift) discussed the inspiration for this overall project.  This script is a key solution to building the overall project which transitions between many songs by shifting tempo.

#twosongshift.py

Determines the ideal transition between 2 songs while ignoring tempo.

Usage: python twosongtransition.py first_filename second_filename ratio output_file

Dependencies: math, sys, pyechonest.track

###Process

twosongshift.py works using a similar algorithm that infinitejuke.com uses.  Each segment of a song is compared to each segment of the other song using a weighted Euclidean distance formula.  The "best transition" is the one with the smallest distance.

twosongshift.py only compares a given section of the 2 songs.  This is specified by the user with the ratio argument.  A ratio of .5 will only compare the middle 1/2 of a song.  Example: if a song has 100 segments, a ratio of .5 will only cause comparisons with segments 25 to 75.
