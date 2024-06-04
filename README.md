# OpenAI GPT API reference program

## Overview

- Simple turn-based chatbot with context history.
- Saves chat logs to file.
- Procedural programming.

## Add OpenAI API Key environment variable in Windows

1. **Copy the OpenAI API Key:**
   - Ensure you have your OpenAI API key copied to your clipboard. You'll need this key for the following steps.

2. **Open the Start Menu:**
   - Click on the **Start** button (Windows icon) on the bottom left corner of your screen or press the **Windows key** on your keyboard.

3. **Open Settings:**
   - In the Start menu, click on **Settings** (the gear icon).

4. **Navigate to System Settings:**
   - In the Settings window, click on **System**.

5. **Open Advanced System Settings:**
   - Scroll down and select **About** from the left sidebar.
   - On the right side, under "Related settings," click on **Advanced system settings**. This will open the System Properties window.

6. **Open Environment Variables:**
   - In the System Properties window, click on the **Environment Variables...** button near the bottom right corner.

7. **Create a New Environment Variable:**
   - In the Environment Variables window, you will see two sections: "User variables" and "System variables."
   - Click the **New...** button under the "User variables" section if you want to set it for your user only, or under the "System variables" section if you want it to be available system-wide.

8. **Set the Variable Name and Value:**
   - In the New User Variable or New System Variable window that pops up, enter `OPEN_API_KEY` in the **Variable name** field.
   - In the **Variable value** field, paste your OpenAI API key.

9. **Save the Environment Variable:**
   - Click **OK** to close the New User Variable or New System Variable window.
   - Click **OK** again to close the Environment Variables window.
   - Click **OK** once more to close the System Properties window.

10. **Verify the Environment Variable:**
    - Open a new Command Prompt or PowerShell window to verify that the environment variable has been set correctly.
    - Type `echo %OPEN_API_KEY%` in Command Prompt or `echo $env:OPEN_API_KEY` in PowerShell and press Enter. This should display your OpenAI API key.
