import os
import platform
from openai import OpenAI

# Global Constants.

APPLICATION_STATE_IDLE                         = 0
APPLICATION_STATE_RUNNING                      = 1
APPLICATION_STATE_STOPPED                      = 2
APPLICATION_COMMAND_NONE                       = 0
APPLICATION_COMMAND_EXIT                       = 1
APPLICATION_COMMAND_CLEAR_TERMINAL             = 2
APPLICATION_PROMPT_TEXT_EXIT                   = 'exit'
APPLICATION_PROMPT_TEXT_CLEAR_TERMINAL_WINDOWS = 'cls'
APPLICATION_PROMPT_TEXT_CLEAR_TERMINAL_LINUX   = 'clear'

MODEL_NAME_GPT_3_5_TURBO  = 'gpt-3.5-turbo'
MODEL_NAME_GPT_4          = 'gpt-4'
MODEL_NAME_GPT_4O         = 'gpt-4o'

# Global variables. 

application_state           = APPLICATION_STATE_IDLE
application_agent_name_user = 'User'
application_agent_name_ai   = 'AI'
application_chat_log_folder = 'chat_log'
model_name                  = MODEL_NAME_GPT_3_5_TURBO
model_max_tokens            = 1024
model_temperature           = 0.7
model_streaming_enabled     = True
model_system_prompt         = 'You are a general purpose AI assistant. You always provide well-reasoned answers that are both correct and helpful.'

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main loop. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def main_loop ():

    # Initialise local variables. 

    client               = OpenAI ( api_key = os.environ [ 'OPENAI_API_KEY' ] )
    conversation_history = [ { "role" : "system", "content" : model_system_prompt } ]
    
    # Execute main loop. 

    application_state   = APPLICATION_STATE_RUNNING
    application_command = APPLICATION_COMMAND_NONE

    while application_state == APPLICATION_STATE_RUNNING:
 
        # Get user input prompt, and check the user input for application commands. 

        user_input          = get_user_prompt ()
        application_command = get_application_command ( user_input )

        # Get response from language model. 

        if application_command == APPLICATION_COMMAND_NONE:

            # Query language model and update conversation history. 
            # 1. Append user prompt to conversation history.
            # 2. Query language model. 
            # 3. Append language model response to conversation history. 

            conversation_history.append ( { "role": "user", "content": user_input } )        
            response      = query_language_model ( client, conversation_history )
            response_text = render_language_model_response ( response )
            conversation_history.append ( { "role": "assistant", "content": response_text } )

        else:

            # Execute application command. 

            application_state, application_command = execute_application_command ( application_command )

    # Shut down program.

    save_chat_log_to_file ( conversation_history )
            

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get user prompt. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_user_prompt ():

    # Compile console prompt for the user.

    console_prompt_user = f'[{application_agent_name_user}]'

    # Get prompt text from the user and return the prompt to the caller. 

    user_prompt = input ( f'\n{console_prompt_user}\n' )

    # REturn user prompt to the caller.     

    return user_prompt

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Process application command. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_application_command ( user_prompt ):

    # Inisialize local variables. 

    command     = APPLICATION_COMMAND_NONE
    user_prompt = user_prompt.lower()       # Normalise user prompt to lower case. 

    # Identify any application commands the user intends to execute.    

    if user_prompt == APPLICATION_PROMPT_TEXT_EXIT:
        command = APPLICATION_COMMAND_EXIT

    elif user_prompt in ( APPLICATION_PROMPT_TEXT_CLEAR_TERMINAL_WINDOWS, APPLICATION_PROMPT_TEXT_CLEAR_TERMINAL_LINUX):
        command = APPLICATION_COMMAND_CLEAR_TERMINAL

    else:
        command = APPLICATION_COMMAND_NONE

    # Return selected command to the caller. 

    return command

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Execute application command. 
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
            os.system ( 'cls' )

        else:
            os.system ( 'clear' )

    else:
        application_state = APPLICATION_STATE_RUNNING

    # Return application state and reset command. 

    return application_state, APPLICATION_COMMAND_NONE

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get language model response. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def query_language_model ( client, conversation_history ):
    
    try:

        # Query the language model. 

        response = client.chat.completions.create (
            model       = model_name,
            messages    = conversation_history,
            max_tokens  = model_max_tokens,
            temperature = model_temperature,
            stream      = model_streaming_enabled
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

def render_language_model_response ( response ):

    # Initialise local variables.

    response_text     = ''                                  # Initialise to empty string. We'll populate after handing streaming or non-streaming responses.
    console_prompt_ai = f'[{application_agent_name_ai}]'    # Compile terminal prompt.

    # Print response. 

    print ( f'\n{console_prompt_ai}')

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

def print_program_info ():

    print ()
    print ( f'Language Model:' )
    print ( f'- Model:             {model_name}' )
    print ( f'- Max Tokens:        {model_max_tokens}' )
    print ( f'- Temperature:       {model_temperature}' )
    print ( f'- Streaming Enabled: {model_streaming_enabled}' )    

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Shutdown application.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def save_chat_log_to_file ( conversation_history ):

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

        for row in conversation_history:
            file.write ( f'[{row [ "role" ]}]\n{row [ "content" ]}\n\n' )

    print ( f'\nConversation history saved to "{file_name}."' )

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main program.
# - Program entry point. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def main():

    # Display program information.

    print_program_info ()

    # Execute main loop. 

    main_loop ()

if __name__ == "__main__":

    main ()
