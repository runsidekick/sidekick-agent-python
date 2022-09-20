<p align="center">
  <img width="30%" height="30%" src="https://4750167.fs1.hubspotusercontent-na1.net/hubfs/4750167/Sidekick%20OS%20repo/logo-1.png">
</p>
<p align="center">
  Sidekick Python Agent
</p>

<p align="center">
    <a href="https://github.com/runsidekick/sidekick" target="_blank"><img src="https://img.shields.io/github/license/runsidekick/sidekick?style=for-the-badge" alt="Sidekick Licence" /></a>&nbsp;
    <a href="https://www.runsidekick.com/discord-invitation?utm_source=sidekick-python-readme" target="_blank"><img src="https://img.shields.io/discord/958745045308174416?style=for-the-badge&logo=discord&label=DISCORD" alt="Sidekick Discord Channel" /></a>&nbsp;
    <a href="https://www.runforesight.com?utm_source=sidekick-python-readme" target="_blank"><img src="https://img.shields.io/badge/Monitored%20by-Foresight-%239900F0?style=for-the-badge" alt="Foresight monitoring" /></a>&nbsp;
    <a href="https://app.runsidekick.com/sandbox?utm_source=sidekick-python-readme" target="_blank"><img src="https://img.shields.io/badge/try%20in-sandbox-brightgreen?style=for-the-badge" alt="Sidekick Sandbox" /></a>&nbsp;
    
</p>

<a name="readme-top"></a>

<div align="center">
    <a href="https://github.com/runsidekick/sidekick"><strong>Sidekick Main Repository »</strong></a>
</div>

<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#what-is-sidekick">What is Sidekick?</a>
      <ul>
        <li><a href="#sidekick-actions">Sidekick Actions</a></li>
      </ul>
    </li>
    <li>
      <a href="#sidekick-python-agent">Sidekick Python Agent</a>
    </li>
    <li>
      <a href="#usage">Usage</a>
    </li>
    <li>
      <a href="#build">Build the agent</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
      </ul>
    </li>
    <li>
      <a href="#official-sidekick-agents">Official Sidekick Agents</a>
    </li>
    <li>
      <a href="#resources">Resources</a>
    </li>
    <li><a href="#questions-problems-suggestions">Questions? Problems? Suggestions?</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

## What is Sidekick?
Sidekick is a live application debugger that lets you troubleshoot your applications while they keep on running.

Add dynamic logs and put non-breaking breakpoints in your running application without the need of stopping & redeploying.

Sidekick Open Source is here to allow self-hosting and make live debugging more accessible. Built for everyone who needs extra information from their running applications. 
<p align="center">
  <img width="70%" height="70%" src="https://4750167.fs1.hubspotusercontent-na1.net/hubfs/4750167/Sidekick%20OS%20repo/HowSidekickWorks.gif">
</p>


##### Sidekick Actions:
Sidekick has two major actions; Tracepoints & Logpoints.

- A **tracepoint** is a non-breaking remote breakpoint. In short, it takes a snapshot of the variables when the code hits that line.
- **Logpoints** open the way for dynamic(on-demand) logging to Sidekick users. Replacing traditional logging with dynamic logging has the potential to lower stage sizes, costs, and time for log searching while adding the ability to add new logpoints without editing the source code, redeploying, or restarting the application.

Supported runtimes: Java, Python, Node.js

