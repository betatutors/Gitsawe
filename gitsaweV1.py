import tkinter as tk
from tkinter import font, PhotoImage
from tkcalendar import Calendar
import csv
import datetime
import os
from PIL import Image, ImageTk  # Import from Pillow

from ethiopian_date import EthiopianDateConverter

bg_col = "#aaeeee"
fg_col = 'black'

script_directory = os.path.dirname(os.path.abspath(__file__))
icon_dir = os.path.join(script_directory, 'iconpic.webp')


root = tk.Tk()
root.title("Gitsawe App")
root.geometry("560x500")
root.configure(bg=bg_col)
root.iconbitmap(icon_dir) 
root.resizable(False, False)

# Convert Gregorian date to Ethiopian date
ethiopian_date = EthiopianDateConverter.to_ethiopian(2024, 10, 28)

# Convert Ethiopian date back to Gregorian date
gregorian_date = EthiopianDateConverter.to_gregorian(2017, 2, 19)

custom_font = font.Font(family="Helvetica", size=12, weight="normal")
small_font = font.Font(family="Helvetica", size=10) 

# Get the directory of the current script
bible_dir = os.path.join(script_directory, 'bible1.csv')
print("Bible directory:", bible_dir)

image_path = os.path.join(script_directory, 'giorgis.png') # Update this path to your image file
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)
image_label = tk.Label(root, image=photo)
image_label.place(x=290, y=90)  # Adjust the x, y coordinates as needed

# Initial label definition for the verse 
today_verse_num_label = tk.Label(root, text="", font=('Helvetica', 14), bg=bg_col, fg=fg_col)
today_verse_num_label.place(x=120, y=400)

# Load the CSV file containing data
with open(bible_dir, newline='', encoding="utf8") as f:
    reader = csv.reader(f)
    data = list(reader)

# Function to display the selected date and quote in a new window
def display_date(event=None):
    
    bg_col_dis = "#1a1a1a"
    fg_col_dis = 'white'
    selected_date = cal.get_date()

    # Convert selected date to Ethiopian date 
    date_obj = datetime.datetime.strptime(selected_date, "%m/%d/%y") 

    try:     # Get the week number of the selected date 
        eth_date_str = convert_to_ethiopian_date(date_obj) 
        selected_date_label.config(text=f"ቀን በኢትዮጵያ: {eth_date_str}", font=custom_font)
    except ValueError as e:
        print(f"Error: {e}")

    eth_date = EthiopianDateConverter.to_ethiopian(date_obj.year, date_obj.month, date_obj.day)

    week_number = date_obj.isocalendar()[1]  # Get the ISO week number

    # Select the appropriate quote based on the week number
    quote_index = week_number - 1 if week_number <= 52 else None
    quote_geez = data[quote_index][1] if quote_index is not None else "No quote for this week."
    quote_english = data[quote_index][2] if quote_index is not None else "No quote for this week."
    geeze_verse = data[quote_index][3] if quote_index is not None else "No verse for this week." 
    english_verse= data[quote_index][4] if quote_index is not None else "No verse for this week." 

    # Update the misbak label with the selected verse
    #delete label 
    selected_date_label_verse.destroy() 
    today_verse_num_label.destroy()

    misbak_amharic_label.config(text=quote_geez)
    misbak_amharic_label.place(x=10, y=310)  # Adjust the x, y coordinates as needed
    misbak_amharic_label.configure(font=('Nyala',17),bg=bg_col, fg=fg_col)
    #Update the verse label text 

    today_verse_num_label_two.config(text=geeze_verse, font=('Nyala', 15), bg=bg_col, fg=fg_col)
    today_verse_num_label_two.place(x=120, y=400)  # Adjust the x, y coordinates as needed

    # Open a new window to display the full quote
    new_window = tk.Toplevel(root)
    new_window.title("የዛሬ ምስባክ  / Today's Gitsawe")
    new_window.configure(bg=bg_col_dis)   
    new_window.iconbitmap(icon_dir) 
    
    # Get screen size and set the new window to fill the screen
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    new_window.geometry(f"{screen_width}x{screen_height}")

    # welcome_frame = tk.Frame(root) 
    # welcome_frame.pack(pady=(10, 10))

    # Display the quote in the new window
    quote_geez= tk.Label(new_window, text=quote_geez, wraplength=screen_width - screen_width/60, font=("Nyala", 60), fg=fg_col_dis, justify="center", bg=bg_col_dis)
 
    #Display verses - it should come from CSV file 
    geeze_verses= tk.Label(new_window, text=geeze_verse, wraplength=screen_width - screen_width/60, font=("Helvetica", 30),fg=fg_col_dis, justify="left", bg=bg_col_dis)
    english_verses= tk.Label(new_window, text=english_verse, wraplength=screen_width - screen_width/60, font=("Helvetica", 30),fg=fg_col_dis, justify="left", bg=bg_col_dis)
 
    # Display English transaltion for misback
    quote_english = tk.Label(new_window,text=quote_english, wraplength=screen_width - screen_width/60, font=("Helvetica", 40), fg=fg_col_dis, justify="center", bg=bg_col_dis)

    # Place the labels at the calculated positions 
    quote_geez.pack(expand= False, pady=40) 
    geeze_verses.pack(expand=False, pady =1)
    quote_english.pack(expand=False, pady =40)
    english_verses.pack(expand=False, pady =1)

    # # Close button
    close_button = tk.Button(new_window, text="Close", command=new_window.destroy, font=("Helvetica", 14), fg=fg_col_dis, bg=bg_col_dis)
    #close_button.pack(pady=1)
    close_button.place(x= screen_width-100, y=screen_height-150)

