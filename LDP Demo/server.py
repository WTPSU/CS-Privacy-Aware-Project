import socket
import tkinter as tk
import threading
from statistics import median, mode
import random

serverData = []

#random starting data
for i in range(1,100):
    serverData.append(random.randrange(1,99))

def main():
    #setup server
    host = "localhost"
    port = 8000
    serverSocket = socket.socket()
    serverSocket.bind((host, port))
    serverSocket.listen()

    # tkinker window
    root = tk.Tk()
    root.attributes('-topmost', True)
    root.title("LDP Demo Server")
    root.geometry("400x300")

    # output
    output = tk.Text(root, height=15, width=50)
    output.pack(padx=10, pady=10)
    output.insert(tk.END, "Server Output:")
    output.config(state=tk.DISABLED) #read-only

    # frame so that buttons are side by side
    button_frame = tk.Frame(root)
    button_frame.pack(pady=5)

    # clear
    clearButton = tk.Button(button_frame, text="Clear",width=12, command=lambda: clearOutput(output))
    clearButton.pack(side=tk.LEFT, padx=5)

    # end
    root.protocol("WM_DELETE_WINDOW", lambda: cleanExit(serverSocket, root)) # window close (X) button
    exitButton = tk.Button(button_frame, text="End", width=12, command=lambda: cleanExit(serverSocket, root))
    exitButton.pack(side=tk.LEFT, padx=5)

    # start
    threading.Thread(target=handleConnections,args=(serverSocket,output), daemon=True).start()
    root.mainloop()

#since ctrl+c wasn't working, this is a tkinker implementation :[
def cleanExit(serverSocket,root):
    serverSocket.close()
    root.destroy()

def clearOutput(output):
    output.config(state=tk.NORMAL)
    output.delete("1.0", tk.END)
    output.insert(tk.END, "Server Output:")
    output.config(state=tk.DISABLED)

#seperate thread for listening
def handleConnections(serverSocket,output):
    print("Server started.")

    while True:
        try:
            clientSocket, add = serverSocket.accept()

            while True:
                data = clientSocket.recv(1024).decode()
                if not data:
                    break
            
                # add to list
                data = int(data)
                serverData.append(data)

                # output data
                outputStr = "\nServer Data Count: " + str(len(serverData))
                outputStr += "\nRange: " + str(max(serverData) - min(serverData))
                outputStr += "\nmedian: " + str(median(serverData))
                outputStr += "\nmode: " + str(mode(serverData))

                output.config(state=tk.NORMAL)
                output.insert(tk.END, "\n"+outputStr)
                output.config(state=tk.DISABLED)
                output.yview(tk.END)#autoscroll

            clientSocket.close()
        except:
            break
    print("Server Ended.")

if __name__ == "__main__":
    main()