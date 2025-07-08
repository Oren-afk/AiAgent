from functions.run_python import run_python_file

def main():
    print("-----First test")
    result1 = run_python_file("calculator", "main.py")
    print(result1)

    print("\n-----Second test")
    result2 = run_python_file("calculator", "tests.py")
    print(result2)

    print("\n-----Third test")
    result3 = run_python_file("calculator", "../main.py")
    print(result3)

    print("\n-----Forth test")
    result4 = run_python_file("calculator", "nonexistent.py")
    print(result4)

if __name__ == "__main__":
    main()