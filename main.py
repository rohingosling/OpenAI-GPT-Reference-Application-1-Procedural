#---------------------------------------------------------------------------------------------------------------------------------------------------------
# Application   Conversation Agent Reference Application
# Version:      2.0
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
#   - 2.     Get application command from user input prompt. 
#   - 3.     Append user input prompt to conversation history.
#   - 4. Query language model using user input prompt.
#   - 5.     Render language model response.
#   - 6.     Append language model response to conversation history.
#   - 7. Execute application command. 
#
# Features:
#
# - Turn-based conversation agent, with conversation history.
# - Autosave conversation history to a text file.
# 
# Dependencies:
# 
# - OpenAI Library:
#
#   pip install --upgrade openai 
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
#   1. `venv_activate.bat` to activate the Python virtual environment.
#
# - To-Do:
#   1. Update README.md file. 
#   2. Add more error handling and testing. 
#
#---------------------------------------------------------------------------------------------------------------------------------------------------------

import os
import platform
from openai import OpenAI

# Global Constants.

# Constants: Terminal Management.
# - Terminal formatting and rendering.

TERMINAL_PROMPT_AGENT_NAMETAG = '<agent_name>'                              # Markdown tag to be replaced with actual agent name.
TERMINAL_PROMPT_FORMAT        = '[' + TERMINAL_PROMPT_AGENT_NAMETAG + ']'   # Terminal prompt format, e.g. "[USer]".
TERMINAL_ERROR                = '[Error]'
TERMINAL_SYSTEM               = '[SYSTEM]'
TERMINAL_BULLET               = '- '

# Constants: Application States.
# - Application states are used to control application flow. 

APPLICATION_STATE_IDLE    = 0   # Default application state. Usually used to initialise application state variables before giving them a value later. 
APPLICATION_STATE_RUNNING = 1   # The application main loop is running.
APPLICATION_STATE_STOPPED = 2   # The application main loop is stopped.

# Constants: Application commands.
# - Application commands control application state, or trigger actions.
# - Note:
#   - In a more sophisticated application we would define "events" that drive application state, in the form of a state machine. Where anything could raise an event.
#   - For the sake of simplicity, this reference application will just make use of simple user triggered commands to drive application state and actions. 

APPLICATION_COMMAND_NONE           = 0
APPLICATION_COMMAND_EXIT           = 1
APPLICATION_COMMAND_CLEAR_TERMINAL = 2

# Constants: User Prompt Commands. 
# - When the user types any of the commands defined below, the text will be translated to application command constants (see below) to be executed by the command manager.

PROMPT_COMMAND_NONE  = ''       # No command issued by the user. 
PROMPT_COMMAND_EXIT  = 'exit'   # The user wants to exit the application.
PROMPT_COMMAND_CLEAR = 'clear'  # The user wants to clear the application terminal. 

# Constants: Terminal Commands. 
# - Terminal commands that can be issued to the OS terminal.
# - When I user enters a prompt command, the command interpreter will convert the prompt command to an application command.
# - The command manager will execute the latest command. If the latest command is to issue a command to the terminal, then these constants will be used
#   to execute actual command on the appropriate OS terminal. 

TERMINAL_COMMAND_CLEAR_TERMINAL_WINDOWS = 'cls'
TERMINAL_COMMAND_CLEAR_TERMINAL_LINUX   = 'clear'

# Constants: Language Model Meta Parameters.

MODEL_NAME_GPT_3_5_TURBO      = 'gpt-3.5-turbo'
MODEL_NAME_GPT_4              = 'gpt-4'
MODEL_NAME_GPT_4O             = 'gpt-4o'
MODEL_MESSAGE_ROLE_SYSTEM     = 'system'
MODEL_MESSAGE_ROLE_USER       = 'user'
MODEL_MESSAGE_ROLE_AI         = 'assistant'
MODEL_SYSTEM_PROMPT_FILE_NAME = 'data\system_prompt.txt'
MODEL_SYSTEM_PROMPT_DEFAULT   = 'You are a general purpose AI assistant. You always provide well-reasoned answers that are both correct and helpful.'


# Constants: Dictionary key names.

