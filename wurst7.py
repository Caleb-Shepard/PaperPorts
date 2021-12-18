import sys
# ! Validate args
if len(sys.argv) != 2:
    print('\nIncorrect number of args. Usage: `wurst7.py BRANCH_NAME`')
    print('Tip: branch names normally correspond to game version. E.G. "1.18" will get the 1.18 branch.\n')
    exit()

# Assumed constants - here to make updates simple and keep it readable
REPO_NAME       = 'Wurst7'
WURST_REPO      = f'https://github.com/Wurst-Imperium/{REPO_NAME}'
BRANCH          = sys.argv[1]
OUTPUT_JAR_NAME = f'wurst7-{BRANCH}.jar' 

from git_clone import git_clone
from pathlib import Path
import platform
import tempfile
import shutil
import os

# Determining the correct output jar is risky and not deterministic :^)
def build_wurst(wurst_directory):
    gradlew_file = None
    gradlew      = None
    # Adjust instructions and build depending on runtime environment platform
    if platform.system()=='Windows':
        gradlew_file = 'gradlew.bat'
        gradlew = f'{os.pathsep}{os.path.join(wurst_directory, gradlew_file)}'
    else:
        gradlew_file = 'gradlew'
        gradlew = f'{os.path.join(wurst_directory, gradlew_file)}'

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
            wurst_directory,
            'build',
            'libs'
        )
    )

    compiled_jars = os.listdir(compiled_jars_dir)
    wurst_jar_path = None
    for filename in compiled_jars:
        if '-dev' not in filename and '-sources' not in filename:
            wurst_jar_path = os.path.join(
                compiled_jars_dir, filename
            )

    return wurst_jar_path


if __name__ == '__main__':

    # Platform Specific Runtime Environment Vars
    #tmp_dir = Path("/tmp") if platform.system() == "Darwin" else tempfile.gettempdir())
    tmp_dir = tempfile.mkdtemp()
    starting_directory = os.getcwd()
    wurst_directory = os.path.join(tmp_dir, REPO_NAME)

    # Clear landing pad XD
    try:
        shutil.rmtree(os.path.join(tmp_dir, REPO_NAME))
    except:
        pass

    # Clone
    os.chdir(tmp_dir)
    git_clone(WURST_REPO, tmp_dir, BRANCH)

    # Compile
    os.chdir(wurst_directory)
    wurst_jar = build_wurst(wurst_directory)

    # Move jar and give output
    jar_destination = os.path.join(starting_directory, OUTPUT_JAR_NAME)
    shutil.move(wurst_jar, jar_destination)
    print(f"\nThe compiled wurst7.jar is at {jar_destination}")

    # Clean up and reset cwd
    os.chdir(os.path.sep)
    shutil.rmtree(wurst_directory)
    os.chdir(starting_directory)

    print('\n-------------------- Additional Mods -------------------------------------\n')
    print('Fabric API Releases:   https://github.com/FabricMC/fabric/releases')
    print('Sodium Fabric:         https://github.com/CaffeineMC/sodium-fabric/releases')
    print('Iris Shaders:          https://irisshaders.net/download.html')

    print('\n------------------   Resource Packs -------------------------------------\n')
    print('BetterVanillaBuilding: https://www.curseforge.com/minecraft/texture-packs/bettervanillabuilding/files')
    print('Bare Bones:            https://www.curseforge.com/minecraft/texture-packs/bare-bones-texture-pack/files')
