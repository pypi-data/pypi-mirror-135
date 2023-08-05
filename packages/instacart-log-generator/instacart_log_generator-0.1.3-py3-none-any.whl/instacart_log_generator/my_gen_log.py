import os
import random
import json
import random
import socket
import struct
from datetime import datetime
import pkg_resources
import time
import numpy as np
from instacart_log_generator.INFO import REQUEST_URL, BODY, USER_AGENTS, RESPONSE_CODE_WEIGHT_DICT, REQUEST_TYPE_WEIGHT_DICT

stream = pkg_resources.resource_stream(__name__, 'sample.npy')

class InstacartLogGenerator:

    def __init__(self):
        self.url = REQUEST_URL
        self.body = BODY
        self.user_agents = USER_AGENTS
        self.response_code = RESPONSE_CODE_WEIGHT_DICT
        self.request_type = REQUEST_TYPE_WEIGHT_DICT
        self.info = np.load(stream, allow_pickle=True)

    def write(self, write_path, text):
        is_new = False
        try:
            with open(write_path, 'r') as f:
                data = f.readline()
                if len(data) > 0:
                    is_new = True
        except FileNotFoundError:
            pass
        with open(write_path, 'a+') as f:
            if is_new:
                f.write('\n')
            f.write(text)


    def logging(self, write_path, lps=1):
        sleep_time = 1 / lps
        while True:
            self.gen_log(write_path)
            time.sleep(sleep_time)

    def gen_log(self, write_path):
        ip = self.gen_ip()
        date = self.gen_date()
        url = self.pick_one(self.url)
        body = json.dumps(self.gen_random_info(self.body))
        user_agnet = self.pick_one(self.user_agents)
        response_code = self.pick_one(self.response_code)
        request_type = self.pick_one(self.request_type)

        self.write(
            write_path,
            f'{ip} - - [{date}] \"{request_type} {url} HTTP/1.1\" {response_code} \"-\" \"{user_agnet}\"'
        )

        if request_type == 'POST':
            self.write(
                write_path,
                f'{ip} - - [{date}] {body}'
            )


    def gen_ip(self):
        return socket.inet_ntoa(struct.pack('>I', random.randint(1, 0xffffffff)))

    def gen_date(self):
        return datetime.now().strftime("%d/%b/%Y:%H:%M:%S +0900")

    def gen_random_info(self, body):
        num = np.random.randint(self.info.shape[0])
        picked_info = self.info[num]
        
        body['order_id'] = int(picked_info[0])
        body['product_id'] = int(picked_info[1])
        body['add_to_cart_order'] = int(picked_info[2])
        body['reordered'] = int(picked_info[3])
        body['aisle_id'] = int(picked_info[4])
        body['department_id'] = int(picked_info[5])
        body['order_number'] = int(picked_info[6])
        body['order_dow'] = int(picked_info[7])
        body['order_hour_of_day'] = int(picked_info[8])
        body['days_since_prior_order'] = int(picked_info[9])

        return body

    def pick_one(self, obj):
        rand_val = random.random()
        total = 0

        if type(obj) == list:
            return random.choice(obj)
        else:
            for k, v in obj.items():
                total += v
                if rand_val <= total:
                    return k