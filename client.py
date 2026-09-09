import collections

class WorkStealingRuntime:
    """
    M:N Work-Stealing Runtime Scheduler (Go runtime model).
    P (Processors/Logical Cores) maintain local runqueues.
    Idle processors attempt work-stealing (steal half) from victim processors.
    Global runqueue handles overflow and periodic sysmon fairness.
    """
    def __init__(self, num_p=4):
        self.num_p = num_p
        self.p_queues = [collections.deque() for _ in range(num_p)]
        self.global_queue = collections.deque()
        self.completed_tasks = []

    def spawn(self, p_id, task_id, fn):
        task = (task_id, fn)
        if len(self.p_queues[p_id]) < 256:
            self.p_queues[p_id].append(task)
        else:
            self.global_queue.append(task)

    def step(self, p_id):
        if self.global_queue and len(self.p_queues[p_id]) == 0:
            task = self.global_queue.popleft()
            tid, fn = task
            res = fn()
            self.completed_tasks.append((tid, res))
            return tid

        if self.p_queues[p_id]:
            task = self.p_queues[p_id].popleft()
            tid, fn = task
            res = fn()
            self.completed_tasks.append((tid, res))
            return tid

        for offset in range(1, self.num_p):
            victim = (p_id + offset) % self.num_p
            if len(self.p_queues[victim]) > 1:
                steal_count = len(self.p_queues[victim]) // 2
                for _ in range(steal_count):
                    stolen = self.p_queues[victim].pop()
                    self.p_queues[p_id].append(stolen)
                task = self.p_queues[p_id].popleft()
                tid, fn = task
                res = fn()
                self.completed_tasks.append((tid, res))
                return tid

        return None
