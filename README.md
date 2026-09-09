# CBP OIT Traveler Processing Sandbox — Fictional Security Demo

> **Synthetic demonstration repository only.**
> This repository contains fictional code, fictional identities, and intentionally imperfect security logic for a Cognition Devin Security Swarm demonstration. It is not derived from CBP source code, does not represent a real CBP system, and contains no operational government information.

## Scenario

A fictional CBP Office of Information and Technology engineering team is prototyping a traveler-processing workflow composed of three services:

- **Gateway** — authenticates users and forwards requests to internal services.
- **Traveler Service** — stores synthetic traveler profiles and risk data.
- **Inspection Service** — manages inspection cases and release decisions.

OIT wants an independent review before the prototype is promoted into a more realistic test environment.

The review should focus on issues that are easy to miss when looking at only one file or service, including authentication and authorization, trust boundaries, business-logic flaws, sensitive-data exposure, and chained weaknesses spanning multiple services.

## Suggested Devin Security Swarm prompt

Review this repository as if you are supporting a federal engineering team preparing a prototype for security review. Use parallel agents to investigate different parts of the codebase. Identify vulnerabilities and business-logic weaknesses that require reasoning across files or services, especially authentication failures, authorization bypasses, unsafe trust boundaries, sensitive-data exposure, and chained exploit paths.

For each finding:
1. assign severity,
2. identify the affected files/functions,
3. explain the cross-service data flow,
4. describe the impact in plain English,
5. recommend a concrete remediation.

Do not modify the code until you have presented the findings.
