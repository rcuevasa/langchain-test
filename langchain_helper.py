import ollama
import wikipedia

from langchain_ollama import OllamaLLM

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from langchain.agents import create_agent
from langchain.tools import tool
from ollama import ChatResponse, chat

from openai import OpenAI

from datetime import date

from dotenv import load_dotenv


load_dotenv()

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

    #mytools = [{'tool_wikipedia': tool_wikipedia}]
    
    available_tools = {
        'tool_wikipedia': tool_wikipedia,
        'current_date': current_date,
    }

    mytools = [tool_wikipedia, current_date]
    
    #[
    #    {
    #        "type": "function",
    ##        "function": {
    ##            "name": "tool_wikipedia",
    #            "description": "Search a query in wikipedia.",
    #            "parameters": {
    #                "type": "object",
    #                "properties": {
    ###                       "type": "string",
    #                        "description": "question from the user or llm agent",
    #                        },
    #                },
    #                "required": ["query"],
    #            },
    #        },
    #    }
    #]

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
    print('Model response:', result)
    print()

    if result.message.tool_calls:
        # There may be multiple tool calls in the response
        for tool in result.message.tool_calls:
            # Ensure the function is available, and then call it
            if function_to_call := available_tools.get(tool.function.name):
                print('Calling function:', tool.function.name)
                print('Arguments:', tool.function.arguments)
                output = function_to_call(**tool.function.arguments)
                print('Function output:', output)
                # Add the function response to messages for the model to use
                messages.append(result.message)
                messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})
            else:
                print('Function', tool.function.name, 'not found')

    # Only needed to chat with the model using the tool call results
    if result.message.tool_calls:
        # Add the function response to messages for the model to use
        #messages.append(result.message)
        #messages.append({'role': 'tool', 'content': str(output), 'tool_name': tool.function.name})
        # Get final response from model with function outputs
        final_response = chat('qwen3', messages=messages)
        print('\nFinal response:', final_response.message.content)

    else:
        print('No tool calls returned from model')
        
    
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

    print("LangChain Chain Results:")
    print(generate_pet_names('cat', 'black'))

    print("\nLangChain Ollama Chat Tool Results:")
    print(langchain_ollama_chat())
    #print(langchain_agent())
    #test_wikipedia()
