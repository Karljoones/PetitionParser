import time

def generate_report_performance_check(func):
    def wrapper(df, output_directory, output_filename):
        print(f"Starting {func.__name__}...")
        start_time = time.time()

        func(df, output_directory, output_filename)

        print(f"Finished {func.__name__}...")
        print(f"Time elapsed: {time.time() - start_time} seconds")
    return wrapper