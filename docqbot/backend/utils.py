# utils.py
import os
import psutil

def log_resource_usage(tag=""):
    process = psutil.Process(os.getpid())
    mem_mb = process.memory_info().rss / 1024 / 1024
    cpu_percent = process.cpu_percent(interval=0.1)
    print(f"[{tag}] 💾 Memory: {mem_mb:.2f} MB | ⚙️ CPU: {cpu_percent:.2f}%")
