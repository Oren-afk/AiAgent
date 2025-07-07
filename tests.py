from functions.get_file_content import get_file_content

def main():
    print("-----First test")
    result1 = get_file_content("calculator", "main.py")
    print(result1)

    print("\n-----Second test")
    result2 = get_file_content("calculator", "pkg/calculator.py")
    print(result2)

    print("\n-----Third test")
    result3 = get_file_content("calculator", "/bin/cat")
    print(result3)

if __name__ == "__main__":
    main()