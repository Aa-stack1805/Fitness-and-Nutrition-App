# Tkinter Calendar Login App

A Python desktop application built with Tkinter that features a user login system, calendar utilities, and local database storage.

## Features

- User authentication with username and password
- Local data persistence using SQLite
- Calendar and date-related functionalities
- Optional API requests via `requests` module
- Clean and responsive GUI using Tkinter & ttk

## Installation

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/your-repo-name.git
   cd your-repo-name
   ```

2. Install dependencies
   Most dependencies are standard with Python. If needed:
   ```bash
   pip install requests
   ```

3. Run the application
   ```bash
   python main.py
   ```

## Requirements

- Python 3.x
- Tkinter (included with Python)
- `requests`
- `sqlite3` (standard with Python)

## Project Structure

```
├── main.py          # Main application logic
├── README.md        # Project documentation
└── database.db      # (Generated at runtime if not present)
```

## Notes

- Make sure you have internet access if the app makes external API calls.
- The SQLite database is created automatically and stored locally.

## License

This project is open source under the MIT License.
