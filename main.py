from argparse import ArgumentParser
from dotenv import load_dotenv
from os import environ
from google.genai import Client,types

from heather import heather

def main():
    print("Hello from Heather!")

    #prompt collection
    parser = ArgumentParser(description="Heatherbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    #set ignition key
    load_dotenv()
    api_key = environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("Missing GEMINI_API_KEY")
    
    client = Client(api_key=api_key)

    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

    
    #check for verbose flag
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
    
    heather(client,messages,args.verbose)
    
if __name__ == "__main__":
    main()

    '''for _ in range(20):
        heather()
        if _ == 19:
            print("Heatherbot has completed 20 iterations. Ending program.")
            exit(1)
'''