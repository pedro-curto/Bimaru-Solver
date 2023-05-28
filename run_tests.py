import os
import subprocess

input_folder = 'instances'
output_folder = 'tests'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

input_files = sorted([f for f in os.listdir(input_folder) if f.startswith('instance')])

for i, input_file in enumerate(input_files):
    input_path = os.path.join(input_folder, input_file)
    output_file = os.path.join(output_folder, f'time{i+1:02d}.txt')
    command = f"/usr/bin/time -f 'real %e s\nuser %U s\nsys %S s' -o {output_file} /bin/python3 '/mnt/c/Users/Pedro Curto/Desktop/Desktop/Uni/IArt/Projeto/bimaru.py' < {input_path}"
    subprocess.run(command, shell=True)

print("Execution times saved.")