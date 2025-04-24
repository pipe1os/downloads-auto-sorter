# Windows Downloads Folder Sorter

This project contains a Python script that automatically sorts files in your Windows Downloads folder into subfolders based on their file type.

## How it Works

The script runs in the background. Every 30 minutes, it checks your Downloads folder. It looks at each file's extension (like `.pdf`, `.jpg`, `.zip`) and moves the file into a corresponding subfolder (like `Documents`, `Images`, `Archives`) inside your Downloads folder. Any files it doesn't recognize go into an `Other` folder. It logs what it does to a file called `sorter_log.txt`.

## Prerequisites

- Python 3 installed.
- PyInstaller (`pip install pyinstaller`).

## Setup & Compilation

1.  **Get the Code:** Make sure you have the `download_sorter.pyw` file.
2.  **Open Command Prompt:** Search for `cmd` in the Start Menu.
3.  **Install PyInstaller:** If you don't have it, run:
    ```bash
    pip install pyinstaller
    ```
4.  **Go to Code Folder:** Navigate to where you saved the script.
    ```bash
    cd C:\Route\To\download_sorter.pyw\
    ```
5.  **Compile to .exe:** Run the PyInstaller command:
    ```bash
    pyinstaller --onefile --windowed download_sorter.pyw
    ```
    This creates a single executable file without a console window.
6.  **Find the .exe:** The compiled file `download_sorter.exe` will be in the `dist` folder inside your project directory.

## Running Automatically (Task Scheduler)

Use Windows Task Scheduler to run the compiled `.exe` automatically when you log in.

1.  **Open Task Scheduler:** Search for it in the Start Menu.
2.  **Create Basic Task...** (in the right-hand Actions pane).
3.  **Name:** `Download Folder Sorter`
4.  **Trigger:** `When I log on`.
5.  **Action:** `Start a program`.
6.  **Start a Program:**
    - **Program/script:** Enter the full path to your compiled `.exe`
    - **Add arguments:** Leave empty.
    - **Start in:** Enter the directory containing the `.exe`
7.  **Finish:** Check `Open the Properties dialog...` and click Finish.
8.  **Properties (General Tab):** Check `Run whether user is logged on or not` (or `Run only when user is logged on`) and `Hidden`. Click OK.

The sorter will now start automatically when you log in and run silently in the background.

## Log File

The script writes status and error messages to `sorter_log.txt`. This file is located in the same directory as the `download_sorter.exe` file (e.g., `C:\Users\Pipe\Documents\autosortdownloads\dist\sorter_log.txt`). Check this file if you need to see what the script is doing or troubleshoot issues.
