#!/usr/bin/python3
"""
Title: Easy-GC

Date: 15.03.2021

Author: Mara Vizitiu

Description: Application that opens as a GUI where the user can choose to plot the GC-content across a nucleotide sequence, or graphically compare the GC-contents across two separate nucleotide sequences. The window and step sizes are chosen by the user. The resulting figure can be saved locally.

Procedure:  1. Define functions that are independent of the mode the            application is used in (one sequence vs two sequences).
            2. Define functions to be used in "one sequence" mode.
            3. Define functions to be used in "two sequences" mode.
            4. Generate the widgets to be used for creating the GUI and assign the corresponding functions to each widget.
"""
#MODULES##################################################################

import tkinter as tk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pandas import DataFrame
import re

#FUNCTIONS_INDEPENDENT_OF_MODE############################################

#Function that clears all fields --> Clear all button
def clear_all():
    frm_plot.grid_forget() #Remove plot frame to allow window to shrink to original size
    txt_sequence1.delete("1.0", tk.END) #Clear sequence input fields
    txt_sequence2.delete("1.0", tk.END)
    ent_window.delete(0, tk.END) #Clear window field
    ent_step.delete(0, tk.END) #Clear step field

#Function that only allows integers to be input --> Window and step
def keyPress(event):
    if event.char in ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"):
        pass #Allow numeric characters
    elif event.keysym not in ('BackSpace', 'Delete'):
        return 'break' #Allow the use of Backspace and Delete keys

#Function that calculates the GC-content of a sequence ("reading frame")
def calc_GC_content(seq):
    seq_length = len(seq)
    total_GC = seq.count("G") + seq.count("C")
    GC_content = (total_GC*100)/seq_length
    return(GC_content)

#FUNCTIONS_FOR_ONE_SEQUENCE###############################################

#Function that takes the input sequence from the text box
def process_sequence(txt_sequence):
    sequence = txt_sequence.get("1.0", tk.END)
    sequence = re.sub("\s+", "", sequence) #Delete and spaces
    sequence = sequence.upper() #Account for lowercase sequences
    return(sequence)

#Function that retieves the name of the input file --> Browse button
def open_file():
    filename = tk.filedialog.askopenfilename() #Browse files stored locally
    return(filename)

#Function that takes the sequence from the input file and pastes it into the text field
def seq_from_file():
    input_file = open_file() #Store the name of the file to be parsed
    file_in = open(input_file, "r")
    for line in file_in:
        if not line.startswith(">"): #Sequence line
            txt_sequence1.insert(tk.END, line.rstrip()) #Insert in sequence field
    file_in.close()

#Function that creates a data frame from the x and y axes lists
def create_dataframe():
    sequence = process_sequence(txt_sequence1) #Nucleotide sequence from text field
    window = int(ent_window.get()) #Window size
    step = int(ent_step.get()) #Step size
    position = 0 #First position of sequence
    x = [0] #List of x-axis positions
    y = [] #List of GC-contents
    while position+step <= (len(sequence)-1):
        x.append(position+step) #Store positions where GC-content is calculated
        position = position+step
    x_axis = [i+1 for i in x] #First position is 1, sequence index is 0
    for pos1 in x:
        pos2 = pos1 + window #"Reading frame" start and end
        reading_frame = sequence[pos1:pos2] #"Reading frame"
        GC_content = calc_GC_content(reading_frame)
        y.append(GC_content) #Store GC-content for the frame
    df = DataFrame(list(zip(x_axis, y)), columns=["Position", "GC(%)"]) #Create data frame
    if pos2 > len(sequence): #When the last "frame" is incomplete
        warning_text = "Warning: Final reading frame is shorter than the window size."
        lbl_warning = tk.Label(master=frm_plot,
                       text=warning_text,
                       fg="red") #Display warning message above plot
        lbl_warning.pack()
    return(df)

#Function that creates the plot
def create_plot():
    for widget in frm_plot.winfo_children():
       widget.destroy() #Remove any previous plot
    fig = plt.Figure() #Create plot figure
    ax = fig.add_subplot(111) #Create plot axis
    dataframe = create_dataframe()[["Position", "GC(%)"]].groupby("Position").sum() #Data frame to be plotted
    ax.plot(dataframe)
    ax.set_ylim([-1,101])
    ax.set_xlabel("Position")
    ax.set_ylabel("GC-content (%)")
    frm_plot.grid(row=1, column=3, sticky="w") #Load frame that contains plot
    canvas = FigureCanvasTkAgg(fig, master=frm_plot) #Widget
    canvas.draw()
    canvas.get_tk_widget().pack()
    result = tk.messagebox.askyesno("Save plot", "A figure has been generated. \nWould you like to save the plot?") #New window that allows for saving the plot
    if result== True: #If user chooses to save the plot
        file = tk.filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*"),("Portable Document Format", "*.pdf"),("JPEG Image", "*.jpg")), defaultextension='.png') #Open window that allows for choosing the location, name, and format
        fig.savefig(file)

