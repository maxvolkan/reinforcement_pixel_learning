# Vision-Based Reinforcement Learning

This project experiments with learning from raw screen pixels using
computer vision and reinforcement learning techniques.

## Setup

First, clone the repo.

Then create and activate a Python virtual environment, then install dependencies.

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python nexus_bot.py
```

## Notes

- once you run the python code, fit your rotmg game window to the Rotmg Window View that python opens.
- game resolution was tested in Windowed mode at 1512x982
- uses screen capture only (does not access memory)
- intended for learning reinforcement learning

## Current stage
- ~~basic keyboard control and window view~~
- automatic window view and random movement
- punish and reward system (need to figure out how to teleport player back to start)
