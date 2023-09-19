import readline

def create_input_with_history(input_fn: callable = input):
    """
    This function creates an input function with history.
    It uses the readline module to add the user input to the history.
    
    @param input_fn: The input function to use. Defaults to the built-in input function.
    @return: A function that gets user input and adds it to the history.
    """
    def input_with_history_fn(prompt):
        """
        This function gets user input and adds it to the history.
        
        @param prompt: The prompt message to display to the user.
        @return: The input entered by the user.
        """
        user_input = input_fn(prompt)
        if user_input:
            readline.add_history(user_input)
            return user_input
    return input_with_history_fn

def create_input_with_clear(input_fn: callable = input):
    def input_with_clear_fn(prompt):
        """
        This function gets user input and clears the line.
        It uses ANSI escape codes to move the cursor up and clear the line.
        \033[A moves the cursor up by one line.
        \033[K clears the line from the current cursor position to the end of the line.
        
        @param prompt: The prompt message to display to the user.
        @return: The input entered by the user.
        """
        user_input = input_fn(prompt)
        
        # Use ANSI escape codes to move the cursor up and clear the line
        # \033[A moves the cursor up by one line
        # \033[K clears the line from the current cursor position to the end of the line
        print("\033[A\033[K", end='')
        
        return user_input
    return input_with_clear_fn


user_input = create_input_with_history(create_input_with_clear(input))

if __name__ == '__main__':   
   while True: 
       try:
           input = user_input("Enter command: ")
           if (input == 'exit'):
               raise KeyboardInterrupt()
           print(input)
       except(EOFError, KeyboardInterrupt):
           print("Exiting...")
           exit(0)