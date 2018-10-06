import argparse
import os, sys

RACES = 5
GENDERS = 2

def main(args):
    print("Preprocessing:", args.utk_raw_dir)

    # initialize statistics
    dataset_size = 0
    if args.print_stats:
        race_count = [0 for i in range(RACES)]
        gender_count = [0 for i in range(GENDERS)]

    for img_name in os.listdir(args.utk_raw_dir):
        img_path = os.path.join(args.utk_raw_dir, img_name)

        # validate file name
        img_name_split = img_name.split("_")
        if len(img_name_split) != 4: 
            print(img_path, "removed!")
            os.remove(img_path)
            continue

        # store image in its own identity directory
        img_new_path = os.path.join(args.utk_raw_dir, img_name.split(".")[0])
        if not os.path.exists(img_new_path):
            os.makedirs(img_new_path)
        os.rename(img_path, os.path.join(img_new_path, img_name))

        # update stats
        dataset_size = dataset_size + 1
        if args.print_stats:
            gender_count[int(img_name_split[1])] = gender_count[int(img_name_split[1])] + 1
            race_count[int(img_name_split[2])] = race_count[int(img_name_split[2])] + 1

    # output dataset statistics
    print("Total:", dataset_size)
    if args.print_stats:
        print("----------------- Dataset Statistics -----------------")
        print("Gender Distribution:", gender_count, "Total:", sum(gender_count))
        print("Race   Distribution:", race_count, "Total:", sum(race_count))
        print("------------------------------------------------------")

def parse_arguments(argv):
    parser = argparse.ArgumentParser()

    parser.add_argument('utk_raw_dir', type=str,
        help='Path to the data directory containing UTK face patches.')
    parser.add_argument('--print_stats',
        help='Prints dataset statistics.', action='store_true')
    return parser.parse_args(argv)

if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))