#!/usr/bin/env python3
# -*- coding:utf-8 -*-
"""
OD-Lens

@Author: Otkupman D.G.
@Description: calculation of the main optical parameters
@License: MIT
"""

import tkinter as tk
import numpy as np

def update_mode():
    for e in (f_entry, fov_entry, image_entry):
        e.config(state="normal", bg="white")
    if mode_var.get() == "f":
        f_entry.config(state="readonly", readonlybackground="#e0ffe0")
    elif mode_var.get() == "fov":
        fov_entry.config(state="readonly", readonlybackground="#e0ffe0")
    elif mode_var.get() == "image":
        image_entry.config(state="readonly", readonlybackground="#e0ffe0")
    fov_half_label.config(text="-")
    y_label.config(text="-")
    A_label.config(text="-")
    pupil_area_label.config(text="-")

def update_aperture_mode():
    D_entry.config(state="normal", bg="white")
    N_entry.config(state="normal", bg="white")
    if aperture_mode_var.get() == "D":
        D_entry.config(state="readonly", readonlybackground="#e0ffe0")
    elif aperture_mode_var.get() == "N":
        N_entry.config(state="readonly", readonlybackground="#e0ffe0")

def recalc(*args):
    try:
        mode = mode_var.get()
        amode = aperture_mode_var.get()
        projection = projection_var.get()

        f_val = f_entry.get().strip()
        fov_val = fov_entry.get().strip()
        image_val = image_entry.get().strip()
        D_val = D_entry.get().strip()
        N_val = N_entry.get().strip()

        f = float(f_val) if f_val and mode != "f" else None
        fov = float(fov_val) if fov_val and mode != "fov" else None
        image = float(image_val) if image_val and mode != "image" else None
        D = float(D_val) if D_val and amode != "D" else None
        N = float(N_val) if N_val and amode != "N" else None

        fov_half = np.deg2rad(fov / 2) if fov is not None else None
        fov_half_deg = fov / 2 if fov is not None else None
        image_half = image / 2 if image is not None else None

        if mode == "f":
            if fov_half is not None and image_half is not None:
                if projection == "rectilinear":
                    f = image_half / np.tan(fov_half)
                else:  # equidistant
                    f = image_half / fov_half
                f_entry.config(state="normal")
                f_entry.delete(0, tk.END)
                f_entry.insert(0, f"{f:.7g}")
                f_entry.config(state="readonly")
        elif mode == "fov":
            if f is not None and image_half is not None and f != 0:
                if projection == "rectilinear":
                    fov_half = np.arctan(image_half / f)
                else:  # equidistant
                    fov_half = image_half / f
                fov_half_deg = np.rad2deg(fov_half)
                fov = fov_half_deg * 2
                fov_entry.config(state="normal")
                fov_entry.delete(0, tk.END)
                fov_entry.insert(0, f"{fov:.7g}")
                fov_entry.config(state="readonly")
        elif mode == "image":
            if f is not None and fov_half is not None:
                if projection == "rectilinear":
                    image_half = f * np.tan(fov_half)
                else:  # equidistant
                    image_half = f * fov_half
                image = image_half * 2
                image_entry.config(state="normal")
                image_entry.delete(0, tk.END)
                image_entry.insert(0, f"{image:.7g}")
                image_entry.config(state="readonly")

        if f is not None:
            if amode == "D":
                if N is not None and N != 0:
                    D = f / N
                    D_entry.config(state="normal")
                    D_entry.delete(0, tk.END)
                    D_entry.insert(0, f"{D:.7g}")
                    D_entry.config(state="readonly")
            elif amode == "N":
                if D is not None and D != 0:
                    N = f / D
                    N_entry.config(state="normal")
                    N_entry.delete(0, tk.END)
                    N_entry.insert(0, f"{N:.7g}")
                    N_entry.config(state="readonly")

        if f is not None and D is not None and D != 0:
            A_label.config(text=f"1:{N:.7g} = {D/f:.5g}")
            pupil_area = np.pi * (D/2)**2
            pupil_area_label.config(text=f"{pupil_area:.7g} mm²")
        else:
            A_label.config(text="-")
            pupil_area_label.config(text="-")

        fov_half_label.config(text=f"{fov_half_deg:.7g}°" if fov_half_deg is not None else "-")
        y_label.config(text=f"{image_half:.7g} mm" if image_half is not None else "-")

    except ValueError:
        pass

