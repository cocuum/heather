from argparse import ArgumentParser
from dotenv import load_dotenv
from functions.call_functions import available_functions,call_function
from google.genai import Client,types
from prompts import system_prompt
from os import environ


def heather():

    #prompt collection
    parser = ArgumentParser(description="Heatherbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user",parts=[types.Part(text=args.user_prompt)])]

    #set ignition key
    load_dotenv()
    api_key = environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Missing API_KEY")

    client = Client(api_key=api_key)

    #start engine
    generate_content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]),
        )

    if generate_content.usage_metadata == None:
        raise RuntimeError("API is Non-Responsive")

    #check for verbose flag
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {generate_content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {generate_content.usage_metadata.candidates_token_count}")
    
    if len(generate_content.function_calls) == 0:
        print(generate_content.text)
    else:
        function_calls_response = []
        for c in generate_content.function_calls:
            call_result = call_function(c, verbose=args.verbose)
            if len(call_result.parts) == 0:
                raise Exception("No functions were called")
            called_func_name = call_result.parts[0].function_response
            if called_func_name == None:
                raise Exception("No response has been provided")
            response = called_func_name.response
            if response == None:
                raise Exception("No response was produced")
            function_calls_response.append(response)
            if args.verbose:
                print(f'    -> {response}')