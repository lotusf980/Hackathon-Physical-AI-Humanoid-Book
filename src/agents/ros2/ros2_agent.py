"""
ROS 2 Agent for Physical AI & Humanoid Robotics

This agent specializes in explaining ROS 2 concepts, architecture, and implementation
for humanoid robotics applications.
"""

from typing import Dict, Any, List
import json


class ROS2Agent:
    """Specialized agent for ROS 2 explanations in humanoid robotics"""

    def __init__(self):
        self.knowledge_base = {
            "architecture": {
                "nodes": "Nodes are executables that perform specific tasks in ROS 2. Each node runs independently and communicates with other nodes through topics, services, or actions.",
                "topics": "Topics are named buses over which nodes exchange messages using a publish-subscribe pattern. Messages are sent asynchronously.",
                "services": "Services provide request-response communication between nodes. A client sends a request and waits for a response from the server.",
                "actions": "Actions are for long-running tasks that provide feedback during execution. They support goals, feedback, and results with cancellation capability.",
                "parameters": "Parameters are named values that can be configured at runtime and shared between nodes."
            },
            "middleware": {
                "rmw": "ROS Middleware (RMW) provides the abstraction layer between ROS 2 and the underlying communication middleware (e.g., DDS implementations).",
                "dds": "Data Distribution Service (DDS) is the underlying communication standard that ROS 2 uses for message passing between nodes.",
                "qos": "Quality of Service (QoS) policies control how messages are delivered, including reliability, durability, and history settings."
            },
            "tools": {
                "rclpy": "Python client library for ROS 2. Provides APIs for creating nodes, publishers, subscribers, services, and actions.",
                "rclcpp": "C++ client library for ROS 2. Offers better performance for computationally intensive tasks.",
                "ros2cli": "Command-line interface tools for ROS 2 including ros2 run, ros2 launch, ros2 param, etc."
            },
            "robot_specific": {
                "urdf": "Unified Robot Description Format. XML format to describe robot models including links, joints, and visual/collision properties.",
                "tf2": "Transform library for keeping track of coordinate frames in a robot system over time.",
                "navigation": "ROS 2 navigation stack for path planning, obstacle avoidance, and localization.",
                "control": "ROS 2 control framework for hardware abstraction and controller management."
            }
        }

    def explain_concept(self, concept: str) -> str:
        """Explain a specific ROS 2 concept"""
        concept_lower = concept.lower().strip()

        # Flatten the knowledge base to search across all categories
        for category, items in self.knowledge_base.items():
            if concept_lower in items:
                return items[concept_lower]

        # Try to find partial matches
        for category, items in self.knowledge_base.items():
            for key, value in items.items():
                if concept_lower in key.lower() or concept_lower.replace(" ", "") in key.lower().replace("_", ""):
                    return value

        return f"I don't have specific information about '{concept}' in my ROS 2 knowledge base. Please ask about ROS 2 architecture, middleware, tools, or robot-specific concepts."

    def provide_example(self, topic: str) -> str:
        """Provide a practical example for a ROS 2 topic"""
        topic_lower = topic.lower().strip()

        examples = {
            "publisher": """# ROS 2 Publisher Example
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalPublisher(Node):
    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self):
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = MinimalPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
""",
            "subscriber": """# ROS 2 Subscriber Example
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class MinimalSubscriber(Node):
    def __init__(self):
        super().__init__('minimal_subscriber')
        self.subscription = self.create_subscription(
            String,
            'topic',
            self.listener_callback,
            10)
        self.subscription  # prevent unused variable warning

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

def main(args=None):
    rclpy.init(args=args)
    minimal_subscriber = MinimalSubscriber()
    rclpy.spin(minimal_subscriber)
    minimal_subscriber.destroy_node()
    rclpy.shutdown()
""",
            "service": """# ROS 2 Service Server Example
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class MinimalService(Node):
    def __init__(self):
        super().__init__('minimal_service')
        self.srv = self.create_service(AddTwoInts, 'add_two_ints', self.add_two_ints_callback)

    def add_two_ints_callback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info('Incoming request\na: %d b: %d' % (request.a, request.b))
        return response

def main(args=None):
    rclpy.init(args=args)
    minimal_service = MinimalService()
    rclpy.spin(minimal_service)
    rclpy.shutdown()
""",
            "action": """# ROS 2 Action Server Example
import rclpy
from rclpy.action import ActionServer
from rclpy.node import Node
from example_interfaces.action import Fibonacci

class FibonacciActionServer(Node):
    def __init__(self):
        super().__init__('fibonacci_action_server')
        self._action_server = ActionServer(
            self,
            Fibonacci,
            'fibonacci',
            self.execute_callback)

    def execute_callback(self, goal_handle):
        self.get_logger().info('Executing goal...')
        feedback_msg = Fibonacci.Feedback()
        feedback_msg.sequence = [0, 1]

        for i in range(1, goal_handle.request.order):
            if goal_handle.is_cancel_requested:
                goal_handle.canceled()
                self.get_logger().info('Goal canceled')
                return Fibonacci.Result()

            feedback_msg.sequence.append(
                feedback_msg.sequence[i] + feedback_msg.sequence[i-1])
            goal_handle.publish_feedback(feedback_msg)

        goal_handle.succeed()
        result = Fibonacci.Result()
        result.sequence = feedback_msg.sequence
        return result
"""
        }

        for key, example in examples.items():
            if topic_lower in key:
                return example

        return f"No example available for '{topic}'. Available examples: {', '.join(examples.keys())}"

    def get_architecture_info(self) -> Dict[str, Any]:
        """Return detailed information about ROS 2 architecture"""
        return {
            "title": "ROS 2 Architecture Overview",
            "description": "ROS 2 provides a flexible framework for writing robot software with a distributed architecture.",
            "components": {
                "nodes": self.knowledge_base["architecture"]["nodes"],
                "topics": self.knowledge_base["architecture"]["topics"],
                "services": self.knowledge_base["architecture"]["services"],
                "actions": self.knowledge_base["architecture"]["actions"],
                "parameters": self.knowledge_base["architecture"]["parameters"]
            }
        }

    def get_best_practices(self) -> List[str]:
        """Return ROS 2 best practices for humanoid robotics"""
        return [
            "Use meaningful node names that reflect their function",
            "Design topics with clear, consistent naming conventions",
            "Implement proper error handling and logging",
            "Use QoS profiles appropriately for different message types",
            "Leverage launch files for complex system startup",
            "Use parameters for configuration rather than hardcoding values",
            "Implement proper shutdown procedures in nodes",
            "Use composition for better performance when needed"
        ]

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request to the ROS 2 agent"""
        intent = request.get("intent", "explain")
        topic = request.get("topic", "")
        details = request.get("details", {})

        if intent == "explain":
            explanation = self.explain_concept(topic)
            return {
                "type": "explanation",
                "topic": topic,
                "content": explanation,
                "source": "ros2_agent"
            }
        elif intent == "example":
            example = self.provide_example(topic)
            return {
                "type": "example",
                "topic": topic,
                "content": example,
                "source": "ros2_agent"
            }
        elif intent == "architecture":
            arch_info = self.get_architecture_info()
            return {
                "type": "architecture_info",
                "content": arch_info,
                "source": "ros2_agent"
            }
        elif intent == "best_practices":
            practices = self.get_best_practices()
            return {
                "type": "best_practices",
                "content": practices,
                "source": "ros2_agent"
            }
        else:
            return {
                "type": "error",
                "content": f"Unknown intent: {intent}",
                "source": "ros2_agent"
            }