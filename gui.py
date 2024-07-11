import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import scrape
import threading

root = ttk.Window(themename="darkly", title="Total Ranked Games")

l1 = ttk.Label(root, text="USER NAME")
l2 = ttk.Label(root, text="RIOT ID")
e1 = ttk.Entry(root)
e2 = ttk.Entry(root)
l3 = ttk.Label(root, text="TOTAL: ...")

progress = ttk.Progressbar(root, mode='indeterminate')


def start_counting(username, userid):
    # Start the progress bar animation
    progress.start()
    try:
        number = scrape.iterate_through_seasons(f"{username}-{userid}")
        l3.config(text=f"TOTAL: {username}-{userid} : {number}")
    finally:
        # Stop the progress bar animation and hide it
        progress.stop()
        progress.grid_remove()
        b1.config(state=NORMAL)  # Enable the button again


def counting():
    username = e1.get()
    userid = e2.get()
    b1.config(state=DISABLED)  # Disable the button to prevent multiple clicks
    progress.grid(row=3, column=0, columnspan=3, padx=5, pady=5)  # Show the progress bar
    thread = threading.Thread(target=start_counting, args=(username, userid))
    thread.start()


l1.grid(row=0, column=0, padx=5, pady=5)
l2.grid(row=0, column=1, padx=5, pady=5)
e1.grid(row=1, column=0, padx=5, pady=5)
e2.grid(row=1, column=1, padx=5, pady=5)
l3.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

b1 = ttk.Button(root, text="Count", bootstyle=SUCCESS, command=counting)
b1.grid(row=1, column=2, padx=5, pady=5)


progress.grid_remove()
root.mainloop()
