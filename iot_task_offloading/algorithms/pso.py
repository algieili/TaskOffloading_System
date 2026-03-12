import random

def compute_pso_score(task_params):
    """
    Placeholder for Particle Swarm Optimization algorithm score.
    In a real scenario, this would use an iterative process to find the global optimum.
    """
    # PSO usually finds a global minimum. Simulating optimization here.
    base_score = (task_params['cpu_load'] * 0.3) + (task_params['power_usage'] * 0.7)
    optimized_score = base_score * random.uniform(0.8, 1.1)
    return round(optimized_score, 2)
