import tkinter as tk
from tkinter import messagebox, ttk
import datetime, sqlite3, requests, calendar

class LoginScreen:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.label = tk.Label(self.frame, text="Login", font=("Arial", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=2, pady=20)

        self.username_label = tk.Label(self.frame, text="Username:", width=7, anchor="w")
        self.username_label.grid(row=1, column=0, sticky="e", pady=10)
        self.username_entry = tk.Entry(self.frame, width=25)
        self.username_entry.grid(row=1, column=1, pady=10)

        self.password_label = tk.Label(self.frame, text="Password:", width=7, anchor="w")
        self.password_label.grid(row=2, column=0, sticky="e", pady=10)
        self.password_entry = tk.Entry(self.frame, show="*", width=25)
        self.password_entry.grid(row=2, column=1, pady=10)

        self.show_password_var = tk.BooleanVar()
        self.show_password_checkbox = tk.Checkbutton(self.frame, text="Show Password", variable=self.show_password_var, command=self.toggle_password_visibility)
        self.show_password_checkbox.grid(row=3, column=1, columnspan=2, sticky="w", pady=20)  # Use grid for placement

        self.login_button = tk.Button(self.frame, text="Login", command=self.login, width=30)
        self.login_button.grid(row=4, column=0, columnspan=2, pady=20, padx=100)

        self.frame.config(bg="#808080")
        self.label.config(bg="#808080", fg="#343a40")
        self.username_label.config(bg="#808080", fg="#343a40")
        self.password_label.config(bg="#808080", fg="#343a40")
        self.username_entry.config(bg="#ffffff", fg="#343a40")
        self.password_entry.config(bg="#ffffff", fg="#343a40")

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.config(show="")
        else:
            self.password_entry.config(show="*")

    def login(self):
        valid_username = "user"
        valid_password = "password"

        username = self.username_entry.get()
        password = self.password_entry.get()

        if not username:
            messagebox.showerror("Error", "Username cannot be empty.")
            return
        if not password:
            messagebox.showerror("Error", "Password cannot be empty.")
            return

        if username == valid_username and password == valid_password:
            if self.login_callback:
                self.login_callback(username)
        else:
            messagebox.showerror("Error", "Invalid username or password.")

    def set_login_callback(self, callback):
        self.login_callback = callback

class Workout:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.label = tk.Label(self.frame, text="Workout Tracker", font=("Roboto", 16, "bold"))

        self.current_date = datetime.date.today()
        self.date_label = tk.Label(self.frame, text=self.current_date.strftime("%Y-%m-%d"))
        self.date_label.grid(row=1, column=0, pady=5, columnspan=5, sticky="n")

        self.prev_date_button = tk.Button(self.frame, text="<", command=self.load_previous_day)
        self.next_date_button = tk.Button(self.frame, text=">", command=self.load_next_day)

        self.prev_date_button.grid(row=1, column=0, pady=(0, 5), sticky="e", padx=(5, 0))
        self.next_date_button.grid(row=1, column=4, pady=(0, 5), sticky="w", padx=(0, 5))

        self.create_treeview()

        self.add_exercise_button = ttk.Button(self.frame, text="Add Exercise", command=self.open_add_exercise_page)
        self.add_exercise_button.grid(row=3, column=0, columnspan=5, pady=10)

        self.delete_set_button = ttk.Button(self.frame, text="Delete Set", command=self.delete_selected_set)
        self.delete_set_button.grid(row=4, column=0, columnspan=5, pady=10)

        self.menu_button = tk.Button(self.frame, text="Menu", command=self.open_menu)
        self.menu_button.grid(row=5, column=0, columnspan=5, pady=10)

        self.create_database()
        self.load_exercises()

    def create_treeview(self):
        self.tree = ttk.Treeview(self.frame, columns=("Number", "Exercise Name", "Sets", "Reps", "Weight", "ID"))
        self.tree.heading("#1", text="Number", anchor=tk.W)
        self.tree.heading("#2", text="Exercise Name", anchor=tk.W)
        self.tree.heading("#3", text="Sets", anchor=tk.W)
        self.tree.heading("#4", text="Reps", anchor=tk.W)
        self.tree.heading("#5", text="Weight (lbs)", anchor=tk.W)
        self.tree.heading("#6", text="ID", anchor=tk.W)
        self.tree.grid(row=2, column=0, columnspan=5, padx=10, pady=10, sticky="nsew")

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.column("#6", width=0, stretch=tk.NO) 

    def create_database(self):
        conn = sqlite3.connect("workout.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS exercises
                          (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                           exercise_date DATE,
                           exercise_name TEXT, 
                           sets INTEGER, 
                           reps INTEGER, 
                           weight REAL,
                           date DATE)''')

        conn.commit()
        conn.close()

    def load_previous_day(self):
        self.current_date -= datetime.timedelta(days=1)
        self.update_date_label()
        self.load_exercises()

    def load_next_day(self):
        self.current_date += datetime.timedelta(days=1)
        self.update_date_label()
        self.load_exercises()

    def update_date_label(self):
        self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))

    def load_exercises(self):
        conn = sqlite3.connect("workout.db")
        cursor = conn.cursor()

        today = datetime.date.today()

        cursor.execute("SELECT id, exercise_name, sets, reps, weight FROM exercises WHERE exercise_date = ?", (today,))
        exercises = cursor.fetchall()

        for item in self.tree.get_children():
            self.tree.delete(item)

        for row in exercises:
            db_id, exercise_name, sets, reps, weight = row
            data = (db_id, exercise_name, sets, reps, weight, db_id)
            self.tree.insert("", "end", values=data)

        conn.close()

    def open_add_exercise_page(self):
        add_exercise_window = tk.Toplevel(self.parent)
        add_exercise_window.title("Add Exercise")

        add_exercise_frame = ttk.Frame(add_exercise_window)
        add_exercise_frame.grid()

        exercise_label = ttk.Label(add_exercise_frame, text="Exercise Name:")
        exercise_label.grid(row=0, column=0, padx=10, pady=5, sticky="e")
        exercise_entry = ttk.Entry(add_exercise_frame)
        exercise_entry.grid(row=0, column=1, padx=10, pady=5)

        sets_label = ttk.Label(add_exercise_frame, text="Sets:")
        sets_label.grid(row=1, column=0, padx=10, pady=5, sticky="e")
        sets_entry = ttk.Entry(add_exercise_frame)
        sets_entry.grid(row=1, column=1, padx=10, pady=5)
        sets_entry.insert(0, "1")  

        reps_label = ttk.Label(add_exercise_frame, text="Reps:")
        reps_label.grid(row=2, column=0, padx=10, pady=5, sticky="e")
        reps_entry = ttk.Entry(add_exercise_frame)
        reps_entry.grid(row=2, column=1, padx=10, pady=5)
        reps_entry.insert(0, "1")  

        weight_label = ttk.Label(add_exercise_frame, text="Weight (lbs):")
        weight_label.grid(row=3, column=0, padx=10, pady=5, sticky="e")
        weight_entry = ttk.Entry(add_exercise_frame)
        weight_entry.grid(row=3, column=1, padx=10, pady=5)

        add_button = ttk.Button(add_exercise_frame, text="Add", command=lambda: self.add_exercise(exercise_entry.get(), sets_entry.get(), reps_entry.get(), weight_entry.get(), add_exercise_window))
        add_button.grid(row=4, columnspan=2, pady=10)

    def add_exercise(self, exercise_name, sets, reps, weight, add_exercise_window):
        if not exercise_name or not sets or not reps or not weight:
            messagebox.showerror("Error", "Please enter all exercise details.")
            return

        try:
            sets = int(sets)
            reps = int(reps)
            weight = float(weight)
        except ValueError:
            messagebox.showerror("Error", "Sets, reps, and weight must be valid numbers.")
            return

        today = datetime.date.today()

        conn = sqlite3.connect("workout.db")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO exercises (exercise_date, exercise_name, sets, reps, weight) VALUES (?, ?, ?, ?, ?)''',
                       (today, exercise_name, sets, reps, weight))
        conn.commit()

        exercise_id = cursor.lastrowid

        self.tree.insert("", "end", values=(exercise_id, exercise_name, sets, reps, weight, exercise_id))

        conn.close()

        messagebox.showinfo("Success", "Exercise added successfully.")
        add_exercise_window.destroy()
        self.load_exercises()


    def delete_selected_set(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select a set to delete.")
            return
        exercise_id = self.tree.item(selected_item, "values")[0]


        conn = sqlite3.connect("workout.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM exercises WHERE id = ?", (exercise_id,))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Set deleted successfully.")
        self.load_exercises()

    def open_menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        menu_window = MenuPage(self.parent)

class Food:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.label = tk.Label(self.frame, text="Food Diary", fg="#333333", bg="#F2F2F2", font=("Helvetica", 16, "bold"))
        self.label.grid(row=0, column=0, columnspan=5, pady=(10, 5))

        self.current_date = datetime.date.today()
        self.date_label = tk.Label(self.frame, text=f"{self.current_date}", fg="#333333", bg="#F2F2F2")
        self.date_label.grid(row=1, column=0, columnspan=5, pady=(5, 0), sticky="n")

        self.prev_date_button = tk.Button(self.frame, text="<", fg="#333333", bg="#F2F2F2", activebackground="#E0E0E0", command=self.load_previous_day)
        self.next_date_button = tk.Button(self.frame, text=">", fg="#333333", bg="#F2F2F2", activebackground="#E0E0E0", command=self.load_next_day)

        self.prev_date_button.grid(row=1, column=0, pady=(0, 5), sticky="e", padx=(5, 0))
        self.next_date_button.grid(row=1, column=4, pady=(0, 5), sticky="w", padx=(0, 5))
        
        self.tree = ttk.Treeview(self.frame, columns=("ID", "Number", "Food/Exercise", "Calories", "Protein", "Carbohydrates", "Fats", "Fiber", "Sugar", "Serving Size"))
        self.tree.heading("#1", text="Number", anchor=tk.W)
        self.tree.heading("#2", text="ID", anchor=tk.W) 
        self.tree.heading("#3", text="Food/Exercise", anchor=tk.W)
        self.tree.heading("#4", text="Calories", anchor=tk.W)
        self.tree.heading("#5", text="Protein (g)", anchor=tk.W)
        self.tree.heading("#6", text="Carbohydrates (g)", anchor=tk.W)
        self.tree.heading("#7", text="Fats (g)", anchor=tk.W)
        self.tree.heading("#8", text="Fiber (g)", anchor=tk.W)
        self.tree.heading("#9", text="Sugar (g)", anchor=tk.W)
        self.tree.heading("#10", text="Serving Size (g)", anchor=tk.W)

        self.tree.grid(row=2, column=0, columnspan=5, padx=10, sticky="nsew")

        for i in range(5):
            self.frame.columnconfigure(i, weight=1)

        self.tree.column("#0", width=0, stretch=tk.NO)
        self.tree.heading("#0", text="", anchor=tk.W)
        self.tree.column("#2", width=0, stretch=tk.NO)
        self.tree.heading("#2", text="", anchor=tk.W)

        self.add_food_button = tk.Button(self.frame, text="Add Food", fg="#333333", bg="#4285F4", activebackground="#6DB3FF", command=self.open_add_food_script)
        self.add_food_button.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="w")

        self.delete_button = tk.Button(self.frame, text="Delete Entry", fg="#333333", bg="#4285F4", activebackground="#6DB3FF", command=self.delete_selected_entry)
        self.delete_button.grid(row=3, column=0, padx=10, pady=(0, 10), sticky="e")

        self.add_cardio_button = tk.Button(self.frame, text="Add Cardio Exercise", fg="#333333", bg="#4285F4", activebackground="#6DB3FF", command=self.open_add_cardio_exercise)
        self.add_cardio_button.grid(row=3, column=1, padx=10, pady=(0, 10), sticky="w")

        self.macro_frame = tk.Frame(self.frame)
        self.macro_frame.grid(row=4, column=4, rowspan=2, padx=10, sticky="n")
        self.macro_frame.configure(bg="#F2F2F2")

        self.create_macro_progress_bars() 

        self.menu_button = tk.Button(self.frame, text="Menu", fg="#333333", bg="#4285F4", activebackground="#6DB3FF", command=self.open_menu)
        self.menu_button.grid(row=3, column=2, pady=10)
        
        self.create_database()
        self.load_food_data()


    def create_database(self):
        conn = sqlite3.connect("food_diary.db")
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS foods
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        calories INTEGER,
                        protein REAL,
                        carbohydrates REAL,
                        fats REAL,
                        fiber REAL,
                        sugar REAL,
                        serving REAL,
                        date Date)''')

        conn.commit()
        conn.close()

    def load_previous_day(self):
        self.current_date -= datetime.timedelta(days=1)
        self.update_date_label()
        self.load_food_data()

    def load_next_day(self):
        self.current_date += datetime.timedelta(days=1)
        self.update_date_label()
        self.load_food_data()

    def update_date_label(self):
        self.date_label.config(text=self.current_date.strftime("%Y-%m-%d"))

    def load_food_data(self):
        conn = sqlite3.connect("food_diary.db")
        cursor = conn.cursor()

        current_date_str = self.current_date.strftime("%Y-%m-%d")

        cursor.execute('''SELECT id, name, calories, protein, carbohydrates, fats, fiber, sugar, serving
                        FROM foods
                        WHERE date = ?''', (current_date_str,))

        for item in self.tree.get_children():
            self.tree.delete(item)

        row_number = 1  
        for row in cursor.fetchall():
            item_id = row[0]  
            self.tree.insert("", "end", values=(row_number, item_id,) + row[1:] + ("Delete",), tags=("deletable",))
            row_number += 1 

        conn.close()

        self.create_macro_progress_bars()



    def fetch_daily_progress(self):
        conn = sqlite3.connect("food_diary.db")
        cursor = conn.cursor()

        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='foods' ''')
        table_exists = cursor.fetchone()

        if table_exists:
            cursor.execute('''SELECT SUM(calories), SUM(protein), SUM(carbohydrates), SUM(fats)
                            FROM foods
                            WHERE date = DATE('now')''')

            result = cursor.fetchone()
            conn.close()

            if result:
                calories, protein, carbs, fats = result
                return calories, protein, carbs, fats
            else:
                return 0, 0, 0, 0
        else:
            conn.close()
            return 0, 0, 0, 0
        
    def show(self, username):
        self.label.config(text=f"Food Diary")
        self.load_food_data()
        self.frame.pack()

    def hide(self):
        self.frame.pack_forget()

    def open_add_food_script(self):
        add_food_window = tk.Toplevel(self.parent)
    
        AddFoodApp(add_food_window, self, self.parent)

    def open_add_cardio_exercise(self):
        cardio_add_window = tk.Toplevel(self.parent)

        CardioExerciseApp(cardio_add_window, self, self.parent)

    def delete_selected_entry(self):
        selected_items = self.tree.selection()

        if not selected_items:
            messagebox.showwarning("No Selection", "Please select a food entry to delete.")
            return

        confirmation = messagebox.askyesno("Delete Food Entry", "Are you sure you want to delete the selected food entry?")

        if confirmation:
            conn = sqlite3.connect("food_diary.db")
            cursor = conn.cursor()

            for item in selected_items:
                item_values = self.tree.item(item, "values")
                if item_values:
                    item_id = item_values[1] 
                    cursor.execute("DELETE FROM foods WHERE id=?", (item_id,))
                    conn.commit()
                    self.tree.delete(item)

            conn.close()

        self.load_food_data()

    def create_macro_progress_bars(self):
        for widget in self.macro_frame.winfo_children():
            widget.destroy()

        calories, protein, carbs, fats = self.fetch_daily_progress()


        conn = sqlite3.connect('users.db')

        cursor = conn.cursor()
        cursor.execute('''SELECT BMR FROM users''')
        result = cursor.fetchone()


        cursor.execute("SELECT goal_rate FROM users")
        goal = cursor.fetchone()

        cursor.execute("SELECT COUNT(*) FROM users")
        row = cursor.fetchone()[0]

        conn.close()

        target_calories = result[-1] + 1100 * goal[-1]
        target_fats = target_calories * 0.3 / 9  
        target_protein = target_calories * 0.25 / 4
        target_carbs = target_calories * 0.45 / 4


        if fats is None:
            fats = 0

        if protein is None:
            protein = 0

        if carbs is None:
            carbs = 0

        if calories is None:
            calories = 0

        protein_percent = (protein / target_protein) * 100
        fats_percent = (fats / target_fats) * 100
        carbs_percent = (carbs / target_carbs) * 100
        calories_percent = (calories / target_calories) * 100

        fats_color = "#5733FF"
        protein_color = "#FF5733"
        carbs_color = "#33FF57"
        calories_color = "#5733FF"

        current_row = 0

        current_row = self.create_progress_bar(self.macro_frame, "Fats Progress", fats_percent, fats_color, current_row)
        current_row = self.create_progress_bar(self.macro_frame, "Protein Progress", protein_percent, protein_color, current_row)
        current_row = self.create_progress_bar(self.macro_frame, "Carbs Progress", carbs_percent, carbs_color, current_row)
        self.create_progress_bar(self.macro_frame, "Calories Progress", calories_percent, calories_color, current_row)

    def create_progress_bar(self, frame, label, percent, color, row):
        label_widget = tk.Label(frame, text=label, font=("Helvetica", 10))
        label_widget.grid(row=row, column=0, sticky=tk.W)

        canvas = tk.Canvas(frame, width=150, height=20, bg="white", highlightthickness=0)
        canvas.grid(row=row, column=1, padx=5)

        fill_width = percent * 1.5  
        canvas.create_rectangle(0, 0, fill_width, 20, fill=color, outline="")

        percentage_label = tk.Label(frame, text=f"{percent:.1f}%", font=("Helvetica", 8))
        percentage_label.grid(row=row, column=2, sticky=tk.W)

        return row + 1

    def add_percentage_label(self, frame, label_text, percent, row):
        percentage_label = tk.Label(frame, text=f"{label_text}: {percent:.1f}%", font=("Helvetica", 8))
        percentage_label.grid(row=row, column=1, padx=5)
        return row + 1  
    
    def update_user_weight(self):
        conn = sqlite3.connect("food_diary.db")
        cursor = conn.cursor()
        cursor.execute('''SELECT SUM(calories)
                        FROM foods
                        WHERE date = DATE('now')''')
        total_calories_consumed = cursor.fetchone()[0] or 0
        conn.close()

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT weight, BMR FROM users")
        user_data = cursor.fetchone()

        if user_data:
            weight, bmr = user_data
            new_weight = weight - (total_calories_consumed - bmr) / 7700 
            new_weight = round(new_weight, 1) 

            cursor.execute("UPDATE users SET weight=?", (new_weight,))
            conn.commit()
            conn.close()
    
    def open_menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        menu_window = MenuPage(self.parent)

