import random

class ServerSimulator:
    """
    Simulates different server tiers in an Edge-enabled IoT system.
    """
    def __init__(self):
        self.servers = {
            "Edge": {"lat_range": (5, 15), "proc_range": (100, 300), "energy_coeff": 0.5},
            "Fog": {"lat_range": (20, 50), "proc_range": (50, 150), "energy_coeff": 1.2},
            "Cloud": {"lat_range": (100, 300), "proc_range": (10, 50), "energy_coeff": 5.0}
        }

    def simulate_execution(self, server_name):
        """
        Simulates the processing of a task on a specific server tier.
        """
        config = self.servers.get(server_name, self.servers["Edge"])
        
        latency = random.randint(*config["lat_range"])
        proc_time = random.randint(*config["proc_range"])
        energy = round(proc_time * config["energy_coeff"] * random.uniform(0.9, 1.1), 2)
        
        return {
            "server": server_name,
            "latency": latency,
            "proc_time": proc_time,
            "energy": energy,
            "status": "Success"
        }

    def get_best_server(self, gbfs_val, pso_val):
        """
        Simple decision logic to choose a server based on scores.
        """
        if gbfs_val < 30:
            return "Edge"
        elif pso_val < 50:
            return "Fog"
        else:
            return "Cloud"
