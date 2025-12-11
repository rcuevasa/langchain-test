import wikipedia

from langchain_ollama import OllamaLLM

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from langchain.agents import create_agent
from langchain.tools import tool


from dotenv import load_dotenv


load_dotenv()
    

def langchain_agent():
    model = OllamaLLM(
        model="deepseek-r1",
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
        model="deepseek-r1",
        base_url="http://localhost:11434",
        stream=False,
        #output_key="names"
        #reasoning=True,
        format="json"
    )
    
    output_parser = JsonOutputParser()

    #response = llm.generate(model="deepseek-r1", template='prompt_template', format="json")
    chain = prompt_template | model | output_parser

    response = chain.invoke({"color": color, "animal_type": animal_type})

    return response

if __name__ == "__main__":

    print(generate_pet_names('cat', 'black'))
    #print(langchain_agent())
    #test_wikipedia()
