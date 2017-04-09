# Blender-Boosters
**Blender-Boosters** is a script/plugin designed to find optimal render settings for reducing [Blender 3Ds](https://www.blender.org/) render time on any given machine.


## Usage

* To use the program simply set up your animation to be the highest quality render that you are happy with.
* Select your render output folder and change the file extentions to be .PNG
* Then open up the script and run it. You may want to open the command prompt so you can see the progress.

Unfortunately boosters is windows only currently.


### Approach 

**Blender-Boosters** uses a genetic algorithm to optimize render settings for a given scene on a given machine. It does this by rendering several sample/prototype renders with different settings. Then out of the samples it uses the the settings that rendered the image the fastest and continues to iterate upon that prototype, repeating the process for several generations until you hopefully have much more time efficient settings for your set up.


### Benefits


### Drawbacks 



#### Quick References

[Cycles Render Settings API](https://docs.blender.org/api/blender_python_api_2_64_1/bpy.types.CyclesRenderSettings.html#bpy.types.CyclesRenderSettings.debug_cancel_timeout)
