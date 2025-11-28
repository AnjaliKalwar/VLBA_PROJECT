# Open input file
with open("input.txt", "r") as f:
    lines = f.readlines()

# Filtering lines that do NOT contain 'n'
filtered_lines = []
for line in lines:
    line = line.rstrip("\n")  # remove only newline
    if 'n' not in line:
        filtered_lines.append(line)

processed_lines = []
for line in filtered_lines:
    columns = line.split()
    word_count = len(columns)
    if len(columns) >= 8:
        columns.pop(7)  # removing 8th column
    processed_lines.append((word_count, columns))

# Sort by number of words (stable sort)
# print(processed_lines)
# print("-------")
processed_lines.sort(key=lambda x: x[1])
# print(processed_lines)

# Print in required format
for word_count, columns in processed_lines:
    # print(f"{word_count}:" + "\t".join(columns))
    print(f"{word_count}:" + "\t".join(columns) + "\t")

