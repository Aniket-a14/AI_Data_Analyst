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

def interpret_and_execute(instruction: str, df: pd.DataFrame) -> tuple[str, str]:
    """
    Uses deepseek-r1 via the Ollama interface to generate Python code 
    for a given natural language instruction and execute it.
    
    Args:
        instruction: Natural language instruction for data analysis
        df: Pandas DataFrame to analyze
        
    Returns:
        tuple: (execution_result, generated_code)
    """
    prompt = create_prompt(instruction, list(df.columns))
    response = llm.invoke(prompt)
    code = response.content.strip()
    
    try:
        code_lines = []
        in_code_block = False
        
        for line in code.split('\n'):
            line = line.strip()
            
            if not line or line.startswith(('<think>', 'To ', 'Here', 'This ', 'Alternatively', 'Wait', 'Putting')):
                continue
                
            if '```' in line:
                if line.startswith('```'):
                    in_code_block = not in_code_block
                continue
                
            if in_code_block or any(code_indicator in line for code_indicator in [
                'df.', 'print(', 'plt.', 'sns.', 'np.', 'pd.'
            ]):
                code_lines.append(line)
        
        code = '\n'.join(code_lines).strip()
        
        if not code:
            for line in response.content.split('\n'):
                if any(indicator in line for indicator in ['df.', 'print(', 'plt.']):
                    code = line.strip()
                    break
        
        for col in df.columns:
            if col.lower() in code.lower():
                code = code.replace(col.lower(), col)
        
        # Remove invalid characters
        code = code.replace('—', '-')  # Replace em dash with a regular dash
        code = code.replace('‘', "'").replace('’', "'")  
        
        print("\n--- Generated Code ---")
        print(code)
        print("----------------------\n")
        
        exec_globals = {
            "df": df, 
            "np": np, 
            "pd": pd, 
            "sns": sns, 
            "plt": plt,
            "__builtins__": {
                k: __builtins__[k] for k in __builtins__ 
                if k not in ['eval', 'exec', 'open']
            }
        }
        
        if 'plt' in code or 'sns' in code:
            # Handle plotting operations
            try:
                exec(code, exec_globals)
                plt.show()
                plt.close()
                return "Plot generated successfully.", code
            except Exception as e:
                plt.close()  # Clean up any partial plots
                return f"Error in plotting: {str(e)}", code
                
        elif any(op in code.lower() for op in ['df.head', 'df.tail', 'df.describe', 'df.info', 'df.iloc']):
            # Handle DataFrame display operations
            try:
                result = eval(code, exec_globals)
                return str(result), code
            except Exception as e:
                return f"Error in DataFrame operation: {str(e)}", code
                
        elif any(op in code.lower() for op in ['mean', 'sum', 'count', 'std', 'corr']):
            # Handle statistical operations
            try:
                result = eval(code, exec_globals)
                return str(result), code
            except Exception as e:
                return f"Error in statistical operation: {str(e)}", code
                
        else:
            # Other operations
            try:
                exec(code, exec_globals)
                return "Operation executed successfully.", code
            except Exception as exec_error:
                try:
                    result = eval(code, exec_globals)
                    return str(result), code
                except Exception as eval_error:
                    return f"Error executing code: {str(eval_error)}", code
                    
    except Exception as e:
        return f"Error processing code: {str(e)}", code

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

#This code is for the agent to execute the code and return the result
#It is a zero shot agent that uses the deepseek-r1 model to generate the code
#It then executes the code and returns the result
#It uses the langchain library to create the agent
#It uses the langchain.tools library to create the tools
#It uses the langchain.agents library to create the agent
