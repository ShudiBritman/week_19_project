from row_consumer import ConsumerConn as row
from analytics_consumer import ConsumerConn as analytics
from clean_lower_consumer import ConsumerConn as clean
import threading



def main():
    t1 = threading.Thread(target=row.consumer_loop, name="row-consumer")
    t2 = threading.Thread(target=analytics.consumer_loop, name="analytics-consumer")
    t3 = threading.Thread(target=clean.consumer_loop, name="clean-consumer")

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()



if __name__ == "__main__":
    main()