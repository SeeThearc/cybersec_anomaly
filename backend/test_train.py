import os
import sys
from pathlib import Path
import pytest

# Ensure the backend directory is in the path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

# Skip full training in quick tests by default unless explicitly enabled,
# but the user requested "full train.py" testing, so we will execute the pipeline.
# To prevent a 30-minute test run during development, we patch the DATA_LIMIT
# or let it run depending on CI environment variables.

def test_full_training_pipeline():
    """
    Tests the end-to-end ML training pipeline.
    This imports the main function from train.py and executes it.
    """
    from train import main
    
    # Run the main training loop
    try:
        main()
        success = True
    except Exception as e:
        print(f"Training pipeline failed: {e}")
        success = False
        
    assert success == True, "The training pipeline encountered an error during execution."
