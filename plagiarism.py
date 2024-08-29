import tkinter as tk
from tkinter import filedialog
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def choose_file1():
    file_path = filedialog.askopenfilename()
    file_button1.config(text=file_path)

def choose_file2():
    file_path = filedialog.askopenfilename()
    file_button2.config(text=file_path)

def check_plagiarism():
    global plagiarised_text
    file_path1 = file_button1.cget("text")
    file_path2 = file_button2.cget("text")

    if file_path1 == "Choose File" or file_path2 == "Choose File":
        result_label.config(text="Error!\nPlease select the files to check for plagiarism.", fg="red")
    else:
        with open(file_path1, "r") as f:
            text1 = f.read()

        with open(file_path2, "r") as f:
            text2 = f.read()

        seqMatch = SequenceMatcher(None, text1, text2)
        match = seqMatch.find_longest_match(0, len(text1), 0, len(text2))
        ratio = (match.size * 2) / (len(text1) + len(text2)) * 100

        if ratio > 1.0:
            result_label.config(text="Plagiarism detected!\nSimilarity : {:.2f}".format(ratio) + "%", fg=result_color)

            def display_plagiarised_text():
                window = tk.Toplevel(root)
                window.title("Plagiarised Text")
                window.geometry("700x600")
                window.config(bg=bg_color)

                text_label = tk.Label(window, text="PLAGIARISED TEXT", font=("SF Pro Display Black", 16), fg=text_color, bg=bg_color)
                text_label.pack(pady=10)

                matches = SequenceMatcher(None, text1, text2).get_matching_blocks()
                plagiarised_text = ''
                for match in matches:
                    if match.size > 0:
                        plagiarised_text += text1[match.a: match.a + match.size] + '\n\n'

                if plagiarised_text:
                    text_box = tk.Text(window, font=("Bahnschrift SemiBold", 12), bg="black", fg="white")
                    text_box.insert(tk.END, plagiarised_text)
                    text_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
                else:
                    no_plagiarism_label = tk.Label(window, text="No plagiarism detected!", font=("SF Pro Display Black", 14), fg=text_color, bg=bg_color)
                    no_plagiarism_label.pack(pady=50)

            display_button = tk.Button(root, text="Display Plagiarised Text", font=("JetBrains Mono", 12), bg=highlight_color, fg=button_text_color, command=display_plagiarised_text)
            display_button.pack(pady=10)

        else:
            result_label.config(text="No plagiarism detected!\nSimilarity : {:.2f}".format(ratio) + "%", fg=text_color)

        # Plot similarity percentage
        plot_similarity(ratio)

def plot_similarity(ratio):
    labels = 'Similarity', 'Difference'
    sizes = [ratio, 100 - ratio]
    colors = ['#4ADB16', '#FF4C4C']
    explode = (0.1, 0)  # explode the similarity slice

    fig, ax = plt.subplots()
    ax.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

root = tk.Tk()
root.title("Plagiarism Checker")
root.geometry("800x800")
root.resizable(True, True)

bg_color = "black"
highlight_color = "grey"
button_text_color = "black"
text_color = "#DDD1AE"
result_color = "#4ADB16"

root.config(bg=bg_color)

heading_label = tk.Label(root, text="PLAGIARISM CHECKER", font=("SF Pro Display Black", 20), fg="WHITE", pady=20, bg="#001A38")
heading_label.pack(fill=tk.X)

# Frame to hold the file labels and buttons
file_frame = tk.Frame(root, bg=bg_color)
file_frame.pack(pady=20)

# Original file label and button on separate lines with 20px spacing between columns
file_label1 = tk.Label(file_frame, text="Select original file:", font=("Cascadia Mono", 12), fg=text_color, pady=10, bg=bg_color)
file_label1.grid(row=0, column=0, padx=10, sticky="w")

file_button1 = tk.Button(file_frame, text="Choose File", font=("Cascadia Mono", 12), bg=highlight_color, fg=button_text_color, command=choose_file1)
file_button1.grid(row=1, column=0, padx=10, sticky="w")

# File to compare label and button on separate lines with 20px spacing between columns
file_label2 = tk.Label(file_frame, text="Select file to compare with:", font=("Cascadia Mono", 12), fg=text_color, pady=10, bg=bg_color)
file_label2.grid(row=0, column=1, padx=20, sticky="w")  # 20px distance between columns

file_button2 = tk.Button(file_frame, text="Choose File", font=("Cascadia Mono", 12), bg=highlight_color, fg=button_text_color, command=choose_file2)
file_button2.grid(row=1, column=1, padx=20, sticky="w")  # 20px distance between columns

check_button = tk.Button(root, text="Check for plagiarism", font=("Cascadia Mono", 12), bg=highlight_color, fg=button_text_color, command=check_plagiarism)
check_button.pack(pady=20, ipadx=10)

result_label = tk.Label(root, text="", font=("JetBrains Mono ExtraBold", 16), fg=text_color, bg=bg_color)
result_label.pack(pady=20)

footer_label = tk.Label(root, text="Plagiarism detection using python gui", font=("SF Pro Display", 12), fg="WHITE", pady=5, bg="#2F5061")
footer_label.pack(fill=tk.X, side=tk.BOTTOM)

root.mainloop()
