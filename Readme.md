# AI Data Analyst

AI Data Analyst is a Python-based project that leverages an AI agent to interpret natural language data analysis tasks and execute them on a CSV dataset. The project uses LangChain alongside Ollama’s ChatOllama interface (with the deepseek‑r1 model by default) to dynamically generate and run Python code for data analysis. User feedback is collected to help improve the system over time.

## Features

- **Natural Language Interface:** Describe your data analysis tasks in plain English.
- **Dynamic Code Generation:** Converts user instructions into executable Python code.
- **Integrated Execution:** Runs generated code on your dataset and displays results (including visualizations).
- **Feedback Loop:** Collects feedback on the generated code to store examples of successes and failures.
- **Modular Structure:** Separate modules for dataset loading, code generation, execution, and feedback management.

## Repository Structure

Below is a breakdown of the repository's structure:

```plaintext
AI_Data_Analyst/
├── __pycache__/                # Cached Python files
├── dataset/                   # Folder containing sample or generated datasets
├── prompts/                   # Contains prompt templates for the AI model
├── .gitignore                 # Specifies intentionally untracked files to ignore
├── agent.py                   # Implements the AI agent for code generation and execution
├── config.py                  # Configuration file (default model settings)
├── data_tools.py              # Utilities for loading and processing datasets
├── dataset_generator.py       # Optional: Script for generating sample datasets
├── feedback_data.json         # JSON file for storing user feedback
├── feedback_store.py          # Manages feedback collection and storage
├── main.py                    # Main execution loop for the application
├── requirements.txt           # List of required Python dependencies
├── test.py                    # Script for testing functionality
└── train.py                   # Script for training or refining the agent using feedback
```

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Aniket-a14/AI_Data_Analyst.git
   cd AI_Data_Analyst
   ```

2. **Install the required dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuration:**

   - Check the `config.py` file to ensure the correct model name is set. By default, it uses `"deepseek-r1"`. You can change this to any other supported model from Ollama if desired.

## Usage

1. **Run the main program:**

   ```bash
   python main.py
   ```

2. **Follow the prompts:**
   - Enter the path to your CSV dataset when prompted.
   - Review dataset details (shape, columns, etc.).
   - Describe your data analysis task in plain English.
   - The AI agent will generate Python code to perform the requested task.
   - The generated code is executed, and the result (or plot) is displayed.
   - Provide feedback on whether the output was correct. If not, you can optionally supply the correct code to improve future performance.

## Contributing

Contributions are welcome! If you have ideas for improvements or new features, please consider:
- Reporting issues or suggesting enhancements via the repository’s Issues tab.
- Submitting a pull request with your proposed changes.
- Providing feedback through the integrated feedback mechanism to help train and refine the AI agent.


## Acknowledgements

- This project utilizes [LangChain](https://github.com/hwchase17/langchain) for building the AI agent.
- The AI code generation is powered by Ollama’s ChatOllama interface.
- Special thanks to the open-source community.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