def save_results():
    """Saves current values to the text field"""
    f_val = f_entry.get().strip()
    fov_val = fov_entry.get().strip()
    image_val = image_entry.get().strip()
    D_val = D_entry.get().strip()
    N_val = N_entry.get().strip()

    if all(not val for val in (f_val, fov_val, image_val, D_val, N_val)):
        return  # don't write anything if all fields are empty

    text_output.delete("1.0", tk.END)
    if f_val: text_output.insert(tk.END, f"F = {f_val} mm\n")
    if fov_val: text_output.insert(tk.END, f"FOV = {fov_val}°\n")
    if image_val: text_output.insert(tk.END, f"Image = {image_val} mm\n")
    if D_val: text_output.insert(tk.END, f"Pupil = {D_val} mm\n")
    if N_val: text_output.insert(tk.END, f"f/{N_val}")

# --- GUI ---
root = tk.Tk()
root.title("Optical Mini Calculator (OD-Lens)")
# Set icon
icon = "iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAAxHpUWHRSYXcgcHJvZmlsZSB0eXBlIGV4aWYAAHjabVDbDcMgDPxnio7gF8QehzRU6gYdvwacKrQ9ieP80GGc2uv5SLcOQkmSNy1WCjjExKi6UJiogxFkcARwiiWfPgXyFPvNM9QS/WceYXHC6ipfjPQehX0tmIS/fhnFQ9wnIhdHGFkYMc0ChkGd34Jiul2/sDdYofOkTnu4jongN5bNt3dkf4eJGiODM7POAbifnLi6UGdk80bkPDQ5C5eYxBfyb08n0hs5KlnVNimJyQAAAYRpQ0NQSUNDIHByb2ZpbGUAAHicfZE9SMNAGIbfpkqLtDi0g4hDhupkFxVxLFUsgoXSVmjVweTSP2jSkKS4OAquBQd/FqsOLs66OrgKguAPiLvgpOgiJX6XFFrEeMdxD+9978vdd4DQrjPVHEgAqmYZ2VRSLBRXxcArgoggRDMsMVNP5xbz8Bxf9/Dx/S7Os7zr/hxhpWQywCcSJ5huWMQbxLObls55nzjKqpJCfE48adAFiR+5Lrv8xrnisMAzo0Y+O08cJRYrfSz3MasaKvEMcUxRNcoXCi4rnLc4q/Um696TvzBU0lZyXKc1hhSWkEYGImQ0UUMdFuK0a6SYyNJ50sM/6vgz5JLJVQMjxwIaUCE5fvA/+N1bszw95SaFksDgi21/jAOBXaDTsu3vY9vunAD+Z+BK6/kbbWDuk/RWT4sdAcPbwMV1T5P3gMsdYORJlwzJkfy0hHIZeD+jbyoCkVtgaM3tW/ccpw9Annq1fAMcHAITFcpe93h3sL9v/9Z0+/cDYH1yn+N6ILkAAA12aVRYdFhNTDpjb20uYWRvYmUueG1wAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlIenJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5zOm1ldGEvIiB4OnhtcHRrPSJYTVAgQ29yZSA0LjQuMC1FeGl2MiI+CiA8cmRmOlJERiB4bWxuczpyZGY9Imh0dHA6Ly93d3cudzMub3JnLzE5OTkvMDIvMjItcmRmLXN5bnRheC1ucyMiPgogIDxyZGY6RGVzY3JpcHRpb24gcmRmOmFib3V0PSIiCiAgICB4bWxuczp4bXBNTT0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wL21tLyIKICAgIHhtbG5zOnN0RXZ0PSJodHRwOi8vbnMuYWRvYmUuY29tL3hhcC8xLjAvc1R5cGUvUmVzb3VyY2VFdmVudCMiCiAgICB4bWxuczpkYz0iaHR0cDovL3B1cmwub3JnL2RjL2VsZW1lbnRzLzEuMS8iCiAgICB4bWxuczpHSU1QPSJodHRwOi8vd3d3LmdpbXAub3JnL3htcC8iCiAgICB4bWxuczp0aWZmPSJodHRwOi8vbnMuYWRvYmUuY29tL3RpZmYvMS4wLyIKICAgIHhtbG5zOnhtcD0iaHR0cDovL25zLmFkb2JlLmNvbS94YXAvMS4wLyIKICAgeG1wTU06RG9jdW1lbnRJRD0iZ2ltcDpkb2NpZDpnaW1wOmZhZTkwZGM3LWEyZmMtNDBiZS05N2RkLTAzZDVkMmRiYWFhNCIKICAgeG1wTU06SW5zdGFuY2VJRD0ieG1wLmlpZDo5MDc2NDNkZi03M2U2LTRkNTktYTk1Mi0zNjNkZWFkYzE5MzMiCiAgIHhtcE1NOk9yaWdpbmFsRG9jdW1lbnRJRD0ieG1wLmRpZDphZDk5NWExOS02YTRmLTQ5N2MtOTUyNS0zZThmMjEzM2Q0MjAiCiAgIGRjOkZvcm1hdD0iaW1hZ2UvcG5nIgogICBHSU1QOkFQST0iMi4wIgogICBHSU1QOlBsYXRmb3JtPSJXaW5kb3dzIgogICBHSU1QOlRpbWVTdGFtcD0iMTc1NTYwNTU2NjU4Nzg2OSIKICAgR0lNUDpWZXJzaW9uPSIyLjEwLjM4IgogICB0aWZmOk9yaWVudGF0aW9uPSIxIgogICB4bXA6Q3JlYXRvclRvb2w9IkdJTVAgMi4xMCIKICAgeG1wOk1ldGFkYXRhRGF0ZT0iMjAyNTowODoxOVQxNToxMjo0NiswMzowMCIKICAgeG1wOk1vZGlmeURhdGU9IjIwMjU6MDg6MTlUMTU6MTI6NDYrMDM6MDAiPgogICA8eG1wTU06SGlzdG9yeT4KICAgIDxyZGY6U2VxPgogICAgIDxyZGY6bGkKICAgICAgc3RFdnQ6YWN0aW9uPSJzYXZlZCIKICAgICAgc3RFdnQ6Y2hhbmdlZD0iLyIKICAgICAgc3RFdnQ6aW5zdGFuY2VJRD0ieG1wLmlpZDo2YTRiZGRjYy03NzdkLTQ5YzEtODEyNS0zMzBmZmEyZTI3MTQiCiAgICAgIHN0RXZ0OnNvZnR3YXJlQWdlbnQ9IkdpbXAgMi4xMCAoV2luZG93cykiCiAgICAgIHN0RXZ0OndoZW49IjIwMjUtMDgtMTlUMTU6MTI6NDYiLz4KICAgIDwvcmRmOlNlcT4KICAgPC94bXBNTTpIaXN0b3J5PgogIDwvcmRmOkRlc2NyaXB0aW9uPgogPC9yZGY6UkRGPgo8L3g6eG1wbWV0YT4KICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAKICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgIAogICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgICAgCiAgICAgICAgICAgICAgICAgICAgICAgICAgIAo8P3hwYWNrZXQgZW5kPSJ3Ij8+s488gAAAAAZiS0dEAAAAAAAA+UO7fwAAAAlwSFlzAAAOxAAADsQBlSsOGwAAAAd0SU1FB+kIEwwMLvY66P0AAADwSURBVDjLnZO7DgFBFIa/2UhOT3SiEoXobE+pVoh4AK1n0XoAEYWWcvVKUYhKdEKh22oUMpuZsbPEn2yyZy7f/nsuEFC3v9ehvTRNtXmiostFEBFRAOpeaziHBu0lAONZncX0AsD6MAKgcj0r48CcV/qJA+gN94xn9SxeTC8kq5hHq+FAjCIKNGlWs/fy8QyA7zjyv25rfro563mQDwe2fYBk03FiH1L4CyHZkL8APyfRzoMtuyIfAFP7UOyX0wEkqzjXhVnP64WfcxBqpJLZyNR+27Zb2b9sWllElPo2ibttrPKmUUSUPRN/jbPWWr8Adp6CS+v7D9YAAAAASUVORK5CYII="
img = tk.PhotoImage(data=icon)
root.tk.call("wm", "iconphoto", root._w, img)

