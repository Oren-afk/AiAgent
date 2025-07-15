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
    for i in range(20):
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash-001",
                contents=messages,
                config=types.GenerateContentConfig(tools=[available_functions],
                                                system_instruction=system_prompt)
            )
            if response.candidates:
                for candidate in response.candidates:
                    messages.append(candidate.content)
            if verbose:
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
                print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
            has_function_calls = False
            if response.candidates:
                for candidate in response.candidates:
                    if candidate.content.parts:
                        for part in candidate.content.parts:
                            if hasattr(part, 'function_call') and part.function_call is not None:
                                has_function_calls = True
                                function_response = call_function(part.function_call, verbose)
                                messages.append(function_response)
                                if not function_response.parts[0].function_response.response:
                                    raise Exception("Something went wrong with the function call.")
                                if verbose:
                                    print(f"-> {function_response.parts[0].function_response.response}")

            if not has_function_calls:
                print(response.text)
                break
        except Exception as e:
            return f"Error: {e}"

if __name__ == "__main__":
    main()
