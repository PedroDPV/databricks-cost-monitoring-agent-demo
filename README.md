# Databricks Cost Monitoring Agent Demo

This is a portfolio and demo project that implements a cost monitoring agent for Databricks style workloads, inspired by an agent I built professionally on top of the system.billing.usage table.

Disclaimer: all data used in this project is synthetically generated, see src/billing_data_generator.py. No real workspace, account, or billing data is used anywhere in this repository. This is a simplified sample meant to illustrate architecture and coding practices, not a production system.

## What it does

Generates synthetic Databricks billing usage records, shaped like system.billing.usage rows, including workspace, SKU, cluster, DBUs consumed, and estimated cost.

Summarizes total cost and DBUs per cluster.

Detects cost anomalies by flagging cluster-days whose cost is significantly above that cluster's own historical average.

Generates an automated Markdown report summarizing costs and anomalies, similar in spirit to the automated pipeline documentation generator I built alongside the real agent.

## Project structure

src/config.py: environment based configuration with no hardcoded secrets.

src/billing_data_generator.py: synthetic billing usage generator.

src/cost_analyzer.py: cost summarization and anomaly detection logic.

src/report_generator.py: Markdown report generator.

src/agent.py: orchestrates the full run.

tests: unit tests for the cost analyzer.

SECURITY.md: security practices applied in this demo.

## Running locally

Create a virtual environment and install dependencies from requirements.txt.

Copy .env.example to .env and adjust values if needed.

Run the agent with: python -m src.agent

The generated report will be written to the reports folder by default.

## Tech stack

Python, pandas, pytest, python-dotenv, tabulate.

## About this repository

This project is part of my professional portfolio and demonstrates the kind of cost monitoring and FinOps oriented work described in my LinkedIn profile and resume. It is a self-contained sample built specifically for this purpose using synthetic data, not an export of proprietary employer code.
