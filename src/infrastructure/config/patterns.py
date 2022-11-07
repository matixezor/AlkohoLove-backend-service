from re import compile

email_pattern = compile(r'[a-zA-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}')
password_pattern = compile(r'^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[a-zA-Z]).{8,}$')
