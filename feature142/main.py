# Open and read the input file
with open("input.txt", "r") as f:
    data = f.readlines()

# Step 1: Remove lines containing 'n'
filtered_data = []
for line in data:
    if 'n' not in line:
        filtered_data.append(line.strip())

# Step 2: Process each line: remove column 8 if exists
processed_data = []
for line in filtered_data:
    columns = line.split('\t')
    if len(columns) >= 8:
        columns.pop(7)  # remove 8th column
    word_count = len(columns)
    # store as tuple (word_count, line)
    processed_data.append((word_count, '\t'.join(columns)))

# Step 3: Sort by number of words
processed_data.sort(key=lambda x: x[0])

# Step 4: Print in the required format
for word_count, line in processed_data:
    print(f"{word_count}:{line}")
