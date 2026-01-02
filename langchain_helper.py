import ollama

import wikipedia

from langchain_ollama import OllamaLLM
from langchain_ollama.chat_models import ChatOllama

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import SystemMessagePromptTemplate, HumanMessagePromptTemplate, ChatPromptTemplate

from langchain.agents import create_agent
from langchain.tools import tool
from ollama import ChatResponse, chat

from openai import OpenAI

from datetime import date

from dotenv import load_dotenv

import time
import sys
import threading
from typing import Callable, Any

# Not used for now
#load_dotenv()


def typewriter_effect(text, delay=0.03):
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
        
    print()  # For a new line after the text is printed

def dynamic_braille_loader(process_func: Callable, loader_text: str = "Processing", *args, **kwargs) -> Any:
    """
    Run a process function while displaying a braille loader animation.
    
    Args:
        process_func: The function to run in the background
        *args, **kwargs: Arguments to pass to the process function
    
    Returns:
        The result of the process function
    """
    frames = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    result = None
    error = None
    process_running = True
    
    # This function will run our process in the background
    def run_process():
        nonlocal result, error, process_running
        try:
            result = process_func(*args, **kwargs)
        except Exception as e:
            error = e
        finally:
            process_running = False
    
    # Start the process in a separate thread
    process_thread = threading.Thread(target=run_process)
    process_thread.start()
    
    # Display the loader while the process is running
    frame_index = 0
    while process_running:
        sys.stdout.write(f'\r{frames[frame_index % 8]} {loader_text}...')
        sys.stdout.flush()
        time.sleep(0.08)
        frame_index += 1
    
    # Wait for the thread to complete
    process_thread.join()
    
    # Clear the loader
    sys.stdout.write('\r' + ' ' * 20 + '\r')
    sys.stdout.flush()
    
    # Raise any errors that occurred
    if error:
        raise error
    
    return result


def langchain_ollama_tool_agent():

    llm = ChatOllama(model="qwen3")

    @tool
    def current_date() -> str:
        """Get the current date."""
        return str(date.today())

    @tool
    def tool_wikipedia(query: str) -> str:
        """Search a query in wikipedia.
        Args:
            query: question from the user or llm agent
        """
        wikipedia.set_lang("en")
        # Search for articles
        search_results = wikipedia.summary(query)
        return search_results


    mytools = [current_date, tool_wikipedia]

    system_message_prompt = {"role": "system", "content": """You are a helpful assistant with a bunch of tools available. 
                    Elaborate your answers considering the information received from tools, do not
                    hypothesize or make up answers if you don't have enough information.
                    Finally, you must be aware of the current date.
                    """}

    messages = [
                #{
                #    "role": "user", 
                #    "content": "get the current date."
                #    },
                {
                    "role": "user",
                    "content": "Current date president of the United States?. Use the wikipedia tool to find out."
                    }
            ]
    inputs = {
        "messages": messages
    }

    agent = create_agent(model=llm, tools=mytools, system_prompt=system_message_prompt.get("content"))

    # After running your agent stream
    final_response = None
    for chunk in agent.stream(inputs, stream_mode="updates"):
        #for step, data in chunk.items():
        #    print(f"step: {step}")
        #    print(f"content: {data['messages'][-1].content_blocks}")
        #print(chunk)
        if 'model' in chunk:
            final_response = chunk['model']['messages'][0].content

    # Extract the final answer
    if final_response:
       return final_response.strip()
       


def langchain_ollama_chat():

    def current_date() -> str:
        """Get the current date."""
        return str(date.today())

    def tool_wikipedia(query: str) -> str:
        """Search a query in wikipedia.

        Args:
            query: question from the user or llm agent
        """
        wikipedia.set_lang("en")
        # Search for articles
        search_results = wikipedia.summary(query)
        return search_results
    
    available_tools = {
        'tool_wikipedia': tool_wikipedia,
        'current_date': current_date,
    }

    mytools = [tool_wikipedia, current_date]

    messages = [
                {
                    "role": "system", 
                    "content": "You are a helpful assistant with a bunch of tools available."
                    },
                {
                    "role": "user", 
                    "content": "get the current date."
                    },
                {
                    "role": "user",
                    "content": "Current date president of the United States?. Use the wikipedia tool to find out."
                    }
            ]
     
    #Call the Ollama API with the user message and the tools list
    result: ChatResponse = chat(
        model='qwen3', # Use a model known for tool support (e.g., llama3.1, qwen3, command-r)
        messages=messages,
        tools=mytools,
        #format="json",
        #think=True,  # Set the think level to 'medium' for better reasoning
        #stream=False
        )
    #print('Model response:', result)
    #print()

    if result.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in result.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_tools.get(tool.function.name):
                #print('Calling function:', tool.function.name)
                #print('Arguments:', tool.function.arguments)
                output = function_to_call(**tool.function.arguments)
                #print('Function output:', output)
                # Add the function response to messages for the model to use
                messages.append(result.message)
                messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})
            else:
                return "Function " + tool.function.name + " not found"

    # Only needed to chat with the model using the tool call results
    if result.message.tool_calls:
        # Add the function response to messages for the model to use
        #messages.append(result.message)
        #messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})
        # Get final response from model with function outputs
        final_response = chat('qwen3', messages=messages)
        return final_response.message.content.strip()

    else:
       return 'No tool calls returned from model'
        
    
def langchain_ollama_agent():
    model = OllamaLLM(
        model="qwen3",
        base_url="http://localhost:11434",
        stream=False
    )

    @tool("tool_wikipedia")
    def tool_wikipedia(query: str) -> str:
        """Search a query in wikipedia.

        Args:
            query: question from the user or llm agent
        """
        wikipedia.set_lang("en")
        # Search for articles
        search_results = wikipedia.summary(query, sentences=2, max_chars=500)
        return search_results

    mytools = [tool_wikipedia]

    myagent = create_agent(tools=mytools, model=model)

    result = myagent.invoke({"messages": [{"role": "user", "content": "Who is the president of the United States?"}]})

    print(result)

def generate_pet_names(animal_type, color):
    prompt_template = PromptTemplate(
        input_variables=["animal_type", "color"],
        template='I have a {color} {animal_type} pet, suggest me 10 names for my pet. Deliver all the the pet names in a json array under the key "names".',
        format="json"
    )
	
    model = OllamaLLM(
        model="qwen3",
        base_url="http://localhost:11434",
        stream=False,
        #output_key="names"
        reasoning=True,
        format="json"
    )
    
    output_parser = JsonOutputParser()

    #response = llm.generate(model="deepseek-r1", template='prompt_template', format="json")
    chain = prompt_template | model | output_parser

    response = chain.invoke({"color": color, "animal_type": animal_type})

    return response

if __name__ == "__main__":

    # Test LangChain with Ollama tool agent
    #print("\nLangChain Ollama and react agent Tool Results:")
    #langchain_ollama_tool_agent()

    final = dynamic_braille_loader(langchain_ollama_tool_agent, "Running LangChain Ollama Tool Agent")
    typewriter_effect("Final result: " + final.strip(), delay=0.02)

    # Test LangChain with Ollama direct chat
    #final = dynamic_braille_loader(langchain_ollama_chat, "Running LangChain Ollama Chat Tool Results")
    #typewriter_effect("Final result: " + final.strip(), delay=0.02)

    # Testing langchain chains with ollama generate llm (OllamaLLM)
    #final = dynamic_braille_loader(generate_pet_names, "Generating Pet Names", 'dog', 'brown')
    #typewriter_effect("Generated pet names: " + str(final), delay=0.02)
    
    #print(langchain_agent())
    #test_wikipedia()