# Get today's date
today = datetime.date.today()
    
def convert_to_ethiopian_date(gregorian_date):
    eth_date = EthiopianDateConverter.to_ethiopian(gregorian_date.year, gregorian_date.month, gregorian_date.day)
    # Unpack the tuple
    ethiopian_year, ethiopian_month, ethiopian_day = eth_date
    # Format the Ethiopian date as day/month/year
    return f"{ethiopian_day:02d}/{ethiopian_month:02d}/{ethiopian_year}"

# Create Amharic and English welcome labels
welcome_amharic_label = tk.Label(root, text="የግጻዌ መተግበሪያ / Gitsawe App",font=('Nyala', 20), fg=fg_col,bg=bg_col, justify="center")
additional_amharic_label = tk.Label(root, text="የሚፈልጉትን ቀን ይምረጡ / Select day",font=("Nyala", 17), fg=fg_col,bg=bg_col,justify = 'center')

welcome_amharic_label.place(x=152, y=0) 
additional_amharic_label.place(x=165, y = 30)

# Create the Calendar widget set to today’s date 
cal = Calendar(root, selectmode='day', year=today.year, month=today.month, day=today.day)
cal.place( x=20, y=80)

# Bind the calendar selection event to the display_date function
cal.bind("<<CalendarSelected>>", display_date)

selected_date_label = tk.Label(root, text="Select Date:" )
selected_date_label.place(x=25, y=275)  # Adjust the x, y coordinates as needed
selected_date_label.configure(font=('Helvetica',12),bg=bg_col,fg=fg_col)

today_date = datetime.date.today()

try:
    eth_date_str = convert_to_ethiopian_date(today_date)
    # eth_date_str1 = {eth_date_str[1], eth_date_str[2],eth_date_str[0] }
    selected_date_label.config(text=f"ቀን በኢትዮጵያ: {eth_date_str}", font=custom_font)
except ValueError as e:
    print(f"Error: {e}")

week_number = today_date.isocalendar()[1] 

quote_index = week_number - 1 if week_number <= 52 else None
today_verse = data[quote_index][1] if quote_index is not None else "No verse for this week."
today_verse_num = data[quote_index][3] if quote_index is not None else "No verse for this week."
today_amharic_verse= data[quote_index][4] if quote_index is not None else "No verse for this week."

selected_date_label_verse = tk.Label(root, text=today_verse)
selected_date_label_verse.place(x=10, y=315)  # Adjust the x, y coordinates as needed
selected_date_label_verse.configure(font=('Helvetica',20),bg=bg_col,fg=fg_col)

today_verse_num_label = tk.Label(root, text=today_verse_num)
today_verse_num_label.place(x=120, y=415)
today_verse_num_label.configure(font=('Helvetica',15),bg=bg_col,fg=fg_col)

# Label for misbak (Bible 1) below the calendar 
misbak_amharic_label = tk.Label(root, text="", font=small_font,fg="black", bg=bg_col,justify="center") 
misbak_amharic_label.place(x=30, y=250)
today_verse_num_label_two = tk.Label(root,text='',font=small_font,fg=fg_col,bg=bg_col )    
today_verse_num_label_two.place(x=120,y=400)

# Close button for the main window
close_main_button = tk.Button(root, text="Close", command=root.destroy, font=("Helvetica", 14), fg=fg_col,bg=bg_col)
close_main_button.place(x=485, y=450)

# Run the main loop
root.mainloop()