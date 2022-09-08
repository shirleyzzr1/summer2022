import rclpy
from rclpy.action import ActionClient
from rclpy.node import Node
import yaml

from demo_interfaces.action import OT2Job
from demo_interfaces.msg import OT2Job as OT2Jobmsg
from demo_interfaces.msg import JobHeader
from demo_interfaces.srv import ExecuteJob
from std_msgs.msg import String
class DemoActionClient(Node):
    """

    """
    def __init__(self,name,type):
        """
        
        """
        super().__init__('demo_action_client')
        self._action_client = ActionClient(self, OT2Job, '/'+name+'/'+type)
        # self.heartbeat_publisher = self.create_publisher()

        self.srv = self.create_service(ExecuteJob,'/'+name+'/execute_job',self.exectute_job_callback)

        self.get_logger().info(name+" Action Client running!")
        self.get_logger().info("Send rc_path and pc_path with /execute_job service call")
        

    def exectute_job_callback(self,request,response):
        """

        """
        self.get_logger().info("call execute job service")

        rc_config = None
        pc_config = None
        try:
            rc_config = yaml.dump(yaml.safe_load(open(request.rc_path)))
        except IOError:
            response.error_msg = "No such file or directory:" + request.rc_path
            response.success = False
            return response
            
        try:
            pc_config = yaml.dump(yaml.safe_load(open(request.pc_path)))
        except IOError:
            response.error_msg = "No such file or directory:" + request.pc_path
            response.success = False
            return response

        response.success = True
        self.send_goal(protocol_config=pc_config,robot_config=rc_config)

        return response


    def send_goal(self, pc_path=None, rc_path=None, protocol_config="", robot_config=""):
        """

        """
        goal_msg = OT2Job.Goal()
        if rc_path is not None:
            goal_msg.job.rc_path = rc_path
        if pc_path is not None:
            goal_msg.job.pc_path = pc_path

        goal_msg.job.robot_config = robot_config
        goal_msg.job.protocol_config = protocol_config
        goal_msg.job.simulate = True
        
        self._action_client.wait_for_server()

        print("Sending goal to action server ...")

        self.goal_future = self._action_client.send_goal_async(goal_msg) #, feedback_callback=self.goal_feedback_callback)
        self.goal_future.add_done_callback(self.goal_respond_callback)
        

    def goal_feedback_callback(self,feed):
        pass
        # feedback_msg = feed.feedback
        # self.get_logger().info("Progress: {:.2f}".format(feedback_msg.total_percentage_progress))


    def goal_respond_callback(self, future):
        goal_handle = future.result()

        if not goal_handle.accepted:
            self.get_logger().info('Goal rejected')
            return
        self.get_logger().info('Goal accepted')

        self.goal_result_future = goal_handle.get_result_async()
        self.goal_result_future.add_done_callback(self.goal_result_callback)

    def goal_result_callback(self, future):
        result = future.result().result
        self.get_logger().info("Result from action server:")
        self.get_logger().info("--success: {}".format(result.success))
        self.get_logger().info("--message: {}".format(result.error_msg))
        # if not result.success:
        #     self.get_logger().info("Error Message: " + result.error_msg)
        # rclpy.shutdown()

class ActionManager(Node):
    def __init__(self):
        super().__init__('action_manager')
        self.workcell_data = None
        self.machines = self.parse_machines()
        self.machine_states = self.create_states()

        self.create_subs()
        self.create_action_clients()

        self.steps = self.workcell_data['actions']
        self.executeJob_client = self.create_client(ExecuteJob, 'ot2_1/execute_job')

    def parse_machines(self):
        user_path = "/root/example_ws.yml"
        self.workcell_data = yaml.safe_load(open(user_path))
        machines= self.workcell_data['modules']
        names = []
        for m in machines:
            names.append([m['name'],m['type']])
        return names

    def create_states(self):
        dicts = {}
        for machine,type in self.machines:
            self.get_logger().info(machine)
            dicts[machine]="ERROR"
        return dicts

    def common_callback(self,msg):
        # self.get_logger().info('I heard: "%s"'%msg.data)
        data = msg.data.split("/")
        machine = data[0]
        states = data[1]
        info = data[2]
        if self.machine_states[machine]=="ERROR" and states=="IDLE":
            self.get_logger().info(machine+" is now IDLE!")
            self.machine_states[machine]="IDLE"
        elif self.machine_states[machine]=="ERROR":
            self.get_logger().info(machine + info)
            self.machine_states[machine]="ERROR"

    def create_subs(self):
        for name,type in self.machines:
            setattr(self,"sub"+name, self.create_subscription(String,"/"+name+"/status",lambda msg:self.common_callback(msg),10))

    # def create_action_clients(self):
    #     for name,type in self.machines:
    #         setattr(self,"client_"+name,DemoActionClient(name,type))


    def send_request(self,rc_path,pc_path,machine):
        self.get_logger().info("Sending request")
        req = ExecuteJob.Request()
        req.rc_path = rc_path
        req.pc_path = pc_path
        self.future = self.executeJob_client.call_async(req)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)
    action_manager = ActionManager()
    module = action_manager.steps[0]['module']
    start_exec = 1
    while True:
        if start_exec==1:
            if action_manager.machine_states[module]=="IDLE":
                action_manager.get_logger().info("Result from if")
                pc_path = action_manager.steps[0]['command']['args']['pc_path']
                rc_path = action_manager.steps[0]['command']['args']['rc_path']
                response = action_manager.send_request(rc_path=rc_path,pc_path=pc_path,machine = module)
                start_exec = 2
        rclpy.spin_once(action_manager,timeout_sec=0)

# def main(args=None):
#     rclpy.init(args=args)
#     demo_action_client = DemoActionClient()
#     steps= demo_action_client.workcell_data['actions']
#     module = steps[0]['module']
#     start_exec = 1
#     while True:
#         if start_exec==1:
#             if demo_action_client.machine_states[module]=="IDLE":
#                 demo_action_client.get_logger().info("Result from if")
#                 pc_path = steps[0]['command']['args']['pc_path']
#                 rc_path = steps[0]['command']['args']['rc_path']
#                 response = demo_action_client.send_request(rc_path=rc_path,pc_path=pc_path)
#                 start_exec = 2
#         rclpy.spin_once(demo_action_client,timeout_sec=0)
        
    

if __name__ == '__main__':
    main()