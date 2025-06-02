import socket
import numpy as np
import time

def main():
    #intro text
    print("This program is to demo and showcase LDP (local differential privacy).")
    print("We'll start by taking some data, then add noise to it, and finally; send it to the server.")
    print("By adding noise we ensure individual privacy.\n")

    #setup client
    host = "localhost"
    port = 8000
    clientSocket = socket.socket()
    clientSocket.connect((host, port))

    #input/noise
    epsilonInput = float(input("Enter the epsilon, (lower = +privacy -accuracy) and (higher = -privacy +accuracy)\n> "))
    repeatCount = input("Enter The times to repeat:\n> ")

    dataInput = input("Enter some data (q to quit)\nNumbers only for now, Pretend that this number is something like someone's age (1-100).\n> ")

    while dataInput != "q":
        for i in range(1,int(repeatCount)):
            dataInput = int(dataInput)
            noiseData = laplace_num(dataInput,99,epsilonInput,1,100)
            noiseData = int(noiseData)# age usually isn't a decimal value.

            print("\nReal Value:",dataInput)
            print("Data w/Noise:", noiseData, " <- This will be sent to server.")
            print("Data sent.")

            #send
            clientSocket.send(str(noiseData).encode())  # send message
            time.sleep(0.03)

        dataInput = input("\nEnter some data (q to quit)\n> ")

    # close the connection
    clientSocket.close()

#laplace for numbers
def laplace_num(value, sensitivity, epsilon, min, max):
    noisy_value =  value + np.random.laplace(loc=0, scale = sensitivity/epsilon)
    
    if noisy_value > max:
        noisy_value = max
    if noisy_value < min:
        noisy_value = min

    return noisy_value

if __name__ == "__main__":
    main()