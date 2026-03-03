from functions.get_file_content import get_file_content
from config import MAXCHARS

def to_print(text):
    print("")
    print("====TEST======")
    print(text)

try:
    test_1 = get_file_content("calculator", "lorem.txt")
    print(f'    File as {len(test_1)} chars\n   {test_1[MAXCHARS:]}')
    try:
        test_2 = get_file_content("calculator", "main.py")
        to_print(test_2)

        test_3 = get_file_content("calculator","pkg/calculator.py")
        to_print(test_3)

        test_4 = get_file_content("calculator","/bin/cat")
        to_print(test_4)

        test_5 = get_file_content("calculator","pkg/does_not_exist.py")
        to_print(test_5)
    except Exception as e:
        print(f'    Error: {e}')
except Exception as e:
    print(f' Error: first test {e}')