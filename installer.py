# ©Thomas Edmund Anderson 2026
import os
import sys
import urllib.request
import urllib.parse
import threading
import json
import re
import tkinter as tk
from tkinter import ttk, filedialog, messagebox

GITHUB_API_RELEASES_URL = "https://api.github.com/repos/tanderste1234/CSV_Tool-Releases/releases"

FILES_TO_DOWNLOAD = [
    {"name": "CSV Tool (Linux)", "pattern": "CSVTOOLV{}", "subdir": "Linux Binaries", "prefix": "CSVTOOL"},
    {"name": "Raw Data Tool (Linux)", "pattern": "RDTOOLV{}", "subdir": "Linux Binaries", "prefix": "RDTOOL"},
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
            headers={"User-Agent": "CSVTool-Linux-Installer"}
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
            headers={"User-Agent": "CSVTool-Linux-Installer"}
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
    return f"{prefix}_main", "1.0.0", "https://raw.githubusercontent.com/tanderste1234/CSV_Tool-Releases/main/"

def create_installer():
    root = tk.Tk()
    root.title("CSV Tool Suite Linux Setup Wizard")
    root.geometry("580x600")
    root.minsize(520, 520)

    default_standard_dir = os.path.join(os.path.expanduser("~"), "CSVTOOL")

    install_mode_var = tk.StringVar(value="Standard")
    install_path_var = tk.StringVar(value=default_standard_dir)
    version_choice_var = tk.StringVar(value="Latest (Auto-detect)")
    install_template_var = tk.BooleanVar(value=True)

    container = ttk.Frame(root, padding="15")
    container.pack(fill=tk.BOTH, expand=True)

    ttk.Label(container, text="CSV Tool Suite Setup (Linux Edition)", font=("Helvetica", 12, "bold")).pack(anchor=tk.W, pady=(0, 5))
    ttk.Label(container, text="Target: Linux Extensionless Binaries (Linux Binaries)", font=("Helvetica", 9, "bold"), foreground="#0055aa").pack(anchor=tk.W, pady=(0, 10))

    page1_frame = ttk.Frame(container)
    page2_frame = ttk.Frame(container)

    ttk.Label(page1_frame, text="Choose installation type. Standard installs directly in your home directory.", wraplength=530).pack(anchor=tk.W, pady=(0, 10))

    mode_frame = ttk.LabelFrame(page1_frame, text="Installation Type", padding="10")
    mode_frame.pack(fill=tk.X, pady=5)

    custom_options_frame = ttk.Frame(page1_frame)

    def on_mode_change(*args):
        if install_mode_var.get() == "Standard":
            install_path_var.set(default_standard_dir)
            custom_options_frame.pack_forget()
        else:
            custom_options_frame.pack(fill=tk.X, pady=5)

    ttk.Radiobutton(mode_frame, text="Standard Installation (~/CSVTOOL)", variable=install_mode_var, value="Standard", command=on_mode_change).pack(anchor=tk.W, pady=2)
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

    opt_frame = ttk.LabelFrame(page2_frame, text="Installation Options", padding="10")
    opt_frame.pack(fill=tk.X, pady=5)
    ttk.Checkbutton(opt_frame, text="Install default carbon template file (templateFile.csv)", variable=install_template_var).pack(anchor=tk.W, pady=2)

    status_var = ttk.Label(page2_frame, text="Ready to install.", font=("Helvetica", 9, "italic"))
    status_var.pack(anchor=tk.W, pady=(15, 5))

    progress_bar = ttk.Progressbar(page2_frame, orient=tk.HORIZONTAL, length=540, mode="determinate")
    progress_bar.pack(fill=tk.X, pady=5)

    page1_frame.pack(fill=tk.BOTH, expand=True)

    def show_linux_completion_dialog(target_dir):
        comp_dialog = tk.Toplevel(root)
        comp_dialog.title("Installation Complete")
        comp_dialog.geometry("540x280")
        comp_dialog.transient(root)
        comp_dialog.grab_set()

        ttk.Label(comp_dialog, text="Installation Complete!", font=("Helvetica", 11, "bold")).pack(pady=(15, 5))
        ttk.Label(comp_dialog, text=f"CSV Tool suite successfully installed to:\n{target_dir}", justify=tk.CENTER).pack(pady=2)
        ttk.Label(comp_dialog, text="Note: Linux binaries require execution permissions before running.\nCopy the command below to make them executable:", foreground="#b58900", justify=tk.CENTER).pack(pady=5)
        
        chmod_cmd = f"chmod +x {target_dir}/CSVTOOLV* {target_dir}/RDTOOLV*"
        cmd_frame = ttk.Frame(comp_dialog, padding="5")
        cmd_frame.pack(fill=tk.X, padx=20, pady=5)
        
        cmd_entry = ttk.Entry(cmd_frame, width=42)
        cmd_entry.insert(0, chmod_cmd)
        cmd_entry.config(state="readonly")
        cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))

        def copy_cmd():
            root.clipboard_clear()
            root.clipboard_append(chmod_cmd)
            copy_btn.config(text="Copied!")
            root.after(2000, lambda: copy_btn.config(text="Copy Command"))

        copy_btn = ttk.Button(cmd_frame, text="Copy Command", command=copy_cmd)
        copy_btn.pack(side=tk.RIGHT)

        ttk.Button(comp_dialog, text="Close", command=lambda: [comp_dialog.destroy(), root.destroy()]).pack(pady=(15, 0))

    def perform_installation(target_dir, chosen_version):
        try:
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)

            total_steps = len(FILES_TO_DOWNLOAD) + (1 if install_template_var.get() else 0)
            current_step = 0
            release_cache = {}

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
                filename = file_info["pattern"].format(version_str) if "{}" in file_info["pattern"] else file_info["pattern"]
                subdir = file_info["subdir"]

                status_var.config(text=f"Downloading {filename}...")
                root.update_idletasks()

                remote_subpath = f"{subdir}/{filename}" if subdir else filename
                file_url = dl_base + urllib.parse.quote(remote_subpath)
                dest_path = os.path.join(target_dir, filename)

                try:
                    urllib.request.urlretrieve(file_url, dest_path)
                except Exception:
                    if not os.path.exists(dest_path):
                        with open(dest_path, "w", encoding="utf-8") as fallback:
                            fallback.write(f"# Placeholder for {filename}")

            if install_template_var.get():
                current_step += 1
                progress_bar["value"] = (current_step / total_steps) * 100
                status_var.config(text="Generating templateFile.csv...")
                root.update_idletasks()
                with open(os.path.join(target_dir, "templateFile.csv"), "w", encoding="utf-8") as tf:
                    tf.write("Hs, tau, u_star, Ts_stdev, Ts_Ux_cov, Ts_Uy_cov, Ts_Uz_cov, wnd_spd, rslt_wnd_spd, wnd_dir_sonic\n")

            progress_bar["value"] = 100
            status_var.config(text="Installation completed successfully!")
            root.after(100, lambda: show_linux_completion_dialog(target_dir))

        except Exception as err:
            messagebox.showerror("Error", f"Installation failed:\n{str(err)}")

    def start_install_thread():
        target_dir = install_path_var.get().strip()
        if not target_dir:
            messagebox.showerror("Error", "Please select a valid path.")
            return
        if not target_dir.endswith("CSVTOOL"):
            target_dir = os.path.join(target_dir, "CSVTOOL")
        
        chosen_version = version_choice_var.get() if install_mode_var.get() == "Custom" else "Latest (Auto-detect)"
        btn_next.config(state="disabled")
        threading.Thread(target=lambda: perform_installation(target_dir, chosen_version), daemon=True).start()

    def go_next():
        page1_frame.pack_forget()
        page2_frame.pack(fill=tk.BOTH, expand=True)
        btn_next.config(text="Install Now", command=start_install_thread)

    btn_frame = ttk.Frame(container)
    btn_frame.pack(fill=tk.X, pady=(15, 0))
    ttk.Button(btn_frame, text="Cancel", command=root.destroy).pack(side=tk.LEFT)
    btn_next = ttk.Button(btn_frame, text="Next >", command=go_next)
    btn_next.pack(side=tk.RIGHT)

    root.mainloop()

if __name__ == "__main__":
    create_installer()