class AddFoodApp:
    def __init__(self, root, food_diary_screen, parent=None):
        self.root = root
        self.root.title("Add Food")
        self.food_diary_screen = food_diary_screen
        self.parent = parent

        self.name_label = tk.Label(root, text="Food Name:")
        self.name_label.pack(pady=10)
        self.name_entry = tk.Entry(root)
        self.name_entry.pack(pady=5)

        self.search_button = tk.Button(root, text="Search Food", command=self.search_food_api)
        self.search_button.pack(pady=10)

        self.food_item = {
            "name": tk.StringVar(),
            "calories": tk.StringVar(),
            "protein": tk.StringVar(),
            "carbs": tk.StringVar(),
            "fats": tk.StringVar(),
            "fiber": tk.StringVar(),
            "sugar": tk.StringVar(),
            "serving": tk.StringVar()
        }

        for key, var in self.food_item.items():
            label = tk.Label(root, text=f"{key.capitalize()}:")
            label.pack()
            entry = tk.Entry(root, textvariable=var, state="readonly")
            entry.pack()

        self.add_button = tk.Button(root, text="Add Food Item", command=self.add_food_to_database)
        self.add_button.pack(pady=10)

    def search_food_api(self):
        query = self.name_entry.get()
        food_item = self.fetch_food_details(query)
        if food_item:
            self.food_item["name"].set(food_item["name"])
            self.food_item["calories"].set(food_item["calories"])
            self.food_item["protein"].set(food_item["protein_g"])
            self.food_item["carbs"].set(food_item["carbohydrates_total_g"])
            self.food_item["fats"].set(food_item["fat_total_g"])
            self.food_item["fiber"].set(food_item["fiber_g"])
            self.food_item["sugar"].set(food_item["sugar_g"])
            self.food_item["serving"].set(food_item["serving_size_g"])
        else:
            messagebox.showerror("Error", "Food item not found or API error.")

    def fetch_food_details(self, query):
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query={}'.format(query)
        headers = {'X-Api-Key': 'TXqT/L88G9ed4PgtYRn7yw==TBUGuUIZBqGMSinh'}

        response = requests.get(api_url, headers=headers)
        if response.status_code == requests.codes.ok:
            result = response.json()
            if result and len(result) > 0:
                return result[0]  
        return None

    def add_food_to_database(self):
        food_details = {key: var.get() for key, var in self.food_item.items()}

        if not food_details["name"] or "N/A" in food_details.values():
            messagebox.showerror("Error", "Please search for a valid food item first.")
            return
        
        conn = sqlite3.connect("food_diary.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO foods (name, calories, protein, carbohydrates, fats, fiber, sugar, serving, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                    (food_details["name"], food_details["calories"], food_details["protein"],
                        food_details["carbs"], food_details["fats"], food_details["fiber"], food_details["sugar"], food_details["serving"],
                        datetime.datetime.today().date()))

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Food item added to the database.")

        if self.food_diary_screen:
            self.food_diary_screen.load_food_data()
        self.root.destroy()

