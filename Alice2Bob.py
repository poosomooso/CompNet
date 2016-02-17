#Serena Chen
#alice2bob
from rsa import RSA
maxPW = 99999
def Alice2Bob(newpassword):
    if 0 > newpassword  or  newpassword > maxPW:
        raise ValueError("Password must be between 0 and {}".format(maxPW))
    rsa = RSA()
    rsa.from_message_bit_length(maxPW.bit_length())
    #rsa.from_given_pqe(61,53,17,opt=0)
    rsa_encrypted_newpassword = rsa.public.encrypt(newpassword)
    rsa_decrypted_newpassword = rsa.private.decrypt(rsa_encrypted_newpassword)
    print(
        "newpassword:",newpassword,
        "\nrsa_encrypted_newpassword:",rsa_encrypted_newpassword,
        "\nrsa_decrypted_newpassword:",rsa_decrypted_newpassword

        )

    return

