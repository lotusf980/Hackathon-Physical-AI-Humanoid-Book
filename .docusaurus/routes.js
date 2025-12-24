import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/Hackathon-Physical-AI-Humanoid-Book/',
    component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/', 'de3'),
    exact: true
  },
  {
    path: '/Hackathon-Physical-AI-Humanoid-Book/',
    component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/', '008'),
    routes: [
      {
        path: '/Hackathon-Physical-AI-Humanoid-Book/',
        component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/', '5ca'),
        routes: [
          {
            path: '/Hackathon-Physical-AI-Humanoid-Book/',
            component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/', 'e26'),
            routes: [
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/capstone/guide/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/capstone/guide/', 'bc0'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/architecture/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/architecture/', 'dfd'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/code_examples/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/code_examples/', 'e9a'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/introduction/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/introduction/', '274'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/packages/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/packages/', 'df8'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/urdf/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-1-ros2/urdf/', '71d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/introduction/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/introduction/', 'e3f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/physics/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/physics/', 'a36'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/sensors/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/sensors/', '796'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/setup/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/setup/', '4f4'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/unity/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-2-gazebo/unity/', 'ddf'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/introduction/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/introduction/', '411'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/isaac_sim/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/isaac_sim/', '579'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/rl/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/rl/', '2d9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/sim2real/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/sim2real/', '820'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/synthetic_data/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/synthetic_data/', 'edf'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/vslam/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-3-isaac/vslam/', 'd7f'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/introduction/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/introduction/', 'b60'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/llm_planning/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/llm_planning/', '96c'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/reasoning/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/reasoning/', 'c8b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/whisper/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/module-4-vla/whisper/', '4d9'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/Hackathon-Physical-AI-Humanoid-Book/',
                component: ComponentCreator('/Hackathon-Physical-AI-Humanoid-Book/', '108'),
                exact: true,
                sidebar: "tutorialSidebar"
              }
            ]
          }
        ]
      }
    ]
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
