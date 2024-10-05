import uvicorn
import multiprocessing

def run_room_booking():
    uvicorn.run("room_booking.main:app", host="127.0.0.1", port=8000, reload=True)

def run_table_reservation():
    uvicorn.run("table_reservation.main:app", host="127.0.0.1", port=8001, reload=True)

def run_tour_booking():
    uvicorn.run("tour_booking.main:app", host="127.0.0.1", port=8002, reload=True)

if __name__ == "__main__":
    # Use multiprocessing to run each service in parallel
    processes = [
        multiprocessing.Process(target=run_room_booking),
        multiprocessing.Process(target=run_table_reservation),
        multiprocessing.Process(target=run_tour_booking)
    ]

    for process in processes:
        process.start()

    for process in processes:
        process.join()
