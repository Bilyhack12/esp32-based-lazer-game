# ESP32 Laser Shooting Game

## Overview

This project implements an exciting laser shooting game using ESP32 microcontrollers. The game features a gun that shoots a laser beam aimed at a board equipped with a light-dependent resistor (LDR). The objective is to hit the center of the board. Upon a successful hit, the game signals the player with a buzzer noise and a blinking light.

## Components

- **ESP32 Microcontroller**: The brain of the game, controlling the laser, LDR, and communication with other devices.
- **Laser Diode**: Emits a laser beam when activated.
- **Light-Dependent Resistor (LDR)**: Detects the impact of the laser beam.
- **Buzzer**: Produces sound effects, such as a hit notification.
- **Bluetooth Module**: Facilitates communication between the gun and the board.

## How It Works

1. **Gun Operation**:
   - The gun emits a laser beam towards the board when the trigger is pressed.
   - The laser beam hits the board, where the LDR detects the impact.

2. **Board Operation**:
   - The board is equipped with an LDR to sense the laser beam.
   - When a hit is detected, the buzzer produces a sound, and a light blinks to indicate a successful hit.

## Communication

- The gun and the board communicate using Bluetooth Low Energy (BLE) technology.
- The gun sends a "shoot" command to the board when the trigger is pressed.
- The board acknowledges a successful hit by sending a response back to the gun.

## How to Play

1. **Gun Operation**:
   - Press the trigger to shoot the laser beam.
   - Aim for the center of the board to score a hit.

2. **Board Operation**:
   - Detects the laser beam impact using the LDR.
   - Produces a buzzer sound and blinks a light to indicate a successful hit.

## Project Files

- **gun.py**: Code for the gun controller, handling laser emission, Bluetooth communication, and trigger events.
- **board.py**: Code for the board controller, managing LDR readings, buzzer sounds, light blinks, and Bluetooth communication.

## Setup Instructions

1. Flash the `gun.py` script on one ESP32 device (gun) and the `board.py` script on another ESP32 device (board).
2. Connect the laser diode to the gun and the LDR to the board as per the circuit diagram.
3. Power up both devices.
4. Pair the gun and the board via Bluetooth.
5. Start the game by pressing the trigger on the gun.
6. Aim for the center of the board to score hits and enjoy the game!

## Notes

- Ensure proper safety precautions when using lasers.
- Modify the code and circuit as needed based on your specific hardware components and requirements.

Have fun playing the ESP32 Laser Shooting Game! 🎯🔫
