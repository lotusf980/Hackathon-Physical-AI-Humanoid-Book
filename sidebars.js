// @ts-check

/** @type {import('@docusaurus/plugin-content-docs').SidebarsConfig} */
const sidebars = {
  tutorialSidebar: [
    'index',
    {
      type: 'category',
      label: 'Module 1 - ROS 2',
      items: [
        'module-1-ros2/introduction',
        'module-1-ros2/architecture',
        'module-1-ros2/code_examples',
        'module-1-ros2/urdf',
        'module-1-ros2/packages',
      ],
    },
    {
      type: 'category',
      label: 'Module 2 - Gazebo and Unity',
      items: [
        'module-2-gazebo/introduction',
        'module-2-gazebo/setup',
        'module-2-gazebo/physics',
        'module-2-gazebo/sensors',
        'module-2-gazebo/unity',
      ],
    },
    {
      type: 'category',
      label: 'Module 3 - NVIDIA Isaac',
      items: [
        'module-3-isaac/introduction',
        'module-3-isaac/isaac_sim',
        'module-3-isaac/synthetic_data',
        'module-3-isaac/vslam',
        'module-3-isaac/rl',
        'module-3-isaac/sim2real',
      ],
    },
    {
      type: 'category',
      label: 'Module 4 - Vision-Language-Action',
      items: [
        'module-4-vla/introduction',
        'module-4-vla/whisper',
        'module-4-vla/llm_planning',
        'module-4-vla/reasoning',
      ],
    },
    {
      type: 'category',
      label: 'Capstone Project',
      items: [
        'capstone/guide',
      ],
    },
  ],
};

module.exports = sidebars;