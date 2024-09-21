### Descripción General del Código

Este script permite cambiar la dirección MAC de una interfaz de red en sistemas basados en Unix. Utiliza los módulos **subprocess** para ejecutar comandos del sistema y **argparse** para manejar argumentos desde la línea de comandos. Además, usa **re** para extraer la dirección MAC actual de la interfaz.

### Desglose del Código

#### 1. **Importación de Módulos**

```python
import subprocess
import argparse
import re
```

- **`subprocess`**: Permite ejecutar comandos del sistema operativo.
- **`argparse`**: Facilita la creación de interfaces de línea de comandos.
- **`re`**: Utilizado para trabajar con expresiones regulares, especialmente para buscar patrones en cadenas.

#### 2. **Función `get_arguments()`**

Esta función maneja la entrada de argumentos desde la línea de comandos.

```python
def get_arguments():
    parser = argparse.ArgumentParser(description='Mac changer')
    parser.add_argument("-i", "--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m", "--mac", dest="new_mac", help="New Mac address")
    args = parser.parse_args()
    if not args.interface:
        parser.error("[-] Please specify an interface, use --help for more info.")
    elif not args.new_mac:
        parser.error("[-] Please specify an MAC, use --help for more info.")
    return args
```

- Se crea un objeto `ArgumentParser` con una descripción.
- Se definen dos argumentos:
  - **`-i` o `--interface`**: Interfaz de red cuya MAC se va a cambiar.
  - **`-m` o `--mac`**: Nueva dirección MAC.
- Se valida que se hayan proporcionado ambos argumentos. Si no, se muestra un mensaje de error.

#### 3. **Función `change_mac(interface, new_mac)`**

Esta función realiza el cambio de la dirección MAC.

```python
def change_mac(interface, new_mac):
    print("Changing MAC address for " + interface + " to " + new_mac)

    subprocess.run(["ifconfig", interface, "down"])
    subprocess.run(["ifconfig", interface, "hw", "ether", new_mac])
    subprocess.run(["ifconfig", interface, "up"])
```

- Imprime un mensaje indicando que se va a cambiar la MAC.
- Utiliza `subprocess.run()` para ejecutar comandos del sistema:
  - **`ifconfig <interface> down`**: Baja la interfaz.
  - **`ifconfig <interface> hw ether <new_mac>`**: Cambia la dirección MAC.
  - **`ifconfig <interface> up`**: Vuelve a levantar la interfaz.

#### 4. **Función `get_current_mac(interface)`**

Esta función obtiene la dirección MAC actual de la interfaz especificada.

```python
def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    ifconfig_result_str = ifconfig_result.decode('utf-8')  # Decodificar los bytes a una cadena de texto
    mac_address_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", ifconfig_result_str)
    if mac_address_result:
        return mac_address_result.group(0)
    else:
        print("Could not read MAC address")
```

- Utiliza `subprocess.check_output()` para obtener la salida del comando `ifconfig`.
- Decodifica la salida de bytes a una cadena UTF-8.
- Usa una expresión regular para buscar la dirección MAC en la salida.
- Si se encuentra una dirección MAC, se retorna; de lo contrario, se imprime un mensaje de error.

#### 5. **Ejecución del Script**

```python
args = get_arguments()

current_mac = get_current_mac(args.interface)
print("Current MAC = " + str(current_mac))

change_mac(args.interface, args.new_mac)

current_mac = get_current_mac(args.interface)
if current_mac == args.new_mac:
    print("MAC address was successfully changed to " + str(current_mac))
else:
    print("MAC address did not get changed")
```

- Se obtienen los argumentos de la línea de comandos.
- Se obtiene y muestra la dirección MAC actual.
- Se llama a `change_mac()` para cambiar la dirección MAC.
- Se verifica si el cambio fue exitoso y se imprime un mensaje apropiado.

### Ejemplo de Uso

Puedes ejecutar el script desde la línea de comandos de la siguiente manera:

```bash
python3 mac_changer.py -i eth0 -m 00:1A:2B:3C:4D:5E
```

### Resumen

Este script es una herramienta útil para cambiar la dirección MAC de una interfaz de red en sistemas basados en Unix. Es particularmente valioso para administradores de red y para propósitos de privacidad. Sin embargo, debe usarse con cuidado, ya que cambiar la dirección MAC puede tener implicaciones en la conectividad de red y la seguridad.
