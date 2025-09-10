from passlib.context import CryptContext

pwd_cxt = CryptContext(schemes=["bcrypt"], deprecated="auto")


class HashPassword:
    def bcrypt_pwd(password: str):
        return pwd_cxt.hash(password)

    def verify(hashed_password, plain_password):
        # It will take the parameters as the plain password and the hashed password ,and it will re-has from the plain text to the hashed and compare with the hased db password
        return pwd_cxt.verify(plain_password, hashed_password)