root.configure(bg="#bfcfde")
bg="#eaf0ff"

frm = tk.Frame(root, padx=10, pady=10, bg=bg)
frm.pack(fill="both", expand=True)

# Projection type selection: Rectilinear (Perspective) or Equidistant (Equi-angular)
projection_var = tk.StringVar(value="rectilinear")
tk.Label(frm, text="Projection function:", font=("Courier New", 10), bg=bg).grid(row=0, column=0, sticky="w")
projection_menu = tk.OptionMenu(frm, projection_var, "rectilinear", "equidistant", command=recalc)
projection_menu.grid(row=0, column=1, sticky="w")

mode_var = tk.StringVar(value="f")
tk.Radiobutton(frm, text="Focal length:", font=("Courier New", 12, "bold"), variable=mode_var, value="f", command=update_mode, bg=bg).grid(row=1, column=0, sticky="w")
f_entry = tk.Entry(frm)
f_entry.grid(row=1, column=1)
tk.Label(frm, text="mm", bg=bg).grid(row=1, column=2, sticky="w")

tk.Radiobutton(frm, text="Field of view:", font=("Courier New", 12, "bold"), variable=mode_var, value="fov", command=update_mode, bg=bg).grid(row=2, column=0, sticky="w")
fov_entry = tk.Entry(frm)
fov_entry.grid(row=2, column=1)
tk.Label(frm, text="°", bg=bg).grid(row=2, column=2, sticky="w")

