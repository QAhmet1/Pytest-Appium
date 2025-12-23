import argparse
import subprocess
import sys
import os
import shutil

def main() -> int:
    parser = argparse.ArgumentParser(description="Run mobile tests via pytest.")
    parser.add_argument("--platform", default="android", help="Target platform: android or ios")
    parser.add_argument("--env", default="local", help="Execution environment: local or browserstack")
    parser.add_argument("-k", dest="keyword", default=None, help="Pytest keyword filter")
    args = parser.parse_args()

    # --- STEP 1: Auto-detect Virtual Environment ---
    venv_python = os.path.join(os.getcwd(), "venv", "Scripts", "python.exe")
    python_exe = venv_python if os.path.exists(venv_python) else sys.executable

    # --- STEP 2: Clean Old Reports ---
    report_dir = "reports"
    if os.path.exists(report_dir):
        print(f"\n--- Cleaning: Removing old reports from {report_dir} ---")
        shutil.rmtree(report_dir)
    os.makedirs(report_dir)

    # --- STEP 3: Construct and Run Test Command ---
    cmd = [
        python_exe, "-m", "pytest",
        f"--platform={args.platform}",
        f"--env={args.env}",
        f"--alluredir={report_dir}"
    ]
    if args.keyword:
        cmd.extend(["-k", args.keyword])

    print(f"\n--- Execution: Running tests using {python_exe} ---")
    result = subprocess.run(cmd)

    # --- STEP 4: Generate and Open Allure Report ---
    if os.path.exists(report_dir) and os.listdir(report_dir):
        print("\n--- Success: Generating and opening Allure Report ---")
        subprocess.call(['allure', 'serve', report_dir], shell=True)
    else:
        print("\n--- Error: No report data found. Allure could not be started. ---")

    return result.returncode

if __name__ == "__main__":
    main()