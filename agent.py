import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_ollama import ChatOllama 
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from config import MODEL_NAME
from data_tools import load_dataset  
from prompts import create_prompt 


llm = ChatOllama(model=MODEL_NAME)

def interpret_and_execute(instruction: str, df):
    """
    Uses deepseek-r1 via the Ollama interface to generate Python code 
    for a given natural language instruction and execute it.
    """
    prompt = create_prompt(instruction, list(df.columns))
    response = llm.invoke(prompt)
    code = response.content.strip()
    
    try:
        if 'CODE:' in code:
            code = code.split('CODE:')[-1].split('\n')[0].strip() 
        #We are removing any markdown formatting or special characters
        code = code.replace('```python', '').replace('```', '').strip()
        code = code.replace('*', '').replace('`', '').strip()
        
        print("\n--- Generated Code ---")
        print(code)
        print("----------------------\n")
        
        exec_globals = {"df": df, "np": np, "pd": pd, "sns": sns, "plt": plt}
        
        try:
            if any(x in code.lower() for x in ['df.head', 'df.describe', 'df.info', 'df.tail']):
                result = eval(code, exec_globals)
                print("\n--- Output ---")
                print(result)
                print("-------------\n")
                
            # Plotting operations
            elif 'plt' in code or 'sns' in code:
                try:
                    exec(code + '\nplt.show()', exec_globals)
                    plt.close()  # Clean up plot
                except Exception as plot_error:
                    return f"Error in plotting: {plot_error}", code
                    
            # Statistical operations
            elif any(x in code.lower() for x in ['mean', 'sum', 'count', 'std', 'corr']):
                result = eval(code, exec_globals)
                print("\n--- Output ---")
                print(result)
                print("-------------\n")
                
            # Other operations
            else:
                result = eval(code, exec_globals)
                print("\n--- Output ---")
                print(result)
                print("-------------\n")
                
            return "Operation executed successfully.", code
            
        except NameError as e:
            return f"Error: Variable or function not found - {e}", code
        except SyntaxError as e:
            return f"Error: Invalid syntax in code - {e}", code
        except ValueError as e:
            return f"Error: Invalid value or operation - {e}", code
        except AttributeError as e:
            return f"Error: Invalid attribute or method - {e}", code
        except Exception as e:
            return f"Error executing code: {e}", code
    except Exception as e:
        return f"Error executing code: {e}", code

def create_agent(df):
    """
    Create and return a LangChain agent that uses two tools:
    - Load Data: Loads a CSV file into a DataFrame.
    - Interpret and Execute Command: Uses deepseek-r1 via Ollama to generate and execute code.
    """
    tools = [
        Tool(
            name="Interpret and Execute Command",
            func=lambda x: interpret_and_execute(x, df),
            description="Executes data analysis tasks on the loaded DataFrame."
        )
    ]
    
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True
    )
    return agent
