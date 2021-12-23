from passlib.context import CryptContext

passwdContext = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashPasswd(password: str):
    return passwdContext.hash(password)

def verifyPasswd(plainPasswd, hashPasswd):
    return passwdContext.verify(plainPasswd, hashPasswd)