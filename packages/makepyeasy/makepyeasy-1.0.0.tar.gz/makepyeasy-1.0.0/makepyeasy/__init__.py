# Made by Viraj Khanna <viraj@virajkhanna.in>
import requests
import os
import sys
import socket
import math
import random

class math:
    def add(num1, num2, *args, **kwargs):
        total = 0
        total = total + num1 + num2
        for i in args:
            total = total + i
        return total

    def multiply(num1, num2, *args, **kwargs):
        total = 0
        total = num1 * num2
        for i in args:
            total = total * i
        return total
    
    def average(num1, num2, *args):
        sum_of_numbers = num1 + num2
        for i in args:
            sum_of_numbers = sum_of_numbers + i
        average = sum_of_numbers / (len(args) + 2)

        return average
    def gen_rand_num():
        return random.randint(1,10000)
    def gen_rand_num_with_range(start, end):
        return random.randint(start, end)
class urls:
    def request_url(url, method="GET"):
        if (method=="GET"):
            website = requests.get(url)
            return website
        elif (method=="POST"):
            website = requests.post(url)
            return website
        else:
            print("makepyeasy error: Unknown Request Method", file=sys.stderr)
class files:
    def list_files(directory=None):
        if (directory == None):
            files = os.listdir()
        else:
            files = os.listdir(str(directory))

        return files
    def read_file(file_location):
        try:
            file = open(file_location, "r")
            data = file.read()
            file.close()
        except:
            print("makepyeasy error: Error occured in reading files", file=sys.stderr)
        return data

    def write_file(file_location, data):
        try:
            file = open(file_location, "w")
            file.write(data)
            file.close()
        except:
            print("makepyeasy error: Error while writing to files", file=sys.stderr)
    def append_file(file_location, data):
        try:
            file = open(file_location, "a")
            file.append(data)
            file.close()
        except:
            print("makepyeasy error: Error while appending to files", file=sys.stderr)

class networking:
    def open_socket():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        return s
    def socket_connect(socket1, ip, port):
        socket1.connect((ip, port))
    def socket_close(socket1):
        socket1.close()
