from functions.write_file import write_file

def to_print(text):
    print("")
    print("====TEST======")
    print(text)

try:
    test_1 = write_file("calculator","lorem.txt", "wait, this isn't lorem ipsum")
    to_print(test_1)
    try:
        test_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
        to_print(test_2)

        test_3 = write_file("calculator","/tmp/temp.txt", "this should not be allowed")
        to_print(test_3)
    except Exception as e:
        print(f'    Error: {e}')
except Exception as e:
    print(f' Error: first test. {e}')