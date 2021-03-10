print("\n\n/===================================================/")
print("\\===================================================\\")
print("/=========  Tecplot 360 Video/GIF Creator  =========/ ")
print("\\=========       By: Oscar Alvarez         =========\\")
print("/=========             2021                =========/ ")
print("\\=========   mathoscaralvarez@gmail.com    =========\\")
print("/===================================================/ ")
print("\\---------------------------------------------------\\")
print("/----------- PRESS CTRL + 'C' TO EXIT --------------/ ")
print("\\---------------------------------------------------\\")

## Load files
import os

path = os.getcwd()
print("Current Directory: " + path)
f_found = False # Files found boolean
while(not f_found):
    f_begin = input("\nENTER THE FIRST SNAPSHOT NUMBER:  ")
    f_end = int(input("ENTER THE LAST SNAPSHOT NUMBER:  "))
    f_interval = int(input("ENTER THE SNAPSHOT INCREMENT NUMBER:  "))

    # f_begin = str(120100)
    # f_end = 121000
    # f_interval = 100

    snapshot = []
    f_num = f_begin
    f_count = 0
    for f in os.listdir():
        f_name, extension = os.path.splitext(f)
        if f_num in f_name:
            snapshot.append(f_name)
            f_count += 1
            f_num = str(int(f_num) + f_interval)
        if int(f_num) > f_end:
            break

    print("\nFiles Found: ")
    print(*snapshot, sep = '\n') # Printing files separated by new line character
    print("Number of files found:  " + str(f_count))

    confirm = input("\nCONTINUE? [Y/y for YES; ANY KEY to TRY AGAIN]:  ")
    f_found = (confirm.lower() == 'y') # Checks if the files were found

# Optional file for plotting stream traces
# seed_file = os.path.join(path, "seedpoints.txt")

## Starting up Tecplot
import logging
import sys
import tecplot as tp
from tecplot.plot import IsosurfaceGroup
from tecplot.constant import *

print("Opening Tecplot ...\n")
logging.basicConfig(level=logging.DEBUG)
if '-c' in sys.argv:
    tp.session.connect()

print("Tecplot Open.")


#### Creating Tecplot Images

## Creating Temporary Image Folder
img_fname = f_begin + '-' + str(f_end) + ' Images' # Image folder name

# Check if temporary folder already exists, if not create it.
if not os.path.isdir(img_fname) : os.mkdir(img_fname)
img_fpath = os.path.join(path, img_fname)

func_file = [None] * f_count
grid_file = [None] * f_count
for i in range(f_count):
    ## Read Files
    print("Reading " + snapshot[i] + " ...")

    ## Creating function (.fun) and grid (.xyz) files
    func_file[i] = os.path.join(path, snapshot[i] + '.fun')
    grid_file[i] = os.path.join(path, snapshot[i] + '.xyz')

    tp.new_layout() # Deleting old layout and starting a new one

    # Opening grid and function file in Tecplot
    dataset = tp.data.load_plot3d(grid_filenames=grid_file[i], function_filenames=func_file[i])
    print("\t" + snapshot[i] + " Loaded.")

    print("\tConfiguring Settings ...")
    ## Setup frame as Cartesinan 3D
    frame = tp.active_frame()
    frame.plot_type = tp.constant.PlotType.Cartesian3D
    plot = frame.plot()

    ## Camera View Settings
    #view = plot.view
    #view.psi = 65.777
    #view.theta = 166.415
    #view.alpha = -1.05394
    #view.position = (-23.92541680486183, 101.8931504712126, 47.04269529295333)
    #view.width = 1.3844

    ## Iso Surface / Contour Settings
    plot.show_isosurfaces = True
    contour = plot.contour(0)
    contour.colormap_name = 'Magma'
    contour.variable = dataset.variable('F1V11') # Set Liutex Magnitude as Iso-Surface
    contour.legend.show = True

    iso = plot.isosurface(0)
    iso.show = True
    iso.definition_contour_group = contour
    iso.isosurface_selection = IsoSurfaceSelection.OneSpecificValue
    iso.isosurface_values = 0.2 # Value of Iso surface that will be drawn
    iso.shade.use_lighting_effect = True
    iso.effects.lighting_effect = LightingEffect.Gouraud
    iso.contour.show = True
    iso.contour.contour_type = ContourType.Flood

    ## Liutex Lines (stream traces)
    #plot.show_streamtraces = True

    ## Set up plot stream trace variables
    #plot.vector.u_variable = dataset.variable('F1V8')   # Liutex_x
    #plot.vector.v_variable = dataset.variable('F1V9')   # Liutex_y
    #plot.vector.w_variable = dataset.variable('F1V10')  # Liutex_z

    ## Setup slices
    #plot.show_slices = True

    print("\tSettings Configured.")

    ## Saving as .png image
    print("\tSaving PNG Image ...")
    img_name = snapshot[i] + '.png'
    img_file = os.path.join(img_fpath, img_name)
    tp.export.save_png(img_file, 1200, supersample=3) # save_png(img_name, [SIZE in pixels] of the image, anti-aliasing)
    print(snapshot[i] + " PNG Image Saved.\n")


## Close Tecplot
tp.session.stop()
print("Tecplot closed.\n")


#### Creating Video from Images
import moviepy.editor

# Entering Folder that Contains Pictures
os.chdir(img_fpath)
print("New Current Folder: ")
print(os.getcwd())

#### Pictures per second
fps = 2
####

# Saving All Picture Names into a List
frames = []
pics = [ f for f in os.listdir() if f.lower().endswith('.png') ]

# Creating Temporary Video Clip Object
clip = moviepy.editor.ImageSequenceClip(pics, fps)

# Creating Video File Name
vid_name = f_begin + '-' + str(f_end) + ' Video.MP4'
vid_file = os.path.join(path, vid_name)

# Saving Video File
clip.write_videofile(vid_file)

# Creating Video File Name
gif_name = f_begin + '-' + str(f_end) + ' GIF.gif'
gif_file = os.path.join(path, gif_name)

# Saving a GIF File
clip.write_gif(gif_file, fps=4)
