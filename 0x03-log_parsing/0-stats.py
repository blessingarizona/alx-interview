#!/usr/bin/python3

import sys
import signal

# Initialize variables to hold metrics
total_file_size = 0
status_code_count = {200: 0, 301: 0, 400: 0, 401: 0, 403: 0, 404: 0, 405: 0, 500: 0}
line_count = 0

def print_statistics():
    print("Total file size:", total_file_size)
    for code in sorted(status_code_count.keys()):
        if status_code_count[code] > 0:
            print(f"{code}: {status_code_count[code]}")
    print()

def signal_handler(sig, frame):
    print_statistics()
    sys.exit(0)

# Register SIGINT handler
signal.signal(signal.SIGINT, signal_handler)

try:
    for line in sys.stdin:
        line = line.strip()
        parts = line.split()
        if len(parts) == 7:
            ip, date, method, path, protocol, status_code, file_size = parts
            if status_code.isdigit():
                status_code = int(status_code)
                if status_code in status_code_count:
                    total_file_size += int(file_size)
                    status_code_count[status_code] += 1
                    line_count += 1
        if line_count == 10:
            print_statistics()
            line_count = 0

except KeyboardInterrupt:
    print_statistics()
