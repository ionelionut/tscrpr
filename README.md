# Telegram Export

A Python application for exporting members and messages from various types of Telegram entities (forums, channels, and groups).

## Features

- Export the list of members from groups or channels.
- Export messages from forums, channels, or groups.
- Supports exporting messages from specific topics in forums.

## Requirements

- Python 3.8+
- Telethon

## Installation

1. Clone the repository:
   git clone <repository-URL>
   cd telegram_export

2. Create and activate a virtual environment:

    python -m venv .venv
    # On Windows
    .venv\Scripts\activate
    # On Linux/Mac
    source .venv/bin/activate

3. Install the dependencies:
    pip install -r requirements.txt

4. Configure the config.py file:
    Replace YOUR_API_ID and YOUR_API_HASH with the values obtained from my.telegram.org.


Project Structure 
telegram_export/
│
├── scrpr.py               # Main script
├── config.py              # API settings for Telegram
├── utils.py               # Utility functions, such as the logo display
├── requirements.txt       # List of required packages
├── README.md              # Project documentation
└── .gitignore             # Files and directories to ignore in Git

Contributing
Contributions are welcome! Please follow these steps to contribute:

    Fork the repository.
    Create a new branch (git checkout -b feature-name).
    Make your changes and commit them (git commit -m 'Add feature X').
    Push your changes (git push origin feature-name).
    Open a Pull Request.

License
This project is licensed under the MIT License.