from testeo import Car, Highway
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from random import randint
import numpy as np
import cv2

def rotate_bound(image, angle):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w // 2, h // 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH), borderValue=(255,255,255))


Auto_colors = ['Auto_y', 'Auto_b', 'Auto_k', 'Auto_w']

agp = Highway(length = 14 * 1000)

agp.add_Auto(Car(x=0  , v=0, vel_max=120, a=2, l=5, tr=1, vd=120, fc=None, bc=None, will_measure=True))
agp.add_Auto(Car(x=100, v=0, vel_max=100, a=2, l=5, tr=1, vd=120, fc=None, bc=None, will_measure=True))
agp.add_Auto(Car(x=200, v=0, vel_max=110, a=2, l=5, tr=1, vd=120, fc=None, bc=None, will_measure=True))
agp.add_Auto(Car(x=300, v=0, vel_max=150, a=2, l=5, tr=1, vd=120, fc=None, bc=None, will_measure=True))
agp.add_Auto(Car(x=400, v=0, vel_max=200, a=2, l=5, tr=1, vd=1000, fc=None, bc=None, will_measure=True))

# Add more Autos
for i in range(30):
    agp.add_Auto(Car(x=500 + i*100, v=0, vel_max=120 + i*2, a=2, l=5, tr=1, vd=120, fc=None, bc=None, will_measure=True))

fig, ax = plt.subplots(figsize=(22, 2))

# tight_layout makes sure the axis and title are not cropped
fig.tight_layout()

ax.set_xlim(0, agp.length)
ax.set_ylim(-3, 10)

# ax hide y axis
ax.set_yticks([])

# Hide the right and top spines
# ax.spines['left'].set_visible(False)
# ax.spines['top'].set_visible(False)
# ax.spines['bottom'].set_visible(False)


lw = 4
# Plot lane lines
ax.plot([2, agp.length], [lw/2, lw/2], color='black', linewidth=2)
ax.plot([2, agp.length], [-lw/2, -lw/2], color='black', linewidth=2)

# Plot asphalt area
ax.fill_between([2, agp.length], [-lw/2, -lw/2], [lw/2, lw/2], color='lightgrey')

# Plot dashed center line
ax.plot([2, agp.length], [0, 0], color='white', linewidth=2, linestyle='dashed', dashes=(5, 5))

#Auto_im = OffsetImage(plt.imread('assets/Auto_y.png', format="png"), zoom=.2)

Auto_ims = [OffsetImage(plt.imread(f'assets/{Auto_color}.png', format="png"), zoom=.4) for Auto_color in Auto_colors]

# Animate with AnnotationBbox for each Car
def init():
    return []

def update(frame):
    # Once per frame
    # One frame is one second

    # Delete previous rendered Autos
    for artist in ax.artists:
        artist.remove()
    
    # Clear previous text
    # ax.texts = [] AttributeError: can't set attribute
    # fix
    for txt in ax.texts:
        #txt.set_visible(False)
        txt.remove()

    status = agp.update()

    #if len(agp.get_Autos()) < 5:
    if agp.get_back_Auto().get_position() > agp.length / np.random.normal(20, 2):

        agp.add_Auto(
            Car(x=None, v=0, 
            #vel_max=2,
            vel_max=int(np.random.normal(120, 10)),
            a=int(np.random.normal(2, 1)),
            l=1.5, tr=1, vd=10, fc=None, bc=None, will_measure=True)
        )

    if not status:
        # Stop animation
        # return []
        pass

    artists = []

    for Car in agp.get_Autos()[::-1]:           
        
        x = Car.get_position()
        v = Car.v
        
        Auto_color = Auto_colors[Car.id % len(Auto_colors)]
        #if Car.crashed:
        #    Auto_color = 'Auto_r'
        #Auto_im = #cv2.imread(f'assets/{Auto_color}.png', cv2.IMREAD_UNCHANGED)
        Auto_im = plt.imread(f'assets/{Auto_color}.png', format="png")
        
        # Drift: saAuto
        # if v > 140:
        #   angle = -20 * np.sin(2 * np.pi * frame / 100)
        #   Auto_im = rotate_bound(Auto_im, angle)
        
        Auto_oi = OffsetImage(Auto_im, zoom=.4)
        ab = AnnotationBbox(Auto_oi, (x, 0), frameon=False)
        
        artists.append(ax.add_artist(ab))


    xdata = agp.get_Autos_positions()
    vdata = agp.get_Autos_velocities()
    tdata = agp.get_Autos_times()
    crashes = [1 if Car.crashed else 0 for Car in agp.get_Autos()]
    ids = [Car.id for Car in agp.get_Autos()]
        
    # Plot Car velocities and positions as text
    ax.text(0.1, 0.9, f"Velocities: {vdata}", transform=ax.transAxes)
    ax.text(0.1, 0.8, f"Positions: {xdata}", transform=ax.transAxes)
    ax.text(0.1, 0.7, f"Times: {tdata}", transform=ax.transAxes)
    ax.text(0.1, 0.6, f"Crashes: {crashes}", transform=ax.transAxes)
    ax.text(0.1, 0.5, f"IDs: {ids}", transform=ax.transAxes)

    # set font family and font size
    for txt in ax.texts:
        txt.set_fontfamily('monospace')
        #txt.set_fontsize(10)


    return artists

FRAMES = 500
INTERVAL = 0
FPS = 30

# Frames = 500
# Interval (Delay between frames in milliseconds) = 0
# FPS = 30
# For the saved animation the duration is going to be frames * (1 / fps) (in seconds)
# 500 * (1 / 30) = 16.666666666666668 seconds

FRAMES = 60
INTERVAL = 0
FPS = 1

ani = animation.FuncAnimation(fig, update, frames=FRAMES, init_func=init, blit=True, interval=INTERVAL)
ani.save('animation.mp4', fps=FPS, extra_args=['-vcodec', 'libx264', '-pix_fmt', 'yuv420p'])