#FUNCTIONS_FOR_TWO_SEQUENCES##############################################

#Function that packs the second text box and hides Browse button
def handle_multiple(): #When two-sequences mode is chosen
    if CheckVar.get(): #Variable of the checkmark widget
        lbl_sequence2.pack() #Sequence 2 label
        txt_sequence2.pack() #Sequence 2 text field
        btn_browse.pack_forget() #Remove Browse button
        btn_plot.pack_forget() #Switch plotting button to one fit for two sequences
        btn_plot_mult.pack()
    else: #When checkmark is unckecked (one sequence mode)
        lbl_sequence2.pack_forget() #Remove sequence 2 label
        txt_sequence2.pack_forget() #Remove sequence 2 text field
        btn_browse.pack() #Add Browse button
        btn_plot_mult.pack_forget() #Change plotting button to handle one sequence
        btn_plot.pack()

#Function that trims the longer sequence
def trim_seq(sequence1, sequence2):
    if len(sequence1) > len(sequence2): #Sequence 1 is longer
        sequence1 = sequence1[0:len(sequence2)] #Trim to length of shorter sequence
        txt_sequence1.delete("1.0", tk.END) #Delete current sequence
        txt_sequence1.insert(tk.END, sequence1) #Replace with shortened sequence
    elif len(sequence2) > len(sequence1): #Sequence 2 is longer
        sequence2 = sequence2[0:len(sequence1)]
        txt_sequence2.delete("1.0", tk.END)
        txt_sequence2.insert(tk.END, sequence2)

#Function that creates a dataframe for the two sequences
def create_dataframe_multiple():
    sequence1 = process_sequence(txt_sequence1)
    sequence2 = process_sequence(txt_sequence2)
    if len(sequence1) != len(sequence2): #When one sequence is longer
        trim_seq(sequence1, sequence2) #Trim it to the length of the shorter one
        warning_text = "Warning: The sequences did not have the same length. The longer one has been trimmed automatically. To continue, click 'Generate plot' again" #Warn the user about trimming the sequence
        frm_plot.grid(row=1, column=3, sticky="w") #Load frame that contains the plot and the warning message
        lbl_warning = tk.Label(master=frm_plot,
                       text=warning_text,
                       fg="red",
                       wraplength=400)
        lbl_warning.pack()
        return 'break' #Stop running the function
    window = int(ent_window.get())
    step = int(ent_step.get())
    position = 0 #First position of the sequences
    x = [0] #List of positions
    y1 = [] #List of sequence1 GC-contents
    y2 = [] #List of sequence2 GC-contents
    while position+step <= (len(sequence1)-1):
        x.append(position+step) #Store positions where GC-content is calculated
        position = position+step
    x_axis = [i+1 for i in x] #First position is 1, sequence index is 0
    for pos1 in x:
        pos2 = pos1 + window
        reading_frame1 = sequence1[pos1:pos2] #GC-contents for sequence1
        GC_content1 = calc_GC_content(reading_frame1)
        y1.append(GC_content1)
        reading_frame2 = sequence2[pos1:pos2] #GC-contents of sequence2
        GC_content2 = calc_GC_content(reading_frame2)
        y2.append(GC_content2)
    df = DataFrame(list(zip(x_axis, y1, y2)), columns=["Position", "Sequence_1", "Sequence_2"]) #Create dataframe of the positions and the corresponding GC-contents in both sequences
    if pos2 > len(sequence1): #When the last "frame" is incomplete
        warning_text = "Warning: Final reading frame is shorter than the window size."
        lbl_warning = tk.Label(master=frm_plot,
                       text=warning_text,
                       fg="red") #Display warning message above plot
        lbl_warning.pack()
    return(df)

