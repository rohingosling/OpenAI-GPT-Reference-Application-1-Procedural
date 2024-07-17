# OpenAI GPT Chatbot Reference Application
**Version:** 1.0 (Procedural version)

General purpose OpenAI GPT API reference application, demonstrating the basic layout and features of a LLM based chatgpt with conversation history, user commands, and saving to chat log file.

## Table of Contents
3. [Features](#features)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Features](#features)
5. [Contributing](#contributing)
6. [License](#license)
7. [Contact Information](#contact-information)
8. [Acknowledgements](#acknowledgements)

## Features
- Terminal hosted tern-based chatbot. 
- Conversation history maintained during conversation. 
- System prompt loaded from text file. 
- Chat log saved to text file.

## Usage

Run the program with `python main.py`, or using the `run.bat` batch file. 

```cmd.exe
X:\Projects\common_python\application\chatbot\v1>venv_activate

X:\Projects\common_python\application\chatbot\v1>venv\scripts\activate

(venv) X:\Projects\common_python\application\chatbot\v1>python main.py

Application:
- Name:    Conversation Agent Reference Application
- Version: 2.0

Model:
- Name:              gpt-3.5-turbo
- Max Tokens:        1024
- Temperature:       0.7
- Streaming Enabled: True

[User]
Hello, how are you doing?

[AI]
Hello! I'm here and ready to assist you. How can I help you today?

[User]
What is 1 + 1?

[AI]
1 + 1 equals 2. If you have any more math questions or need further assistance, feel free to ask!

[User]
List the UAE Emirates.

[AI]
The United Arab Emirates (UAE) consists of seven emirates. Here is a list of the seven emirates:
1. Abu Dhabi
2. Dubai
3. Sharjah
4. Ajman
5. Umm Al-Quwain
6. Ras Al Khaimah
7. Fujairah

If you have any more questions about the UAE or anything else, feel free to ask!

[User]
exit

[SYSTEM]
Conversation history saved to "chat_log\chat_log_8.txt."

(venv) X:\Projects\common_python\application\chatbot\v1>
```

## Installation

### Prerequisites

- Python 3.x
- OpenAI API
  
  - `pip install --upgrade openai`
  
    or

  - `pip install openai`

    or
    
  - use the `venv_install_requirements.bat` batch file, which will `pip install` the dependencies from the `venv_requirements.txt` file. 

### Clone repository

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/your-repo.git
    ```

2. Navigate to the project directory:
    ```sh
    cd your-repo
    ```

### Python Virtual Environment Setup

3. Create and activate the virtual environment using the provided batch files:

   If you are using Windows, for the sake of convenience, a set of `venv_*.bat` batch files is provided to create, manage and maintain the Python virtual environment.

    - To create the virtual environment and activate it, run:
      ```sh
      venv_create.bat
      ```
    - If you need to activate the virtual environment later, run:
      ```sh
      venv_activate.bat
      ```
    - To deactivate the virtual environment, run:
      ```sh
      venv_deactivate.bat
      ```
    - To delete the virtual environment, run:
      ```sh
      venv_delete.bat
      ```

4. Install the required packages:
    ```sh
    venv_install_requirements.bat
    ```

5. To save the current list of installed packages to `venv_requirements.txt`, run:
    ```sh
    venv_save_requirements.bat
    ```
## Contributing
Contributions are welcome! Please follow the contribution guidelines.
1. Fork the project.
2. Create your feature branch (git checkout -b feature/AmazingFeature).
3. Commit your changes (git commit -m 'Add some AmazingFeature').
4. Push to the branch (git push origin feature/AmazingFeature).
5. Open a pull request.

## License
Distributed under the MIT License. See LICENSE for more information.

## Contact Information
- Twitter: [@rohingosling](https://x.com/rohingosling)
- Project Link: [https://github.com/rohingosling/OpenAI-GPT-Reference-Application-1-Procedural](https://github.com/rohingosling/OpenAI-GPT-Reference-Application-1-Procedural)

## Acknowledgments
- [OpenAI Platform](https://platform.openai.com/docs/overview)
