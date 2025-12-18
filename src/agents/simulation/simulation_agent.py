"""
Simulation Agent for Physical AI & Humanoid Robotics

This agent specializes in explaining simulation concepts, tools, and best practices
for humanoid robotics applications.
"""

from typing import Dict, Any, List
import json


class SimulationAgent:
    """Specialized agent for simulation concepts in humanoid robotics"""

    def __init__(self):
        self.knowledge_base = {
            "gazebo": {
                "physics": "Gazebo uses ODE (Open Dynamics Engine), Bullet, or DART physics engines to simulate realistic physics interactions including gravity, collision, and friction.",
                "models": "3D models of robots and environments created in SDF (Simulation Description Format) that define visual, collision, and inertial properties.",
                "sensors": "Simulated sensors including cameras, LiDAR, IMU, force/torque sensors, and GPS with realistic noise models.",
                "plugins": "Custom plugins that extend Gazebo functionality, written in C++ or Python to control robot behavior or modify simulation."
            },
            "unity": {
                "rendering": "High-fidelity rendering with realistic lighting, materials, and visual effects for photorealistic simulation.",
                "xr": "Extended reality support for VR/AR applications allowing immersive interaction with simulated environments.",
                "physics": "Unity's physics engine provides realistic collision detection and response with configurable material properties.",
                "ros_integration": "ROS# and other packages enabling communication between Unity simulation and ROS 2 systems."
            },
            "isaac_sim": {
                "photorealistic": "NVIDIA Isaac Sim provides photorealistic rendering using RTX technology for training AI models.",
                "domain_randomization": "Technique for varying simulation parameters to make AI models more robust to real-world variations.",
                "synthetic_data": "Generation of labeled training data from simulation environments for AI model training.",
                "robot_simulation": "High-fidelity robot simulation with accurate dynamics, sensors, and control systems."
            },
            "concepts": {
                "digital_twin": "A digital twin is a virtual replica of a physical system that mirrors its properties, state, and behavior in real-time.",
                "sensor_simulation": "Accurate simulation of real-world sensors including noise, latency, and environmental effects.",
                "physics_fidelity": "The accuracy of physical simulation including gravity, collision, friction, and material properties.",
                "real_time_factor": "Ratio of simulation time to real time. RTF=1.0 means simulation runs at real-time speed."
            }
        }

    def explain_concept(self, concept: str) -> str:
        """Explain a specific simulation concept"""
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

        return f"I don't have specific information about '{concept}' in my simulation knowledge base. Please ask about Gazebo, Unity, Isaac Sim, or general simulation concepts."

    def provide_example(self, topic: str) -> str:
        """Provide a practical example for a simulation topic"""
        topic_lower = topic.lower().strip()

        examples = {
            "gazebo_world": """<?xml version="1.0" ?>
<sdf version="1.6">
  <world name="default">
    <!-- A global light source -->
    <include>
      <uri>model://sun</uri>
    </include>

    <!-- A ground plane -->
    <include>
      <uri>model://ground_plane</uri>
    </include>

    <!-- Your robot model -->
    <include>
      <uri>model://my_robot</uri>
    </include>

    <!-- Physics engine configuration -->
    <physics type="ode">
      <max_step_size>0.001</max_step_size>
      <real_time_factor>1</real_time_factor>
      <real_time_update_rate>1000</real_time_update_rate>
    </physics>
  </world>
</sdf>
""",
            "gazebo_plugin": """#include <gazebo/gazebo.hh>
#include <gazebo/physics/physics.hh>
#include <gazebo/common/common.hh>

namespace gazebo
{
  class MyRobotPlugin : public ModelPlugin
  {
    public: void Load(physics::ModelPtr _parent, sdf::ElementPtr /*_sdf*/)
    {
      // Store the model pointer for convenience
      this->model = _parent;

      // Listen to the update event
      this->updateConnection = event::Events::ConnectWorldUpdateBegin(
          std::bind(&MyRobotPlugin::OnUpdate, this));
    }

    public: void OnUpdate()
    {
      // Apply a small linear velocity to the model
      this->model->SetLinearVel(math::Vector3(0.01, 0, 0));
    }

    private: physics::ModelPtr model;
    private: event::ConnectionPtr updateConnection;
  };

  // Register this plugin with the simulator
  GZ_REGISTER_MODEL_PLUGIN(MyRobotPlugin)
}
""",
            "sensor_configuration": """# Sensor configuration for a humanoid robot
# Example: IMU sensor in URDF/SDF
<sensor name="imu_sensor" type="imu">
  <always_on>true</always_on>
  <update_rate>100</update_rate>
  <topic>imu/data</topic>
  <imu>
    <angular_velocity>
      <x>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </x>
      <y>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </y>
      <z>
        <noise type="gaussian">
          <mean>0.0</mean>
          <stddev>2e-4</stddev>
        </noise>
      </z>
    </angular_velocity>
  </imu>
</sensor>
""",
            "unity_ros_integration": """using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using RosSharp;

public class RobotController : MonoBehaviour
{
    public string rosBridgeServerUrl = "ws://192.168.1.1:9090";
    private RosSocket rosSocket;

    void Start()
    {
        RosBridgeClient.RosSocket.Bootstrap();
        rosSocket = new RosSocket(new RosSharp.Communication.Protocol.WebSocketNET(rosBridgeServerUrl));

        // Subscribe to a topic
        rosSocket.Subscribe<geometry_msgs.Twist>("/cmd_vel", ReceiveTwist);
    }

    void ReceiveTwist(geometry_msgs.Twist message)
    {
        // Process the received message
        Vector3 linear = new Vector3((float)message.linear.x, (float)message.linear.y, (float)message.linear.z);
        transform.Translate(linear * Time.deltaTime);
    }
}
"""
        }

        for key, example in examples.items():
            if topic_lower in key:
                return example

        return f"No example available for '{topic}'. Available examples: gazebo_world, gazebo_plugin, sensor_configuration, unity_ros_integration"

    def get_simulation_setup(self, platform: str) -> Dict[str, Any]:
        """Return setup information for different simulation platforms"""
        platform_lower = platform.lower().strip()

        setups = {
            "gazebo": {
                "title": "Gazebo Simulation Setup",
                "description": "Gazebo is a robot simulator with realistic physics and rendering capabilities.",
                "components": [
                    "Install Gazebo with ROS 2 integration",
                    "Create SDF models for your robot",
                    "Configure physics parameters",
                    "Add sensors and plugins as needed",
                    "Launch with appropriate world file"
                ],
                "best_practices": [
                    "Use appropriate physics step size for stability",
                    "Configure QoS settings for sensor data",
                    "Use model database for common objects",
                    "Implement proper plugin interfaces"
                ]
            },
            "unity": {
                "title": "Unity Simulation Setup",
                "description": "Unity provides high-fidelity rendering for photorealistic simulation.",
                "components": [
                    "Install Unity with appropriate packages",
                    "Import robot models in FBX or other formats",
                    "Set up physics materials and colliders",
                    "Configure lighting and rendering settings",
                    "Integrate with ROS using ROS# or similar packages"
                ],
                "best_practices": [
                    "Use appropriate polygon counts for performance",
                    "Configure realistic material properties",
                    "Implement LOD systems for complex scenes",
                    "Use occlusion culling for large environments"
                ]
            },
            "isaac_sim": {
                "title": "Isaac Sim Setup",
                "description": "NVIDIA Isaac Sim provides photorealistic simulation for AI training.",
                "components": [
                    "Install Isaac Sim with Omniverse",
                    "Import robot models in USD format",
                    "Configure RTX rendering settings",
                    "Set up domain randomization parameters",
                    "Integrate with Isaac ROS packages"
                ],
                "best_practices": [
                    "Use RTX features for realistic rendering",
                    "Implement domain randomization for robustness",
                    "Generate diverse synthetic data",
                    "Use Omniverse for collaborative simulation"
                ]
            }
        }

        return setups.get(platform_lower, {
            "title": f"{platform} Setup",
            "description": f"Information about setting up {platform} for robotics simulation.",
            "components": ["Platform-specific setup information"],
            "best_practices": ["Platform-specific best practices"]
        })

    def get_best_practices(self) -> List[str]:
        """Return simulation best practices for humanoid robotics"""
        return [
            "Start with simple models and gradually add complexity",
            "Validate simulation results against real-world data",
            "Use appropriate physics parameters for your robot",
            "Implement realistic sensor noise models",
            "Optimize simulation for real-time performance",
            "Use domain randomization for robust AI training",
            "Implement proper logging and visualization tools",
            "Consider computational requirements for your hardware"
        ]

    def process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process a request to the simulation agent"""
        intent = request.get("intent", "explain")
        topic = request.get("topic", "")
        details = request.get("details", {})

        if intent == "explain":
            explanation = self.explain_concept(topic)
            return {
                "type": "explanation",
                "topic": topic,
                "content": explanation,
                "source": "simulation_agent"
            }
        elif intent == "example":
            example = self.provide_example(topic)
            return {
                "type": "example",
                "topic": topic,
                "content": example,
                "source": "simulation_agent"
            }
        elif intent == "setup":
            platform = details.get("platform", "general")
            setup_info = self.get_simulation_setup(platform)
            return {
                "type": "setup_info",
                "platform": platform,
                "content": setup_info,
                "source": "simulation_agent"
            }
        elif intent == "best_practices":
            practices = self.get_best_practices()
            return {
                "type": "best_practices",
                "content": practices,
                "source": "simulation_agent"
            }
        else:
            return {
                "type": "error",
                "content": f"Unknown intent: {intent}",
                "source": "simulation_agent"
            }