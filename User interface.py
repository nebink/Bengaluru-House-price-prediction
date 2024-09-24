import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import pickle
import numpy as np
import pandas as pd

# Sample lists for autocomplete
location_list = ['Whitefield', 'Koramangala', 'Indiranagar', 'HSR Layout', 'Jayanagar', 'Marathahalli', 'Hebbal']
sqft_list = ['500', '750', '1000', '1250', '1500', '1750', '2000', '2250', '2500']
bhk_list = ['1', '2', '3', '4', '5', '6']
bathroom_list = ['1', '2', '3', '4']

# Load the machine learning model
model_path = 'RidgeModel.pk1'  # Ensure this file is in the same directory as this script
with open(model_path, 'rb') as file:
    model = pickle.load(file)


# Function to predict the house price
def predict_price():
    try:
        location = location_entry.get()
        bhk = bhk_entry.get()
        bathrooms = bathroom_entry.get()
        sqft = sqft_entry.get()

        # Validate that BHK, bathrooms, and sqft are numeric
        if not (bhk.isdigit() and bathrooms.isdigit() and sqft.replace('.', '', 1).isdigit()):
            raise ValueError("BHK, Bathrooms, and Square Feet must be numeric values.")

        # Convert the inputs to proper types
        bhk = int(bhk)
        bathrooms = int(bathrooms)
        sqft = float(sqft)

        # Prepare the input DataFrame (Ensure your input format matches what the model expects)
        input_data = pd.DataFrame([[location, sqft, bhk, bathrooms]],
                                  columns=['location', 'total_sqft', 'bhk', 'bath'])

        # Predict the price using the loaded model
        prediction = model.predict(input_data)

        # Debug: Print prediction to console (for debugging purposes)
        print(f"Predicted Price: {prediction[0]}")

        # Display the result in the label
        result_label.config(text=f"Predicted House Price: ₹ {round(prediction[0], 2)}")
    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")


# Autocomplete for various entries
def autocomplete(event, entry, suggestion_list):
    typed_text = entry.get()

    # Filter the list of suggestions based on the current text in the entry
    if typed_text:
        filtered_suggestions = [s for s in suggestion_list if typed_text.lower() in s.lower()]
    else:
        filtered_suggestions = suggestion_list

    show_suggestions(filtered_suggestions, entry)


# Show suggestions in a popup
def show_suggestions(suggestions, entry):
    # Destroy any previous suggestion window if it exists
    if hasattr(window, 'suggestion_window') and window.suggestion_window.winfo_exists():
        window.suggestion_window.destroy()

    # Create a new suggestion window
    window.suggestion_window = tk.Toplevel(window)
    window.suggestion_window.geometry(f"250x150+{entry.winfo_rootx()}+{entry.winfo_rooty() + entry.winfo_height()}")
    window.suggestion_window.wm_overrideredirect(True)

    for i, suggestion in enumerate(suggestions):
        suggestion_label = ttk.Label(window.suggestion_window, text=suggestion, background="white", font=("Arial", 12),
                                     anchor="w")
        suggestion_label.pack(fill='x', padx=5, pady=2)

        # Event when clicking on the suggestion
        suggestion_label.bind("<Button-1>", lambda e, s=suggestion: select_suggestion(s, entry))


# Function to set the selected suggestion in the entry field
def select_suggestion(selected_value, entry):
    entry.delete(0, tk.END)
    entry.insert(0, selected_value)
    window.suggestion_window.destroy()


# Initialize the tkinter window
window = tk.Tk()
window.title("House Price Prediction")
window.geometry('1920x1080')  # Set window size to 700x500
window.configure(bg='#f5f5f5')

# Styling the UI elements
style = ttk.Style()
style.configure('TLabel', font=('Arial', 14), background='#f5f5f5')
style.configure('TEntry', font=('Arial', 14))
style.configure('TButton', font=('Arial', 14), padding=8)

# Create a header
header = tk.Label(window, text="Predict Your House Price", font=('Arial Bold', 20), bg='#4CAF50', fg='white', pady=10)
header.pack(fill='x')

# Frame for the form
form_frame = ttk.Frame(window, padding="20 20")
form_frame.pack(pady=20)

# Location entry with autocomplete
ttk.Label(form_frame, text="Location:").grid(row=0, column=0, pady=10, padx=20, sticky='W')
location_entry = ttk.Entry(form_frame, width=30)
location_entry.grid(row=0, column=1, pady=10, padx=20)
location_entry.bind('<KeyRelease>', lambda event: autocomplete(event, location_entry, location_list))

# Square Footage entry with autocomplete
ttk.Label(form_frame, text="Total Square Feet (sqft):").grid(row=1, column=0, pady=10, padx=20, sticky='W')
sqft_entry = ttk.Entry(form_frame, width=30)
sqft_entry.grid(row=1, column=1, pady=10, padx=20)
sqft_entry.bind('<KeyRelease>', lambda event: autocomplete(event, sqft_entry, sqft_list))

# Number of BHK entry with autocomplete
ttk.Label(form_frame, text="Number of BHK:").grid(row=2, column=0, pady=10, padx=20, sticky='W')
bhk_entry = ttk.Entry(form_frame, width=30)
bhk_entry.grid(row=2, column=1, pady=10, padx=20)
bhk_entry.bind('<KeyRelease>', lambda event: autocomplete(event, bhk_entry, bhk_list))

# Number of Bathrooms entry with autocomplete
ttk.Label(form_frame, text="Number of Bathrooms:").grid(row=3, column=0, pady=10, padx=20, sticky='W')
bathroom_entry = ttk.Entry(form_frame, width=30)
bathroom_entry.grid(row=3, column=1, pady=10, padx=20)
bathroom_entry.bind('<KeyRelease>', lambda event: autocomplete(event, bathroom_entry, bathroom_list))

# Predict Button
predict_button = ttk.Button(window, text="Predict Price", command=predict_price, style='TButton')
predict_button.pack(pady=20)

# Result Label
result_label = ttk.Label(window, text="", font=('Arial', 14, 'bold'), foreground='#333')
result_label.pack(pady=10)

# Footer
footer = tk.Label(window, text="Developed by Nebin K Raj", font=('Arial', 10), bg='#f5f5f5', fg='grey')
footer.pack(side='bottom', pady=10)

# Start the main event loop
window.mainloop()
