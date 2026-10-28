# Expense Tracker

A beginner-friendly Python command-line application for recording expenses and summarising spending.

## Features

- Add expenses with an amount, date, category, and description
- View saved expenses, ordered by date
- Calculate total spending
- Calculate spending by category
- Save expenses locally using JSON
- Validate user input and handle invalid saved data

## Built With

- Python 3
- Python standard library
- JSON file storage

No additional Python packages are required.

## How to Run

1. Install Python 3.
2. Download or clone this repository.
3. Open the project folder in VS Code.
4. Open a terminal in the project folder.
5. Run:

   ```bash
   python3 main.py
   ```

6. Follow the menu instructions.

## Data Storage

The application saves expenses in a local file named `expenses.json`. This file is created automatically when the first expense is saved.

Expense data is stored locally on your computer. Do not use this application to store sensitive financial information.

## Testing

The initial version has been manually tested for adding an expense and calculating its spending total.

Additional checks should include invalid input, category totals, restarting the application, and handling invalid JSON data.

## Current Limitations

- Command-line interface only
- No editing or deleting of expenses
- No charts or monthly reports
- Data is stored locally

## Future Improvements

- Export expenses to CSV
- Add monthly summaries
- Add automated tests
- Create a graphical interface

## Project Status

Initial version: expense recording and spending summaries.