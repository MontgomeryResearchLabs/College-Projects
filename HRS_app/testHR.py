
import max30102
import hrcalc
import time
import socket

# Define the host and port to connect to
host = '' #<- your pi's IP
port = #<- whatever port you specify, i used 4030

# Create a TCP/IP socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((host, port))

m = max30102.MAX30102()

dataHR=[]
time.sleep(5)   # Wait 5 seconds to place finger on the sensor.
for i in range(5):

    red, ir = m.read_sequential()

    dataHR[i*100:(i+1)*100] = red    # For raw data capturing. Not required!
    hr, hr_valid, spo2, spo2_valid = hrcalc.calc_hr_and_spo2(ir[:100], red[:100])  # Calculating heart rate and SpO2 values from raw data.

    print(hr, hr_valid, spo2, spo2_valid)


    #send data to the server
    message = str(hr)
    client_socket.sendall(message.encode())

    # Recieve data from the server
    data = client_socket.recv(1024).decode()

    # Display the recieved data
    print('Recieved: ', data) 


# Close the socket connection
client_socket.close()
