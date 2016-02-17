#alice2bob
from rsapowpow import RSA
maxPW = 2**16
maxPW = 2**32
maxPw = 2**24
def Alice2Bob(newpassword):
    global rsa1
    if 0 > newpassword  or  newpassword > maxPW:
        raise ValueError("Password must be between 0 and {}".format(maxPW))
    rsa1 = RSA(maxPW.bit_length(),opt=3)
    print("test RSA encryption/decryption")
    #rsa.from_given_pqe(61,53,17,opt=0)
    rsa_encrypted_newpassword = rsa1.public.encrypt(newpassword)
    rsa_decrypted_newpassword = rsa1.private.decrypt(rsa_encrypted_newpassword)

    print(
        "newpassword:",newpassword,
        "\nrsa_encrypted_newpassword:",rsa_encrypted_newpassword,
        "\nrsa_decrypted_newpassword:",rsa_decrypted_newpassword )
    print()
    print("test RSA digital signature ")
    rsa_signed_newpassword = rsa1.private.sign(newpassword)
    print(rsa_signed_newpassword)
    rsa_authenticated_newpassword = rsa1.public.authenticate(*rsa_signed_newpassword)

    print(
        "newpassword:",newpassword,
        "\nrsa_signed_newpassword:",rsa_signed_newpassword,
        "\nrsa_authenticated_newpassword:",rsa_authenticated_newpassword )

    
if __name__ == "__main__":
    Alice2Bob(99)