KEY_APPLICATION_NAME                    = 'name'
KEY_APPLICATION_VERSION                 = 'version'
KEY_APPLICATION_AGENT_NAME_USER         = 'agent_name_user'
KEY_APPLICATION_AGENT_NAME_AI           = 'agent_name_ai'
KEY_APPLICATION_CHAT_LOG_FOLDER         = 'chat_log_folder'
KEY_APPLICATION_CHAT_LOG_FILE_NAME      = 'chat_log_file_name'
KEY_APPLICATION_CHAT_LOG_FILE_EXTENSION = 'chat_log_file_extension'
KEY_APPLICATION_COMMAND                 = 'command'
KEY_APPLICATION_STATE                   = 'state'

KEY_MODEL_CLIENT               = 'client'
KEY_MODEL_NAME                 = 'name'
KEY_MODEL_MAX_TOKENS           = 'max_tokens'
KEY_MODEL_TEMPERATURE          = 'temperature'
KEY_MODEL_STREAMING_ENABLED    = 'streaming_enabled'
KEY_MODEL_CONVERSATION_HISTORY = 'conversation_history'

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Initialize application settings and model configurations.
#
# Function name:
# - application_initialize
#
# Description:
# - This function initializes the application and model configuration settings.
# - It returns a dictionary containing the application's initial state and model configurations.
#
# Parameters:
# - None.
#
# Return Values:
# - application: dict : Dictionary containing the application's initial state.
# - model: dict : Dictionary containing the model configuration settings.
#
# Preconditions:
# - None.
#
# Postconditions:
# - Application and model dictionaries are initialized and returned.
#
# To-Do:
# 1. Add error handling for missing API key.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def application_initialize ():
   
    application = {
        KEY_APPLICATION_NAME                    : 'Conversation Agent Reference Application',
        KEY_APPLICATION_VERSION                 : 2.0,
        KEY_APPLICATION_AGENT_NAME_USER         : 'User',
        KEY_APPLICATION_AGENT_NAME_AI           : 'AI',
        KEY_APPLICATION_CHAT_LOG_FOLDER         : 'chat_log',
        KEY_APPLICATION_CHAT_LOG_FILE_NAME      : 'chat_log_',
        KEY_APPLICATION_CHAT_LOG_FILE_EXTENSION : '.txt',
        KEY_APPLICATION_COMMAND                 : APPLICATION_COMMAND_NONE,
        KEY_APPLICATION_STATE                   : APPLICATION_STATE_IDLE        
    }

    model = {
        KEY_MODEL_CLIENT                  : OpenAI ( api_key = os.environ [ 'OPENAI_API_KEY' ] ),
        KEY_MODEL_NAME                    : MODEL_NAME_GPT_3_5_TURBO,
        KEY_MODEL_MAX_TOKENS              : 1024,
        KEY_MODEL_TEMPERATURE             : 0.7,
        KEY_MODEL_STREAMING_ENABLED       : True,
        KEY_MODEL_CONVERSATION_HISTORY    : []     
    }

    return application, model

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main loop of the application handling user input and querying the language model.
#
# Function name:
# - main_loop
#
# Description:
# - This function runs the main loop of the application.
# - It handles user input, queries the language model, and executes application commands.
#
# Parameters:
# - application : dict : Dictionary containing the application's state.
# - model : dict : Dictionary containing the model configuration settings.
#
# Return Values:
# - None.
#
# Preconditions:
# - Application and model dictionaries must be initialized.
#
# Postconditions:
# - User input is processed and language model responses are generated and rendered.
#
# To-Do:
# 1. Improve error handling within the loop.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def main_loop ( application, model ):

    # Initialise system prompt.
    # - If a system prompt can not be loaded from the file, then just use the default system prompt. 

    model_system_prompt = load_text_to_string ( MODEL_SYSTEM_PROMPT_FILE_NAME )

    if model_system_prompt == '':
        model_system_prompt = MODEL_SYSTEM_PROMPT_DEFAULT

    # Add system prompt to the beginning of conversion history.

    add_message_to_conversation_history ( model, model_system_prompt, MODEL_MESSAGE_ROLE_SYSTEM )

    # Initialise main loop.  

    application [ KEY_APPLICATION_COMMAND ] = APPLICATION_COMMAND_NONE
    application [ KEY_APPLICATION_STATE   ] = APPLICATION_STATE_RUNNING    

    # Execute the main loop.

    while application [ KEY_APPLICATION_STATE ] == APPLICATION_STATE_RUNNING:
 
        # Get user input prompt.
        # 1. Get the user's input prompt from the terminal.
        # 2. Identify and initialize any application commands the user may have issued.
        # 3. Save the user's prompt to the conversation history.

        user_input                              = get_user_prompt ( application )        
        application [ KEY_APPLICATION_COMMAND ] = get_application_command ( user_input )                
        
        # Query language model and update conversation history.             
        # 1. Query language model. We will return the response object, not the text. The renderer will decide whether to extract response text or use the 
        #    object based on whether `model_streaming_enabled` is True or not.
        # 2. Render model response. `model_streaming_enabled` is True then we will render streaming output from the model, otherwise we will just render
        #    the complete response text from the model. 
        # 3. Append language model response to conversation history.

        if application [ KEY_APPLICATION_COMMAND ] == APPLICATION_COMMAND_NONE:

            add_message_to_conversation_history ( model, user_input, MODEL_MESSAGE_ROLE_USER )
            model_response      = query_language_model ( model )
            model_response_text = render_language_model_response ( application, model, model_response )
            add_message_to_conversation_history ( model, model_response_text, MODEL_MESSAGE_ROLE_AI )

        # Execute application command.            

        execute_application_command ( application )            

    # Shut down program.

    save_chat_log_to_file ( application, model, include_system_prompt_enabled = False )
            
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Add a message to the conversation history.
#
# Function name:
# - add_message_to_conversation_history
#
# Description:
# - This function appends a message to the model's conversation history.
#
# Parameters:
# - model : dict : Dictionary containing the model configuration settings.
# - message : str : The message to be added to the conversation history.
# - message_role : str : The role of the message sender (e.g., user, assistant, system).
#
# Return Values:
# - None.
#
# Preconditions:
# - The model dictionary must be initialized.
# - The message must be a string.
# - The message_role must be a valid role string.
#
# Postconditions:
# - The message is appended to the conversation history.
#
# To-Do:
# 1. Validate message and message_role before appending.
# 2. Add error handling for invalid inputs.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def add_message_to_conversation_history ( model, message, message_role ):
    
    model [ KEY_MODEL_CONVERSATION_HISTORY ].append ( { 'role': message_role, 'content': message } )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Retrieve the user prompt from the terminal.
