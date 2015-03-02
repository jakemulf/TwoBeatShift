"""
TODO: make use of the transition limit.  currently only does with a limit of 1
""" 

"""
twosongtransition.py

Takes 2 songs and determines the ideal transitions between them if tempo is ignored.

Created by Jacob Mulford on 3/01/2015

Based on infinitejuke.com
"""
import math
import sys
import pyechonest.track as track

usage = """
Usage: python twosongtransition.py <first_filename> <second_filename> <transition_limit> <ratio> <output_file>

Example: python twosongtransition.py CallMeMaybe.mp3 ShakeItOff.mp3 10 .33 Transitions.txt

This will determine the transitions between the segments .33 of each side from the middle of CallMeMaybe.mp3 and ShakeItOff.mp3, and will put the
10 best transitions into Transitions.txt.  Transitions.txt will hold 2 integers on each line.
The first integer will be the segment in CallMeMaybe.mp3, and the second integer will be the
segment in ShakeItOff.mp3.
"""
def main(first_filename, second_filename, transition_limit, ratio, output_file):
    #set up the 2 files for analysis
    track_one = track.track_from_filename(first_filename)
    track_one.get_analysis()

    track_two = track.track_from_filename(second_filename)
    track_two.get_analysis()

    if (transition_limit > len(track_one.segments) * len(track_two.segments) * ratio * 2):
        print "Error: transition limit is greater than number of transitions"
        sys.exit(-1)

    if (ratio > 1.0 or ratio < 0.0):
        print "Error: ratio must be between 0.0 and 1.0"
        sys.exit(-1)

    first_middle = len(track_one.segments)/2
    second_middle = len(track_two.segments)/2

    first_start = int(first_middle - (first_middle * ratio))
    first_end = int(first_middle + (first_middle * ratio))

    second_start = int(second_middle - (second_middle * ratio))
    second_end = int(second_middle + (second_middle * ratio))

    #compare each segment in the first file to each segment in the second file
    comparisons = []
    for i in range(first_start,first_end):
        appender = []
        for j in range(second_start,second_end):
            compare = compare_segments(track_one.segments[i],track_two.segments[j])
            appender.append(compare)
        comparisons.append(appender)

    (first_low,second_low) = (0,0)

    for i in range(0,len(comparisons)):
        for j in range(0,len(comparisons[i])):
            if comparisons[i][j] < comparisons[first_low][second_low]:
                first_low = i
                second_low = j

    print first_low+first_start
    print second_low+second_start
    print comparisons[first_low][second_low]

#determines the weighted Euclidean distance between 2 segments
def compare_segments(seg_one, seg_two):
    timbre_distance = euc_dist(seg_one['timbre'],seg_two['timbre'])
    pitch_distance = euc_dist(seg_one['pitches'],seg_two['pitches'])
    loud_distance = (seg_one['loudness_start'] - seg_two['loudness_start'])**2
    return timbre_distance + 10*pitch_distance + loud_distance

#calculates euclidean distance
def euc_dist(arr_one,arr_two):
    sum = 0
    for i in range(0,min(len(arr_one),len(arr_two))):
        sum = sum + (arr_one[i] - arr_two[i])**2
    return math.sqrt(sum)

#returns the index of the worst transition in the array
def max_distance(array, comparisons):
    worst_first = 0
    worst_second = 0
    index = 0

    for i in range(0,len(array)):
        (first,second) = array[i]
        if comparisons[first][second] > comparisons[worst_first][worst_second]:
            worst_first = first
            worst_second = second
            index = i
    return (worst_first, worst_second, index)

#prints the 2 parameters to the given file on the same line separated by a comma
def print_to_file(param_one, param_two, file_name):
    f = open(file_name, "w")
    f.write(str(param_one) + "," + str(param_two))
    f.close()

if __name__ == '__main__':
    import sys
    try:
        first_filename = sys.argv[1]
        second_filename = sys.argv[2]
        transition_limit = int(sys.argv[3])
        ratio = float(sys.argv[4])
        output_file = sys.argv[5]
    except:
        print usage
        sys.exit(-1)
    main(first_filename, second_filename, transition_limit, ratio, output_file)
