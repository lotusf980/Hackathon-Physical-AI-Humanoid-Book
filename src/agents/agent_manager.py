"""
Agent Manager for Physical AI & Humanoid Robotics

This module manages the specialized agents for ROS 2, Simulation, and VLA reasoning.
"""

from typing import Dict, Any, Union
from .ros2.ros2_agent import ROS2Agent
from .simulation.simulation_agent import SimulationAgent
from .vla.vla_agent import VLAAgent


class AgentManager:
    """Manages specialized agents for different domains in humanoid robotics"""

    def __init__(self):
        self.ros2_agent = ROS2Agent()
        self.simulation_agent = SimulationAgent()
        self.vla_agent = VLAAgent()

        self.agents = {
            'ros2': self.ros2_agent,
            'simulation': self.simulation_agent,
            'vla': self.vla_agent
        }

    def route_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Route a request to the appropriate agent based on domain"""
        domain = request.get('domain', '').lower()
        topic = request.get('topic', '').lower()

        # Try to infer domain from topic if not specified
        if not domain:
            domain = self._infer_domain(topic)

        if domain in self.agents:
            return self.agents[domain].process_request(request)
        else:
            # Try to determine best agent based on keywords
            agent = self._select_best_agent(topic)
            return agent.process_request(request)

    def _infer_domain(self, topic: str) -> str:
        """Infer the appropriate domain based on the topic"""
        topic_lower = topic.lower()

        # Keywords for ROS 2
        ros2_keywords = [
            'node', 'topic', 'service', 'action', 'parameter', 'rclpy', 'rclcpp',
            'publisher', 'subscriber', 'launch', 'urdf', 'tf', 'ros2', 'rmw', 'dds',
            'qos', 'message', 'package', 'workspace', 'colcon', 'ament'
        ]

        # Keywords for Simulation
        simulation_keywords = [
            'gazebo', 'unity', 'isaac', 'simulation', 'sdf', 'physics', 'model',
            'world', 'sensor', 'plugin', 'rendering', 'collision', 'dynamics',
            'digital twin', 'domain randomization', 'synthetic data'
        ]

        # Keywords for VLA
        vla_keywords = [
            'vision', 'language', 'action', 'vqa', 'vlm', 'reasoning', 'grounding',
            'whisper', 'llm', 'planning', 'multi-step', 'perception', 'nlp',
            'object detection', 'pose estimation', 'task decomposition'
        ]

        # Count keyword matches
        ros2_score = sum(1 for keyword in ros2_keywords if keyword in topic_lower)
        simulation_score = sum(1 for keyword in simulation_keywords if keyword in topic_lower)
        vla_score = sum(1 for keyword in vla_keywords if keyword in topic_lower)

        # Return domain with highest score
        scores = {'ros2': ros2_score, 'simulation': simulation_score, 'vla': vla_score}
        return max(scores, key=scores.get) if max(scores.values()) > 0 else 'ros2'

    def _select_best_agent(self, topic: str) -> Union[ROS2Agent, SimulationAgent, VLAAgent]:
        """Select the best agent based on topic content"""
        return self.agents[self._infer_domain(topic)]

    def process_ros2_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request specifically for the ROS 2 agent"""
        return self.ros2_agent.process_request(request)

    def process_simulation_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request specifically for the simulation agent"""
        return self.simulation_agent.process_request(request)

    def process_vla_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request specifically for the VLA agent"""
        return self.vla_agent.process_request(request)

    def get_agent_capabilities(self) -> Dict[str, Any]:
        """Return information about each agent's capabilities"""
        return {
            'ros2_agent': {
                'description': 'Specialized in ROS 2 architecture, nodes, topics, services, actions, and robot-specific implementations',
                'intents': ['explain', 'example', 'architecture', 'best_practices'],
                'topics': ['nodes', 'topics', 'services', 'actions', 'rclpy', 'urdf', 'tf2', 'navigation', 'control']
            },
            'simulation_agent': {
                'description': 'Specialized in Gazebo, Unity, Isaac Sim, and general simulation concepts for robotics',
                'intents': ['explain', 'example', 'setup', 'best_practices'],
                'topics': ['gazebo', 'unity', 'isaac_sim', 'physics', 'sensors', 'plugins', 'digital_twin', 'domain_randomization']
            },
            'vla_agent': {
                'description': 'Specialized in Vision-Language-Action integration, reasoning, and multi-modal robotics',
                'intents': ['explain', 'example', 'reasoning_framework', 'best_practices'],
                'topics': ['vision', 'language', 'action', 'vqa', 'vlm', 'reasoning', 'whisper', 'llm_planning']
            }
        }

    def chat(self, message: str) -> Dict[str, Any]:
        """Simple chat interface that automatically routes messages to appropriate agents"""
        # Determine the most relevant agent based on message content
        inferred_domain = self._infer_domain(message)
        agent = self.agents[inferred_domain]

        # Create a request based on the message
        request = {
            'domain': inferred_domain,
            'intent': 'explain',
            'topic': message,
            'details': {}
        }

        return agent.process_request(request)