#
# Function name:
# - get_user_prompt
#
# Description:
# - This function retrieves the user's input prompt from the terminal.
# - It compiles the terminal prompt using the user's agent name and returns the prompt.
#
# Parameters:
# - application : dict : Dictionary containing the application's state.
#
# Return Values:
# - user_prompt : str : The user's input prompt.
#
# Preconditions:
# - The application dictionary must be initialized.
#
# Postconditions:
# - The user's input prompt is retrieved and returned.
#
# To-Do:
# 1. Add input validation for user prompt.
# 2. Handle edge cases for empty or invalid inputs.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_user_prompt ( application ):

    # Initialise local variables. 

    application_agent_name_user = application [ KEY_APPLICATION_AGENT_NAME_USER ]

    # Compile terminal prompt, get prompt text from the user, and return the prompt to the caller.

    terminal_prompt_user = f'[{application_agent_name_user}]'
    user_prompt          = input ( f'\n{terminal_prompt_user}\n' )

    return user_prompt

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Convert the user prompt to an application command.
#
# Function name:
# - get_application_command
#
# Description:
# - This function converts the user's input prompt to an application command.
# - It normalizes the user prompt to lowercase and identifies any application commands to execute.
#
# Parameters:
# - user_prompt : str : The user's input prompt.
#
# Return Values:
# - application_command : int : The application command constant.
#
# Preconditions:
# - The user prompt must be a string.
#
# Postconditions:
# - The appropriate application command is identified and returned.
#
# To-Do:
# 1. Add more user prompt commands.
# 2. Improve error handling for unrecognized commands.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_application_command ( user_prompt ):

    # Initialize local variables. 

    application_command = APPLICATION_COMMAND_NONE
    user_prompt         = user_prompt.lower()       # Normalize user prompt to lower case. 

    # Identify any application commands the user intends to execute.    

    if user_prompt == PROMPT_COMMAND_EXIT:
        application_command = APPLICATION_COMMAND_EXIT

    elif user_prompt == PROMPT_COMMAND_CLEAR:
        application_command = APPLICATION_COMMAND_CLEAR_TERMINAL

    else:
        application_command = APPLICATION_COMMAND_NONE

    # Return selected command to the caller. 

    return application_command

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Execute the application command.
#
# Function name:
# - execute_application_command
#
# Description:
# - This function executes the identified application command.
# - It handles commands like exiting the application or clearing the terminal.
#
# Parameters:
# - application : dict : Dictionary containing the application's state.
#
# Return Values:
# - None.
#
# Preconditions:
# - The application dictionary must be initialized.
# - A valid application command must be set.
#
# Postconditions:
# - The application command is executed and the application state is updated.
#
# To-Do:
# 1. Add more application commands and their handling.
# 2. Improve error handling for command execution.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def execute_application_command ( application ):

    # No Command.

    if application [ KEY_APPLICATION_COMMAND ] == APPLICATION_COMMAND_NONE:
        pass

    # Exit application.

    if application [ KEY_APPLICATION_COMMAND ] == APPLICATION_COMMAND_EXIT:        
        application [ KEY_APPLICATION_STATE ] = APPLICATION_STATE_STOPPED

    # Clear the application terminal.

    if application [ KEY_APPLICATION_COMMAND ] == APPLICATION_COMMAND_CLEAR_TERMINAL:
        if platform.system () == "Windows":
            os.system ( TERMINAL_COMMAND_CLEAR_TERMINAL_WINDOWS )
        else:
            os.system ( TERMINAL_COMMAND_CLEAR_TERMINAL_LINUX )

    # Reset command to no command. 

    application [ KEY_APPLICATION_COMMAND ] = APPLICATION_COMMAND_NONE


