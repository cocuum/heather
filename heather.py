from functions.call_functions import available_functions,call_function
from google.genai import Client,types
from prompts import system_prompt

def heather(client,messages,verbose):
    #start engine
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[available_functions]
        ),
    )
    #check for API response
    if response.usage_metadata == None:
        raise RuntimeError("Gemini API is Non-Responsive")
    
    #check for verbose flag to print tokens count
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    
    if not response.function_calls:
        print("Response:")
        print(response.text)
        return response
            
    function_responses = []
    for c in response.function_calls:
        call_result = call_function(c, verbose)

        if not call_result.parts:
            raise Exception("No functions were called")
        
        if not call_result.parts[0].function_response:
            raise Exception("No response has been provided")
        
        if not call_result.parts[0].function_response.response:
            raise Exception("No response was produced")
        
        if verbose:
            print(f'    -> {call_result.parts[0].function_response.response}')
    
        function_responses.append(call_result.parts[0])
    
    #inclusion of function response in the message history for next iteration
    messages.append(types.Content(role="user",parts=function_responses))
    
    return response
        