tk.Radiobutton(frm, text="Image size:", font=("Courier New", 12, "bold"), variable=mode_var, value="image", command=update_mode, bg=bg).grid(row=3, column=0, sticky="w")
image_entry = tk.Entry(frm)
image_entry.grid(row=3, column=1)
tk.Label(frm, text="mm", bg=bg).grid(row=3, column=2, sticky="w")

tk.Label(frm, text="Half field angle:", font=("Courier New", 11), bg=bg).grid(row=4, column=0, sticky="w")
fov_half_label = tk.Label(frm, text="-", bg=bg)
fov_half_label.grid(row=4, column=1, sticky="w")

tk.Label(frm, text="Half image size:", font=("Courier New", 11), bg=bg).grid(row=5, column=0, sticky="w")
y_label = tk.Label(frm, text="-", bg=bg)
y_label.grid(row=5, column=1, sticky="w")

# Aperture
aperture_mode_var = tk.StringVar(value="D")
tk.Label(frm, text="Aperture parameter", font=("Courier New", 10, "underline"), bg=bg).grid(row=6, column=0, sticky="w")

tk.Radiobutton(frm, text="Entrance pupil:", font=("Courier New", 12, "bold"), variable=aperture_mode_var, value="D", command=update_aperture_mode, bg=bg).grid(row=7, column=0, sticky="w")
D_entry = tk.Entry(frm)
D_entry.grid(row=7, column=1)
tk.Label(frm, text="mm", bg=bg).grid(row=7, column=2, sticky="w")

tk.Radiobutton(frm, text="F-number (f/#):", font=("Courier New", 12, "bold"), variable=aperture_mode_var, value="N", command=update_aperture_mode, bg=bg).grid(row=8, column=0, sticky="w")
N_entry = tk.Entry(frm)
N_entry.grid(row=8, column=1)

tk.Label(frm, text="Relative aperture:", font=("Courier New", 11), bg=bg).grid(row=9, column=0, sticky="w")
A_label = tk.Label(frm, text="-", bg=bg)
A_label.grid(row=9, column=1, sticky="w")

tk.Label(frm, text="Pupil area:", font=("Courier New", 11), bg=bg).grid(row=10, column=0, sticky="w")
pupil_area_label = tk.Label(frm, text="-", bg=bg)
pupil_area_label.grid(row=10, column=1, sticky="w")

# Save button
btn_save = tk.Button(root, text="Save calculations", command=save_results, bg="lightgreen", font=("Arial", 10, "bold"))
btn_save.pack(pady=10)

# Output text field
text_output = tk.Text(root, height=5, width=35, font=("Courier New", 11))
text_output.pack()

copyright = tk.Label(root, text="© Otkupman D.G., 2020", fg="#777777", bg="#bfcfde")
copyright.pack()

# Bind events
for entry in (f_entry, fov_entry, image_entry, D_entry, N_entry):
    entry.bind("<KeyRelease>", recalc)

update_mode()
update_aperture_mode()

root.mainloop()