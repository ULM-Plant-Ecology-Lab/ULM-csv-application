# ©Thomas Edmund Anderson 2026
import os
import sys
import ctypes
import urllib.request
import urllib.parse
import threading
import json
import re
from datetime import datetime
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

GITHUB_API_RELEASES_URL = "https://api.github.com/repos/tanderste1234/CSV_Tool-Releases/releases"
GITHUB_RAW_BASE_URL = "https://raw.githubusercontent.com/tanderste1234/CSV_Tool-Releases/main/"

FILES_TO_DOWNLOAD = [
    {"name": "CSV Tool (Windows)", "pattern": "CSVTOOLV{}.exe", "subdir": "WindowsEXEs", "prefix": "CSVTOOL"},
    {"name": "Raw Data Tool (Windows)", "pattern": "RDTOOLV{}.exe", "subdir": "WindowsEXEs", "prefix": "RDTOOL"},
    {"name": "EULA", "pattern": "EULA.txt", "subdir": "", "prefix": "CSVTOOL"}
]

def parse_version_tuple(tag_str):
    match = re.search(r'(\d+)\.(\d+)\.(\d+)', tag_str)
    if match:
        return tuple(map(int, match.groups()))
    return (0, 0, 0)

def extract_version_digits(tag_str):
    match = re.search(r'(\d+\.\d+\.\d+)', tag_str)
    if match:
        return match.group(1)
    return "1.0.0"

