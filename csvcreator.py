# importing the csv module
import csv
import os


def csv_creator(data_list, output_folder, output_name):

    if not os.path.exists(output_folder) and not output_folder == None:
        os.makedirs(output_folder)
        print(f"Directory '{output_folder}' created.")

    # else:
    #     print(f"Directory '{output_folder}' already exists.")

    csv_file = f"{output_folder}/{output_name}"

    # Get the keys from the first dictionary to use as headers
    headers = data_list[0].keys()

    # Write data to CSV file
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=headers)
        writer.writeheader()
        writer.writerows(data_list)

    print(f"CSV file '{csv_file}' created successfully.")
