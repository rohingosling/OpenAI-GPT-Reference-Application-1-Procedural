#---------------------------------------------------------------------------------------------------------------------------------------------------------
# Application   Conversation Agent Reference Application
# Version:      1.0
# Release Date: 2024-04-06
# Author:       Rohin Gosling
#
# Description:
#
# - General-purpose conversation agent reference application, that can be used as the starting point for an OpenAI API-style chatbot.
#
# - main_loop:
#
#   - 1. Get user input prompt. 
#   - 2.     Get application command from uer input prompt. 
#   - 3.     Append user input prompt to conversation history.
#   - 4. Query language model using user input prompt.
#   - 5.     Render language model response.
#   - 6.     Append language model response to conversation history.
#   - 7. Execute application command. 
#
# Features:
#
# - Turn-based conversation agent, with conversation history.
# - Autosave conversation history to text file. 
#
# Usage Notes:
#
# - The variable `model_client` is initialized to an instance of `OpenAI`.
#   - OpenAI.api_key is set using the environment variable `OPENAI_API_KEY`.
#   - You will need to set `OPENAI_API_KEY` to hold your OpenAI API key. 
#   - Or replace `api_key = os.environ [ 'OPENAI_API_KEY' ]` with `api_key = <Your OpenAI API key>`.
#
# - On first use run the following batch files in order.
#   1. `venv_create.bat` to create the Python virtual environment.
#   2. 'venv_install_requirements.bat` to install dependent packages. 
#
# - For general use, run the following batch files before use. 
#   1. `venv_activate.bat` to activate Python virtual environment.
#
# - To-Do:
#   - None.
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------

import os
import platform
from openai import OpenAI

# Global Constants.

APPLICATION_STATE_IDLE                              = 0
APPLICATION_STATE_RUNNING                           = 1
APPLICATION_STATE_STOPPED                           = 2
APPLICATION_COMMAND_NONE                            = 0
APPLICATION_COMMAND_EXIT                            = 1
APPLICATION_COMMAND_CLEAR_TERMINAL                  = 2
APPLICATION_PROMPT_TEXT_EXIT                        = 'exit'
APPLICATION_PROMPT_TEXT_CLEAR_TERMINAL              = 'clear'
APPLICATION_TERMINAL_COMMAND_CLEAR_TERMINAL_WINDOWS = 'cls'
APPLICATION_TERMINAL_COMMAND_CLEAR_TERMINAL_LINUX   = 'clear'

MODEL_NAME_GPT_3_5_TURBO = 'gpt-3.5-turbo'
MODEL_NAME_GPT_4         = 'gpt-4'
MODEL_NAME_GPT_4O        = 'gpt-4o'


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main loop.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function name: main_loop
#
# Description:
# - This function is the main execution loop of the conversation agent application.
# - It initializes the necessary variables, manages user input, queries the language model for responses, handles application commands, and maintains the 
#   conversation history.
#
# Parameters:
# - None
#
# Return Values:
# - None
#
# Preconditions:
# - The environment variable 'OPENAI_API_KEY' must be set with a valid OpenAI API key.
# - The required OpenAI library must be installed and importable.
#
# Postconditions:
# - The application continuously runs, processing user input and generating responses from the language model until an exit command is received.
# - The conversation history is saved to a log file upon program termination.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------


