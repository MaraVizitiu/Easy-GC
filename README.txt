Easy-GC - An easy-to-use tool for plotting GC-contents across nucleotide sequences

DESCRIPTION
Easy-GC is an application designed for plotting the GC-content across either one
or two nucleotide sequences, comparatively. The plotting is based on the GC-content
of a sliding window that is determined by the parameters "window size" and "step".

Easy-GC can be operated in two modes, "one-sequence" mode and "comparative" mode.

"One-sequence" mode: the user can provide one nucleotide sequence, a window size
and a step size, and a plot of the GC-content across the sequence is generated.
"Comparative" mode: the user can provide two nucleotide sequences, a window size
and a step size, and a plot containing the GC-content across both sequences (one
line for each sequence) is generated.

INSTALLATION AND USAGE
Easy-GC is implemented in Python 3.8.8, which is necessary for the application to
run. The program can only be run as an interface, and does not have any command
line options.

The application can be run simply by double-clicking on the program file; the GUI
will open in "one-sequence" mode. This is the default mode and features the following
components:
(1)	A brief introduction to the program and how it should be used
(2) Mode switch checkbox - should be unchecked for "one-sequence" mode
(3)	Sequence text box - the nucleotide sequence to be plotted can be typed into
this box. The sequence CAN contain spaces and line breaks, but it should not
contain any headers or non-nucleotide characters
(4)	Window size entry box - allows the user to choose a numeric window size. Only
integers can be used as input
(5)	Step size entry box - allows the user to choose a numeric step size. Only
integers can be used as input
(6)	Browse button - allows the user to choose a fasta format file located on
the local computer that will be used as input. The file should only contain one
nucleotide sequence, and headers are automatically excluded by the program
(7)	Clear all button - clears all fields
(8)	Generate plot button - creates a plot after all of the input data has been
filled in

To generate a plot, a nucleotide sequence needs to be used as input in the "sequence
text box", which can either be typed in without any headers, or opened from file
using the "Browse" button.
Window and step sizes also need to be provided.
The plot can be created using the "Generate plot" button. A window will pop up
asking whether the figure should be saved locally or not. Upon choosing "Yes",
a window will appear that allows for the plot to be saved under a desired
name and format. The formats PNG, JPEG and PDF are supported. Choosing "No" will
leave the plot open in the main application window. The plot needs to be generated
again if saving it is desired.

If the final sliding window that is plotted contains fewer nucleotides than the
specified window length, a warning message will be generated above the plot window
informing the user. This warning message will NOT be visible when the figure is
saved as a separate file.


The second mode Easy-GC can be run in is the "comparative" mode. It can be accessed
by ticking the "mode switch checkbox". The following components will appear in the
interface:
(1)	A brief introduction to the program and how it should be used
(2) Mode switch checkbox - should be checked for "comparative" mode
(3)	Sequence text box 1 - the first nucleotide sequence to be plotted can be
typed into this box. The sequence CAN contain spaces and line breaks, but it
should not contain any headers or non-nucleotide characters
(4)	Sequence text box 2 - the second nucleotide sequence to be plotted can be
typed into this box. The sequence CAN contain spaces and line breaks, but it
should not contain any headers or non-nucleotide characters
(5)	Window size entry box - allows the user to choose a numeric window size to
be used for both sequences. Only integers can be used as input
(6)	Step size entry box - allows the user to choose a numeric step size to be
used for both sequences. Only integers can be used as input
(7)	Clear all button - clears all fields
(8)	Generate plot button - creates a plot after all of the input data has been
filled in.

The two nucleotide sequences that will be plotted must be typed into the corresponding
text boxes, and cannot be imported directly from a file. They can span multiple
lines, but should not contain any headers. The two sequences do not need to be
the same length; however, in order to generate a comparative plot, the longer
sequence will be trimmed automatically.
The user also needs to provide the window and step sizes that will be used in the
case of both sequences.

In order to generate a comparative plot, the "Generate plot" button should be clicked.
If the sequences do not have the same length originally, the longer sequence will
be trimmed automatically and the user will be informed via a warning message.
To create the plot, the "Generate plot" button needs to be clicked again. A window
will pop up asking whether the figure should be saved locally or not. Upon choosing
"Yes", a window will appear that allows for the plot to be saved under a desired
name and format. The formats PNG, JPEG and PDF are supported. Choosing "No" will
leave the plot open in the main application window. The plot needs to be generated
again if saving it is desired.

If the final sliding window that is plotted contains fewer nucleotides than the
specified window length, a warning message will be generated above the plot window
informing the user. This warning message will NOT be visible when the figure is
saved as a separate file.

EXAMPLES
Some input and output examples have been provided for both modes. They are located 
in "Input-Output_Examples.zip". The example input files contain randomly generated 
nucleotide sequences.

The "test_file1.txt" example input file has been used in the "one-sequence" mode
to generate the example plot "plot1.jpeg". The nucleotide sequence was imported
using the "Browse" button, but the sequence can also be pasted manually, without
the header. The following parameters were used: window size = 100, step size = 10.

The "test_file2.txt" example input file has been used in the "comparative" mode
to generate the example plot "plot2.jpeg". The sequences have been pasted into the
application manually, without the headers. The following parameters were used:
window size = 25, step size = 10.
