import psutil
import csv
import sys
import time

def get_process_metrics(process_id, duration, interval):
    process_metrics = []
    start_time = time.time()
    print("called get_process_metrics")

    # Gather process metrics for the specified duration
    while time.time() - start_time < duration:
        try:
            process_history = [p for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_fds'])]
            for p1 in process_history:
                process_info = p1.info
                print(f"process_info: {process_info}")
            process = [p for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'num_fds']) if p.info['pid'] == process_id]
            for p1 in process:
                process_info = p1.info
                print(f"process_info: {process_info}")
                process_metrics.append(process_info)
        except psutil.NoSuchProcess:
            print("# If the process is not found, we'll skip it.")
            pass
        time.sleep(interval)

    return process_metrics

def write_to_csv(filename, process_metrics):
    # Write the process metrics to a CSV file
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

def detect_memory_leak(process_metrics, memory_threshold=5.0):
    # Check for memory leak by comparing initial and final memory usages
    initial_memory = process_metrics[0]['memory_percent']
    final_memory = process_metrics[-1]['memory_percent']
    memory_increase = final_memory - initial_memory

    if memory_increase > memory_threshold:
        return True
    else:
        return False

def calculate_average(process_metrics):
    # Calculate the average CPU and memory percent for the given process
    cpu_percent_sum = sum(process_info['cpu_percent'] for process_info in process_metrics)
    memory_percent_sum = sum(process_info['memory_percent'] for process_info in process_metrics)
    num_samples = len(process_metrics)

    avg_cpu_percent = cpu_percent_sum / num_samples
    avg_memory_percent = memory_percent_sum / num_samples

    return avg_cpu_percent, avg_memory_percent


if __name__ == "__main__":

    if len(sys.argv) != 4:
        print("Usage: python script_name.py <process_pid> <duration> <interval>")
    else:
        process_pid = int(sys.argv[1])
        duration = float(sys.argv[2])
        interval = float(sys.argv[3])

        process_metrics = get_process_metrics(process_pid, duration, interval)
        if not process_metrics:
            print(f"No data collected for process: {process_pid}")
        else:
            # Write process metrics to a CSV file
            filename = f"{process_pid}_metrics.csv"
            write_to_csv(filename, process_metrics )

            # Calculate and display average CPU and memory percent
            avg_cpu_percent, avg_memory_percent = calculate_average(process_metrics)
            print(f"Average CPU Percent: {avg_cpu_percent:.2f}%")
            print(f"Average Memory Percent: {avg_memory_percent:.2f}%")

            # Detect memory leaks and raise a warning if found
            if detect_memory_leak(process_metrics):
                print("Memory leak detected! Check the process for possible memory issues.")
