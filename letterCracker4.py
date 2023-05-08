import subprocess
import itertools
import time

MAX_ATTEMPTS = 5
letter_combinations = [''.join(comb) for comb in itertools.product('abcdefghijklmnopqrstuvwxyz', repeat=4)]
num_attempts = 0
timestamp = time.strftime("%Y%m%d_%H%M%S")
output_file = open(f"output_{timestamp}.txt", "w")

while True:
    for combination in letter_combinations:
        print(f"Trying combination {combination}...")
        process = subprocess.Popen(['java', 'password3'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        process.stdin.write(combination + '\n')
        process.stdin.flush()
        output = process.stdout.readline().strip()
        if 'incorrect' not in output:
            print(f"The correct combination is {combination}")
            output_file.write(f"The correct combination is {combination}\n")
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time: {execution_time} seconds")
            output_file.write(f"Execution time: {execution_time} seconds\n")
            output_file.close()
            exit(0)
        else:
            if output.startswith('too high'):
                letter_combinations = [c for c in letter_combinations if c < combination]
            elif output.startswith('too low'):
                letter_combinations = [c for c in letter_combinations if c > combination]
        process.stdin.close()
        process.stdout.close()
        process.stderr.close()
        process.wait()

    num_attempts += 1

    if num_attempts == MAX_ATTEMPTS:
        print(f"Reached maximum number of attempts ({MAX_ATTEMPTS}). Restarting Java program...")
        num_attempts = 0
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        output_file.close()
        output_file = open(f"output_{timestamp}.txt", "w")
        start_time = time.time()
