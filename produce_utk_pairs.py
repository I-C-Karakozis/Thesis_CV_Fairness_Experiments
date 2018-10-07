import argparse
import os, sys
import random

RACES = 5
GENDERS = 2

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
    indices = [i for i in range(len(subdirectories))]

    # form pairs of test set
    with open(args.pairs, "w") as file:
        for i, sub in enumerate(subdirectories):
            if i % 1000 == 0: print("{0} samples generated so far.".format(i))
           
            # sample random negative example       
            j = random.choice(indices[:i] + indices[(i+1):])
            negative_sample = "{0}\t1\t{1}\t1\n".format(sub, subdirectories[j])
            file.write(negative_sample)
            negative_pairs = negative_pairs + 1

            # update class statistics
            if args.print_stats:
                sub_split = sub.split("_")
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
    return parser.parse_args(argv)

# Sample execution: python produce_utk_pairs.py ../utk_preprocessed/raw/ pairs.txt
if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