def fetch_available_releases(prefix="CSVTOOL"):
    try:
        req = urllib.request.Request(
            GITHUB_API_RELEASES_URL,
            headers={"User-Agent": "CSVTool-Windows-Installer"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            releases = []
            for rel in data:
                tag = rel.get("tag_name", "")
                if prefix.upper() in tag.upper():
                    v_tuple = parse_version_tuple(tag)
                    if v_tuple != (0, 0, 0):
                        releases.append((v_tuple, tag))
            releases.sort(key=lambda x: x[0], reverse=True)
            return [tag for _, tag in releases]
    except Exception:
        return []

def get_tool_release_info(prefix="CSVTOOL", target_tag=None):
    try:
        req = urllib.request.Request(
            GITHUB_API_RELEASES_URL,
            headers={"User-Agent": "CSVTool-Windows-Installer"}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            releases = []
            for rel in data:
                tag = rel.get("tag_name", "")
                if prefix.upper() in tag.upper():
                    v_tuple = parse_version_tuple(tag)
                    if v_tuple != (0, 0, 0):
                        releases.append((v_tuple, tag, rel))
            
            if releases:
                releases.sort(key=lambda x: x[0], reverse=True)
                if target_tag and target_tag != "Latest (Auto-detect)":
                    for v_tuple, tag, rel in releases:
                        if tag == target_tag or extract_version_digits(tag) == target_tag:
                            return tag, extract_version_digits(tag), f"https://raw.githubusercontent.com/tanderste1234/CSV_Tool-Releases/{tag}/"
                
                best_release = releases[0]
                return best_release[1], extract_version_digits(best_release[1]), f"https://raw.githubusercontent.com/tanderste1234/CSV_Tool-Releases/{best_release[1]}/"
    except Exception:
        pass
    return f"{prefix}_main", "1.0.0", GITHUB_RAW_BASE_URL

def create_windows_shortcut(shortcut_path, target_path, working_dir, description=""):
    try:
        ps_script = r"""
        $WshShell = New-Object -ComObject WScript.Shell
        $Shortcut = $WshShell.CreateShortcut("{shortcut_path}")
        $Shortcut.TargetPath = "{target_path}"
        $Shortcut.WorkingDirectory = "{working_dir}"
        $Shortcut.Description = "{description}"
        $Shortcut.Save()
        """.format(shortcut_path=shortcut_path, target_path=target_path, working_dir=working_dir, description=description)
        import subprocess
        subprocess.run(["powershell", "-Command", ps_script], capture_output=True, text=True, timeout=10)
    except Exception:
        pass

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False

def run_as_admin():
    try:
        script = os.path.abspath(sys.argv[0])
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
    except Exception as e:
        messagebox.showerror("Privilege Error", f"Failed to elevate privileges: {str(e)}")

def create_installer():
    root = tk.Tk()
    root.title("CSV Tool Suite Windows Setup Wizard")
    root.geometry("580x520")
    root.minsize(520, 480)

    default_standard_dir = os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "CSVTOOL")

    install_mode_var = tk.StringVar(value="Standard")
    install_path_var = tk.StringVar(value=default_standard_dir)
    version_choice_var = tk.StringVar(value="Latest (Auto-detect)")
    install_template_var = tk.BooleanVar(value=True)
    create_shortcut_var = tk.BooleanVar(value=True)

    container = ttk.Frame(root, padding="15")
    container.pack(fill=tk.BOTH, expand=True)

    ttk.Label(container, text="CSV Tool Suite Setup (Windows Edition)", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
    ttk.Label(container, text="Target: Windows .exe Binaries (WindowsEXEs)", font=("Helvetica", 9, "bold"), foreground="#0055aa").pack(anchor=tk.W, pady=(0, 10))

    page1_frame = ttk.Frame(container)
    page2_frame = ttk.Frame(container)

    # --- PAGE 1: Installation Type & Paths ---
    ttk.Label(page1_frame, text="Choose your installation type. Standard installs in Program Files (requires Administrator rights).", wraplength=530).pack(anchor=tk.W, pady=(0, 10))

    mode_frame = ttk.LabelFrame(page1_frame, text="Installation Type", padding="10")
    mode_frame.pack(fill=tk.X, pady=5)

    custom_options_frame = ttk.Frame(page1_frame)

    def on_mode_change(*args):
        if install_mode_var.get() == "Standard":
            install_path_var.set(default_standard_dir)
            custom_options_frame.pack_forget()
        else:
            custom_options_frame.pack(fill=tk.X, pady=5)

    ttk.Radiobutton(mode_frame, text="Standard Installation (Program Files)", variable=install_mode_var, value="Standard", command=on_mode_change).pack(anchor=tk.W, pady=2)
    ttk.Radiobutton(mode_frame, text="Custom Installation (Custom Folder & Version)", variable=install_mode_var, value="Custom", command=on_mode_change).pack(anchor=tk.W, pady=2)

    dir_frame = ttk.LabelFrame(custom_options_frame, text="Custom Destination Folder", padding="10")
    dir_frame.pack(fill=tk.X, pady=5)
    dir_entry = ttk.Entry(dir_frame, textvariable=install_path_var, width=42)
    dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

    def browse_dir():
        chosen = filedialog.askdirectory(title="Select Custom Installation Folder")
        if chosen:
            target = chosen if os.path.basename(os.path.normpath(chosen)).upper() == "CSVTOOL" else os.path.join(chosen, "CSVTOOL")
            install_path_var.set(target)

    ttk.Button(dir_frame, text="Browse...", command=browse_dir).pack(side=tk.RIGHT)

    ver_frame = ttk.LabelFrame(custom_options_frame, text="Version Selection", padding="10")
    ver_frame.pack(fill=tk.X, pady=5)
    ttk.Label(ver_frame, text="Select target version:").pack(anchor=tk.W, pady=(0, 2))
    version_combo = ttk.Combobox(ver_frame, textvariable=version_choice_var, values=["Latest (Auto-detect)"], state="readonly", width=40)
    version_combo.pack(anchor=tk.W, fill=tk.X, pady=2)

    def load_versions_background():
        tags = fetch_available_releases("CSVTOOL") or fetch_available_releases("RDTOOL")
        if tags:
            combined = ["Latest (Auto-detect)"] + list(dict.fromkeys(tags + [extract_version_digits(t) for t in tags]))
            root.after(0, lambda: version_combo.config(values=combined))

    threading.Thread(target=load_versions_background, daemon=True).start()

    # --- PAGE 2: Options & Progress ---
    opt_frame = ttk.LabelFrame(page2_frame, text="Installation Options", padding="10")
    opt_frame.pack(fill=tk.X, pady=5)
    ttk.Checkbutton(opt_frame, text="Install default carbon template file (templateFile.csv)", variable=install_template_var).pack(anchor=tk.W, pady=2)
    ttk.Checkbutton(opt_frame, text="Create desktop shortcuts", variable=create_shortcut_var).pack(anchor=tk.W, pady=2)

    status_var = ttk.Label(page2_frame, text="Ready to install.", font=("Helvetica", 9, "italic"))
    status_var.pack(anchor=tk.W, pady=(15, 5))

    progress_bar = ttk.Progressbar(page2_frame, orient=tk.HORIZONTAL, length=540, mode="determinate")
    progress_bar.pack(fill=tk.X, pady=5)

    page1_frame.pack(fill=tk.BOTH, expand=True)
    current_step_index = 1

    def perform_installation(target_dir, chosen_version):
        try:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            total_steps = len(FILES_TO_DOWNLOAD) + (1 if install_template_var.get() else 0) + (1 if create_shortcut_var.get() else 0)
            current_step = 0
            release_cache = {}
            last_version_str = "1.0.0"

            for file_info in FILES_TO_DOWNLOAD:
                current_step += 1
                progress_bar["value"] = (current_step / total_steps) * 100
                prefix = file_info["prefix"]

                cache_key = (prefix, chosen_version)
                if cache_key not in release_cache:
                    status_var.config(text=f"Resolving {prefix} version ({chosen_version})...")
                    root.update_idletasks()
                    release_cache[cache_key] = get_tool_release_info(prefix, chosen_version)

                detected_tag, version_str, dl_base = release_cache[cache_key]
                last_version_str = version_str

                filename = file_info["pattern"].format(version_str) if "{}" in file_info["pattern"] else file_info["pattern"]
                subdir = file_info["subdir"]

                status_var.config(text=f"Downloading {filename}...")
                root.update_idletasks()

                remote_subpath = f"{subdir}/{filename}" if subdir else filename
                file_url = dl_base + urllib.parse.quote(remote_subpath, safe="/")
                dest_path = os.path.join(target_dir, filename)

                urllib.request.urlretrieve(file_url, dest_path)

            if install_template_var.get():
                current_step += 1
                progress_bar["value"] = (current_step / total_steps) * 100
                status_var.config(text="Generating templateFile.csv...")
                root.update_idletasks()
                with open(os.path.join(target_dir, "templateFile.csv"), "w", encoding="utf-8") as tf:
                    tf.write("Hs, tau, u_star, Ts_stdev, Ts_Ux_cov, Ts_Uy_cov, Ts_Uz_cov, wnd_spd, rslt_wnd_spd, wnd_dir_sonic\n")

            if create_shortcut_var.get():
                current_step += 1
                progress_bar["value"] = (current_step / total_steps) * 100
                status_var.config(text="Creating desktop shortcuts...")
                root.update_idletasks()
                desk_dir = os.path.join(os.path.expanduser("~"), "Desktop")
                if not os.path.exists(desk_dir):
                    desk_dir = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
                
                c_exe = os.path.join(target_dir, f"CSVTOOLV{last_version_str}.exe")
                r_exe = os.path.join(target_dir, f"RDTOOLV{last_version_str}.exe")
                if os.path.exists(c_exe):
                    create_windows_shortcut(os.path.join(desk_dir, "CSV Tool.lnk"), c_exe, target_dir, "CSV Tool")
                if os.path.exists(r_exe):
                    create_windows_shortcut(os.path.join(desk_dir, "Raw Data Tool.lnk"), r_exe, target_dir, "Raw Data Tool")

            progress_bar["value"] = 100
            status_var.config(text="Installation completed successfully!")
            root.after(100, lambda: [messagebox.showinfo("Complete", f"Installation successful to:\n{target_dir}"), root.destroy()])

        except Exception as err:
            messagebox.showerror("Error", f"Installation failed:\n{str(err)}")

    def start_install_thread():
        target_dir = install_path_var.get().strip()
        if not target_dir:
            messagebox.showerror("Error", "Please select a valid path.")
            return
        if install_mode_var.get() == "Standard" and not is_admin():
            if messagebox.askyesno("Admin Required", "Standard installation requires Administrator privileges.\n\nRestart as Administrator?"):
                run_as_admin()
                root.destroy()
                return
            return
        if not target_dir.endswith("CSVTOOL"):
            target_dir = os.path.join(target_dir, "CSVTOOL")
        
        chosen_version = version_choice_var.get() if install_mode_var.get() == "Custom" else "Latest (Auto-detect)"
        btn_next.config(state="disabled")
        btn_back.config(state="disabled")
        threading.Thread(target=lambda: perform_installation(target_dir, chosen_version), daemon=True).start()

    def go_next():
        nonlocal current_step_index
        if current_step_index == 1:
            page1_frame.pack_forget()
            page2_frame.pack(fill=tk.BOTH, expand=True)
            current_step_index = 2
            btn_back.config(state="normal")
            btn_next.config(text="Install Now", command=start_install_thread)

    def go_back():
        nonlocal current_step_index
        if current_step_index == 2:
            page2_frame.pack_forget()
            page1_frame.pack(fill=tk.BOTH, expand=True)
            current_step_index = 1
            btn_back.config(state="disabled")
            btn_next.config(text="Next >", command=go_next)

    btn_frame = ttk.Frame(container)
    btn_frame.pack(fill=tk.X, pady=(15, 0))
    
    ttk.Button(btn_frame, text="Cancel", command=root.destroy).pack(side=tk.LEFT)
    
    right_buttons_frame = ttk.Frame(btn_frame)
    right_buttons_frame.pack(side=tk.RIGHT)
    
    btn_back = ttk.Button(right_buttons_frame, text="< Back", command=go_back, state="disabled")
    btn_back.pack(side=tk.LEFT, padx=(0, 5))
    
    btn_next = ttk.Button(right_buttons_frame, text="Next >", command=go_next)
    btn_next.pack(side=tk.LEFT)

    root.mainloop()

if __name__ == "__main__":
    create_installer()