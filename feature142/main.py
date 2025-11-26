def main():
    rows = []
    f = open("input.txt", "r", encoding="utf-8")
    for line in f:
        line = line.rstrip("\n")
        if "n" in line or not line:
            continue
        cols = line.split("\t")
        count = len(cols)
        if count > 7:
            del cols[7]
        rows.append((count, cols))
    f.close()

    rows.sort(key=lambda x: x[0])

    for count, cols in rows:
        print(f"{count}:" + "\t".join(cols))


if __name__ == "__main__":
    main()
