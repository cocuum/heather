from functions.run_python_file import run_python_file

def to_print(text):
    print("")
    print("=====TEST=====")
    print(text)

test_1 = run_python_file("calculator","main.py")
to_print(test_1)

test_2 = run_python_file("calculator","main.py",["3 + 5"])
to_print(test_2)

test_3 = run_python_file("calculator","tests.py")
to_print(test_3)

test_4 = run_python_file("calculator","../main.py")
to_print(test_4)

test_5 = run_python_file("calculator","nonexistent.py")
to_print(test_5)

test_6 = run_python_file("calculator","lorem.txt")
to_print(test_6)
