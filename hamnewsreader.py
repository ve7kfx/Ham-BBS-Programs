import subprocess
import sys

def display_disclaimer():
    print("Disclaimer: This program filters out copyrighted material. System operators are responsible for modifying the code as per their local laws and requirements.")

def display_program_info():
    print("\nProgram Information:")
    print("This program allows users to search news over ham radio.")
    print("You can search news by content or topic. The results will be fetched from the respective scripts: ")
    print("- 'newsreaderbycontentsham.py' for content-based searches")
    print("- 'newsreaderbytopicham.py' for topic-based searches")
    print("It also provides options for image conversion to ASCII or ANSI formats, with an option to exclude images.\n")

def main_menu():
    print("Welcome to the Ham Radio News Reader")
    print("1. Search News by Content")
    print("2. Search News by Topic")
    print("3. Program Information")
    print("4. Exit")
    choice = input("Enter your choice: ")
    return choice

def call_news_reader(script_name, search_query):
    result = subprocess.run(['python', script_name, search_query], capture_output=True, text=True)
    print(result.stdout)

def main():
    display_disclaimer()

    while True:
        user_choice = main_menu()

        if user_choice == "1":
            query = input("Enter search content: ")
            call_news_reader('newsreaderbycontentsham.py', query)

        elif user_choice == "2":
            query = input("Enter search topic: ")
            call_news_reader('newsreaderbytopicham.py', query)

        elif user_choice == "3":
            display_program_info()

        elif user_choice == "4":
            print("Exiting program.")
            sys.exit()

        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
