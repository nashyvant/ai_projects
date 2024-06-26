import pandas as pd

# Define the input text files and output Excel file
input_files = ['output1.txt', 'output2.txt', 'output3.txt', 'output4.txt', 'output5.txt' ]
output_file = 'output.xlsx'

# Initialize an empty list to store the parsed data
all_data = []

# Loop through each input file and parse the data
for input_file in input_files:
    data = []
    with open(input_file, 'r') as file:
        for line in file:
            # Remove whitespace and newline characters
            line = line.strip()
            # Split the line into key-value pairs
            pairs = line.split(', ')
            # Create a dictionary for the current line
            record = {pair.split(': ')[0]: pair.split(': ')[1] for pair in pairs}
            # Append the dictionary to the data list
            data.append(record)
    
    # Extend the all_data list with the data from the current file
    all_data.extend(data)

# Create a DataFrame from the combined data
df = pd.DataFrame(all_data)

# Write the DataFrame to an Excel file
df.to_excel(output_file, index=False, engine='openpyxl')

print(f"Data from all files has been successfully written to {output_file}")
