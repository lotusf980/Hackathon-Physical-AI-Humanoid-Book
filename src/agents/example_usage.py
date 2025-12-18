"""
Example usage of the Physical AI & Humanoid Robotics Agents
"""

from agent_manager import AgentManager


def main():
    # Initialize the agent manager
    agent_manager = AgentManager()

    print("Physical AI & Humanoid Robotics Agents Example")
    print("=" * 50)

    # Example 1: Direct ROS 2 agent usage
    print("\n1. Direct ROS 2 Agent Usage:")
    ros2_request = {
        'domain': 'ros2',
        'intent': 'explain',
        'topic': 'nodes'
    }
    response = agent_manager.process_ros2_request(ros2_request)
    print(f"Topic: {response['topic']}")
    print(f"Response: {response['content'][:200]}...")

    # Example 2: Direct Simulation agent usage
    print("\n2. Direct Simulation Agent Usage:")
    simulation_request = {
        'domain': 'simulation',
        'intent': 'example',
        'topic': 'gazebo_world'
    }
    response = agent_manager.process_simulation_request(simulation_request)
    print(f"Topic: {response['topic']}")
    print(f"Response preview: {response['content'][:100]}...")

    # Example 3: Direct VLA agent usage
    print("\n3. Direct VLA Agent Usage:")
    vla_request = {
        'domain': 'vla',
        'intent': 'reasoning_framework',
        'topic': 'multi-step reasoning'
    }
    response = agent_manager.process_vla_request(vla_request)
    print(f"Topic: {response['type']}")
    print(f"Framework title: {response['content']['title']}")

    # Example 4: Auto-routing based on content
    print("\n4. Auto-routing Example:")
    auto_request = {
        'intent': 'explain',
        'topic': 'What is a ROS 2 node?'
    }
    response = agent_manager.route_request(auto_request)
    print(f"Detected domain: {response['source']}")
    print(f"Response: {response['content'][:200]}...")

    # Example 5: Chat interface
    print("\n5. Chat Interface Example:")
    chat_response = agent_manager.chat("How do I create a publisher in ROS 2?")
    print(f"Detected domain: {response['source']}")
    print(f"Response preview: {chat_response['content'][:100]}...")

    # Example 6: Get capabilities
    print("\n6. Agent Capabilities:")
    capabilities = agent_manager.get_agent_capabilities()
    for agent_name, info in capabilities.items():
        print(f"\n{agent_name}:")
        print(f"  Description: {info['description']}")
        print(f"  Intents: {', '.join(info['intents'])}")
        print(f"  Topics: {', '.join(info['topics'][:3])}...")


if __name__ == "__main__":
    main()