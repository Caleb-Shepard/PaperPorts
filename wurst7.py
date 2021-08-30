from git_clone import git_clone
from pathlib import Path
import platform
import tempfile
import shutil
import os

# Assumed constants - here to make updates simple and keep it readable
OUTPUT_JAR_NAME = 'wurst7.jar'
WURST_REPO      = 'https://github.com/Wurst-Imperium/Wurst7'
BRANCH          = 'master'

# Determining the correct output jar is risky and not deterministic :^)
def build_wurst(wurst_directory):
    gradlew_file = None
    gradlew      = None
    # Adjust instructions and build depending on runtime environment platform
    if platform.system()=='Windows':
        gradlew_file = 'gradlew.bat'
        gradlew = f'./{os.path.join(wurst_directory, gradlew_file)}'
    else:
        gradlew_file = 'gradlew'
        gradlew = f'sh {os.path.join(wurst_directory, gradlew_file)}'

    # Get source dependencies or something idk open a pull request if it matters
    os.system(f"{gradlew} genSources")

    # Optional line for eclipse users below. If activated, modify to keep the script
    # from deleting Wurst7/ from tmp; copy or move to a permanent directory.
    # os.system(f"{gradlew} eclipse")

    # Build the project
    os.system(f"{gradlew} build")

    # Locate the jar >:[]
    compiled_jars_dir = os.path.join(
        os.path.join(
            wurst_directory
            'build/libs/'
        )
    )

    compiled_jars = os.listdir(compiled_jars_dir)
    wurst_jar_path = None
    for filename in compiled_jars:
        if '-dev' not in filename and '-sources' not in filename:
            wurst_jar_path = os.path.join(
                wurst_directory, filename
            )

    return wurst_jar_path


if __name__ == '__main__':
    try:
        # Platform Specific Runtime Environment Vars
        tmp_dir = Path("/tmp" if platform.system() == "Darwin" else tempfile.gettempdir())
        starting_directory = os.getcwd()

        # Clone the repo
        os.chdir(tmp_dir)
        git_clone(WURST_REPO)
        wurst_directory = os.path.join(tmp_dir, WURST_REPO.split('/')[-1])
        os.chdir(wurst_directory)

        # Compile
        wurst_jar = build_wurst(wurst_directory, gradlew_file)
    except:
        print("Failure when cloning and building from repository.")

    # Move jar and give output
    try:
        jar_destination = os.path.join(os.getcwd(), OUTPUT_JAR_NAME
        shutil.move(wurst_jar, jar_destination))
        print(f"The compiled wurst7.jar is at {jar_destination}")
    except:
        print(f"Moving compiled {OUTPUT_JAR_NAME} failed.")

    # Clean up
    shutil.rmtree(wurst_directory)
