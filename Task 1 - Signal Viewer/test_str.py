x = "('C:/Users/ADMIN/Downloads/EEG_example.txt', 'All Files (*.*)')"
s = (x[2:].split(',')[0].replace("'", ''))
print(s)

myfile = open("C:/Users/ADMIN/Downloads/EEG_example.txt", "r")   # 'r' relates to the mode, the mode here is reading 
amplitude = []
time = []
while myfile:
    myline  = myfile.readline()
    if myline == "":  break
    line = myline.split() 
    amplitude.append(float(line [0]))
    time.append(float(line [1])) 
    print(line)

myfile.close() 
print(amplitude) 
print (time)
