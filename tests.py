from functions.write_file import write_file

def main():
    print("-----First test")
    result1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(result1)

    print("\n-----Second test")
    result2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(result2)

    print("\n-----Third test")
    result3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(result3)

if __name__ == "__main__":
    main()