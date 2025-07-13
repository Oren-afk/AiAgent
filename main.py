import os
import sys
import argparse
from schemas import available_functions
from system_prompt import system_prompt
from functions.call_function import call_function
from dotenv import load_dotenv
from google import genai
from google.genai import types

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("prompt", help="The user prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    user_prompt = args.prompt
    verbose = args.verbose
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(tools=[available_functions],
                                           system_instruction=system_prompt)
    )
    if verbose:
        print(f"User prompt: {user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    if response.function_calls:
        for call in response.function_calls:
            function_response = call_function(call, verbose)
            if not function_response.parts[0].function_response.response:
                raise Exception("Something went wrong with the function call.")
            if verbose:
                print(f"-> {function_response.parts[0].function_response.response}")
    else:
        print(response.text)

if __name__ == "__main__":
    main()