#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Query the language model with the conversation history.
#
# Function name:
# - query_language_model
#
# Description:
# - This function queries the language model using the provided conversation history.
# - It handles both streaming and non-streaming responses.
#
# Parameters:
# - model : dict : Dictionary containing the model configuration settings.
#
# Return Values:
# - response : object : The response object from the language model.
#
# Preconditions:
# - The model dictionary must be initialized.
# - The conversation history must be set.
#
# Postconditions:
# - The language model is queried and the response object is returned.
#
# To-Do:
# 1. Add more detailed error handling for the API call.
# 2. Log the query and response for debugging.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def query_language_model ( model ):
    
    try:

        # Query the language model. 

        response = model [ KEY_MODEL_CLIENT ].chat.completions.create (
            model       = model [ KEY_MODEL_NAME                 ],
            messages    = model [ KEY_MODEL_CONVERSATION_HISTORY ],
            max_tokens  = model [ KEY_MODEL_MAX_TOKENS           ],
            temperature = model [ KEY_MODEL_TEMPERATURE          ],
            stream      = model [ KEY_MODEL_STREAMING_ENABLED    ]
        )

        # Return the response object. 
        # - We return the response object rather than the response text, so that the renderer can render streaming responses if `stream` is True.        
        # - If `stream` is False, the renderer will retrieve the response text with `response.choices [ 0 ].message.content`.

        return response
    
    except Exception as e:

        return f'\n[ERROR]\n{str(e)}\n'

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Render the language model's response.
#
# Function name:
# - render_language_model_response
#
# Description:
# - This function renders the language model's response, handling both streaming and non-streaming outputs.
#
# Parameters:
# - application : dict : Dictionary containing the application's state.
# - model : dict : Dictionary containing the model configuration settings.
# - model_response : object : The response object from the language model.
#
# Return Values:
# - response_text : str : The text of the language model's response.
#
# Preconditions:
# - The application and model dictionaries must be initialized.
# - The model_response must be a valid response object.
#
# Postconditions:
# - The language model's response is rendered and the response text is returned.
#
# To-Do:
# 1. Improve handling of different response formats.
# 2. Add error handling for rendering issues.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def render_language_model_response ( application, model, model_response ):

    # Initialise local variables. 

    agent_name_ai           = application [ KEY_APPLICATION_AGENT_NAME_AI ]
    model_streaming_enabled = model       [ KEY_MODEL_STREAMING_ENABLED   ]    
    terminal_prompt_ai      = f'[{agent_name_ai}]'                          # Compile terminal prompt.
    response_text           = ''                                            # Initialise to empty string. We'll populate after handing streaming or non-streaming responses.
    
    # Print response. 

    print ( f'\n{terminal_prompt_ai}')

    # Render model response. 

    if model_streaming_enabled:

        # Output chunk by chunk as the response is streamed. 

        response_stream = { 'role' : 'assistant', 'content' : '' }
    
        for chunk in model_response:
            if chunk.choices [ 0 ].delta.content:
                print ( chunk.choices [ 0 ].delta.content, end = '', flush = True )
                response_stream [ 'content' ] += chunk.choices [ 0 ].delta.content
        print ()

        # For a streamed response, get the response text from the completed response stream.

        response_text = response_stream [ 'content' ]
        
    else:

        # For a non-streamed response, get the response text from the response object, and write to the terminal. 

        response_text = model_response.choices [ 0 ].message.content
        print ( f"{response_text}" )

    # Return language model response text. 

    return response_text
        

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Display application and model information.
#
# Function name:
# - print_application_info
#
# Description:
# - This function prints the application's and model's information to the console.
#
# Parameters:
# - application : dict : Dictionary containing the application's state.
# - model : dict : Dictionary containing the model configuration settings.
#
# Return Values:
# - None.
#
# Preconditions:
# - The application and model dictionaries must be initialized.
#
# Postconditions:
# - The application's and model's information is printed to the console.
#
# To-Do:
# - None.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def print_application_info ( application, model ):

    # Retrieve application and model information. 

    application_name        = application [ KEY_APPLICATION_NAME ]
    application_version     = str ( application [ KEY_APPLICATION_VERSION ] )
    model_name              = model [ KEY_MODEL_NAME ]
    model_max_tokens        = str ( model [ KEY_MODEL_MAX_TOKENS ] )
    model_temperature       = str ( model [ KEY_MODEL_TEMPERATURE ] )
    model_streaming_enabled = str ( model [ KEY_MODEL_STREAMING_ENABLED ] )

    # Print application and model information to the console. 
        
    print ( f'\nApplication:' )
    print ( f'{TERMINAL_BULLET}Name:    {application_name}' )
    print ( f'{TERMINAL_BULLET}Version: {application_version}' )
    print ( f'\nModel:' )
    print ( f'{TERMINAL_BULLET}Name:              {model_name}' )
    print ( f'{TERMINAL_BULLET}Max Tokens:        {model_max_tokens}' )
    print ( f'{TERMINAL_BULLET}Temperature:       {model_temperature}' )
    print ( f'{TERMINAL_BULLET}Streaming Enabled: {model_streaming_enabled}' )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Load the contents of a text file into a string.
