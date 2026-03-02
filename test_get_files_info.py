from functions.get_files_info import get_files_info

def to_print(text, current="."):
    if current == ".":
        print(f"Result for current directory:")
    else:
        print(f"Result for '{current}' directory:")
    print(text)


test_1 = get_files_info("calculator", ".")
to_print(test_1,current=".")

test_2 = get_files_info("calculator", "pkg")
to_print(test_2, current="pkg")

test_3 = get_files_info("calculator","/bin")
to_print(test_3,current="/bin")

test_4 = get_files_info("calculator","../")
to_print(test_4,current="../")


