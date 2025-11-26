# Open and read the input file
with open("input.txt", "r") as f:
    data = f.readlines()

# Remove lines containing 'n'
filtered_data = [line.strip() for line in data if 'n' not in line]

processed_data = []
for line in filtered_data:
    columns = line.split('\t')
    if len(columns) >= 8:
        columns.pop(7) 
    word_count = len(columns)
    processed_data.append((word_count, '\t'.join(columns)))

# Step 3: Sort lines by word count (ascending)
processed_data.sort(key=lambda x: x[0])

for word_count, line in processed_data:
    print(f"{word_count}:{line}")
