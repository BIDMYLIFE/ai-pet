import os
import sys
import time
import tkinter as tk

try:
	from PIL import Image, ImageTk, ImageSequence
except Exception:
	print("Pillow is required. Install with: pip install pillow")
	sys.exit(1)


class GIF:
	def __init__(self, path):
		self.path = path
		self.frames = []
		self.durations = []
		self._load()

	def _load(self):
		if not os.path.exists(self.path):
			raise FileNotFoundError(self.path)
		im = Image.open(self.path)
		for frame in ImageSequence.Iterator(im):
			frame_rgba = frame.convert("RGBA")
			tkimg = ImageTk.PhotoImage(frame_rgba)
			self.frames.append(tkimg)
			duration = frame.info.get("duration", 100)
			try:
				duration = int(duration)
			except Exception:
				duration = 100
			self.durations.append(max(1, duration))


class App:
	def __init__(self, root, gif0_path, gif1_path, watched_path):
		self.root = root
		self.root.title("Character Display")
		self.label = tk.Label(root)
		self.label.pack()

		self.gif0 = GIF(gif0_path)
		self.gif1 = GIF(gif1_path)

		self.current = 0
		self.frame_index = 0
		self.watched_path = watched_path
		self.last_size = None
		if self.watched_path and os.path.exists(self.watched_path):
			try:
				self.last_size = os.path.getsize(self.watched_path)
			except Exception:
				self.last_size = None

		self.switch_to(0)
		self.toggling = False
		self.toggle_interval = 10000  # ms between switches

		self._animate()
		self._poll_watched()

	def switch_to(self, which):
		if which == 0:
			self.current_frames = self.gif0.frames
			self.current_durations = self.gif0.durations
		else:
			self.current_frames = self.gif1.frames
			self.current_durations = self.gif1.durations
		self.current = which
		self.frame_index = 0

	def _animate(self):
		if not self.current_frames:
			return
		img = self.current_frames[self.frame_index]
		self.label.configure(image=img)
		dur = self.current_durations[self.frame_index]
		self.frame_index = (self.frame_index + 1) % len(self.current_frames)
		self.root.after(dur, self._animate)

	def _poll_watched(self):
		try:
			if os.path.exists(self.watched_path):
				# If file exists, check its size and treat creation/size change as event.
				sz = os.path.getsize(self.watched_path)
				if self.last_size is None:
					# first time seeing the file: if size > 0 consider it a change
					if sz != 0:
						print(f"tss.wav appeared with size: {sz}")
						self.switch_to(1)
						# start toggling repeatedly
						self.toggling = True
						self._toggle_loop()
						self.last_size = sz
						return
					self.last_size = sz
				elif sz != self.last_size:
					print(f"tss.wav size changed: {self.last_size} -> {sz}")
					# start toggling repeatedly
					self.switch_to(1)
					self.toggling = True
					self._toggle_loop()
					self.last_size = sz
					return
				# If file exists and size returned to zero, stop toggling
				if self.toggling and sz == 0:
					self.toggling = False
					self.switch_to(0)
					self.last_size = sz
					return
		except Exception:
			pass
		self.root.after(500, self._poll_watched)

	def _toggle_loop(self):
		if not self.toggling:
			return
		next_idx = 0 if getattr(self, 'current', 0) == 1 else 1
		self.switch_to(next_idx)
		self.root.after(self.toggle_interval, self._toggle_loop)


def resource_path(filename):
	return os.path.join(os.path.dirname(__file__), filename)


def main():
	gif0 = resource_path("characters/character0.gif")
	gif1 = resource_path("characters/character1.gif")
	watched = resource_path("tss.wav")

	for p in (gif0, gif1):
		if not os.path.exists(p):
			print(f"Required file missing: {p}")
			sys.exit(1)

	root = tk.Tk()
	app = App(root, gif0, gif1, watched)
	root.mainloop()


if __name__ == "__main__":
	main()

