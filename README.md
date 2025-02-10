# Transfer Learning Project

## Setup Instructions

1. **Clone the repository:**
    ```sh
    git clone https://github.com/FilipeVOl/transfer-learning.git
    cd transfer-learning
    ```

2. **Create and activate a virtual environment:**
    ```sh
    python -m venv myenv
    source myenv/bin/activate  # On Windows use `myenv\Scripts\activate`
    ```

3. **Install the necessary libraries:**
    ```sh
    pip install -r requirements.txt
    ```

4. **Add the image dataset:**
    - Place your image dataset inside the repository. The dataset should be organized in subfolders under a main folder (e.g., `PetImages`).
    - Update the `root` variable in `transfer.py` to match the name of your dataset folder if it is different from `PetImages`.

5. **Run the script:**
    ```sh
    python transfer.py
    ```

## Notes

- Ensure that your dataset is structured with subfolders for each category of images.
- The script will automatically split the dataset into training, validation, and test sets.
- The results, including validation loss and accuracy, will be displayed after training.
