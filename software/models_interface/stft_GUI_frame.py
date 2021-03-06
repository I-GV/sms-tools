# GUI frame for the stft_function.py

from Tkinter import *
import tkFileDialog, tkMessageBox
import sys, os
import pygame
from scipy.io.wavfile import read
import stft_function

class Stft_frame:
	def __init__(self, parent):
		self.parent = parent
		self.initUI()
		pygame.init()

	def initUI(self):

		choose_label = "Input file (.wav, mono and 44100 sampling rate):"
		Label(self.parent, text=choose_label).grid(row=0, column=0, sticky=W, padx=5, pady=(10,2))
 
		#TEXTBOX TO PRINT PATH OF THE SOUND FILE
		self.filelocation = Entry(self.parent)
		self.filelocation.focus_set()
		self.filelocation["width"] = 25
		self.filelocation.grid(row=1,column=0, sticky=W, padx=10)
		self.filelocation.delete(0, END)
		self.filelocation.insert(0, '../../sounds/piano.wav')

		#BUTTON TO BROWSE SOUND FILE
		self.open_file = Button(self.parent, text="Browse...", command=self.browse_file) #see: def browse_file(self)
		self.open_file.grid(row=1, column=0, sticky=W, padx=(220, 6)) #put it beside the filelocation textbox
 
		#BUTTON TO PREVIEW SOUND FILE
		self.preview = Button(self.parent, text=">", command=self.preview_sound, bg="gray30", fg="white")
		self.preview.grid(row=1, column=0, sticky=W, padx=(306,6))

		## STFT

		#ANALYSIS WINDOW TYPE
		wtype_label = "Window type:"
		Label(self.parent, text=wtype_label).grid(row=2, column=0, sticky=W, padx=5, pady=(10,2))
		self.w_type = StringVar()
		self.w_type.set("hamming") # initial value
		window_option = OptionMenu(self.parent, self.w_type, "rectangular", "hanning", "hamming", "blackman", "blackmanharris")
		window_option.grid(row=2, column=0, sticky=W, padx=(95,5), pady=(10,2))

		#WINDOW SIZE
		M_label = "Window size (M):"
		Label(self.parent, text=M_label).grid(row=3, column=0, sticky=W, padx=5, pady=(10,2))
		self.M = Entry(self.parent, justify=CENTER)
		self.M["width"] = 5
		self.M.grid(row=3,column=0, sticky=W, padx=(115,5), pady=(10,2))
		self.M.delete(0, END)
		self.M.insert(0, "1024")

		#FFT SIZE
		N_label = "FFT size (N) (power of two bigger than M):"
		Label(self.parent, text=N_label).grid(row=4, column=0, sticky=W, padx=5, pady=(10,2))
		self.N = Entry(self.parent, justify=CENTER)
		self.N["width"] = 5
		self.N.grid(row=4,column=0, sticky=W, padx=(270,5), pady=(10,2))
		self.N.delete(0, END)
		self.N.insert(0, "1024")

		#HOP SIZE
		H_label = "Hop size (H):"
		Label(self.parent, text=H_label).grid(row=5, column=0, sticky=W, padx=5, pady=(10,2))
		self.H = Entry(self.parent, justify=CENTER)
		self.H["width"] = 5
		self.H.grid(row=5,column=0, sticky=W, padx=(95,5), pady=(10,2))
		self.H.delete(0, END)
		self.H.insert(0, "512")

		#BUTTON TO COMPUTE EVERYTHING
		self.compute = Button(self.parent, text="Compute", command=self.compute_model, bg="dark red", fg="white")
		self.compute.grid(row=6, column=0, padx=5, pady=(10,2), sticky=W)

		#BUTTON TO PLOT
		self.plot = Button(self.parent, text="Plot", command=self.plot_model, bg="gray30", fg="white")
		self.plot.grid(row=7, column=0, padx=5, pady=(5,2), sticky=W)

		#BUTTON TO PLAY OUTPUT
		output_label = "Output:"
		Label(self.parent, text=output_label).grid(row=8, column=0, sticky=W, padx=5, pady=(10,15))
		self.output = Button(self.parent, text=">", command=self.play_out_sound, bg="gray30", fg="white")
		self.output.grid(row=8, column=0, padx=(60,5), pady=(10,15), sticky=W)


		# define options for opening file
		self.file_opt = options = {}
		options['defaultextension'] = '.wav'
		options['filetypes'] = [('All files', '.*'), ('Wav files', '.wav')]
		options['initialdir'] = '../../sounds/'
		options['title'] = 'Open a mono audio file .wav with sample frequency 44100 Hz'

	def preview_sound(self):
		
		filename = self.filelocation.get()

		if filename[-4:] == '.wav':
			(fs, x) = read(filename)
		else:
			tkMessageBox.showerror("Wav file", "The audio file must be a .wav")
			return

		if len(x.shape) > 1 :
			tkMessageBox.showerror("Stereo file", "Audio file must be Mono not Stereo")
		elif fs != 44100:
			tkMessageBox.showerror("Sample Frequency", "Sample frequency must be 44100 Hz")
		else:
			sound = pygame.mixer.Sound(filename)
			sound.play()
 
	def browse_file(self):
		
		self.filename = tkFileDialog.askopenfilename(**self.file_opt)
 
		#set the text of the self.filelocation
		self.filelocation.delete(0, END)
		self.filelocation.insert(0,self.filename)

	def compute_model(self):
		
		try:
			inputFile = self.filelocation.get()
			window = self.w_type.get()
			M = int(self.M.get())
			N = int(self.N.get())
			H = int(self.H.get())
		
			self.x, self.fs, self.mX, self.pX, self.y = stft_function.main(inputFile, window, M, N, H)

		except ValueError as errorMessage:
			tkMessageBox.showerror("Input values error", errorMessage)
	def plot_model(self):
		N = int(self.N.get())
		H = int(self.H.get())
		stft_function.plot(self.x, self.fs, self.mX, H, N, self.pX, self.y)
		
	def play_out_sound(self):

		filename = 'output_sounds/' + os.path.basename(self.filelocation.get())[:-4] + '_stft.wav'
		if os.path.isfile(filename):
			sound = pygame.mixer.Sound(filename)
			sound.play()
		else:
			tkMessageBox.showerror("Output audio file not found", "The output audio file has not been computed yet")
