import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_ollama import ChatOllama 
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from config import MODEL_NAME
from prompts import create_prompt 

llm = ChatOllama(model=MODEL_NAME)

def interpret_and_execute(instruction: str, df: pd.DataFrame) -> tuple[str, str]:
    """Uses deepseek-r1 with our examples to generate code"""
    prompt = create_prompt(instruction, list(df.columns))
    response = llm.invoke(prompt)
    code = response.content.strip()
    return process_code(code, df, instruction)

def process_code(code: str, df: pd.DataFrame, instruction: str = "") -> tuple[str, str]:
    """Process and execute the generated code"""
    try:
        code_lines = []
        in_code_block = False
        seen_lines = set()
        
        if instruction and instruction.lower().strip() in ['show full dataset', 'show all data', 'display full dataset']:
            code_lines = [
                "pd.set_option('display.max_rows', None)",
                "print(df)"
            ]
        else:
            for line in code.split('\n'):
                line = line.strip()
                
                
                if (not line or 
                    line in seen_lines or
                    line.startswith('import ') or
                    '`' in line or
                    line.startswith('#')):
                    continue
                    
                if '```' in line:
                    if line.startswith('```'):
                        in_code_block = not in_code_block
                    continue
                
                
                if in_code_block or any(code_indicator in line for code_indicator in [
                    'df.', 'print(', 'plt.', 'sns.', 'np.', 'pd.', '[', '=', '(', '+'
                ]):
                    code_lines.append(line)
                    seen_lines.add(line)
        
        code = '\n'.join(code_lines).strip()
        
        if not code:
            return "No valid code generated.", ""
            
       
        for col in df.columns:
            if col.lower() in code.lower():
                code = code.replace(col.lower(), col)
        
        code = code.replace('—', '-')  
        code = code.replace(''', "'").replace(''', "'")  
        
        return process_and_execute(code, df)
        
    except Exception as e:
        return f"Error processing code: {str(e)}", code

def process_and_execute(code: str, df: pd.DataFrame = None) -> tuple[str, str]:
    """Helper function to execute the processed code"""
    print("\n--- Generated Code ---")
    print(code)
    print("----------------------\n")
    
    exec_globals = {
        "np": np, 
        "pd": pd, 
        "sns": sns, 
        "plt": plt,
        "__builtins__": {
            k: __builtins__[k] for k in __builtins__ 
            if k not in ['eval', 'exec', 'open']
        }
    }
    
    if df is not None:
        exec_globals["df"] = df
    
    try:
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        
        if 'plt.' in code or 'sns.' in code:
            exec(code, exec_globals)
            plt.show()
            plt.close()
            return "Plot generated successfully.", code
        elif code.strip().startswith('print'):
            import io
            import sys
            output = io.StringIO()
            sys.stdout = output
            
            
            first_print = code.split('\n')[0]
            exec(first_print, exec_globals)
            
            
            sys.stdout = sys.__stdout__
            return output.getvalue(), first_print
        else:
            result = eval(code.split('\n')[0], exec_globals)
            if isinstance(result, pd.DataFrame) or isinstance(result, pd.Series):
                return str(result), code
            return str(result), code
    except Exception as e:
        if 'plt.' in code:
            plt.close()
        return f"Error executing code: {str(e)}", code

def create_agent(df):
    """
    Create and return a LangChain agent that uses deepseek-r1 to:
    - Interpret natural language
    - Generate Python code
    - Execute data analysis tasks
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

# This code creates an agent that uses deepseek-r1 with our curated examples
# to generate and execute Python code for data analysis tasks
