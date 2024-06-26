import jwt
import hashlib
from CaesarSQLDB.caesarcrud import CaesarCRUD
class CaesarJWT:
    def __init__(self,caesarcrud : CaesarCRUD) -> None:
        self.caesarcrud = caesarcrud
        self.JWT_SECRET = "Peter Piper picked a peck of pickled peppers, A peck of pickled peppers Peter Piper picked, If Peter Piper picked a peck of pickled peppers,Where's the peck of pickled peppers Peter Piper picked" #'super-secret'
        # IRL we should NEVER hardcode the secret: it should be an evironment variable!!!
        self.JWT_ALGORITHM = "HS256"
    def secure_encode(self,token):
        # if we want to sign/encrypt the JSON object: {"hello": "world"}, we can do it as follows
        # encoded = jwt.encode({"hello": "world"}, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        encoded_token = jwt.encode(token, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        # this is often used on the client side to encode the user's email address or other properties
        return encoded_token

    def secure_decode(self,token):
        # if we want to sign/encrypt the JSON object: {"hello": "world"}, we can do it as follows
        # encoded = jwt.encode({"hello": "world"}, self.JWT_SECRET, algorithm=self.JWT_ALGORITHM)
        decoded_token = jwt.decode(token, self.JWT_SECRET, algorithms=self.JWT_ALGORITHM)
        # this is often used on the client side to encode the user's email address or other properties
        return decoded_token
    def provide_access_token(self,login_details):
        condition = f"email = '{login_details['email']}'"
        email_exists = self.caesarcrud.check_exists(("*"),"users",condition=condition)

        if email_exists:
            encrypted_password =  hashlib.sha256(login_details["password"].encode('utf-8')).hexdigest()
            email_data = self.caesarcrud.get_data(("email","password"),"users",condition=condition)[0]
            if email_data["password"] == encrypted_password:
                res = self.caesarcrud.caesarsql.run_command(f"SELECT uuid FROM users WHERE {condition}",result_function=self.caesarcrud.caesarsql.fetch)
                uuid_json = self.caesarcrud.tuple_to_json(("uuid",),res)[0]
                access_token = self.secure_encode({"uuid":str(uuid_json["uuid"])}) #create_access_token(identity=email_exists["email"])
                return access_token
            else:
                return "Wrong password"
        else:
            return "Wrong password"