#
# Function name:
# - load_text_to_string
#
# Description:
# - This function loads the contents of a text file into a string.
# - Example:
# 
#   text_string = load_text_to_string ( 'text_file.txt' )
#
# Parameters:
# - file_name : string : File name of the text file whose text content we wish to load into a string. 
#
# Return Values:
# - text_string : string : A string populated with the text loaded from a text file. 
#
# Preconditions:
# - The text file exists. If the text file is empty, the loaded string will just be an empty string. 
#
# Postconditions:
# - The content of the file referenced by `file_name` is returned as a string to the caller.
#
# To-Do:
# 1. Add error handling for file operations.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def load_text_to_string ( file_name ):
    
    try:
        with open ( file_name, 'r', encoding = 'utf-8' ) as file:
            return file.read ()
        
    except FileNotFoundError:
        print ( f"\nError: The file {file_name} was not found." )

    except IOError:
        print (f"\nError: An IOError occurred while reading the file {file_name}." )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Save the chat log to a file.
#
# Function name:
# - save_chat_log_to_file
#
# Description:
# - This function saves the conversation history to a log file.
# - It ensures the log folder exists, determines the next available file name, and writes the conversation history to the file.
#
# Parameters:
# - application                   : dict : Dictionary containing the application's state.
# - model                         : dict : Dictionary containing the model configuration settings.
# - include_system_prompt_enabled : bool : Boolean flag to control whether we will include the system prompt or not.
#                                   Default value is False, i.e. Do not include system prompt. 
#
# Return Values:
# - None.
#
# Preconditions:
# - The application and model dictionaries must be initialized.
# - The conversation history must be set.
#
# Postconditions:
# - The conversation history is saved to a log file.
#
# To-Do:
# 1. Add error handling for file operations.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def save_chat_log_to_file ( application, model, include_system_prompt_enabled = False ):

    # Initialise local variables. 
    
    application_name           = application [ KEY_APPLICATION_NAME                    ]
    application_version        = str ( application [ KEY_APPLICATION_VERSION ] )
    chat_log_folder_path       = application [ KEY_APPLICATION_CHAT_LOG_FOLDER         ]
    chat_log_file_name         = application [ KEY_APPLICATION_CHAT_LOG_FILE_NAME      ]
    chat_log_file_extension    = application [ KEY_APPLICATION_CHAT_LOG_FILE_EXTENSION ]
    model_name                 = model       [ KEY_MODEL_NAME                          ]
    model_max_tokens           = model       [ KEY_MODEL_MAX_TOKENS                    ]
    model_temperature          = model       [ KEY_MODEL_TEMPERATURE                   ]
    model_streaming_enabled    = model       [ KEY_MODEL_STREAMING_ENABLED             ]
    model_conversation_history = model       [ KEY_MODEL_CONVERSATION_HISTORY          ]
    
    # Ensure the folder exists; if not, create it.

    if not os.path.exists ( chat_log_folder_path ):
        os.makedirs ( chat_log_folder_path )
    
    # Determine the next file number to use.

    file_index = 0

    while os.path.exists ( os.path.join ( chat_log_folder_path, f'{chat_log_file_name}{file_index}{chat_log_file_extension}' ) ):
        file_index += 1

    # Create the filename with the next index.

    file_name = os.path.join ( chat_log_folder_path, f'{chat_log_file_name}{file_index}{chat_log_file_extension}' )

    # Write the conversation history to the file.

    with open ( file_name, 'w', encoding = 'utf-8' ) as file:

        # Write chat log header information.

        file.write ( f'\nApplication:\n' )
        file.write ( f'{TERMINAL_BULLET}Name:    {application_name}\n' )
        file.write ( f'{TERMINAL_BULLET}Version: {application_version}\n' )
        file.write ( f'\nModel:\n' )
        file.write ( f'{TERMINAL_BULLET}Name:              {model_name}\n' )
        file.write ( f'{TERMINAL_BULLET}Max Tokens:        {model_max_tokens}\n' )
        file.write ( f'{TERMINAL_BULLET}Temperature:       {model_temperature}\n' )
        file.write ( f'{TERMINAL_BULLET}Streaming Enabled: {model_streaming_enabled}\n' )
        file.write ( '\n' )

        # Write chat log history to file. 
        
        row_index = 0

        for row in model_conversation_history:
            if row_index > 0:
                file.write ( f'[{row [ "role" ]}]\n{row [ "content" ]}\n\n' )
            elif row_index == 0 and include_system_prompt_enabled:
                file.write ( f'[{row [ "role" ]}]\n{row [ "content" ]}\n\n' )
            
            row_index += 1

    print ( f'\n{TERMINAL_SYSTEM}\nConversation history saved to "{file_name}."' )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main entry point of the application.
