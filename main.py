import random
import copy
from collections import deque

def generate_processes(num_processes):
    """
    Generate a list of processes with random arrival and burst times.
    """
    processes = []
    for pid in range(1, num_processes + 1):
        arrival_time = random.randint(0, 10)
        burst_time = random.randint(1, 10)
        priority = random.randint(1, 3)  # Used for MLQ (3 levels)
        processes.append({
            "pid": pid,
            "arrival_time": arrival_time,
            "burst_time": burst_time,
            "priority": priority,
            "remaining_time": burst_time,
            "start_time": None,
            "completion_time": None
        })
    return sorted(processes, key=lambda p: p["arrival_time"])  # Sort by arrival time

def round_robin(processes, time_quantum):
    """
    Simulate Round Robin scheduling.
    """
    queue = deque()
    time = 0
    completed = []
    processes = sorted(processes, key=lambda p: p["arrival_time"])  # Sort by arrival time
    remaining_processes = processes[:]
    
    while remaining_processes or queue:
        while remaining_processes and remaining_processes[0]["arrival_time"] <= time:
            queue.append(remaining_processes.pop(0))
        
        if queue:
            process = queue.popleft()
            if process["start_time"] is None:
                process["start_time"] = time
            
            execution_time = min(time_quantum, process["remaining_time"])
            process["remaining_time"] -= execution_time
            time += execution_time
            
            if process["remaining_time"] == 0:
                process["completion_time"] = time
                completed.append(process)
            else:
                queue.append(process)
        else:
            time += 1
    return completed

def shortest_job_first(processes):
    """
    Simulate Shortest Job First scheduling.
    """
    time = 0
    completed = []
    ready_queue = []
    remaining_processes = processes[:]
    
    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0]["arrival_time"] <= time:
            ready_queue.append(remaining_processes.pop(0))
        
        if ready_queue:
            ready_queue.sort(key=lambda p: p["burst_time"])  # Select shortest job
            process = ready_queue.pop(0)
            process["start_time"] = time if process["start_time"] is None else process["start_time"]
            time += process["burst_time"]
            process["completion_time"] = time
            completed.append(process)
        else:
            time += 1
    return completed

def priority_scheduling(processes):
    """
    Simulate Priority Scheduling (Non-Preemptive).
    """
    processes.sort(key=lambda p: (p["priority"], p["arrival_time"]))
    return shortest_job_first(processes)

def multilevel_queue_scheduler(processes, time_quantum):
    """
    Simulate Multilevel Queue Scheduling with 3 Queues:
    - Queue 1: Round Robin
    - Queue 2: Shortest Job First
    - Queue 3: Priority Scheduling
    """
    queues = {1: [], 2: [], 3: []}  # Three priority levels
    for process in processes:
        queues[process["priority"]].append(process)
    
    completed = []
    completed.extend(round_robin(queues[1], time_quantum))  # Round Robin for Queue 1
    completed.extend(shortest_job_first(queues[2]))  # SJF for Queue 2
    completed.extend(priority_scheduling(queues[3]))  # Priority Scheduling for Queue 3
    
    return completed

def calculate_metrics(processes):
    """
    Calculate average waiting time, turnaround time, response time, and CPU utilization.
    """
    total_waiting_time = 0
    total_turnaround_time = 0
    total_response_time = 0
    num_processes = len(processes)
    total_burst_time = sum(p["burst_time"] for p in processes)
    completion_time = max(p["completion_time"] for p in processes)
    
    for process in processes:
        turnaround_time = process["completion_time"] - process["arrival_time"]
        waiting_time = turnaround_time - process["burst_time"]
        response_time = process["start_time"] - process["arrival_time"]
        
        total_waiting_time += waiting_time
        total_turnaround_time += turnaround_time
        total_response_time += response_time
    
    avg_waiting_time = total_waiting_time / num_processes
    avg_turnaround_time = total_turnaround_time / num_processes
    avg_response_time = total_response_time / num_processes
    cpu_utilization = (total_burst_time / completion_time) * 100
    
    return {
        "avg_waiting_time": avg_waiting_time,
        "avg_turnaround_time": avg_turnaround_time,
        "avg_response_time": avg_response_time,
        "cpu_utilization": cpu_utilization
    }

def main():
    num_processes = 5
    time_quantum = 3
    processes = generate_processes(num_processes)
    
    algorithms = {
        "Round Robin": round_robin(copy.deepcopy(processes), time_quantum),
        "Shortest Job First": shortest_job_first(copy.deepcopy(processes)),
        "Multilevel Queue": multilevel_queue_scheduler(copy.deepcopy(processes), time_quantum)
    }
    
    print("\nPerformance Metrics:")
    for algo, scheduled_processes in algorithms.items():
        metrics = calculate_metrics(scheduled_processes)
        print(f"\n{algo}:")
        for key, value in metrics.items():
            print(f"  {key.replace('_', ' ').title()}: {value:.2f}")

if __name__ == "__main__":
    main()
