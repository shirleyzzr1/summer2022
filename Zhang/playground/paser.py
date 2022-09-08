from sys import modules
from unicodedata import name
import yaml

import enum# Using enum class create enumerations
class States(enum.Enum):
   BUSY = 1
   IDLE = 2
   ERROR = 3

state = States.IDLE

if __name__=="__main__":
   # user_path = "./example_ws.yml"
   # load_data = yaml.safe_load(open(user_path))
   # # print(load_data.keys())
   # steps= load_data['actions']
   # for step in steps:
   #    module = step['module']
   #    path = step['command']['args']
   #    protocol_config = path['protocol_config']
   #    robot_config = path['robot_config']
   #    print(protocol_config)
   #    print(robot_config)
    # names = []
    # for m in machines:
    #     names.append(m['name'])
        
    # print(names)
   a = "nicetry/okkk"
   b = a.split("/")
   print(b[0])
   print(b[1])
