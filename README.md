# Fitness Tracker App

A comprehensive fitness and nutrition tracking application built with Python and Tkinter.

## Features

### Login System
- Secure user authentication
- Password visibility toggle

### Workout Tracker
- Log and monitor your exercises, sets, reps, and weights
- Calendar view to track your workout history
- Easy addition and removal of exercises
- Daily workout summary

### Food Diary
- Track your daily food intake with nutritional information
- Real-time calorie and macronutrient tracking
- Visual progress bars for daily nutrition goals
- Integration with nutrition API for accurate food data
- Track cardio exercises and calculate calories burned

### Profile Management
- Personal information storage (height, weight, age, sex)
- BMI (Body Mass Index) calculator
- BMR (Basal Metabolic Rate) calculator
- Weight goal setting and progress projection
- Data validation for accurate information

## Installation

### Prerequisites
- Python 3.6+
- Tkinter
- SQLite3
- Requests library

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/fitness-tracker-app.git
cd fitness-tracker-app
```

### Step 2: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run the application
```bash
python main.py
```

## Usage Guide

### Login
- Default credentials: 
  - Username: `user`
  - Password: `password`

### Workout Tracking
1. Click on "Workout Tracker" from the main menu
2. Use the date navigation buttons to select a date
3. Click "Add Exercise" to log a new workout
4. Fill in the exercise details (name, sets, reps, weight)
5. View your workout history in the main tracker screen
6. Use "Delete Set" to remove exercises if needed

### Food Tracking
1. Click on "Food Diary" from the main menu
2. Navigate to your desired date using the date controls
3. Click "Add Food" to search for and add food items
   - Enter the food name and click "Search Food"
   - Review the nutritional information
   - Click "Add Food Item" to add it to your daily log
4. Click "Add Cardio Exercise" to log cardio workouts and calculate calories burned
5. Monitor your daily nutrition progress with the macro progress bars
6. Use "Delete Entry" to remove food entries if needed

### Profile Management
1. Click on "Profile" from the main menu
2. Enter your personal information:
   - Sex
   - Birthday (YYYY-MM-DD format)
   - Height (cm)
   - Weight (kg)
   - Body Fat percentage
3. Use the calculation buttons to determine your:
   - BMI (Body Mass Index)
   - BMR (Basal Metabolic Rate)
   - Goal Projection (based on your current and goal weights)
4. Click "Save Data" to store your information
5. Return to the menu by clicking "Menu"

## Technical Details

### Database Structure
The application uses SQLite databases to store user information:
- `workout.db`: Stores workout exercises and history
- `food_diary.db`: Stores food entries and nutritional information
- `users.db`: Stores user profile data and metrics

### API Integration
The food diary uses the API Ninjas Nutrition API to fetch accurate food nutritional information. An API key is required for this functionality.

### Dependencies
- `tkinter`: GUI framework
- `sqlite3`: Local database management
- `requests`: API communication
- `datetime`: Date and time handling
- `calendar`: Calendar utilities

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- API Ninjas for the nutrition data API
- Tkinter documentation and community
- Python SQLite documentation
