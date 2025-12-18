import React from 'react';
import ComponentCreator from '@docusaurus/ComponentCreator';

export default [
  {
    path: '/docs',
    component: ComponentCreator('/docs', '95e'),
    routes: [
      {
        path: '/docs',
        component: ComponentCreator('/docs', '232'),
        routes: [
          {
            path: '/docs',
            component: ComponentCreator('/docs', '21c'),
            routes: [
              {
                path: '/docs/',
                component: ComponentCreator('/docs/', 'b98'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/capstone/guide',
                component: ComponentCreator('/docs/capstone/guide', 'd43'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/architecture',
                component: ComponentCreator('/docs/module-1-ros2/architecture', '288'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/code_examples',
                component: ComponentCreator('/docs/module-1-ros2/code_examples', '038'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/introduction',
                component: ComponentCreator('/docs/module-1-ros2/introduction', '28b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/packages',
                component: ComponentCreator('/docs/module-1-ros2/packages', 'ff5'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-1-ros2/urdf',
                component: ComponentCreator('/docs/module-1-ros2/urdf', '6d3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-gazebo/introduction',
                component: ComponentCreator('/docs/module-2-gazebo/introduction', 'f88'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-gazebo/physics',
                component: ComponentCreator('/docs/module-2-gazebo/physics', '32e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-gazebo/sensors',
                component: ComponentCreator('/docs/module-2-gazebo/sensors', 'be3'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-gazebo/setup',
                component: ComponentCreator('/docs/module-2-gazebo/setup', '3a1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-2-gazebo/unity',
                component: ComponentCreator('/docs/module-2-gazebo/unity', '520'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-isaac/introduction',
                component: ComponentCreator('/docs/module-3-isaac/introduction', '312'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-isaac/isaac_sim',
                component: ComponentCreator('/docs/module-3-isaac/isaac_sim', '74e'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-isaac/rl',
                component: ComponentCreator('/docs/module-3-isaac/rl', '83d'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-isaac/sim2real',
                component: ComponentCreator('/docs/module-3-isaac/sim2real', 'a10'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-isaac/synthetic_data',
                component: ComponentCreator('/docs/module-3-isaac/synthetic_data', '0f6'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-3-isaac/vslam',
                component: ComponentCreator('/docs/module-3-isaac/vslam', '556'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/introduction',
                component: ComponentCreator('/docs/module-4-vla/introduction', 'e9b'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/llm_planning',
                component: ComponentCreator('/docs/module-4-vla/llm_planning', '6a1'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/reasoning',
                component: ComponentCreator('/docs/module-4-vla/reasoning', '847'),
                exact: true,
                sidebar: "tutorialSidebar"
              },
              {
                path: '/docs/module-4-vla/whisper',
                component: ComponentCreator('/docs/module-4-vla/whisper', 'b7b'),
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
    path: '/',
    component: ComponentCreator('/', 'e5f'),
    exact: true
  },
  {
    path: '*',
    component: ComponentCreator('*'),
  },
];
