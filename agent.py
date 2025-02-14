import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from langchain_ollama import ChatOllama 
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
import re
from typing import List

from config import MODEL_NAME
from prompts import create_prompt 

llm = ChatOllama(model=MODEL_NAME)

# Define regex patterns for code and natural language
CODE_PATTERNS = [
    r'df\.[a-zA-Z_]+\(.*\)',  # DataFrame methods
    r'plt\.[a-zA-Z_]+\(.*\)',  # Matplotlib commands
    r'sns\.[a-zA-Z_]+\(.*\)',  # Seaborn commands
    r'np\.[a-zA-Z_]+\(.*\)',   # NumPy operations
    r'pd\.[a-zA-Z_]+\(.*\)',   # Pandas operations
    r'\[.*\]',                 # List/array operations
    r'=(?!=)',                 # Assignment (but not ==)
    r'\(.*\)',                 # Function calls
]

NATURAL_LANGUAGE_PATTERNS = [
    r'^[A-Z][^()]*\.$',       # Sentences starting with capital letter
    r'\b(I|we|let|think|need|want|should|could|would|may|might|can)\b',  # Common words
    r'\b(okay|so|then|now|here|there|just|try|using|remember|recall)\b',
    r'[?!]',                  # Question/exclamation marks
    r'^#.*',                  # Comments
    r'```.*```',              # Code blocks markers
]

def is_code_line(line: str) -> bool:
    """Check if a line looks like code"""
    return any(re.search(pattern, line) for pattern in CODE_PATTERNS)

def is_natural_language(line: str) -> bool:
    """Check if a line looks like natural language"""
    return any(re.search(pattern, line, re.IGNORECASE) for pattern in NATURAL_LANGUAGE_PATTERNS)

def interpret_and_execute(instruction: str, df: pd.DataFrame) -> tuple[str, str]:
    """Uses deepseek-r1 with our examples to generate code"""
    prompt = create_prompt(instruction, list(df.columns))
    response = llm.invoke(prompt)
    code = response.content.strip()
    return process_code(code, df, instruction)

def process_code(code: str, df: pd.DataFrame, instruction: str = "") -> tuple[str, str]:
    """Process and execute the generated code"""
    try:
        if instruction and instruction.lower().strip() in ['show full dataset', 'show all data', 'display full dataset', 'show data']:
            pd.set_option('display.max_rows', None)
            pd.set_option('display.max_columns', None)
            pd.set_option('display.width', None)
            pd.set_option('display.max_colwidth', None)
            return df.to_string(), "df.to_string()"
        
        code_lines = []
        for line in code.split('\n'):
            line = line.strip()
            
            if not line or re.match(r'^[^a-zA-Z0-9_]+$', line):
                continue
                
            if is_natural_language(line):
                continue
                
            if is_code_line(line):
                code_lines.append(line)
        
        code = '\n'.join(code_lines).strip()
        
        if not code:
            return "No valid code generated.", ""
            
        # Fix column names and special characters
        for col in df.columns:
            if col.lower() in code.lower():
                code = code.replace(col.lower(), col)
        
        code = re.sub(r'[''—]', "'", code)  # Replace special quotes and dashes
        
        return process_and_execute(code, df)
        
    except Exception as e:
        return f"Error processing code: {str(e)}", code

def process_and_execute(code: str, df: pd.DataFrame) -> tuple[str, str]:
    """Helper function to execute the processed code"""
    print("\n--- Generated Code ---")
    print(code)
    print("----------------------\n")
    
    exec_globals = {
        "np": np, 
        "pd": pd, 
        "sns": sns, 
        "plt": plt,
        "df": df,
        "__builtins__": {
            k: __builtins__[k] for k in __builtins__ 
            if k not in ['eval', 'exec', 'open']
        }
    }
    
    try:
        # Set display options
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.width', None)
        pd.set_option('display.max_colwidth', None)
        
        if 'plt.' in code or 'sns.' in code:
            exec(code, exec_globals)
            plt.show()
            plt.close()
            return "Plot generated successfully.", code
        elif code.strip().startswith('print'):
            print_content = code.strip()[6:-1]  
            if print_content == 'df':
                return df.to_string(), code
            else:
                result = eval(print_content, exec_globals)
                return str(result), code
        else:
            result = eval(code, exec_globals)
            if isinstance(result, pd.DataFrame):
                return result.to_string(), code
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
# the code is based on the following article: https://medium.com/@josephroque/building-a-data-analysis-agent-with-langchain-and-ollama-2024-11-25-1e1441244e3e
