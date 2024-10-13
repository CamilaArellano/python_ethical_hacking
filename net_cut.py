from time import process_time_ns
import netfilterqueue

def process_packet(packet):
    print("Packet intercepted")
    packet.accept()  # Acepta el paquete para que continúe su camino


queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)

try:
    print("Starting queue...")
    queue.run()
except KeyboardInterrupt:
    print("Stopping queue.")
