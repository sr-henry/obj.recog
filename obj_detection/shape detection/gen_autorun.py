
with open('autorun.bat', 'w') as file:
    for i in range(1, 19):
        file.write('python shape.py ' + str(i) + '.png > ' + str(i) + '.txt\n')
