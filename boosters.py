import bpy
import csv


def main():
    blend = Commands()
    first = Chromosome()
    blend.render_image('hiiiii')
    blend.render_image('byeeee')


class Commands(object):
    '''
    -Mediator
    This is a class for short hand commands. It makes it easier to read,
    write, and use the bpy functions by providing a simpler interface
    for the purposes of this program.
    '''
    def __init__(self):
        self.main_render_path = (str(bpy.data.scenes["Scene"].render.filepath))
        self.current_render_path = self.main_render_path
        self.data_mgmt = Data_Management()


    def render_image(self, image_name):
        image_path = self
        switch_path(image_path, image_name)
        bpy.ops.render.render(write_still=True)
        p = self.current_render_path
        switch_path(image_path, image_name)
        self.data_mgmt.add_csv_log(p, 'test.csv', [1, 3])


def switch_path(path, file_name):
    '''
    This function makes sure to always switch to, or create, a sub path within
    your current rendering path. This helps to keep your 'actual' render 
    images seperate from the sample images that the script creates. The 
    sub folder is called 'creature-pool'.
    '''
    if path.current_render_path == path.main_render_path:
        print ('Switching file path to boosters...')
        sub_folder = (R'boosters-data\ ')
        sub_render_path = (str(path.main_render_path) + sub_folder)
        path.current_render_path = str(sub_render_path + file_name)
    else:
        path.current_render_path = str(path.main_render_path)
    bpy.data.scenes["Scene"].render.filepath = (path.current_render_path)


class Data_Management(object):
    '''
    This is a class for the data management of the .csv files the program
    creates and uses to store data on each gene.
    '''

    def add_csv_log(self, path, file_name, data):
        '''
        This saves the dna of a chromosome in a csv file.
        '''
        path = path + file_name
        with open(path, 'w') as csvfile:
            filewriter = csv.writer(csvfile, delimiter=' ')
            for data_point in data:
                filewriter.writerow('hi')




class Chromosome(object):
    '''
    In the chromosome is where we keep the DNA structure of each individual.
    A strand of DNA is simply a render setting in this case. By default it
    is set to what ever your current render settings are.
    '''
    def __init__(self):
        cycles = bpy.types.CyclesRenderSettings
        scene = bpy.data.scenes[0]
        self.render_duration = 0.0
        self.tile_x = DNA(scene.render.tile_x, 
                                       False,
                                       1,
                                       1000,
                                       None
                                       )
        self.tile_y = DNA(scene.render.tile_y, 
                                       False,
                                       1,
                                       1000,
                                       None
                                       )
        print (scene.render.tile_x)


class DNA(object):
    '''
    - Mediator
    The dna class acts as an adpater between blender settings and the 
    boosters program. It facilates the interactions between boosters
    functions and blenders render settings.
    '''
    def __init__(self, raw_material, boolean, minimum, maximum, key):
        self.real_setting = raw_material
        self.key = key
        if self.key != None:
            self.attribute = self.real_setting[1][self.key]
        else:
            self.attribute = self.real_setting
        self.boolean = boolean
        self.minimum = minimum
        self.maximum = maximum


    def make_real(self):
        '''
        This function re-instantiates the variables into the dna as "real"
        under the .real_setting variable. The .real_setting variable is used
        to give quick access for replacement of a blender render setting.
        This should be used after any time variables may have been changed.
        '''
        if self.key != None:
            self.real_setting[1][self.key] = self.attribute
        else:
            self.real_setting = self.attribute






if __name__ == "__main__":
    main()