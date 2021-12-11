# Python code to rename multiple
# files in a directory or folder

# importing os module
import os

# Function to rename multiple files
def main():

    folder = "/home/charlie/Documents/Uni/Exeter - Data Science/MTHM601_Fundamentals_of_Applied_Data_Science/assignment_Project/data/rawData"
    for count, filename in enumerate(os.listdir(folder)):
        if('-M.csv' in filename):
            dst = f"{filename[:4]}_waterQuality.csv"
            src = f"{folder}/{filename}"
            dst = f"{folder}/{dst}"

            # rename() function will
            # rename all the files
            os.rename(src, dst)


if __name__ == '__main__':

    main()
