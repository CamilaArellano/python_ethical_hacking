
1. **Importación de módulos**:
   ```python
   import time
   import scapy.all as scapy
   ```

2. **Función `get_mac(ip)`**:
   - Envía una solicitud ARP para obtener la dirección MAC de un dispositivo en la red.
   - Crea una solicitud ARP (`arp_request`) preguntando "¿Quién tiene esta IP?".
   - Crea un paquete Ethernet de broadcast (`broadcast`) para enviar la solicitud a todos los dispositivos en la red.
   - Combina ambos paquetes (`arp_request_broadcast`) y los envía.
   - Devuelve la dirección MAC del dispositivo que responde.

3. **Función `spoof(target_ip, spoof_ip)`**:
   - Obtiene la dirección MAC del objetivo (`target_mac`).
   - Crea un paquete ARP falso (`packet`) que dice ser la IP de `spoof_ip`.
   - Envía el paquete para engañar al objetivo haciéndole creer que la IP de `spoof_ip` está en la dirección MAC del atacante.

4. **Función `restore(destination_ip, source_ip)`**:
   - Restaura las tablas ARP a su estado original.
   - Obtiene las direcciones MAC de destino y origen.
   - Crea un paquete ARP legítimo (`packet`) con las direcciones correctas.
   - Envía el paquete varias veces para asegurar la restauración.

5. **Variables `target_ip` y `gateway_ip`**:
   - Definen las IPs del objetivo y del gateway.

6. **Bucle principal**:
   - Envía continuamente paquetes de spoofing para mantener el ataque.
   - Imprime el número de paquetes enviados.
   - Espera 2 segundos entre cada envío.

7. **Manejo de interrupciones**:
   - Si se detecta una interrupción (Ctrl+C), se restauran las tablas ARP a su estado original.