#
# Function name:
# - main
#
# Description:
# - This function serves as the main entry point of the application.
# - It initializes the application, prints application info, and starts the main loop.
#
# Parameters:
# - None.
#
# Return Values:
# - None.
#
# Preconditions:
# - None.
#
# Postconditions:
# - The application is initialized and the main loop is executed.
#
# To-Do:
# 1. Add command-line argument handling.
# 2. Enhance initialization and shutdown processes.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def main ():

     # Initialise application.

    application, model = application_initialize ()

    # Print application and mode info to the console. 

    print_application_info ( application, model )

    # Execute the main loop. 

    main_loop ( application, model )

if __name__ == "__main__":

    main ()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Function tagline. Short one-sentence or phrase description of function. e .g. Execute this or that. 
#
# Function name:
# - function_name
#
# Description:
# - bla bla bla.
# - bla bla bla.
#
# Parameters:
# - parameter_x : Description of value_x.
# - parameter_y : Description of value_y.
# - parameter_z : Description of value_z.
#
# Return Values:
# - Description of return value. Or `none` if there is no return value. 
#
# Preconditions:
# - Description of precondition 1
# - Description of precondition 2
# - Description of precondition 3
#
# Postconditions:
# - Description of postcondition 1.
# - Description of postcondition 2.
# - Description of postcondition 3.
#
# To-Do:
# 1. Improvement or enhancement 1.
# 2. Improvement or enhancement 2.
# 3. Improvement or enhancement 3.
#
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
