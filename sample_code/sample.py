import os

def insecure_function():
    password = "admin123"
    eval("print('Hello')")
    os.system("echo This is a test")