def main_loop ():

    # Initialise local variables. 

    # Global variables. 

    application_state           = APPLICATION_STATE_IDLE
    application_agent_name_user = 'User'
    application_agent_name_ai   = 'AI'
    application_chat_log_folder = 'chat_log'
    model_client                = OpenAI ( api_key = os.environ [ 'OPENAI_API_KEY' ] )
    model_name                  = MODEL_NAME_GPT_4O
    model_max_tokens            = 1024
    model_temperature           = 0.7
    model_streaming_enabled     = True
    model_system_prompt         = 'You are a general purpose AI assistant. You always provide well-reasoned answers that are both correct and helpful.'    
    model_conversation_history  = [ { "role" : "system", "content" : model_system_prompt } ]

    # Print application info to the terminal. 

    print_program_info ( model_name, model_max_tokens, model_temperature, model_streaming_enabled )

    # Execute main loop. 

    application_state   = APPLICATION_STATE_RUNNING
    application_command = APPLICATION_COMMAND_NONE

    while application_state == APPLICATION_STATE_RUNNING:
 
        # Get user input prompt.
        # 1. Get the user's input prompt from the terminal.
        # 2. Identify and initialize any application commands the user may have issued.
        # 3. Save the user's prompt to the conversation history.

        user_input          = get_user_prompt ( application_agent_name_user )        
        application_command = get_application_command ( user_input )
        model_conversation_history.append ( { "role": "user", "content": user_input } )

        # Get response from language model. 

        if application_command == APPLICATION_COMMAND_NONE:

            # Query language model and update conversation history.             
            # 1. Query language model. We will return the response object, not the text. The renderer will decide whether to extract response text or use the 
            #    object based on whether `model_streaming_enabled` is True or not.
            # 2. Render model response. `model_streaming_enabled` is True then we will render streaming output from the model, otherwise we will just render
            #    the complete response text from the model. 
            # 3. Append language model response to conversation history.

            model_response      = query_language_model ( model_client, model_name, model_max_tokens, model_temperature, model_streaming_enabled, model_conversation_history )
            model_response_text = render_language_model_response ( model_response, application_agent_name_ai, model_streaming_enabled )
            model_conversation_history.append ( { "role": "assistant", "content": model_response_text } )

        else:

            # Execute application command. 

            application_state, application_command = execute_application_command ( application_command )

    # Shut down program.

    save_chat_log_to_file ( application_chat_log_folder, model_name, model_max_tokens, model_temperature, model_streaming_enabled, model_conversation_history )
            

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get user prompt.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function name: get_user_prompt
#
# Description:
# - This function prompts the user for input by displaying a terminal prompt with the user's agent name and then captures the input.
#
# Parameters:
# - application_agent_name_user (str): The name of the user agent to be displayed in the terminal prompt.
#
# Return Values:
# - user_prompt (str): The input provided by the user.
#
# Preconditions:
# - The parameter 'application_agent_name_user' must be a valid string representing the user's agent name.
#
# Postconditions:
# - The user's input is captured and returned as a string.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------


