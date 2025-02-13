from data_tools import load_dataset
from agent import interpret_and_execute
from feedback_store import FeedbackStore

def main():
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
    print("\nNow you can describe your data analysis task.")
    
    while True:
        instruction = input("\nDescribe your data analysis task (or type 'exit' to quit): ")
        if instruction.lower() == 'exit':
            break
            
        print("\nProcessing your request...")
        result, code = interpret_and_execute(instruction, df)
        print("\nResult:", result)
        
        # Get feedback
        feedback = input("\nWas this result correct? (y/n): ").lower()
        if feedback in ['y', 'yes']:
            feedback_store.add_example(instruction, code, True)
            print("Great! Added to successful examples.")
        elif feedback in ['n', 'no']:
            feedback_store.add_example(instruction, code, False)
            correct_code = input("What would be the correct code? (press enter to skip): ")
            if correct_code.strip():
                feedback_store.add_example(instruction, correct_code, True)
            print("Thank you for the feedback!")

if __name__ == "__main__":
    main()


#this block of code is used to run the main program
#it loads the dataset, interprets the instruction, and gets feedback
#the feedback is then used to train the agent
#the agent is then used to execute the code
#the result is then displayed


