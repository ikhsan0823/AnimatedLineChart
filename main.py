import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
import pandas as pd

df = pd.read_excel(r"D:\Coding\Python\data.xlsx")
max_frames_displayed = 20
x = {'seri1': [], 'seri2': []}
y = {'seri1': [], 'seri2': []}
paused = True
current_frame = 0

fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=False)
fig.subplots_adjust(left=0.07)

paused_box = plt.Rectangle((0.45, 0.45), 0.1, 0.1, linewidth=3, edgecolor='black', facecolor='white')
ax.add_patch(paused_box)


def update(i):
    global paused, current_frame
    if not paused and i < len(df):
        x['seri1'].append(df.iloc[i, 0])
        y['seri1'].append(df.iloc[i, 1])
        x['seri2'].append(df.iloc[i, 0])
        y['seri2'].append(df.iloc[i, 2])

        current_frame = i
        x_display1 = x['seri1'][-max_frames_displayed:]
        y_display1 = y['seri1'][-max_frames_displayed:]
        x_display2 = x['seri2'][-max_frames_displayed:]
        y_display2 = y['seri2'][-max_frames_displayed:]

        ax.clear()
        ax.plot(x_display1, y_display1, linestyle='-', color='b', label='Suhu A')
        ax.plot(x_display2, y_display2, linestyle='-', color='r', label='Suhu B')
        ax.set_title('SUHU AIR (20 HARI)')
        ax.set_xlabel('WAKTU (JAM)')
        ax.set_ylabel('SUHU (°C)')

        ax.legend(loc='upper left', bbox_to_anchor=(1, 1))

        # Set y-axis range
        ax.set_ylim(26, 29)

        tanggal = df.iloc[i, 3].strftime('%Y-%m-%d')
        ax.text(0.852, 1.012, f'Tanggal: {tanggal}', transform=ax.transAxes)

        # Check if any y-values are outside the desired range
        y_values = y_display1 + y_display2
        min_y, max_y = min(y_values), max(y_values)
        if min_y < 26 or max_y > 29:
            ax.set_ylim(min(min_y, 26), max(max_y, 29))

    elif paused:
        paused_box.set_visible(True)
        ax.text(0.5, 0.5, 'Paused', transform=ax.transAxes, ha='center', va='center', fontsize=15, color='black')
        animation.event_source.stop()

    else:
        animation.event_source.stop()


def start_animation(event):
    global paused
    if paused:
        paused = False
        animation.event_source.start()


def pause_animation(event):
    global paused
    paused = True
    animation.event_source.stop()


def toggle_recording(event):
    global recording
    recording = not recording
    if recording:
        writer = FFMpegWriter(fps=10, metadata=dict(artist='Me'), bitrate=1800)
        animation.save('data.mp4', writer=writer)


recording = False

# Tombol-tombol (tanpa slider)
ax_start = plt.axes([0.905, 0.72, 0.05, 0.05])
ax_pause = plt.axes([0.905, 0.66, 0.05, 0.05])
ax_record = plt.axes([0.905, 0.6, 0.05, 0.05])

btn_start = plt.Button(ax_start, 'Start')
btn_start.on_clicked(start_animation)

btn_pause = plt.Button(ax_pause, 'Pause')
btn_pause.on_clicked(pause_animation)

btn_record = plt.Button(ax_record, 'Record')
btn_record.on_clicked(toggle_recording)

animation = FuncAnimation(fig=fig, func=update, frames=len(df) + 1, interval=100)

plt.show()