class CardioExerciseApp:
    def __init__(self, root, food_diary_screen, parent=None):
        self.root = root
        self.root.title("Add Cardio Exercise")
        self.food_diary_screen = food_diary_screen
        self.parent = parent

        self.exercise_label = tk.Label(root, text="Exercise Name:")
        self.exercise_label.pack(pady=10)
        self.exercise_entry = tk.Entry(root)
        self.exercise_entry.pack(pady=5)

        self.duration_label = tk.Label(root, text="Duration (minutes):")
        self.duration_label.pack()
        self.duration_entry = tk.Entry(root)
        self.duration_entry.pack()

        self.add_button = tk.Button(root, text="Add Cardio Exercise", command=self.add_cardio_exercise)
        self.add_button.pack(pady=10)

    def add_cardio_exercise(self):
        exercise_name = self.exercise_entry.get()
        duration_minutes = self.duration_entry.get()

        if not exercise_name or not duration_minutes:
            messagebox.showerror("Error", "Please enter both exercise name and duration.")
            return

        try:
            duration_minutes = int(duration_minutes)
        except ValueError:
            messagebox.showerror("Error", "Duration must be a valid integer.")
            return
        
        calories_per_hour = self.calculate_calories_per_hour(exercise_name)

        if calories_per_hour is None:
            messagebox.showerror("Error", "Cardio exercise not found.")
            return

        total_calories = (calories_per_hour * duration_minutes) / 60 

        conn = sqlite3.connect("food_diary.db")
        cursor = conn.cursor()

        cursor.execute('''INSERT INTO foods (name, calories, protein, carbohydrates, fats, fiber, sugar, serving, date)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                       (exercise_name, round(-total_calories), None, None, None, None, None, None,
                        datetime.datetime.today().date()))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Cardio exercise added to the database.")
        self.food_diary_screen.load_food_data()
        self.root.destroy() 

    def calculate_calories_per_hour(self, exercise_name):
        common_cardio_exercises = {
            "running": 472,
            "cycling": 472,
            "swimming": 590,
            "jumping rope": 700,
            "aerobics": 413,
            "walking": 314,
            "hiking": 413,
            "dancing": 314,
            "elliptical trainer": 590,
            "rowing": 472,
            "boxing": 708,
            "skiing": 413,
            "basketball": 472,
            "tennis": 472,
            "soccer": 472
        }

        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT weight FROM users WHERE date = DATE('now') ORDER BY date DESC LIMIT 1")
        user_weight = cursor.fetchone()[0]
        conn.close()


        calories_per_hour = common_cardio_exercises.get(exercise_name.lower())
        if calories_per_hour is not None:
            calories_per_hour *= user_weight / 70.0
        return calories_per_hour

class Profile:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0, sticky="nsew")

        self.sex_var = tk.StringVar(value="M")
        self.birthday_var = tk.StringVar(value="1990-01-01")
        self.height_var = tk.DoubleVar(value=170.0)
        self.weight_var = tk.DoubleVar(value=70.0)
        self.body_fat_var = tk.DoubleVar(value=20.0)
        self.bmi_var = tk.DoubleVar()
        self.bmr_var = tk.DoubleVar()
        self.goal_weight_var = tk.DoubleVar(value=65.0)
        self.goal_rate_var = tk.DoubleVar(value=0.5)
        self.goal_projection_var = tk.StringVar()

        self.title_label = tk.Label(self.frame, text="Profile")
        self.sex_label = tk.Label(self.frame, text="Sex:")
        self.sex_dropdown = ttk.Combobox(self.frame, textvariable=self.sex_var, values=["M", "F"], state="readonly")
        self.birthday_label = tk.Label(self.frame, text="Birthday:")
        self.birthday_entry = tk.Entry(self.frame, textvariable=self.birthday_var)
        self.height_label = tk.Label(self.frame, text="Height (cm):")
        self.height_entry = tk.Entry(self.frame, textvariable=self.height_var)
        self.weight_label = tk.Label(self.frame, text="Weight (kg):")
        self.weight_entry = tk.Entry(self.frame, textvariable=self.weight_var)
        self.body_fat_label = tk.Label(self.frame, text="Body Fat (%):")
        self.body_fat_entry = tk.Entry(self.frame, textvariable=self.body_fat_var)
        self.bmi_label = tk.Label(self.frame, text="BMI:")
        self.bmi_entry = tk.Entry(self.frame, textvariable=self.bmi_var, state="readonly")
        self.bmr_label = tk.Label(self.frame, text="BMR:")
        self.bmr_entry = tk.Entry(self.frame, textvariable=self.bmr_var, state="readonly")
        self.goal_weight_label = tk.Label(self.frame, text="Goal Weight (kg):")
        self.goal_weight_entry = tk.Entry(self.frame, textvariable=self.goal_weight_var)
        self.goal_rate_label = tk.Label(self.frame, text="Goal Rate (kg/week):")
        self.goal_rate_entry = tk.Entry(self.frame, textvariable=self.goal_rate_var)
        self.goal_projection_label = tk.Label(self.frame, text="Goal Projection:")
        self.goal_projection_entry = tk.Entry(self.frame, textvariable=self.goal_projection_var, state="readonly")

        self.frame.grid(column=0, row=0, padx=10, pady=10)
        self.title_label.grid(row=0, column=0, columnspan=3, pady=10)

        self.sex_label.grid(row=1, column=0, sticky="e")
        self.sex_dropdown.grid(row=1, column=1, columnspan=2, sticky="w")

        self.birthday_label.grid(row=2, column=0, sticky="e")
        self.birthday_entry.grid(row=2, column=1, columnspan=2, sticky="w")

        self.height_label.grid(row=3, column=0, sticky="e")
        self.height_entry.grid(row=3, column=1, sticky="e")

        self.weight_label.grid(row=3, column=2, sticky="e")
        self.weight_entry.grid(row=3, column=3, sticky="w")

        self.body_fat_label.grid(row=4, column=0, sticky="e")
        self.body_fat_entry.grid(row=4, column=1, sticky="w")
        self.bmi_label.grid(row=4, column=2, sticky="e")
        self.bmi_entry.grid(row=4, column=3, sticky="w")
        self.calculate_bmi_button = tk.Button(self.frame, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_bmi_button.grid(row=4, column=4)


        self.bmr_label.grid(row=5, column=0, sticky="e")
        self.bmr_entry.grid(row=5, column=1, sticky="w")
        self.calculate_bmr_button = tk.Button(self.frame, text="Calculate BMR", command=self.calculate_bmr)
        self.calculate_bmr_button.grid(row=5, column=2)
        self.goal_weight_label.grid(row=5, column=3, sticky="e")
        self.goal_weight_entry.grid(row=5, column=4, sticky="w")

        self.goal_rate_label.grid(row=6, column=0, sticky="e")
        self.goal_rate_entry.grid(row=6, column=1, sticky="w")
        self.goal_projection_label.grid(row=6, column=2, sticky="e")
        self.goal_projection_entry.grid(row=6, column=3, sticky="w")
        self.calculate_goal_projection_button = tk.Button(self.frame, text="Calculate Goal Projection", command=self.calculate_goal_projection)
        self.calculate_goal_projection_button.grid(row=6, column=4)

        self.bmi_label = tk.Label(self.frame, text="BMI:")
        self.bmi_result_label = tk.Label(self.frame, textvariable=self.bmi_var)

        self.bmr_label = tk.Label(self.frame, text="BMR (Calories/Day):")
        self.bmr_result_label = tk.Label(self.frame, textvariable=self.bmr_var)

        self.goal_projection_label = tk.Label(self.frame, text="Goal Projection (Weeks):")
        self.goal_projection_result_label = tk.Label(self.frame, textvariable=self.goal_projection_var)


        menu_button = ttk.Button(self.frame, text="Menu", command=self.open_menu)
        menu_button.grid(row=7, column=2, columnspan=2, pady=(10, 0))

        save_button = ttk.Button(self.frame, text="Save Data", command=self.save_user_data)
        save_button.grid(row=8, column=2, columnspan=2, pady=(10,0))

        self.conn = sqlite3.connect('users.db')
        self.create_user_table()

    
    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users 
                (id INTEGER PRIMARY KEY,
                sex TEXT,
                birthday TEXT,
                height REAL,
                weight REAL,
                body_fat REAL,
                goal_weight REAL,
                goal_rate REAL,
                BMI REAL,
                BMR REAL,
                date Date)''')
        
        self.conn.commit()

    def save_user_data(self):
        self.calculate_bmi()
        self.calculate_bmr()

        try:
            try:
                birthday_date = datetime.datetime.strptime(self.birthday_var.get(), "%Y-%m-%d").date()

                max_days = calendar.monthrange(birthday_date.year, birthday_date.month)[1]
                if birthday_date.day > max_days:
                    raise ValueError(f"Invalid birthday: Invalid day ({birthday_date.day}) for month {birthday_date.month}.")

                if birthday_date.month == 2 and not calendar.isleap(birthday_date.year) and birthday_date.day > 28:
                    raise ValueError("Invalid birthday: February only has 28 days in non-leap years.")

                try:
                    birthday_date = datetime.date.fromisoformat(self.birthday_var.get())
                except ValueError:
                    raise ValueError("Invalid birthday format. Please use YYYY-MM-DD.")

                if (datetime.date.today() - birthday_date).days / 365 < 13:
                    raise ValueError("Minimum age requirement is 13 years old.")
                
            except ValueError:
                raise ValueError("Invalid birthday format. Please use YYYY-MM-DD.")

            if self.height_var.get() < 100 or self.height_var.get() > 200:
                raise ValueError("Invalid height value. Please enter a value between 100 and 200 cm.")

            if self.weight_var.get() < 50 or self.weight_var.get() > 250:
                raise ValueError("Invalid weight value. Please enter a value between 50 and 250 kg.")

            if self.body_fat_var.get() < 5 or self.body_fat_var.get() > 45:
                raise ValueError("Invalid body fat value. Please enter a value between 5 and 45%.")

            if self.goal_weight_var.get() < self.weight_var.get() * 0.8 or self.goal_weight_var.get() > self.weight_var.get() * 1.2:
                raise ValueError("Goal weight should be within 20% of current weight.")

            if self.goal_rate_var.get() < -2.5 or self.goal_rate_var.get() > 2.5:
                raise ValueError("Invalid goal rate value. Please enter a value between -2.5 and 2.5.")

            if not isinstance(self.bmi_var.get(), float):
                raise ValueError("Invalid BMI value. Please ensure BMI calculation is valid.")

            if not isinstance(self.bmr_var.get(), float):
                raise ValueError("Invalid BMR value. Please ensure BMR calculation is valid.")

        except ValueError as e:
            field_name = e.args[0].split()[0].lower() 
            messagebox.showerror(f"Data Validation Error", f"Invalid value for {field_name}: {e}")
            return

        # All validations passed, proceed with saving
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO users (sex, birthday, height, weight, body_fat, goal_weight, goal_rate, BMI, BMR, date)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            self.sex_var.get(),
            self.birthday_var.get(),
            self.height_var.get(),
            self.weight_var.get(),
            self.body_fat_var.get(),
            self.goal_weight_var.get(),
            self.goal_rate_var.get(),
            self.bmi_var.get(),
            self.bmr_var.get(),
            datetime.date.today()
        ))
        self.conn.commit()
        messagebox.showinfo("Data Saved", "Your data has been saved")

    def calculate_bmi(self):
        height = self.height_var.get() / 100 
        weight = self.weight_var.get()
        bmi = weight / (height ** 2)
        self.bmi_var.set(round(bmi, 2))

    def calculate_bmr(self):
        weight = self.weight_var.get()
        height = self.height_var.get()
        sex = self.sex_var.get().lower()
        birthday = self.birthday_var.get()
        age = datetime.date.today().year - int(birthday.split("-")[0])

        if sex == "m":
            bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        elif sex == "f":
            bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
        else:
            bmr = 0 

        self.bmr_var.set(round(bmr, 2))

    def calculate_goal_projection(self):
        current_weight = self.weight_var.get()
        goal_weight = self.goal_weight_var.get()
        goal_rate = self.goal_rate_var.get()

        if goal_rate == 0:
            self.goal_projection_var.set("N/A (Rate cannot be 0)")
            return
        
        if current_weight > goal_weight and goal_rate > 0:
            self.goal_projection_var.set("Goal cannot be reached.")
        elif current_weight < goal_weight and goal_rate < 0:
            self.goal_projection_var.set("Goal cannot be reached.")
        else:
             weeks = abs((current_weight - goal_weight) / goal_rate)
             self.goal_projection_var.set(round(weeks, 2))
        

    def __del__(self):
        if hasattr(self, 'conn'):
            self.conn.close()

    def hide(self):
        self.pack_forget()

    def show(self):
        self.pack()

    def open_menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        menu_window = MenuPage(self.parent)

