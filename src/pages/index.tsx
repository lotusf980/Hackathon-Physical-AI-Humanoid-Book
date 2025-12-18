import React from 'react';
import clsx from 'clsx';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import BookChatbot from '@site/src/components/BookChatbot';
import styles from './index.module.css';

function HomepageHeader() {
  const {siteConfig} = useDocusaurusContext();
  return (
    <header className={clsx('hero hero--primary', styles.heroBanner)}>
      <div className="container">
        <h1 className="hero__title">{siteConfig.title}</h1>
        <p className="hero__subtitle">Embodied Intelligence in the Physical World</p>
        <div className={styles.buttons}>
          <Link
            className="button button--secondary button--lg"
            to="/docs">
            Start Reading
          </Link>
          <Link
            className="button button--outline button--lg"
            href="https://github.com/physical-ai-humanoid-robotics-book">
            View GitHub
          </Link>
        </div>
      </div>
    </header>
  );
}

function WhatIsPhysicalAI() {
  return (
    <section className={styles.section}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2>What is Physical AI</h2>
            <p>
              Physical AI represents the convergence of artificial intelligence and physical systems,
              where digital intelligence is embodied in robotic agents that interact with the real world.
              This field addresses the fundamental challenge of bridging the gap between sophisticated
              AI algorithms and their practical deployment in physical humanoid robots, requiring
              seamless integration of perception, reasoning, planning, and action in dynamic environments.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

function WhatYouWillLearn() {
  return (
    <section className={clsx(styles.section, styles.sectionAlt)}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2>What You Will Learn</h2>
            <div className="row">
              <div className="col col--3">
                <h3>ROS 2</h3>
                <p>Master the Robot Operating System 2 architecture, nodes, topics, services, and actions for robust robot control systems.</p>
              </div>
              <div className="col col--3">
                <h3>Gazebo & Unity</h3>
                <p>Build and simulate realistic environments with physics modeling, sensor simulation, and high-fidelity rendering.</p>
              </div>
              <div className="col col--3">
                <h3>NVIDIA Isaac</h3>
                <p>Implement AI perception and navigation using Isaac Sim, synthetic data generation, and Isaac ROS packages.</p>
              </div>
              <div className="col col--3">
                <h3>Vision-Language-Action</h3>
                <p>Develop LLM-powered robotics with voice recognition, multi-step reasoning, and integrated perception-action systems.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function ToolsAndPlatforms() {
  return (
    <section className={styles.section}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2>Tools & Platforms</h2>
            <div className="row">
              <div className="col col--2">
                <div className={styles.toolCard}>
                  <h3>ROS 2</h3>
                  <p>Middleware</p>
                </div>
              </div>
              <div className="col col--2">
                <div className={styles.toolCard}>
                  <h3>Gazebo</h3>
                  <p>Simulation</p>
                </div>
              </div>
              <div className="col col--2">
                <div className={styles.toolCard}>
                  <h3>Unity</h3>
                  <p>Rendering</p>
                </div>
              </div>
              <div className="col col--2">
                <div className={styles.toolCard}>
                  <h3>Isaac Sim</h3>
                  <p>AI Training</p>
                </div>
              </div>
              <div className="col col--2">
                <div className={styles.toolCard}>
                  <h3>Python</h3>
                  <p>Development</p>
                </div>
              </div>
              <div className="col col--2">
                <div className={styles.toolCard}>
                  <h3>LLMs</h3>
                  <p>Planning</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

function CapstoneHighlight() {
  return (
    <section className={clsx(styles.section, styles.sectionAlt)}>
      <div className="container">
        <div className="row">
          <div className="col col--12">
            <h2>Capstone Project</h2>
            <p>
              The capstone project integrates all concepts learned throughout the textbook to build a
              complete simulation of a humanoid robot. Students will create a robot that can:
            </p>
            <ul>
              <li>Hear a voice command through Whisper voice recognition</li>
              <li>Understand it using LLM planning</li>
              <li>Plan a path and navigate obstacles</li>
              <li>Identify objects in the environment</li>
              <li>Interact with the environment appropriately</li>
            </ul>
            <p>
              This comprehensive project demonstrates the complete pipeline from AI models to physical deployment.
            </p>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  const {siteConfig} = useDocusaurusContext();
  return (
    <Layout
      title={`Home`}
      description="Physical AI & Humanoid Robotics - Embodied Intelligence in the Physical World">
      <HomepageHeader />
      <main>
        <WhatIsPhysicalAI />
        <WhatYouWillLearn />
        <ToolsAndPlatforms />
        <CapstoneHighlight />
      </main>
    </Layout>
  );
}