def get_user_prompt ( application_agent_name_user ):

    # Compile terminal prompt, get prompt text from the user, and return the prompt to the caller. 

    terminal_prompt_user = f'[{application_agent_name_user}]'
    user_prompt          = input ( f'\n{terminal_prompt_user}\n' )
    
    return user_prompt

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get application command from user prompt. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function name: get_application_command
#
# Description:
# - This function processes the user's input prompt to identify and return any application command embedded within the prompt.
# - It normalizes the user prompt to lowercase and checks for specific command keywords to determine the appropriate command.
#
# Parameters:
# - user_prompt (str): The input prompt provided by the user.
#
# Return Values:
# - command (int): An integer representing the identified application command. Possible values are:
#   - APPLICATION_COMMAND_NONE (0): No command identified.
#   - APPLICATION_COMMAND_EXIT (1): Exit command identified.
#   - APPLICATION_COMMAND_CLEAR_TERMINAL (2): Clear terminal command identified.
#
# Preconditions:
# - The parameter 'user_prompt' must be a valid string.
#
# Postconditions:
# - The appropriate application command is returned based on the content of the user prompt.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_application_command ( user_prompt ):

    # Inisialize local variables. 

    command     = APPLICATION_COMMAND_NONE
    user_prompt = user_prompt.lower()       # Normalise user prompt to lower case. 

    # Identify any application commands the user intends to execute.    

    if user_prompt == APPLICATION_PROMPT_TEXT_EXIT:
        command = APPLICATION_COMMAND_EXIT

    elif user_prompt == APPLICATION_PROMPT_TEXT_CLEAR_TERMINAL:
        command = APPLICATION_COMMAND_CLEAR_TERMINAL

    else:
        command = APPLICATION_COMMAND_NONE

    # Return selected command to the caller. 

    return command

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Execute application command.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function name: execute_application_command
#
# Description:
# - This function executes the given application command and returns the updated application state.
# - It handles commands such as running, stopping, and clearing the terminal based on the operating system.
#
# Parameters:
# - command (int): An integer representing the application command to be executed. Possible values are:
#   - APPLICATION_COMMAND_NONE (0): No command to execute.
#   - APPLICATION_COMMAND_EXIT (1): Command to exit the application.
#   - APPLICATION_COMMAND_CLEAR_TERMINAL (2): Command to clear the terminal.
#
# Return Values:
# - application_state (int): An integer representing the current state of the application. Possible values are:
#   - APPLICATION_STATE_IDLE (0): The application is idle.
#   - APPLICATION_STATE_RUNNING (1): The application is running.
#   - APPLICATION_STATE_STOPPED (2): The application is stopped.
# - command (int): Resets the command to APPLICATION_COMMAND_NONE (0).
#
# Preconditions:
# - The parameter 'command' must be a valid integer representing a command.
#
# Postconditions:
# - The application state is updated based on the executed command.
# - The terminal is cleared if the clear terminal command is executed.
# - The command is reset to APPLICATION_COMMAND_NONE.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def execute_application_command ( command ):

    # Initialize local variables. 

    application_state = APPLICATION_STATE_IDLE

    # Execute commands. 

    if command == APPLICATION_COMMAND_NONE:
        application_state = APPLICATION_STATE_RUNNING

    elif command == APPLICATION_COMMAND_EXIT:
        application_state = APPLICATION_STATE_STOPPED

    elif command == APPLICATION_COMMAND_CLEAR_TERMINAL:
        application_state = APPLICATION_STATE_RUNNING

        if platform.system () == "Windows":
            os.system ( APPLICATION_TERMINAL_COMMAND_CLEAR_TERMINAL_WINDOWS )

        else:
            os.system ( APPLICATION_TERMINAL_COMMAND_CLEAR_TERMINAL_LINUX )

    else:
        application_state = APPLICATION_STATE_RUNNING

    # Return application state and reset command. 

    return application_state, APPLICATION_COMMAND_NONE

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get language model response.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function name: query_language_model
#
# Description:
# - This function queries the language model using the provided parameters and returns the response object.
# - It handles both streaming and non-streaming responses.
#
# Parameters:
# - client (OpenAI): An instance of the OpenAI client used to interact with the language model.
# - name (str): The name of the language model to be used for querying.
# - max_tokens (int): The maximum number of tokens to be generated in the response.
# - temperature (float): The sampling temperature to be used for generating the response.
# - streaming_enabled (bool): A flag indicating whether streaming is enabled for the response.
# - conversation_history (list): A list of dictionaries representing the conversation history, including user inputs and system prompts.
#
# Return Values:
# - response (object): The response object from the language model, which can be used to extract the response text or handle streaming responses.
# - In case of an exception, returns a string containing the error message.
#
# Preconditions:
# - The 'client' parameter must be a valid instance of the OpenAI client.
# - The 'name' parameter must be a valid string representing a model name.
# - The 'max_tokens' parameter must be a positive integer.
# - The 'temperature' parameter must be a float between 0 and 1.
# - The 'streaming_enabled' parameter must be a boolean.
# - The 'conversation_history' parameter must be a list of dictionaries formatted correctly for the language model.
#
# Postconditions:
# - The language model is queried with the provided parameters.
# - The response object from the language model is returned, or an error message is returned in case of an exception.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def query_language_model ( client, name, max_tokens, temperature, streaming_enabled, conversation_history ):
    
    try:

        # Query the language model. 

        response = client.chat.completions.create (
            model       = name,
            messages    = conversation_history,
            max_tokens  = max_tokens,
            temperature = temperature,
            stream      = streaming_enabled
        )

        # Return the response object. 
        # - We return the response object rather than the response text, so that the renderer can render streaming responses if `stream` is True.        
        # - If `stream` is False, the renderer will retrieve the response text with `response.choices [ 0 ].message.content`.

        return response
    
    except Exception as e:

        return f'\n[ERROR]\n{str(e)}\n'

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Process language model response.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function name: render_language_model_response
#
# Description:
# - This function processes the response from the language model, rendering it to the terminal.
# - It handles both streaming and non-streaming responses and returns the response text.
#
# Parameters:
# - response (object): The response object from the language model.
# - application_agent_name_ai (str): The name of the AI agent to be displayed in the terminal prompt.
# - model_streaming_enabled (bool): A flag indicating whether streaming is enabled for the response.
#
# Return Values:
# - response_text (str): The response text from the language model.
#
# Preconditions:
# - The 'response' parameter must be a valid response object from the language model.
# - The 'application_agent_name_ai' parameter must be a valid string representing the AI agent's name.
# - The 'model_streaming_enabled' parameter must be a boolean.
#
# Postconditions:
# - The response from the language model is printed to the terminal.
# - The complete response text is returned.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def render_language_model_response ( response, application_agent_name_ai, model_streaming_enabled):

    # Initialise local variables.

    response_text      = ''                                  # Initialise to empty string. We'll populate after handing streaming or non-streaming responses.
    terminal_prompt_ai = f'[{application_agent_name_ai}]'    # Compile terminal prompt.

    # Print response. 

    print ( f'\n{terminal_prompt_ai}')

    if model_streaming_enabled:

        # Output chunk by chunk as the response is streamed. 

        response_stream = { 'role': 'assistant', 'content': '' }
    
        for chunk in response:
            if chunk.choices [ 0 ].delta.content:
                print ( chunk.choices [ 0 ].delta.content, end='', flush = True )
                response_stream [ 'content' ] += chunk.choices [ 0 ].delta.content
        print ()

        # For a streamed response, get the response text from the completed response stream.

        response_text = response_stream [ 'content' ]
        
    else:

        # For a non-streamed response, get the response text from the response object, and write to the terminal. 

        response_text = response.choices [ 0 ].message.content
        print ( f"{response_text}" )

    # Return language model response text. 

    return response_text
        

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Display program info.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function name: print_program_info
#
# Description:
# - This function prints information about the language model being used by the application, including the model name,# maximum tokens, temperature, and 
#   whether streaming is enabled.
#
# Parameters:
# - model_name (str): The name of the language model.
# - model_max_tokens (int): The maximum number of tokens for the language model's responses.
# - model_temperature (float): The temperature setting for the language model, controlling the randomness of the output.
# - model_streaming_enabled (bool): A flag indicating whether streaming is enabled for the language model.
#
# Return Values:
# - None
#
# Preconditions:
# - The 'model_name' parameter must be a valid string representing the model name.
# - The 'model_max_tokens' parameter must be a positive integer.
# - The 'model_temperature' parameter must be a float between 0 and 1.
# - The 'model_streaming_enabled' parameter must be a boolean.
#
# Postconditions:
# - Information about the language model is printed to the terminal.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def print_program_info ( model_name, model_max_tokens, model_temperature, model_streaming_enabled ):

    print ()
    print ( f'Language Model:' )
    print ( f'- Model:             {model_name}' )
    print ( f'- Max Tokens:        {model_max_tokens}' )
    print ( f'- Temperature:       {model_temperature}' )
    print ( f'- Streaming Enabled: {model_streaming_enabled}' )    

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Shutdown application.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Function name: save_chat_log_to_file
#
# Description:
# - This function saves the conversation history of the chat application to a text file.
# - It ensures the target folder exists, determines the next available file name, and writes the conversation history along with model details to the file.
#
# Parameters:
# - application_chat_log_folder (str): The folder path where the chat log will be saved.
# - model_name (str): The name of the language model used.
# - model_max_tokens (int): The maximum number of tokens for the language model's responses.
# - model_temperature (float): The temperature setting for the language model, controlling the randomness of the output.
# - model_streaming_enabled (bool): A flag indicating whether streaming is enabled for the language model.
# - model_conversation_history (list): A list of dictionaries representing the conversation history, including user inputs and model responses.
#
# Return Values:
# - None
#
# Preconditions:
# - The 'application_chat_log_folder' parameter must be a valid directory path as a string.
# - The 'model_name' parameter must be a valid string representing the model name.
# - The 'model_max_tokens' parameter must be a positive integer.
# - The 'model_temperature' parameter must be a float between 0 and 1.
# - The 'model_streaming_enabled' parameter must be a boolean.
# - The 'model_conversation_history' parameter must be a list of dictionaries formatted correctly.
#
# Postconditions:
# - The conversation history is saved to a new text file in the specified folder.
# - The file name is printed to the terminal.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def save_chat_log_to_file ( application_chat_log_folder, model_name, model_max_tokens, model_temperature, model_streaming_enabled, model_conversation_history ):

    folder_path = application_chat_log_folder
    
    # Ensure the folder exists; if not, create it.

    if not os.path.exists ( folder_path ):
        os.makedirs ( folder_path )
    
    # Determine the next file number to use.

    file_index = 0

    while os.path.exists ( os.path.join ( folder_path, f'chat_log_{file_index}.txt') ):
        file_index += 1

    # Create the filename with the next index.

    file_name = os.path.join ( folder_path, f'chat_log_{file_index}.txt' )

    # Write the conversation history to the file.

    with open ( file_name, 'w', encoding = 'utf-8' ) as file:

        file.write ( f'Model:             {model_name}\n' )
        file.write ( f'Max Tokens:        {model_max_tokens}\n' )
        file.write ( f'Temperature:       {model_temperature}\n' )
        file.write ( f'Streaming Enabled: {model_streaming_enabled}\n' )
        file.write ( '\n' )

        for row in model_conversation_history:
            file.write ( f'[{row [ "role" ]}]\n{row [ "content" ]}\n\n' )

    print ( f'\nConversation history saved to "{file_name}."' )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main program.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Function name: main
#
# Description:
# - This is the entry point for the conversation agent application.
# - It initiates the main loop of the application, which handles user input, queries the language model, and processes application commands.
#
# Parameters:
# - parameter_name (data_type): Description of parameter.
# - parameter_name (data_type): Description of parameter.
# - None
#
# Return Values:
# - return_value (data_type): Description of return value.
# - return_value (data_type): Description of return value.
# - None
#
# Preconditions:
# - Precondition description.
# - Precondition description.
#
# Postconditions:
# - Postcondition description.
# - Postcondition description.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():

    # Execute main loop. 

    main_loop ()

if __name__ == "__main__":

    main ()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function tagline. e.g. Execute this or that. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
#
# Function name: function_name
#
# Description:
# - bla bla bla.
# - bla bla bla.
#
# Parameters:
# - None
#
# Return Values:
# - None
#
# Preconditions:
# - The script is executed as the main module.
#
# Postconditions:
# - The main loop of the application is started and runs until an exit command is received.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
