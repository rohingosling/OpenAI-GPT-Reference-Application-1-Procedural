
import os
from datetime import datetime
from openai   import OpenAI

# Constants.

CONSOLE_PROMPT_USER      = '[User]'
CONSOLE_PROMPT_AI        = '[AI]'
COMMAND_NONE             = 0
COMMAND_RUN              = 1
COMMAND_EXIT_APPLICATION = 2
PROGRAM_CHAT_LOG_FOLDER  = 'chat_log'
LM_MODEL_GPT_3_5_TURBO   = 'gpt-3.5-turbo'
LM_MODEL_GPT_4           = 'gpt-4'
LM_MODEL_GPT_4o          = 'gpt-4o'
LM_MODEL                 = LM_MODEL_GPT_3_5_TURBO
LM_MAX_TOKENS            = 1024
LM_TEMPERATURE           = 0.7
LM_STREAMING_ENABLED     = True
LM_SYSTEM_PROMPT         = f'You are an intelligent assistant. You always provide well-reasoned answers that are both correct and helpful.'

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Main loop. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def main_loop ():

    # Initialise local variables. 

    client               = OpenAI ( api_key = os.environ [ 'OPENAI_API_KEY' ] )
    conversation_history = [ { "role": "system", "content": LM_SYSTEM_PROMPT } ]
    command              = COMMAND_RUN

    # Execute main loop. 

    while command == COMMAND_RUN:

        # Get user input prompt, and check the user inpur for application commands. 

        user_input = get_user_prompt         ()
        command    = get_application_command ( user_input )

        # Process user input prompt. 

        if command == COMMAND_RUN:

            # Update conversation history, and send prompt to langauge model.

            conversation_history.append ( { "role": "user", "content": user_input } )        
            response = get_language_model_response ( client, conversation_history, LM_STREAMING_ENABLED )

            # Update conversation history, and process language model response. 
            
            response = process_language_model_response ( response )
            conversation_history.append ( { "role": "assistant", "content": response } )

    # Shut down program.

    save_chat_log_to_file ( conversation_history )
            

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get user prompt. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_user_prompt ():

    user_input = input ( f"{CONSOLE_PROMPT_USER}\n" )

    return user_input

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Process application command. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_application_command ( user_input ):

    if user_input.lower() == "exit":
        command = COMMAND_EXIT_APPLICATION
    else:
        command = COMMAND_RUN

    return command    

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get language model response. 
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def get_language_model_response ( client, conversation_history, streaming_enabled = False ):
    
    try:
        response = client.chat.completions.create (
            model       = LM_MODEL,
            messages    = conversation_history,
            max_tokens  = LM_MAX_TOKENS,
            temperature = LM_TEMPERATURE,
            stream      = LM_STREAMING_ENABLED
        )

        if LM_STREAMING_ENABLED:
            return response
        else:
            return response.choices [ 0 ].message.content
    
    except Exception as e:

        return f"An error occurred: {str(e)}"

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Process language model response.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def process_language_model_response ( response ):

    print ( f"\n{CONSOLE_PROMPT_AI}" )

    if LM_STREAMING_ENABLED:

        response_stream = { "role": "assistant", "content": "" }
    
        for chunk in response:
            if chunk.choices [ 0 ].delta.content:
                print ( chunk.choices [ 0 ].delta.content, end="", flush = True )
                response_stream [ "content" ] += chunk.choices [ 0 ].delta.content

        print ( "\n" )
        return response_stream [ "content" ]
    else:

        print ( f"{response}\n" )
        return response

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Display program info.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def print_program_info ():

    print ()
    print ( f'Language Model:' )
    print ( f'- Model:             {LM_MODEL}' )
    print ( f'- Max Tokens:        {LM_MAX_TOKENS}' )
    print ( f'- Temperature:       {LM_TEMPERATURE}' )
    print ( f'- Streaming Enabled: {LM_STREAMING_ENABLED}' )
    print ()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# Shutdown application.
#-------------------------------------------------------------------------------------------------------------------------------------------------------------

def save_chat_log_to_file ( conversation_history ):

    folder_path = PROGRAM_CHAT_LOG_FOLDER
    
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

    with open ( file_name, 'w' ) as file:

        file.write ( f'Model:             {LM_MODEL}\n' )
        file.write ( f'Max Tokens:        {LM_MAX_TOKENS}\n' )
        file.write ( f'Temperature:       {LM_TEMPERATURE}\n' )
        file.write ( f'Streaming Enabled: {LM_STREAMING_ENABLED}\n' )
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