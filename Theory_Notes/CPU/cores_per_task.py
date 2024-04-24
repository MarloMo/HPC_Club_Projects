import multiprocessing
import os

def task(task_id):
    print(f"Task {task_id} is running on process {os.getpid()}")

if __name__ == "__main__":
    num_tasks = 4
    cores_per_task = 2

    # Create a Pool of processes
    pool = multiprocessing.Pool(processes=num_tasks)

    # Map the tasks to the Pool
    pool.map(task, range(num_tasks))

    # Close the Pool
    pool.close()
    pool.join()
