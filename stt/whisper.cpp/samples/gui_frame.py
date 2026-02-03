import os
import tkinter as tk


def show_init_frame(
    gif_path="characters/character1.gif",
    display_time_ms=None,
    frame_delay_ms=100
):
    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, gif_path) if not os.path.isabs(gif_path) else gif_path

    if not os.path.exists(path):
        print("GIF not found:", path)
        return None

    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes("-topmost", True)

    frames = []
    i = 0

    # Load GIF frames
    while True:
        try:
            frames.append(
                tk.PhotoImage(file=path, format=f"gif -index {i}")
            )
            i += 1
        except Exception:
            break

    if not frames:
        root.destroy()
        return None

    label = tk.Label(root, image=frames[0], bd=0)
    label.pack()

    label.frames = frames
    label.image = frames[0]

    root.update_idletasks()

    # Center window
    w = root.winfo_width()
    h = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (w // 2)
    y = (root.winfo_screenheight() // 2) - (h // 2)
    root.geometry(f"{w}x{h}+{x}+{y}")

    # Animate
    if len(frames) > 1:

        def animate(idx=0):
            label.config(image=frames[idx])
            label.image = frames[idx]

            idx = (idx + 1) % len(frames)

            root.after(frame_delay_ms, animate, idx)

        animate()

    # Auto close
    if display_time_ms:
        root.after(display_time_ms, root.destroy)

    root.mainloop()

    return root
