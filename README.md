# Blender-Boosters
**Blender-Boosters** is a script/plugin designed to find optimal render settings for reducing [Blender 3Ds](https://www.blender.org/) render time on any given machine.


### Approach 

**Blender-Boosters** uses a genetic algorithm to effectively determine what the optimum render settings are  for a given scene on a given machine. It does this by rendering several "sample" renders with different settings. Then out of the samples it uses the fastest rendered settings and continues to iterate upon that, repeating the process for several generations. until you hopefully have much more efficient settings for your set up.
