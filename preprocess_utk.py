import argparse
import os, sys
import cv2

RACES = 5
GENDERS = 2
UTK_CROP_SIZE = 200

def remove(img_path, cause):
    print(cause, img_path, "removed!")
    os.remove(img_path)

def validate(img_name, img_path):
    # validate file name
    img_name_split = img_name.split("_")
    if len(img_name_split) != 4: 
        remove(img_path, "Bad file name:")
        return False

    # validate size
    img = cv2.imread(img_path)
    img_shape = img.shape
    if img_shape[0] != UTK_CROP_SIZE or img_shape[1] != UTK_CROP_SIZE:
        remove(img_path, "Bad crop size:")
        return False 

    return True

def main(args):
    print("Preprocessing:", args.utk_raw_dir)

    # initialize statistics
    dataset_size = 0
    if args.print_stats:
        race_count = [0 for i in range(RACES)]
        gender_count = [0 for i in range(GENDERS)]

    for img_name in os.listdir(args.utk_raw_dir):
        img_path = os.path.join(args.utk_raw_dir, img_name) 

        if validate(img_name, img_path):
            # store image in its own identity directory
            new_dir = img_name.split(".")[0].strip()
            img_new_path = os.path.join(args.utk_raw_dir, new_dir)
            if not os.path.exists(img_new_path):
                os.makedirs(img_new_path)
            new_img_name = "{0}.jpg".format(new_dir)
            os.rename(img_path, os.path.join(img_new_path, new_img_name))

            # update stats
            dataset_size = dataset_size + 1
            if args.print_stats:
                img_name_split = img_name.split("_")
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

# Sample execution: python preprocess_utk.py ../utk_preprocessed/raw/ --print_stats
# python preprocess_utk.py ../datasets/utk_preprocessed/raw/ --print_stats
if __name__ == '__main__':
    main(parse_arguments(sys.argv[1:]))
