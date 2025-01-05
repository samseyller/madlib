import re

regex_match = r'\[(.+?)\]'

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        return content
    except FileNotFoundError:
        return f"The file at {file_path} was not found."
    except Exception as e:
        return f"An error occurred: {e}"

def extract_prompts(input_string):
    # Use regex to find all words inside square brackets
    prompts = re.findall(regex_match, input_string)
    return prompts

def answer_prompts(prompts):
    answers = []
    # Loop through prompts, prompting the user to answer each one
    for prompt in prompts:
        answer = input(f"Please provide a(n) {prompt}: ")
        answers.append(answer)
    return answers

def replace_prompts_with_answers(input_string, answers):
    # Use regex to find all words inside square brackets
    prompts = re.findall(regex_match, input_string)
    
    # Replace each prompt in the input string with the corresponding answer
    for i, prompt in enumerate(prompts):
        input_string = re.sub(r'\[' + re.escape(prompt) + r'\]', answers[i], input_string, 1)
    
    return input_string

if __name__ == '__main__':

    input_string = read_file("1.txt")

    prompts = extract_prompts(input_string)
    answers = answer_prompts(prompts)
    print(replace_prompts_with_answers(input_string, answers))