import os
import argparse
from dotenv import load_dotenv
from google import genai
from prompts import system_prompt
from functions.call_functions import available_functions

def main():
    print("Hello from ai-agent!")
    
    #prompt collection
    parser = argparse.ArgumentParser(description="Heatherbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [genai.types.Content(role="user",parts=[genai.types.Part(text=args.user_prompt)])]

    #set ignition key
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key == None:
        raise RuntimeError("Missing API_KEY")

    client = genai.Client(api_key=api_key)

    #start engine
    generate_content = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=genai.types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]),
        )

    if generate_content.usage_metadata == None:
        raise RuntimeError("API is Non-Responsive")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {generate_content.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {generate_content.usage_metadata.candidates_token_count}")
        if len(generate_content.function_calls) == 0:
            print(generate_content.text)
        else:
            for c in generate_content.function_calls:
                print(f'    Calling function: {c.name}({c.args})')           
    else:
        if len(generate_content.function_calls) == 0:
            print(generate_content.text)
        else:
            for c in generate_content.function_calls:
                print(f'    Calling function: {c.name}({c.args})')

if __name__ == "__main__":
    main()
