import customtkinter as tk
import cv2 as cv
import numpy as np
from CTkColorPicker import CTkColorPicker
from customtkinter import filedialog


def mainfunc(inputFilePath: str, outputFilePath: str, choosenColor):
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
    
    
    outputVideo = cv.VideoWriter(outputFilePath, fourcc, 30.0, (int(capturedVideo.get(3)), int(capturedVideo.get(4))))
    while capturedVideo.isOpened():
        ret, frame = capturedVideo.read()
        if not ret:
            break
        grayedFrame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        blurredFrame = cv.GaussianBlur(grayedFrame, (5, 5), 0)
        edges = cv.Canny(blurredFrame, 50, 150)
        
            
        colored_edges = np.zeros_like(frame)
        colored_edges[edges > 0] = choosenColor
        highlighted_frame = cv.addWeighted(frame, 0.7, colored_edges, 0.3, 0)
        outputVideo.write(highlighted_frame)
        
        
    capturedVideo.release()
    outputVideo.release()
                

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
    color = takecolor()
    print(outputPath)
    outputPath += "." + inputPath.rsplit('.', 1)[1]
    print(outputPath)
    mainfunc(inputPath, outputPath, color)
    return
    

root = tk.CTk()
root.title("Focus Peaking tool")

fileSelectButton = tk.CTkButton(root, text="Select File", command=selectcmd)
fileSelectButton.pack(pady=20)

picker = CTkColorPicker(root, width=250)
picker.pack(padx=10, pady=10)


root.mainloop()