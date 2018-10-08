import argparse
import os, sys
import random

RACES = 5
GENDERS = 2

def get_breakpoints(arr, values):
    breakpoints = []
    for value in range(values):
        breakpoints.append(arr.index(value))
    breakpoints.append(len(arr))
    return breakpoints

def main(args):
    print("Generating testing pairs from:", args.utk_dir)

    # setup counters for test set metrics
    positive_pairs = 0
    negative_pairs = 0
    if args.print_stats:
        race_count = [0 for i in range(RACES)]
        gender_count = [0 for i in range(GENDERS)]

    # fetch subdirectories
    subdirectories = [child[0].split("/")[-1] for child in os.walk(args.utk_dir)][1:]
    age_restrictions = range(args.min_age, args.max_age)
    subdirectories = [sub for sub in subdirectories if int(sub.split("_")[0]) in age_restrictions]

    # group examples according to input
    if args.group_by_gender:
        print("Generating pairs of the same gender!")
        subdirectories = [(sub, int(sub.split("_")[1])) for sub in subdirectories]
        subdirectories = sorted(subdirectories, key=lambda x: x[1])
        breakpoints = get_breakpoints([sub[1] for sub in subdirectories], GENDERS)
    elif args.group_by_race:
        print("Generating pairs of the same race!")
        subdirectories = [(sub, int(sub.split("_")[2])) for sub in subdirectories]
        subdirectories = sorted(subdirectories, key=lambda x: x[1])
        breakpoints = get_breakpoints([sub[1] for sub in subdirectories], RACES)    
    else:
        subdirectories = [(sub, 0) for sub in subdirectories]
        breakpoints = get_breakpoints([sub[1] for sub in subdirectories], 1)
    indices = [i for i in range(len(subdirectories))]

    # form image pairs for test set
    current_class = -1
    with open(args.pairs, "w") as file:
        for i, sub in enumerate(subdirectories):
            # log progress
            if i % 1000 == 0: print("{0} samples generated so far.".format(i))
            if current_class != sub[1]: 
                current_class = sub[1]
                print("Generating examples for class {0}".format(current_class))

            # sample random negative example 
            start = breakpoints[sub[1]]
            end = breakpoints[sub[1]+1]      
            j = random.choice(indices[start:i] + indices[(i+1):end])

            # ensure samples are properly generated
            assert sub[1] == subdirectories[j][1]

            # record negative example
            negative_sample = "{0}\t1\t{1}\t1\n".format(sub[0], subdirectories[j][0])
            file.write(negative_sample)
            negative_pairs = negative_pairs + 1

            # update class statistics
            if args.print_stats:
                sub_split = sub[0].split("_")
                gender_count[int(sub_split[1])] = gender_count[int(sub_split[1])] + 1
                race_count[int(sub_split[2])] = race_count[int(sub_split[2])] + 1

    # output test set class statistics
    if args.print_stats:
        print("-------------- Dataset Class Statistics --------------")
        print("Gender Distribution:", gender_count, "Total:", sum(gender_count))
        print("Race   Distribution:", race_count, "Total:", sum(race_count))   

    # Output test set statistics
    print("------------------------------------------------------")
    print("Positive:", positive_pairs)
    print("Negative:", negative_pairs)
    print("Total:", positive_pairs + negative_pairs)

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('utk_dir', type=str,
        help='Path to the data directory containing UTK identities.')
    parser.add_argument('pairs', type=str,
        help='File to write pairs for test set.')
    parser.add_argument('--print_stats',
        help='Prints dataset statistics.', action='store_true')
    parser.add_argument('--group_by_gender',
        help='Generate samples within the same gender group.', action='store_true')
    parser.add_argument('--group_by_race',
        help='Generate samples within the same gender group.', action='store_true')
    parser.add_argument('--min_age', type=int,
        help='Minimum age for image to be used in sample generation.', default=20)
    parser.add_argument('--max_age', type=int,
        help='Maximum age for image to be used in sample generation.', default=50)
    return parser.parse_args(argv)

# Sample execution: python produce_utk_pairs.py ../utk_preprocessed/raw/ utk_pairs.txt
# python produce_utk_pairs.py ../datasets/utk_preprocessed/raw/ ../facenet/data/utk_pairs.txt
if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
