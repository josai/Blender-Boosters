import bpy
import csv
from pathlib import Path


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
        path = (bpy.data.scenes["Scene"].render.filepath)
        self.main_render_path = clip_path(path)
        self.current_render_path = self.main_render_path
        self.data_mgmt = Data_Management()


    def render_image(self, image_name):
        image_path = ((R'render-bin\ ')[:-1] + image_name)
        switch_path(self, image_path)
        bpy.ops.render.render(write_still=True)
        csv_file_path = self.current_render_path[:-len(image_path)]
        switch_path(self, image_path)
        # test
        t1 = Chromosome()
        t2 = Chromosome()
        t2.tile_x.attribute = 10
        test = [t1, t2]
        # end test
        self.data_mgmt.write_csv(csv_file_path, 'settings_data.csv', test)


def switch_path(path, file_name):
    '''
    This function makes sure to always switch to, or create, a sub path within
    your current rendering path. This helps to keep your 'actual' render 
    images seperate from the sample images that the script creates. The 
    sub folder is called 'creature-pool'.
    '''
    if path.current_render_path == path.main_render_path:
        print ('Switching file path to boosters...')
        sub_folder = (clip_path(R'boosters-data\ '))
        sub_render_path = (str(path.main_render_path) + sub_folder)
        path.current_render_path = str(clip_path(sub_render_path) + file_name)
    else:
        path.current_render_path = clip_path(path.main_render_path)
    bpy.data.scenes["Scene"].render.filepath = (path.current_render_path)


def clip_path(a_file_path):
    '''
    Clips a file path down to the current folder. This is to remove file 
    names from the path name.
    '''
    path = str(a_file_path)[::-1]
    backslash = ((R'\ ')[0])
    index = (path.index(backslash))
    path = ((path[index:])[::-1])
    return (path)


class Data_Management(object):
    '''
    This is a class for the data management of the .csv files the program
    creates and uses to store data on each gene.
    '''

    def write_csv(self, path, file_name, data):
        path = path + file_name
        file = Path(path)
        if file.is_file():
            print ('its reals')
            add_csv_log(path, data)
        else:
            create_csv(path, data)


def create_csv(path, data):
    '''
    This saves the dna of a chromosome in a csv file.
    '''
    head = (data[0].DNA_Strand)
    headers = []
    for header in head:
        headers.append(header.name)
    with open(path, 'w') as f:
        file = csv.writer(f, delimiter=',')
        file.writerow(headers)
    add_csv_log(path, data)


def add_csv_log(path, data):
    '''
    This saves the dna of a chromosome in a csv file.
    '''
    with open(path, 'a') as f:
        file = csv.writer(f, delimiter=',')
        attributes = []
        print (len(data))
        for data_point in data:
            for fine_data in data_point.DNA_Strand:
                attributes.append(fine_data.attribute)
            print (attributes)
            file.writerow(attributes)
            attributes = []


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
                                       None,
                                       'tile_x'
                                       )
        self.tile_y = DNA(scene.render.tile_y, 
                                       False,
                                       1,
                                       1000,
                                       None,
                                       'tile_y'
                                       )
        self.DNA_Strand = [self.tile_x, self.tile_y]


class DNA(object):
    '''
    - Mediator
    The dna class acts as an adpater between blender settings and the 
    boosters program. It facilates the interactions between boosters
    functions and blenders render settings.
    '''
    def __init__(self, raw_material, boolean, minimum, maximum, key, name):
        self.real_setting = raw_material
        self.key = key
        if self.key != None:
            self.attribute = self.real_setting[1][self.key]
        else:
            self.attribute = self.real_setting
        self.boolean = boolean
        self.minimum = minimum
        self.maximum = maximum
        self.name = name


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