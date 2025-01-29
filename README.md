Open-source robot vision library for picking up trash.

**Supported Hardware:** Only Brachiio arm at the moment.

### Installation

If you're experienced, you can setup the environment via CLI (not recommended)

Jupyter Notebook is a headache so I recommend using the Graphical User Interface (GUI) to setup the environment.

1. Go to `computer_vision.ipynb` file and press `select kernel` on the top right corner.
2. Select `Select Another Kernel` -> `Python Environments...` -> `+ Create New Environment` -> `Venv`
3. Choose the option that uses Python 3.12 (best for pytorch)

**How to install dependencies**
Run the first cell in `computer_vision.ipynb` to install the dependencies.

### Dataset

The dataset spans six classes: glass, paper, cardboard, plastic, metal, and trash. Currently, the dataset consists of 2527 images:

- 501 glass
- 594 paper
- 403 cardboard
- 482 plastic
- 410 metal
- 137 trash

Credit: https://github.com/garythung/trashnet