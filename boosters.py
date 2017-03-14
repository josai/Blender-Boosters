import bpy
import csv
import random
from pathlib import Path
from datetime import datetime


def main():
    count = 0
    settings = Settings()
    blend = Commands()
    while count < 5:
        gene = Chromosome(str(count))
        gene.mutagen(settings.mutation_rate)
        gene.make_render_settings()
        blend.render_image(gene)
        count += (1)


class Settings(object):
    '''
    Global settings such as mutation rate
    '''
    def __init__(self):
        self.mutation_rate = 0.5


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


    def render_image(self, chromosome):
        tester(chromosome)
        image_path = ((R'render-bin\ ')[:-1] + chromosome.name)
        switch_path(self, image_path)
        chromosome.start_timer()
        bpy.ops.render.render(write_still=True)
        chromosome.stop_timer()
        csv_file_path = self.current_render_path[:-len(image_path)]
        switch_path(self, image_path)
        self.data_mgmt.write_csv(csv_file_path, 'data.csv', [chromosome])


def tester(dna):
    cycles = bpy.types.CyclesRenderSettings
    scene = bpy.data.scenes[0]
    cy = [cycles.aa_samples, 
               cycles.ao_samples,
               cycles.blur_glossy, 
               cycles.debug_bvh_type,
               cycles.debug_use_spatial_splits,
               cycles.device,
               cycles.diffuse_bounces,
               cycles.film_exposure,
               cycles.samples,
             ]



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
        for data_point in data:
            for fine_data in data_point.DNA_Strand:
                attributes.append(fine_data.attribute)
            file.writerow(attributes)
            attributes = []


class Chromosome(object):
    '''
    In the chromosome is where we keep the DNA structure of each individual.
    A strand of DNA is simply a render setting in this case. By default it
    is set to what ever your current render settings are.
    '''
    def __init__(self, name):
        self.name = name
        cycles = bpy.types.CyclesRenderSettings
        scene = bpy.data.scenes[0]
        self.samples = DNA(scene.cycles.samples,
                                       False,
                                       1,
                                       999,
                                       'samples'
                                       )

        self.tile_x = DNA(scene.render.tile_x, 
                                       False,
                                       1,
                                       1000,
                                       'tile_x'
                                       )
        self.tile_y = DNA(scene.render.tile_y, 
                                       False,
                                       1,
                                       1000,
                                       'tile_y'
                                       )

        self.DNA_Strand = [self.samples,
                           self.tile_x, 
                           self.tile_y
                           ]


    def mutagen(self, mutation_rate):
        '''
        Mutates the DNA in the DNA strand based off random chance and
        mutation rate.
        '''
        for strand in self.DNA_Strand:
            mutation = roll_dice(mutation_rate)
            if mutation:
                strand.mutate()


    def make_render_settings(self):
        #self.DNA_Strand = (list(set(self.DNA_Strand)))
        settings = bpy.data.scenes[0]
        scene_settings = settings.render
        cycles_settings = settings.cycles
        cycles_settings.samples = self.samples.attribute
        scene_settings.tile_x = self.tile_x.attribute
        scene_settings.tile_y = self.tile_y.attribute
        for dna in self.DNA_Strand:
            print (str(dna.name) + ' ' + str(dna.attribute))


    def start_timer(self):
        self.render_duration = DNA(datetime.now(), 
                                       True,
                                       0,
                                       1,
                                       'render_duration'
                                       )


    def stop_timer(self):
        start = self.render_duration.attribute
        self.render_duration.attribute = datetime.now() - start
        self.DNA_Strand.append(self.render_duration)
        print (self.render_duration.attribute)


def roll_dice(odds):
    roll = random.uniform(0.00001, 0.99999)
    if roll < odds:
        return True
    else:
        return False


class DNA(object):
    '''
    - Mediator
    The dna class acts as an adpater between blender settings and the 
    boosters program. It facilates the interactions between boosters
    functions and blenders render settings.
    '''
    def __init__(self, raw_material, boolean, minimum, maximum, name):
        self.attribute = raw_material
        self.boolean = boolean
        self.minimum = minimum
        self.maximum = maximum
        self.name = name


    def mutate(self):
        '''
        Mutates a piece of DNA.
        '''
        if self.boolean:
            self.attribute = random.choice([self.minimum, self.maximum])
        else:
            floating = type(10.00)
            t = type(self.attribute)
            if t == floating:
                self.attribute = random.uniform(self.minimum, self.maximum)
            else:
                self.attribute = random.randint(self.minimum, self.maximum)




if __name__ == "__main__":
    main()