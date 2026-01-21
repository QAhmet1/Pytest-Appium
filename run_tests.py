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

    # --- STEP 4: Generate Allure HTML Report (non-blocking) ---
    if os.path.exists(report_dir) and os.listdir(report_dir):
        print("\n--- Success: Generating Allure HTML Report ---")
        html_dir = os.path.join(report_dir, "html")
        try:
            # Generate static report instead of long‑running `allure serve`
            subprocess.run(
                ["allure", "generate", report_dir, "-o", html_dir, "--clean"],
                check=False,
            )
            if os.path.exists(html_dir):
                print(f"Allure report generated at: {os.path.abspath(html_dir)}")
                # Optional: open report directory in default file browser
                try:
                    if sys.platform.startswith("win"):
                        os.startfile(os.path.abspath(html_dir))  # type: ignore[attr-defined]
                except Exception:
                    # Even if opening the folder fails, it should not affect test result
                    pass
        except FileNotFoundError:
            # Allure CLI is optional; do not treat missing CLI as a warning for the test run itself.
            print(
                "\n[INFO] 'allure' CLI not found. "
                "Results directory was created under 'reports', "
                "but HTML report generation was skipped. "
                "Install Allure CLI if you want local HTML reports."
            )
    else:
        print("\n--- Error: No report data found. Allure could not be started. ---")

    return result.returncode

if __name__ == "__main__":
    main()