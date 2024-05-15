import threading
import time
import random
import sys

class ReaderWriterProblem:
    def __init__(self):
        self.mutex = threading.Lock()
        self.resource = "mutextest.txt"
        self.readers_count = 0
        self.stop_flag = False

    def read(self, reader_id, iterations):
        for _ in range(iterations):
            with self.mutex:
                if self.stop_flag:
                    return
                
                self.readers_count += 1
                if self.readers_count == 1:  
                    print(f"Writer waiting. Reader {reader_id} is reading.")
                else:
                    print(f"Reader {reader_id} is reading.")
            
            # Reading the resource
            with open(self.resource, "r") as file:
                data = file.read()
                print(f"Reader {reader_id} read: {data}")
            
            with self.mutex:
                self.readers_count -= 1
                if self.readers_count == 0:  
                    print(f"Reader {reader_id} finished reading. Writer can write now.")
            time.sleep(random.uniform(0.5, 1)) 

    def write(self, writer_id, iterations):
        for _ in range(iterations):
            with self.mutex:
                if self.stop_flag:
                    return
                
                print(f"Writer {writer_id} is waiting.")
            
            # Writing to the resource
            with open(self.resource, "w") as file:
                file.write(f"Data written by writer {writer_id}")
                print(f"Writer {writer_id} wrote to the resource.")
            
            print(f"Writer {writer_id} finished writing.")
            time.sleep(random.uniform(1, 2))  

def main():
    rw_problem = ReaderWriterProblem()
    iterations = 5

    def reader_thread(reader_id):
        rw_problem.read(reader_id, iterations)

    def writer_thread(writer_id):
        rw_problem.write(writer_id, iterations)

    # Creating reader threads
    reader_threads = []
    for i in range(5):
        thread = threading.Thread(target=reader_thread, args=(i,))
        thread.start()
        reader_threads.append(thread)

    # Creating writer threads
    writer_threads = []
    for i in range(5):
        thread = threading.Thread(target=writer_thread, args=(i,))
        thread.start()
        writer_threads.append(thread)

    
    def listen_for_enter():
        input()
        rw_problem.stop_flag = True

    listener_thread = threading.Thread(target=listen_for_enter)
    listener_thread.start()

    
    for thread in reader_threads + writer_threads:
        thread.join()

    
    listener_thread.join()

if __name__ == "__main__":
    main()
