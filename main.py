from data_tools import load_dataset
from agent import interpret_and_execute
from feedback_store import FeedbackStore

def main():
    try:
        file_path = input("Enter dataset file path (CSV): ")
        df = load_dataset(file_path)
        feedback_store = FeedbackStore()
        
        if isinstance(df, str):
            print(f"Error: {df}")
            return
        
        print("\nDataset loaded successfully!")
        print(f"Shape of dataset: {df.shape}")
        print("\nColumns in dataset:")
        print(df.columns.tolist())
        print("\nType 'help' for available commands or 'exit' to quit.")
        
        while True:
            instruction = input("\nDescribe your data analysis task: ").strip().lower()
            if instruction == 'exit':
                break
            elif instruction == 'help':
                print("\nAvailable commands:")
                print("- exit: Quit the program")
                print("- help: Show this help message")
                print("- Any data analysis task using the columns:", df.columns.tolist())
                continue
            
            print("\nProcessing your request...")
            result, code = interpret_and_execute(instruction, df)
            print("\nResult:", result)
            
            while True:
                feedback = input("\nWas this result correct? (y/n): ").lower()
                if feedback in ['y', 'yes', 'n', 'no']:
                    break
                print("Please enter 'y' or 'n'")
                
            if feedback in ['y', 'yes']:
                example = {
                    "task": instruction,
                    "code": code
                }
                feedback_store.add_example(example)
                print("Great! Added to successful examples.")
            else:
                correct_code = input("What would be the correct code? (press enter to skip): ")
                if correct_code.strip():
                    correct_example = {
                        "task": instruction,
                        "code": correct_code
                    }
                    feedback_store.add_example(correct_example)
                print("Thank you for the feedback!")
                
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()


#this block of code is used to run the main program
#it loads the dataset, interprets the instruction, and gets feedback
#the feedback is then used to train the agent
#the agent is then used to execute the code
#the result is then displayed


