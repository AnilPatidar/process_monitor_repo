# process_monitor_repo
Process resources monitoring application Develop a console application in Python that, for a given process: • periodically gathers process metrics (for a specified amount of time) • creates a report of the gathered process metrics (in CSV format) • outputs the average for each process metric • detects possible memory leaks and raises a warning

Run Command :

python3 src/process_monitor.py 539 5 1
Usage: python script_name.py <process_pid> <duration> <interval>

Modules : 
psutil: to get process data
psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_fds'])


csv: to write CSV File
with open(filename, mode='w', newline='') as csvfile:
        fieldnames = ['Process Name', 'PID', 'CPU Percent', 'Memory Percent']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for process_info in process_metrics:
            writer.writerow({
                'Process Name': process_info['name'],
                'PID': process_info['pid'],
                'CPU Percent': process_info['cpu_percent'],
                 'Memory Percent': process_info['memory_percent'],
            })


macos commands related to process: 

List all the Processes: 
ps aux
ps ef

Output column :

USER PID  %CPU %MEM VSZ RSS  TT  STAT STARTED TIME COMMAND

Print specific column : 
ps aux | awk '{print $11}' here print $11 will print the 11th column value,

 
 The sort command with -k4,4rn option sorts the output based on the 4th column (memory usage in percentage) in reverse numerical order (-n) to sort it by highest memory usage first, and with r option to sort in descending order.


ps aux | sort -k4,4rn  


If you want to see only the top N processes with the highest memory usage, you can use the head command to limit the output:

ps aux | sort -k4,4rn | head -n 10

