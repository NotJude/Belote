for i in range(-5):
    print(i)
"""

            full = self.client.recv(SERIALIZED_LENGTH).decode()
            l_full = full.split('/')[1:-1]
            m = full[0]
            
            """