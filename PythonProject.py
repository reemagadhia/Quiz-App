import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import cv2
from quiz_data import get_quiz_data  # Assuming the quiz_data is in a separate file

# Initialize main window
root = tk.Tk()
root.title("Quiz App")

# Get screen width and height for full-screen effect
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.geometry(f"{screen_width}x{screen_height}")

# Create a Frame for the video
video_frame = tk.Frame(root, width=screen_width, height=screen_height)
video_frame.place(x=0, y=0)

# Load and play video
cap = cv2.VideoCapture(r'C:\Users\DELL\Downloads\Python\istockphoto-1323546436-640_adpp_is.mp4')  # Replace with your video path

def play_video():
    ret, frame = cap.read()
    if ret:
        # Resize frame to fit screen
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image = image.resize((screen_width, screen_height))  # Resize to screen dimensions
        photo = ImageTk.PhotoImage(image)

        # Display video frame as background
        label_video.config(image=photo)
        label_video.image = photo  # Keep a reference to avoid garbage collection

        # Keep playing the video
        label_video.after(10, play_video)
    else:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # Restart video if it ends
        play_video()

# Create a label for the video frame
label_video = tk.Label(video_frame)
label_video.pack(fill="both", expand=True)

# Start the video
play_video()

# Welcome screen (centered over the video, no background)
welcome_label = tk.Label(root, text="Welcome to QuizApp!", font=("Helvetica", 24), fg="black", anchor="center")
welcome_label.place(relx=0.5, rely=0.4, anchor="center")  # Center the welcome message

# Function to proceed to subject selection
def proceed_to_subject_selection():
    welcome_label.place_forget()  # Hide the welcome screen text
    start_quiz_btn.place_forget()  # Hide the start quiz button
    subject_frame.place(relx=0.5, rely=0.5, anchor="center")  # Show subject selection screen in the center

# Add "Start Quiz" button (centered)
start_quiz_btn = tk.Button(root, text="Start Quiz", command=proceed_to_subject_selection, font=("Helvetica", 18), fg="black")
start_quiz_btn.place(relx=0.5, rely=0.5, anchor="center")  # Center the start quiz button

# Function to show the Continue button after subject is selected
def show_continue_button():
    # Show the Continue button after a subject is selected
    continue_btn.place(relx=0.5, rely=0.9, anchor="center")  # Position at the bottom

# Subject selection screen (centered)
subject_frame = ttk.Frame(root)
subject_label = ttk.Label(subject_frame, text="Select a Subject", anchor="center", padding=10)
subject_label.pack(pady=10)

subject_var = tk.StringVar()
subjects = ["General Knowledge", "Maths", "Science"]
for subject in subjects:
    subject_radio = ttk.Radiobutton(subject_frame, text=subject, variable=subject_var, value=subject, command=show_continue_button)
    subject_radio.pack(anchor="w", padx=20, pady=5)

# Add "Continue" button (centered) which will take the user to the quiz
def proceed_to_questions():
    continue_btn.place_forget()  # Hide the continue button after it's clicked
    start_quiz()  # Start the quiz

continue_btn = tk.Button(subject_frame, text="Continue", command=proceed_to_questions, font=("Helvetica", 18), fg="black")
continue_btn.place_forget()  # Initially hidden

# Function to start the quiz after subject selection
def start_quiz():
    global selected_quiz_data, current_question, score
    selected_subject = subject_var.get()
    if selected_subject:
        selected_quiz_data = quiz_data[selected_subject]
        current_question = 0
        score = 0
        score_label.config(text=f"Score: 0/{len(selected_quiz_data)}")
        subject_frame.place_forget()  # Hide subject selection frame
        quiz_frame.place(relx=0.5, rely=0.5, anchor="center")  # Show quiz frame
        show_question()
    else:
        messagebox.showwarning("Selection Required", "Please select a subject to start the quiz!")

# Quiz functionality (start quiz, show questions, and options, back, and next)
# Assuming the quiz_data from `quiz_data.py` is used
quiz_data = get_quiz_data()  # Load quiz data

# Function to display the question
def show_question():
    question = selected_quiz_data[current_question]
    qs_label.config(text=question["question"])
    choices = question["choices"]
    for i in range(len(choices)):
        choice_btns[i].config(text=choices[i], state="normal")
    for i in range(len(choice_btns), 4):  # Hide unused buttons
        choice_btns[i].pack_forget()
    feedback_label.config(text="")
    next_btn.config(state="disabled")  # Disable next button initially

# Function to check the answer
def check_answer(choice):
    question = selected_quiz_data[current_question]
    selected_choice = choice_btns[choice].cget("text")
    if selected_choice == question["answer"]:
        global score
        score += 1
        score_label.config(text=f"Score: {score}/{len(selected_quiz_data)}")
        feedback_label.config(text="Correct!", foreground="green")
    else:
        feedback_label.config(text="Incorrect!", foreground="red")
    for button in choice_btns:
        button.config(state="disabled")
    next_btn.config(state="normal")  # Enable next button after selecting an answer

# Function to move to the next question or end the quiz
def next_question():
    global current_question
    current_question += 1
    if current_question < len(selected_quiz_data):
        show_question()
    else:
        messagebox.showinfo("Quiz Completed!", f"Final Score: {score}/{len(selected_quiz_data)}")
        quiz_frame.place_forget()  # Hide quiz frame
        subject_frame.place(relx=0.5, rely=0.5, anchor="center")  # Show subject frame again

# Function to go back to the subject selection
def go_back_to_subject_selection():
    global current_question, score
    current_question = 0  # Reset to the first question
    score = 0  # Reset score
    score_label.config(text=f"Score: {score}/{len(selected_quiz_data)}")
    quiz_frame.place_forget()  # Hide the quiz frame
    subject_frame.place(relx=0.5, rely=0.5, anchor="center")  # Show subject selection screen

# Quiz frame
quiz_frame = ttk.Frame(root)

# Use tk.Label instead of ttk.Label to control the background color
qs_label = tk.Label(quiz_frame, anchor="center", wraplength=500, padx=10, pady=10, bg="#f0f0f0", font=("Helvetica", 18))
qs_label.pack(pady=10)

choice_btns = []
for i in range(4):
    button = ttk.Button(quiz_frame, command=lambda i=i: check_answer(i))
    button.pack(pady=5)
    choice_btns.append(button)

feedback_label = ttk.Label(quiz_frame, anchor="center", padding=10)
feedback_label.pack(pady=10)

score_label = ttk.Label(quiz_frame, text="Score: 0/0", anchor="center", padding=10)
score_label.pack(pady=10)

next_btn = ttk.Button(quiz_frame, text="Next", command=next_question, state="disabled")
next_btn.pack(pady=10)

back_btn = ttk.Button(quiz_frame, text="Back", command=go_back_to_subject_selection)
back_btn.pack(pady=10)

quiz_frame.place_forget()  # Initially hide the quiz frame

# Start main event loop
root.mainloop()
