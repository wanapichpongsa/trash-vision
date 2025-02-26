TrashVision is an open-source robot vision library for waste management.

**Research Aim**:
1. Find out what quality (angle, distance, lighting, etc.) and quantity of images are needed for a robot to be autonomous (>95% accuracy)
2. How to accurately communicate the location of object and the necessary movement by the robot arm to pick it up.
3. **Bonus:** Discuss how close we are to robots that can autonomously pick up trash in landfills, and explicitly define what is needed to make this a reality. (Hard, needs to ignore irrelevant stuff)

**Supported Hardware:** Only Brachiio arm at the moment.

### Installation

If you're experienced, you can setup the environment via CLI (not recommended)

Jupyter Notebook is a headache so I recommend using the Graphical User Interface (GUI) of your IDE (e.g., VSCode) to setup the environment.

1. Go to `computer_vision.ipynb` file and press `select kernel` on the top right corner.
2. Select `Select Another Kernel` -> `Python Environments...` -> `+ Create New Environment` -> `Venv`
3. Choose the option that uses Python 3.12 (best for pytorch)

**How to install dependencies**
Run the first cell in `computer_vision.ipynb` to install the dependencies.

### Acknowledgements

Pre-existing deep learning trash sorting robot: https://github.com/bandofpv/Trash-Sorting-Robot

The dataset spans six classes: glass, paper, cardboard, plastic, metal, and trash. Currently, the dataset consists of 2527 images:

- 501 glass
- 594 paper
- 403 cardboard
- 482 plastic
- 410 metal
- 137 trash

Credit: https://github.com/garythung/trashnet