class MenuPage:
    def __init__(self, parent):
        self.parent = parent
        self.frame = tk.Frame(parent)

        self.parent.grid_rowconfigure(0, weight=1) 
        self.parent.grid_columnconfigure(0, weight=1)

        self.frame.grid(row=0, column=0, sticky="nsew")

        screen_width = 400
        screen_height = 270

        button_width = 40
        button_height = 10
        spacing_x = 10 
        spacing_y = 10  

        start_x = int((screen_width - button_width * 2 - spacing_x) / 2)
        start_y = int((screen_height - button_height * 2 - spacing_y) / 2)

        workout_button = tk.Button(self.frame, text="Workout Tracker", command=self.run_workout, font=("Arial", 16), width=button_width, height=button_height)
        workout_button.grid(row=0, column=0, padx=start_x, pady=start_y)

        food_button = tk.Button(self.frame, text="Food Diary", command=self.run_food, font=("Arial", 16), width=button_width, height=button_height)
        food_button.grid(row=0, column=1, padx=start_x + button_width + spacing_x, pady=start_y)

        profile_button = tk.Button(self.frame, text="Profile", command=self.run_profile, font=("Arial", 16), width=button_width, height=button_height)
        profile_button.grid(row=1, column=0, padx=start_x, pady=start_y + button_height + spacing_y)

        logout_button = tk.Button(self.frame, text="Log Out", command=self.logout, font=("Arial", 16), width=button_width, height=button_height)
        logout_button.grid(row=1, column=1, padx=start_x + button_width + spacing_x, pady=start_y + button_height + spacing_y)

        self.frame.config(bg="#ffffff")

    def hide(self):
        self.frame.pack_forget()

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def run_workout(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        workout_window = Workout(self.parent)
    
    def run_food(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        food_window = Food(self.parent)

        
    def run_profile(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        profile_window = Profile(self.parent)

    def logout(self):
        messagebox.showinfo("Logout", "You have been logged out.")
        for widget in self.frame.winfo_children():
            widget.destroy()

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Workout App")
        self.geometry("2650x1600")

        # Initialize the login screen directly
        self.login_screen = LoginScreen(self)
        self.login_frame = self.login_screen.frame
        self.login_frame.pack(fill="both", expand=True)  # Show the login frame

        # Set login callback to show the menu page
        self.login_screen.set_login_callback(self.login_success)


    def login_success(self, username):
        # Hide the login screen after successful login
        self.login_frame.destroy()

        # Show the main page
        self.main_page = MenuPage(self)

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.run()