#Function that plots two sequences
def create_plot_multiple():
    for widget in frm_plot.winfo_children():
       widget.destroy() #Remove any previous plot
    fig = plt.Figure() #Plot figure
    ax = fig.add_subplot(111) #Plot axis
    dataframe = create_dataframe_multiple() #Dataframe to be plotted
    dataframe.plot(kind="line", ax=ax, x="Position", y="Sequence_1") #Plot sequence1
    dataframe.plot(kind="line", ax=ax, x="Position", y="Sequence_2") #Plot sequence2
    ax.set_ylim([-1,101])
    ax.set_xlabel("Position")
    ax.set_ylabel("GC-content (%)")
    frm_plot.grid(row=1, column=3, sticky="w") #Load frame that contains plot
    canvas = FigureCanvasTkAgg(fig, master=frm_plot) #Widget
    canvas.draw()
    canvas.get_tk_widget().pack()
    result = tk.messagebox.askyesno("Save plot", "A figure has been generated. \nWould you like to save the plot?") #New window that allows for saving the plot
    if result== True:
        file = tk.filedialog.asksaveasfilename(filetypes=(("PNG Image", "*.png"),("All Files", "*.*"),("Portable Document Format", "*.pdf"),("JPEG Image", "*.jpg")), defaultextension='.png') #Open window that allows for choosing the location, name, and format
        fig.savefig(file)


#GUI######################################################################

application = tk.Tk() #Main window
application.title("Easy-GC") #Set window name
for i in range(0,2): #Allow for resizing of widgets when window is resized
    application.rowconfigure(i, weight=1, minsize=5)
    application.columnconfigure(i, weight=1, minsize=5)

#Frames
frm_intro = tk.Frame() #Row 0
frm_sequence = tk.Frame() #Row 1, Column 0
frm_browse = tk.Frame() #Row1, Column 1
frm_plot = tk.Frame() #Row 1, Column 2
frm_window = tk.Frame() #Row 2, Column 0
frm_button = tk.Frame() #Row 2, Column 1

#frm_intro
lbl_intro = tk.Label(master=frm_intro,
                     text="This program can plot the GC-content across a nucleotide sequence. Either select a file by clicking 'Browse...' or type your sequence below.\nTo compare two nucleotide sequences, tick the box below and type in your two sequences.",
                     wraplength=700,
                     justify="left",
                     font="8")

CheckVar = tk.IntVar()
chk_1 = tk.Checkbutton(master=frm_intro,
                       text="Compare two sequences",
                       command=handle_multiple,
                       variable=CheckVar)

#frm_sequence
lbl_sequence1 = tk.Label(master=frm_sequence,
                        text="Input nucleotide sequence here:")

txt_sequence1 = tk.Text(master=frm_sequence,
                        bg="#E1F2DA",
                        height=10)

lbl_sequence2 = tk.Label(master=frm_sequence,
                         text="Input second nucleotide sequence here:")

txt_sequence2 = tk.Text(master=frm_sequence,
                        bg="#DAF0F2",
                        height=10)

#frm_browse
btn_browse = tk.Button(master=frm_browse,
                         text="Browse...",
                         command=seq_from_file)

#frm_window
lbl_window = tk.Label(master=frm_window,
                      text="Window size:",
                      justify="left")

ent_window = tk.Entry(master=frm_window,
                      bg="#E1F2DA",
                      width=5)
ent_window.bind('<KeyPress>', keyPress)

lbl_step = tk.Label(master=frm_window,
                    text="Step size:",
                    justify="left")

ent_step = tk.Entry(master=frm_window,
                    bg="#E1F2DA",
                    width=5)
ent_step.bind('<KeyPress>', keyPress)

#frm_button
btn_plot = tk.Button(master=frm_button, 
                     text="Generate plot",
                     command=create_plot)

btn_plot_mult = tk.Button(master=frm_button,
                          text="Generate plot",
                          command=create_plot_multiple)

btn_clearall = tk.Button(master=frm_button,
                         text="Clear all",
                         command=clear_all)

#Load various GUI components
frm_intro.grid(row=0, column=0, columnspan=3, sticky="nw")
lbl_intro.pack()
chk_1.pack(side=tk.LEFT)

frm_sequence.grid(row=1, column=0, columnspan=3, sticky="nw", padx=5, pady=5)
lbl_sequence1.pack()
txt_sequence1.pack(fill=tk.BOTH)

frm_browse.grid(row=2, column=1)
btn_browse.pack()

frm_window.grid(row=2, column=0, sticky="w", pady=5)
lbl_window.pack()
ent_window.pack()
lbl_step.pack()
ent_step.pack()

frm_button.grid(row=2, column=2, sticky="w", padx=20)
btn_clearall.pack()
btn_plot.pack()

application.mainloop()
