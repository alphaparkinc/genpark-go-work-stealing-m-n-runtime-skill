from client import WorkStealingRuntime

def main():
    print("=== Testing Go-Style M:N Work Stealing Runtime ===")
    runtime = WorkStealingRuntime(num_p=2)

    # Heavily load P0
    runtime.spawn(0, "task_alpha", lambda: "Result-Alpha")
    runtime.spawn(0, "task_beta", lambda: "Result-Beta")
    runtime.spawn(0, "task_gamma", lambda: "Result-Gamma")

    # P1 is idle -> steals work from P0
    stolen_task = runtime.step(p_id=1)
    print(f"Processor 1 stole and executed: {stolen_task}")
    assert stolen_task is not None

    local_task = runtime.step(p_id=0)
    print(f"Processor 0 popped and executed: {local_task}")

    assert len(runtime.completed_tasks) == 2
    print("Completed tasks so far:", runtime.completed_tasks)
    print("=== All tests passed successfully! ===")

if __name__ == "__main__":
    main()
