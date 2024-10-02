import customtkinter as tk
import cv2 as cv
import numpy as np
from CTkColorPicker import CTkColorPicker
from customtkinter import filedialog

def show_error_message(errorText):
    error_window = tk.CTkToplevel()
    error_window.geometry("200x200")
    error_window.title("Error")
    error_label = tk.CTkLabel(master=error_window, text=errorText)
    error_label.pack(pady=20)
    close_button = tk.CTkButton(master=error_window, text="Close", command=error_window.destroy)
    close_button.pack(pady=30)
    

def mainfunc(inputFilePath: str, outputFilePath: str, choosenColor, width: int | None = None, height:  int | None = None):
    try:
        capturedVideo = cv.VideoCapture(inputFilePath)
        extension = outputFilePath.rsplit('.', 1)[-1].lower()
        
        if extension == 'mp4':
            fourcc = cv.VideoWriter_fourcc(*'mp4v')
        elif extension == 'avi':
            fourcc = cv.VideoWriter_fourcc(*'XVID')
        elif extension == 'mov':
            fourcc = cv.VideoWriter_fourcc(*'avc1')
        elif extension == 'mkv':
            fourcc = cv.VideoWriter_fourcc(*'XVID')
        
        if width and height:
            outputVideo = cv.VideoWriter(outputFilePath, fourcc, capturedVideo.get(cv.CAP_PROP_FPS), (width, height))
        else:
            outputVideo = cv.VideoWriter(outputFilePath, fourcc, capturedVideo.get(cv.CAP_PROP_FPS), (int(capturedVideo.get(3)), int(capturedVideo.get(4))))
        while capturedVideo.isOpened():
            ret, frame = capturedVideo.read()
            if not ret:
                break
            
            if width and height:
                frame = cv.resize(frame, (width, height))
            
            grayedFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            blurredFrame = cv.GaussianBlur(grayedFrame, (5, 5), 0)
            edges = cv.Canny(blurredFrame, 50, 150)
            
                
            colored_edges = np.zeros_like(frame)
            colored_edges[edges > 0] = choosenColor
            highlighted_frame = cv.addWeighted(frame, 0.7, colored_edges, 0.3, 0)
            outputVideo.write(highlighted_frame)
            
            
        capturedVideo.release()
        outputVideo.release()
        end_window = tk.CTkToplevel()
        end_window.geometry("200x200")
        end_window.title("Error")
        error_label = tk.CTkLabel(master=end_window, text="Process succesfuly finished")
        error_label.pack(pady=20)
        close_button = tk.CTkButton(master=end_window, text="Close", command=end_window.destroy)
        close_button.pack(pady=30)
    except:
        show_error_message("Error in focus-peaking-process")
                 

def takecolor():
    color = picker.get()
    color = color.lstrip('#')
    
    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)
    return (int(b), int(g), int(r))
    
    

def selectcmd():
    inputPath = filedialog.askopenfilename()
    outputPath = filedialog.asksaveasfilename()
    if not inputPath or not outputPath:
        return
    
    color = takecolor()
    outputPath += "." + inputPath.rsplit('.', 1)[1]
    try:
        width = width_entry.get()
        height = height_entry.get()
        if len(width)==0 or len(height)==0:
            mainfunc(inputPath, outputPath, color)
        else:
            mainfunc(inputPath, outputPath, color, int(width), int(height))
    except ValueError:
        show_error_message("Error with resolution input.")
    return
    


root = tk.CTk()
root.title("Focus Peaking tool")

fileSelectButton = tk.CTkButton(root, text="Select File", command=selectcmd)
fileSelectButton.pack(pady=20)

picker = CTkColorPicker(root, width=250)
picker.pack(padx=10, pady=10)

width_label = tk.CTkLabel(root, text="width:")
width_label.pack(padx=10)

width_entry = tk.CTkEntry(root)
width_entry.pack(padx=10)

height_label = tk.CTkLabel(root, text="height:")
height_label.pack(padx=10)

height_entry = tk.CTkEntry(root)
height_entry.pack(padx=10)

x = (root.winfo_screenwidth() - root.winfo_reqwidth()) / 2
y = (root.winfo_screenheight() - root.winfo_reqheight()) / 2
root.wm_geometry("+%d+%d" % (x, y))

root.mainloop()