from worker_src.worker import run_worker


def main():
    print("Starting worker...")
    run_worker()
    print("Worker stopped.")


if __name__ == "__main__":
    main()
