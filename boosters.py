import bpy


def main():
    blend = commands()
    blend.render_image('hiiiii')
    blend.render_image('byeeee')


class commands(object):
    '''
    This is a class for short hand commands. It makes it easier to read,
    write, and use the bpy functions by providing a simpler interface
    for the purposes of this program.
    '''
    def __init__(self):
        self.main_render_path = (str(bpy.data.scenes["Scene"].render.filepath))
        self.current_render_path = self.main_render_path


    def render_image(self, image_name):
        switch_path(image_name, self)
        bpy.ops.render.render(write_still=True)
        switch_path(image_name, self)


def switch_path(image_name, path):
    '''
    This function makes sure to always switch to, or create, a sub path within
    your current rendering path. This helps to keep your 'actual' render 
    images seperate from the sample images that the script creates. The 
    sub folder is called 'creature-pool'.
    '''
    sub_folder = (R'creature-pool\ ')
    path.sub_render_path = (str(path.main_render_path) + sub_folder)
    if path.current_render_path == path.main_render_path:
        print ('Switching file path to creature pool...')
        path.current_render_path = str(path.sub_render_path[:-1] + image_name)
    else:
        path.current_render_path = str(path.main_render_path)

    bpy.data.scenes["Scene"].render.filepath = (path.current_render_path)



if __name__ == "__main__":
    main()