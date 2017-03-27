import bpy
import csv
import random
import string
from pathlib import Path
from datetime import datetime


def main():
    procreate(6)


def procreate(num_of_creatures):
    '''
    Creates x amount of creatures improving upon each iteration via
    fitness functions
    '''
    count = 0
    settings = Settings()
    blend = Commands()
    int_gene = Chromosome('master')
    #best_gene.mutagen(0.99)  # seed!
    int_gene.make_render_settings()
    blend.render_image(int_gene)
    best_gene = int_gene
    while count < num_of_creatures:
        gene = best_gene
        gene.name = str(count)
        gene.mutagen(settings.mutation_rate)
        gene.make_render_settings()
        blend.render_image(gene)
        best_gene = fitness_function(gene, blend)
        count += (1)


def fitness_function(gene_A, commands):
    '''
    Returns the fastest gene so far.
    '''
    path = commands.csv_file_path
    raw_csv = commands.data_mgmt.read_csv(path, 'data.csv')
    render_times = []
    if len(raw_csv) > 1:
        for line in raw_csv:
            line = line[::-1]
            render_time = convert_type(line[0])
            render_times.append(render_time)

        fastest = min(render_times)
        indexed = render_times.index(fastest)
        gene_A.import_settings(raw_csv[indexed])

    return (gene_A)


def print_spaces(num):
    '''
    Prints specified number of spaces in console.
    '''
    count = 0
    while count < num:
        print ('')
        count += 1


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
        image_path = ((R'render-bin\ ')[:-1] + chromosome.name)
        switch_path(self, image_path)

        print ('Rendering image: ' + str(chromosome.name))

        chromosome.start_timer()
        bpy.ops.render.render(write_still=True)
        chromosome.stop_timer()

        render_bin_path = self.current_render_path[:-len(chromosome.name)]
        chromosome.measure_fitness(render_bin_path, chromosome.name)

        self.csv_file_path = self.current_render_path[:-len(image_path)]
        switch_path(self, image_path)

        self.data_mgmt.write_csv(self.csv_file_path, 'data.csv', [chromosome])



def switch_path(path, file_name):
    '''
    This function makes sure to always switch to, or create, a sub path within
    your current rendering path. This helps to keep your 'actual' render 
    images seperate from the sample images that the script creates. The 
    sub folder is called 'creature-pool'.
    '''
    if path.current_render_path == path.main_render_path:
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


    def read_csv(self, path, file_name):
        '''
        Returns CSV as lists for each row
        '''
        path = path + file_name
        return_data = []
        with open(path, 'r') as f:
            reader = csv.reader(f)
            first_row = True
            for row in reader:
                if not first_row:
                    if len(row) > 0:
                        return_data.append(row)
                else:
                    first_row = False
        f.close()
        return return_data



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
    f.close()
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
    f.close()


