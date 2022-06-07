### There are two fundamental concepts in ROS, which are: Nodes and Topics

Nodes:  
These are software processes that do 'stuff' (e.g. process data, command hardware, execute algorithms). Nodes provide modularity to robotic projects that use ROS. They are often written in C++ or Python. In this course, we will use Python to write them. ROS Noetic compatible with Python 3.x.

Topics:  
Transport information between nodes, in the form of messages.

In a real robot application you will often have to deal with a large number of nodes and topics. It is important to know which nodes are talking to each other, and what topics are being used to pass the information (messages) between nodes.