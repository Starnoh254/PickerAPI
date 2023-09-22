import bcrypt
def hash_password(password):
    bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    print("Bytes ", bytes)
    print("Salt ", salt)
    print("Hashed password ", hash.decode())
    return hash.decode()

    '''Test'''
  # hashed_password = hash_password("password")

def hash_verify(password,  hashed_password):
    bytes = password.encode('utf-8')
    result = bcrypt.checkpw(bytes, hashed_password.encode())
    print(result)
    return result

    '''Test'''
  # hash_verify("password",hashed_password)

current_id  = 0
def generate_ids():
   global current_id
   current_id +=1
   return "WMS/NRB/0" + str(current_id)