To learn more about Sidekick features and capabilities, see our [web page.](https://www.runsidekick.com/?utm_source=sidekick-python-readme)

<p align="center">
  <a href="https://app.runsidekick.com/sandbox?utm_source=github&utm_medium=readme" target="_blank"><img width="345" height="66" src="https://4750167.fs1.hubspotusercontent-na1.net/hubfs/4750167/Sidekick%20OS%20repo/try(1)%201.png"></a>
</p>

<p align="center">
  <a href="https://www.runsidekick.com/discord-invitation?utm_source=sidekick-python-readme" target="_blank"><img width="40%" height="40%" src="https://4750167.fs1.hubspotusercontent-na1.net/hubfs/4750167/Sidekick%20OS%20repo/joindiscord.png"></a>
</p>
<div align="center">
    <a href="https://www.runsidekick.com/?utm_source=sidekick-python-readme"><strong>Learn More »</strong></a>
</div>
<p align="right">(<a href="#readme-top">back to top</a>)</p>




# Sidekick Python Agent

Sidekick Python agent allows you to inject tracepoints (non-breaking breakpoints) and logpoints dynamically to capture call stack snapshots (with variables) and add log messages on the fly without code modification, re-build and re-deploy. So it helps you, your team, and your organization to reduce MTTR (Minimum Time to Repair/Resolve).

To achieve this, Sidekick Python Agent makes use of [Google Python Cloud Debugger Agent's](https://github.com/GoogleCloudPlatform/cloud-debug-python) breakpoint implementations under the hood.

The advantage of Sidekick over classical APM solutions is that, Sidekick

  - can debug and trace any location (your code base or 3rd party dependency) in your application, not just the external (DB, API, etc ...) calls like APM solutions
  - has zero overhead when you don't have any tracepoint or logpoint but APMs have always
  - doesn't produce too much garbage data because it collects data only at the certain points you specified as long as that point (tracepoint/logpoint) is active


## Usage

Follow the below steps to install Sidekick Agent Python to your application.

- Install the latest Sidekick agent: ```pip install sidekick-agent-python```

Configure the agent via [exporting environment variables](https://docs.runsidekick.com/installation/installing-agents/python/installation#configure-by-environment-variables?utm_source=sidekick-python-readme) or [creating .env file](https://docs.runsidekick.com/installation/installing-agents/python/installation#configure-by-.env-file?utm_source=sidekick-python-readme) and load it in source code.


[Docs](https://docs.runsidekick.com/installation/installing-agents/python?utm_source=sidekick-python-readme)

**ARM64 & M1 support:** Currently ARM64 packages are not published to PyPI directory. They will be published soon and you can build the agent yourself to make use of it on an ARM machine.


## Build

##### Prerequisites
- pipenv

Activate pipenv with the following command and install dependencies mentioned in Pipfile.

```
pipenv shell
```
```
pipenv install
```

Build tracepointdebug.

Check if "setup.cfg" file is created or not

```
./build.sh
```

Check if build directory is created or not. If it is not created, run the following command to generate the source and the distribution binary.

```
./build_tools/build_wheels.sh
```

## Debugging the agent

To debug Sidekick Python Agent, add "build/lib.*/tracepointdebug" by creating a soft link in the application directory and configure your app according to Sidekick docs. 
Make sure your project's Python version is the same with Sidekick Python Agent's version.


##  Official Sidekick Agents

- [Java](https://github.com/runsidekick/sidekick-agent-java)
- [Node.js](https://github.com/runsidekick/sidekick-agent-nodejs)
- [Python](https://github.com/runsidekick/sidekick-agent-python)

## Resources:

- [Documentation](https://docs.runsidekick.com/?utm_source=sidekick-python-readme)
- [Community](https://github.com/runsidekick/sidekick/discussions)
- [Discord](https://www.runsidekick.com/discord-invitation?utm_source=sidekick-python-readme)
- [Contributing](https://github.com/runsidekick/sidekick/blob/master/CONTRIBUTING.md)
- [Sidekick Main Repository](https://github.com/runsidekick/sidekick)

## Questions? Problems? Suggestions?

To report a bug or request a feature, create a [GitHub Issue](https://github.com/runsidekick/sidekick-agent-python/issues). Please ensure someone else has not created an issue for the same topic.

<p align="right">(<a href="#readme-top">back to top</a>)</p>

## Contact

[Reach out on the Discord](https://www.runsidekick.com/discord-invitation?utm_source=sidekick-python-readme). A fellow community member or Sidekick engineer will be happy to help you out.

<p align="right">(<a href="#readme-top">back to top</a>)</p>