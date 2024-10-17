import os
import glob

def merge_wx_data(data_dir, output_file):
    """Merges all .txt files in the data directory into a single output file."""

    with open(output_file, 'w') as outfile:
        for filename in glob.glob(os.path.join(data_dir, "*.txt")):
            with open(filename, 'r') as infile:
                outfile.write(infile.read())

if __name__ == "__main__":
    data_directory = r"C:\Users\mohit\code-challenge-template\data\wx_data"  # Replace with your actual data directory
    merged_output_file = "merged_wx_data.txt"  # Name of the output file
    merge_wx_data(data_directory, merged_output_file)
    print(f"Merged data written to: {merged_output_file}")