class Chromosome(object):
    '''
    -Factory Method?
    In the chromosome is where we keep the DNA structure of each individual.
    A strand of DNA is simply a render setting in this case. By default it
    is set to what ever your current render settings are.
    '''
    def __init__(self, name):
        settings = bpy.data.scenes[0]
        self.name = name
        self.scene_settings = settings.render
        self.cycles_settings = settings.cycles
        self.aa_samples = DNA(self.cycles_settings.aa_samples,
                                       False,
                                       1,
                                       10000,
                                       'aa_samples'
                                       )
        self.ao_samples = DNA(self.cycles_settings.ao_samples,
                                       False,
                                       1,
                                       10000,
                                       'ao_samples'
                                       )
        self.blur_glossy = DNA(self.cycles_settings.blur_glossy,
                                       False,
                                       0,
                                       10,
                                       'blur_glossy'
                                       )
        self.debug_bvh_type = DNA(self.cycles_settings.debug_bvh_type,
                                       True,
                                       'DYNAMIC_BVH',
                                       'STATIC_BVH',
                                       'debug_bvh_type'
                                       )
        self.samples = DNA(self.cycles_settings.samples,
                                       False,
                                       1,
                                       999,
                                       'samples'
                                       )
        self.tile_x = DNA(self.scene_settings.tile_x, 
                                       False,
                                       1,
                                       1000,
                                       'tile_x'
                                       )
        self.tile_y = DNA(self.scene_settings.tile_y, 
                                       False,
                                       1,
                                       1000,
                                       'tile_y'
                                       )
        self.image_fitness = DNA(100.0,
                                       False,
                                       0.0,
                                       1.0,
                                       'image_fitness'
                                 )

        self.DNA_Strand = ['default']


    def mutagen(self, mutation_rate):
        '''
        Mutates a letter in the DNA strand if luck of the die would have it.
        '''
        setting_names = ['render_duration']
        for letter in self.DNA_Strand:
            if self.name not in setting_names:
                mutation = roll_dice(mutation_rate)
                if mutation:
                    letter.mutate()


    def make_render_settings(self):
        self.cycles_settings.aa_samples = self.aa_samples.attribute
        self.cycles_settings.ao_samples = self.ao_samples.attribute
        self.cycles_settings.blur_glossy = self.blur_glossy.attribute
        self.cycles_settings.debug_bvh_type = self.debug_bvh_type.attribute
        self.cycles_settings.samples = self.samples.attribute
        self.scene_settings.tile_x = self.tile_x.attribute
        self.scene_settings.tile_y = self.tile_y.attribute


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
        self.DNA_Strand = [self.aa_samples,
                           self.ao_samples,
                           self.blur_glossy,
                           self.debug_bvh_type,
                           self.samples,
                           self.tile_x, 
                           self.tile_y,
                           self.image_fitness,
                           self.render_duration
                           ]
        if len(self.DNA_Strand) > 3:
            for letter in self.DNA_Strand:
                print (str(letter.name) + ' ' + str(letter.attribute))
        else:
            print ('Defualted settings')


    def measure_fitness(self, path, file_name):
        '''
        Measures the fitness of an image in ralation to the master image.
        Returns the absolute difference in pixels as a proportion.
        '''
        if file_name != 'master.png':
            differences = []
            master = Img(path + 'master.png')
            image = Img(path + file_name + '.png')
            possible_colors = float(len(master.pixels) * 4)
            both_images = zip(image.pixels, master.pixels)
            for (pixel_color, master_color) in both_images:
                color_difference = abs(float(pixel_color - master_color))
                differences.append(color_difference)
            perfect_pixels = possible_colors - sum(differences)
            percent_correct = (perfect_pixels / possible_colors) * 100
            self.image_fitness.attribute = percent_correct


    def import_settings(self, list_of_attributes):
        '''
        Imports settings from a list of attributes.
        '''
        if len(self.DNA_Strand) > 1:
            both_lists = zip(list_of_attributes, self.DNA_Strand)
            for (attribute, dna) in both_lists:
                print (dna.attribute)
                dna.attribute = convert_type(attribute)
        else:
            print ("Couldn't import data from csv")


def convert_type(a_string):
    '''
    Converts a string to the proper data type.
    This is for getting raw data from a csv.

    Parses the string and returns as proper format.
    '''
    a_string = str(a_string)
    alphabet = string.ascii_letters
    numbers = string.digits
    for character in a_string:
        if character in alphabet:
            print ('is alpha')
            if a_string == 'True':
                return (True)
            elif a_string == 'False':
                return (False)
            else:
                return (a_string)
        elif ':' in a_string:
            date = datetime.strptime(a_string,"%H:%M:%S.%f")
            return date
        elif '.' in a_string:
            return float(a_string)
        else:
            return int(a_string)







class Img(object):
    '''
    This acts as a facade for dealing with image data.
    '''
    def __init__(self, image_path):
        images = bpy.data.images
        images.load(image_path)
        self.image = images[0]
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pixel_count = (self.width * self.height)
        self.pixels = self.image.pixels[:] #fl


def roll_dice(odds):
    '''
    Rolls the dice, returns true or false if  the roll is less than the odds.
    '''
    roll = random.uniform(0.00001, 0.99999)
    if roll < odds:
        return True
    else:
        return False


class DNA(object):
    '''
    - Adapter/mold?
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
            attribute_type = type(self.attribute)
            floating_type = type(10.00)
            if attribute_type == floating_type:
                self.attribute = random.uniform(self.minimum, self.maximum)
            else:
                self.attribute = random.randint(self.minimum, self.maximum)




if __name__ == "__main__":
    main()