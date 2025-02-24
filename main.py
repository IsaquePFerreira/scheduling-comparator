import random
import copy
from collections import deque

def generate_processes(num_processes):
    """
    Gera uma lista de processos com tempos de chegada e burst aleatórios.
    """
    processes = []
    for pid in range(1, num_processes + 1):
        arrival_time = random.randint(0, 10)
        burst_time = random.randint(1, 10)
        priority = random.randint(1, 3)  # Usado para MLQ (3 níveis)
        processes.append({
            "pid": pid,
            "arrival_time": arrival_time,
            "burst_time": burst_time,
            "priority": priority,
            "remaining_time": burst_time,
            "start_time": None,
            "completion_time": None
        })
    return sorted(processes, key=lambda p: p["arrival_time"])  # Ordena pelo tempo de chegada

"""
ALGORITMOS DE ESCALONAMENTO
"""

def round_robin(processes, time_quantum):
    """
    Simula o escalonamento Round Robin.
    """
    queue = deque() # criando uma fila vazia
    time = 0
    completed = []
    processes = sorted(processes, key=lambda p: p["arrival_time"])  # Ordena pelo tempo de chegada
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
    Simula o escalonamento Shortest Job First.
    """
    time = 0
    completed = []
    ready_queue = []
    remaining_processes = processes[:]
    
    while remaining_processes or ready_queue:
        while remaining_processes and remaining_processes[0]["arrival_time"] <= time:
            ready_queue.append(remaining_processes.pop(0))
        
        if ready_queue:
            ready_queue.sort(key=lambda p: p["burst_time"])  # Seleciona o menor trabalho
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
    Simula o escalonamento por Prioridade (First Come, First Served).
    """
    # Ordena os processos primeiro por prioridade (mais altos primeiro) e depois por tempo de chegada
    processes.sort(key=lambda p: (p["priority"], p["arrival_time"]))  
    
    completed = []
    time = 0
    
    for process in processes:
        if process["start_time"] is None:
            process["start_time"] = time
        
        time = max(time, process["arrival_time"])  # Assegurar que o processo é iniciado após a sua hora de chegada
        time += process["burst_time"]
        process["completion_time"] = time
        completed.append(process)
    
    return completed

def multilevel_queue_scheduler(processes, time_quantum):
    """
    Simula o escalonamento Multilevel Queue com 3 Filas:
    - Fila 1: Round Robin
    - Fila 2: Shortest Job First
    - Fila 3: Escalonamento por Prioridade (FCFS)
    """
    queues = {1: [], 2: [], 3: []}  # Três níveis de prioridade
    for process in processes:
        queues[process["priority"]].append(process)
    
    completed = []
    
    # Fila 1 (Maior prioridade): Round Robin
    completed.extend(round_robin(queues[1], time_quantum))
    
    # Fila 2 (Prioridade média): Shortest Job First
    completed.extend(shortest_job_first(queues[2]))
    
    # Fila 3 (Menor prioridade): Prioridade (FCFS)
    completed.extend(priority_scheduling(queues[3]))
    
    return completed

def calculate_metrics(processes):
    """
    Calcula o tempo médio de espera, tempo de turnaround, tempo de resposta e utilização da CPU.
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
    
    print("\nMétricas de Desempenho:")
    for algo, scheduled_processes in algorithms.items():
        metrics = calculate_metrics(scheduled_processes)
        print(f"\n{algo}:")
        for key, value in metrics.items():
            if key == "avg_waiting_time":
                print(f"  Tempo médio de espera: {value:.2f}")
            elif key == "avg_turnaround_time":
                print(f"  Tempo médio de turnaround: {value:.2f}")
            elif key == "avg_response_time":
                print(f"  Tempo médio de resposta: {value:.2f}")
            elif key == "cpu_utilization":
                print(f"  Utilização da CPU: {value:.2f}%")

if __name__ == "__main__":
    main()
