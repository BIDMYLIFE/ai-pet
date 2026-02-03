import os
import threading

def show_init_frame(gif_path="characters/character1.gif", display_time_ms=None, frame_delay_ms=100):
    try:
        import tkinter as tk
        from tkinter import PhotoImage
    except Exception:
        return None

    def _tk_thread(path, display_time_ms, frame_delay_ms):
        try:
            root = tk.Tk()
            root.overrideredirect(True)
            root.attributes("-topmost", True)

            frames = []
            i = 0
            while True:
                try:
                    frames.append(PhotoImage(file=path, format=f"gif -index {i}"))
                    i += 1
                except Exception:
                    break

            if not frames:
                root.destroy()
                return

            label = tk.Label(root, image=frames[0], bd=0)
            label.pack()
            label.frames = frames
            label.image = frames[0]

            root.update_idletasks()
            w = root.winfo_width(); h = root.winfo_height()
            x = (root.winfo_screenwidth() // 2) - (w // 2)
            y = (root.winfo_screenheight() // 2) - (h // 2)
            root.geometry(f"{w}x{h}+{x}+{y}")

            if len(frames) > 1:
                def animate(idx=0):
                    try:
                        label.config(image=label.frames[idx])
                        label.image = label.frames[idx]
                        idx = (idx + 1) % len(label.frames)
                        root.after(frame_delay_ms, animate, idx)
                    except Exception:
                        return
                animate()

            if display_time_ms:
                root.after(display_time_ms, root.destroy)

            root.mainloop()
        except Exception:
            return

    script_dir = os.path.dirname(__file__)
    path = os.path.join(script_dir, gif_path) if not os.path.isabs(gif_path) else gif_path
    if not os.path.exists(path):
        return None

    t = threading.Thread(target=_tk_thread, args=(path, display_time_ms, frame_delay_ms), daemon=True)
    t.start()
    return t