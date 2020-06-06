import bpy
import csv
import random
import string
from pathlib import Path
from datetime import datetime


def main():
    timr = Chromosome('timer')
    timr.start_timer()

    total_frames = set_most_difficult_frame()
    procreate(total_frames / 3)

    # Renders animation



    blend = Commands()
    gene = Chromosome('master')
    blend.render_folder = (R'real_render-bin\ ')[:-1]
    blend.render_image(gene)
    scene = bpy.data.scenes[0]
    current_frame = scene.frame_start
    last_frame = scene.frame_end
    while current_frame <= last_frame:
      gene.name = str(current_frame)
      scene.frame_set(current_frame)
      blend.render_image(gene)
      current_frame += 1

    timr.stop_timer()
    print ('Total render time including boosters = ' + str(timr.render_duration.attribute))



def set_most_difficult_frame():


    print ('Finding most difficult frame to render...')
    blend = Commands()
    scene = bpy.data.scenes[0]
    orginal_size = scene.render.resolution_percentage
    scene.render.resolution_percentage = 10

    last_frame = scene.frame_end
    current_frame = scene.frame_start
    total_frames = last_frame - current_frame
    current_render_settings = Chromosome('master')
    blend.csv_file = 'tiny_animation.csv'
    blend.render_folder = (R'tiny_render-bin\ ')[:-1]
    blend.render_image(current_render_settings)
    while current_frame < last_frame:
      current_render_settings.name = str(current_frame)
      scene.frame_set(current_frame)
      blend.render_image(current_render_settings)
      current_frame += 5
    gene = current_render_settings

    
    fast_frame = fitness_function(gene, blend, 0.0, min)
    print ('Fastest frame = ' + str(fast_frame.name) + ' ' + str(fast_frame.render_duration.attribute))
    slowest_frame = fitness_function(gene, blend, 0.0, max)
    print ('flowest frame = ' + str(slowest_frame.name) + ' ' + str(slowest_frame.render_duration.attribute))
    
    if slowest_frame.name != 'master':
      hardest_frame = int(slowest_frame.name)
      print ('Hardest frame to render is: ' + str(hardest_frame))
      scene.frame_set(hardest_frame)

    scene.render.resolution_percentage = orginal_size
    return (total_frames)




def procreate(num_of_creatures):
    '''
    Creates x amount of creatures improving upon each iteration via
    fitness functions
    '''
    count = 1
    settings = Settings()
    blend = Commands()
    int_gene = Chromosome('master')
    #best_gene.mutagen(0.99)  # seed!
    int_gene.make_render_settings()
    blend.render_image(int_gene)
    min_fitness_level = settings.minimum_image_fitness
    best_gene = int_gene
    while count < num_of_creatures:
        gene = best_gene
        gene.samples.attribute = 1
        gene.name = str(count)
        gene.mutagen(settings)
        gene.make_render_settings()
        blend.render_image(gene)
        best_gene = fitness_function(gene, blend, min_fitness_level, min)
        count += (1)

    best_gene = fitness_function(gene, blend, min_fitness_level, min)
    gene.make_render_settings()


def fitness_function(gene_A, commands, min_fitness_level, function):
    '''
    Returns the fastest gene so far.
    '''
    path = commands.csv_file_path
    raw_csv = commands.data_mgmt.read_csv(path, commands.csv_file)
    render_times = []
    indexes = []
    new_gene = gene_A
    if len(raw_csv) > 1:
        in_num = 0
        for line in raw_csv:
            line = line[::-1]
            render_time = convert_type(line[0])
            fitness_level = convert_type(line[1])
            if fitness_level >= min_fitness_level:
              render_times.append(render_time)
              indexes.append(in_num)
            in_num += 1

        fastest = function(render_times)
        indexed = render_times.index(fastest)
        real_index = indexes[indexed]
        new_gene.import_settings(raw_csv[real_index])

    return (new_gene)


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
        self.mutation_rate = 0.05
        self.minimum_image_fitness = 90

        self.original_render_settings = get_original_settings()
        self.safe_mode_exceptions = ['tile_x',
                                     'tile_y',
                                     'debug_bvh_type',
                                     'device',
                                     'progressive',
                                     'seed',
                                     'shading_system'
                                     ]
        self.safe_mode = True
        # Safe mode prevents render settings from being larger than the
        # orginal settings. (i.e. samples being 1000 when the original
        # settings had 30 samples.) It also prevents "dangerous" settings from
        # being allowed. 


def get_original_settings():
  '''
  Gets original render settings
  '''
  return Chromosome('Original_settings')


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
        self.csv_file = 'data.csv'
        self.render_folder = (R'render-bin\ ')[:-1]


    def render_image(self, chromosome):
        image_path = (self.render_folder + chromosome.name)
        switch_path(self, image_path)

        print ('Rendering image: ' + str(chromosome.name))

        chromosome.start_timer()
        bpy.ops.render.render(write_still=True)
        chromosome.stop_timer()

        render_bin_path = self.current_render_path[:-len(chromosome.name)]
        chromosome.measure_fitness(render_bin_path, chromosome.name)
        print (chromosome.image_fitness.attribute)

        self.csv_file_path = self.current_render_path[:-len(image_path)]
        switch_path(self, image_path)

        self.data_mgmt.write_csv(self.csv_file_path, self.csv_file, [chromosome])



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


    def add_csv_log(self, path, data):
        '''
        This saves the dna of a chromosome in a csv file.
        '''
        with open(path, 'a') as f:
            file = csv.writer(f, delimiter=',')
            # Includes name of the image.
            for data_point in data:
                attributes = [str(data_point.name)]
                for fine_data in data_point.DNA_Strand:
                    attributes.append(fine_data.attribute)
                file.writerow(attributes)
                #attributes = []
        f.close()


    def create_csv(self, path, data):
        '''
        This saves the dna of a chromosome in a csv file.
        '''
        head = (data[0].DNA_Strand)
        # Int with name field
        headers = ['name']
        for header in head:
            headers.append(header.name)
        with open(path, 'w') as f:
            file = csv.writer(f, delimiter=',')
            file.writerow(headers)
        f.close()
        self.add_csv_log(path, data)


    def write_csv(self, path, file_name, data):
        path = path + file_name
        file = Path(path)
        if file.is_file():
            self.add_csv_log(path, data)
        else:
            self.create_csv(path, data)


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

        self.device = DNA(self.cycles_settings.device,
                                       True,
                                       'CPU',
                                       'GPU',
                                       'device'
                                       )
        self.diffuse_bounces = DNA(self.cycles_settings.diffuse_bounces,
                                       False,
                                       0,
                                       1024,
                                       'diffuse_bounces'
                                       )
        self.diffuse_samples = DNA(self.cycles_settings.diffuse_samples,
                                       False,
                                       1,
                                       10000,
                                       'diffuse_samples'
                                       )
        self.filter_type = DNA(self.cycles_settings.filter_type,
                                       True,
                                       'BOX',
                                       'GAUSSIAN',
                                       'filter_type'
                                       )
        self.filter_width = DNA(self.cycles_settings.filter_width,
                                       False,
                                       0.01,
                                       10.0,
                                       'filter_width'
                                       )
        self.glossy_bounces = DNA(self.cycles_settings.glossy_bounces,
                                       False,
                                       0,
                                       1024,
                                       'glossy_bounces'
                                       )
        self.glossy_samples = DNA(self.cycles_settings.glossy_samples,
                                       False,
                                       0,
                                       10000,
                                       'glossy_samples'
                                       )
        self.max_bounces = DNA(self.cycles_settings.max_bounces,
                                       False,
                                       0,
                                       1024,
                                       'max_bounces'
                                       )
        self.mesh_light_samples = DNA(self.cycles_settings.mesh_light_samples,
                                       False,
                                       1,
                                       10000,
                                       'mesh_light_samples'
                                       )
        self.min_light_bounces = DNA(self.cycles_settings.min_light_bounces,
                                       False,
                                       0,
                                       1024,
                                       'min_light_bounces'
                                       )
        # Doesn't exist apperently ? -.-
        #self.no_caustics = DNA(self.cycles_settings.no_caustics,
        #                               True,
        #                               True,
        #                               False,
        #                               'no_caustics'
        #                               )
        self.progressive = DNA(self.cycles_settings.progressive,
                                       True,
                                       'PATH',
                                       'BRANCHED_PATH',
                                       'progressive'
                                       )
        # Doesn't exist apperently ? -.-
        #self.sample_clamp = DNA(self.cycles_settings.sample_clamp,
        #                               False,
        #                               0,
        #                               1000, # fake default. It's INF!
        #                               'sample_clamp'
        #                               )
        
        self.samples = DNA(self.cycles_settings.samples,
                                       False,
                                       1,
                                       999,
                                       'samples'
                                       )

        self.seed = DNA(self.cycles_settings.seed,
                                       False,
                                       0,
                                       99999,
                                       'seed'
                                       )
        self.shading_system = DNA(self.cycles_settings.shading_system,
                                       True,
                                       True,
                                       False,
                                       'shading_system'
                                       )
        self.transmission_bounces = DNA(self.cycles_settings.transmission_bounces,
                                       False,
                                       0,
                                       1024,
                                       'transmission_bounces'
                                       )
        self.transparent_max_bounces = DNA(self.cycles_settings.transparent_max_bounces,
                                       False,
                                       0,
                                       1024,
                                       'transparent_max_bounces'
                                       )
        self.min_transparent_bounces = DNA(self.cycles_settings.min_transparent_bounces,
                                       False,
                                       0,
                                       1024,
                                       'min_transparent_bounces'
                                       )

        # Doesn't exist apperently ? -.-
        #self.use_cache = DNA(self.cycles_settings.use_cache,
        #                               True,
        #                               True,
        #                               False,
        #                               'use_cache'
        #                               )



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
        self.int_strand(2)


    def mutagen(self, settings):
        '''
        Mutates a letter in the DNA strand if luck of the die would have it.
        '''
        self.int_strand(2)
        mutation_rate = settings.mutation_rate
        for letter in self.DNA_Strand:
          mutation = roll_dice(mutation_rate)
          if mutation:
              letter.mutate()
              if settings.safe_mode:
                safe_mode_exceptions = settings.safe_mode_exceptions
                letter_index = self.DNA_Strand.index(letter)
                orginal_strand = settings.original_render_settings.DNA_Strand
                original_letter = orginal_strand[letter_index]
                if letter.name not in safe_mode_exceptions:
                  if not letter.boolean:
                    # So that only non-booleans and specific exceptions
                    # are subject to safe mode.
                    if letter.attribute > original_letter.attribute:
                      letter.attribute = original_letter.attribute
                      letter.maximum = original_letter.attribute
        self.int_strand(2)


    def int_strand(self, mode):
      '''
      Assigns self.DNA_strand variable for the appropriate use case. Such
      as printing or mutations. Mode is the use case.
      '''
      strand = [self.aa_samples,
                       self.ao_samples,
                       self.blur_glossy,
                       self.debug_bvh_type,
                       self.device,
                       self.diffuse_bounces, 
                       self.diffuse_samples,
                       self.filter_type,
                       self.filter_width,
                       self.glossy_bounces,
                       self.glossy_samples,
                       self.max_bounces,
                       self.mesh_light_samples,
                       self.min_light_bounces,
                       self.progressive,
                       self.samples,
                       self.seed,
                       self.shading_system,
                       self.transmission_bounces,
                       self.transparent_max_bounces,
                       self.min_transparent_bounces,
                       #self.use_cache,
                       self.tile_x,
                       self.tile_y,
                       ]
      if mode == 1:
        # For printing or saving in a CSV.
        strand = strand + [self.image_fitness, self.render_duration]
      if mode == 2:
        # For mutations or modifications of render settings.
        strand = strand
      if mode == 3:
        # Don't use. This is a null.
        strand = ['Default']
      self.DNA_Strand = strand




    def make_render_settings(self):
        self.cycles_settings.aa_samples = self.aa_samples.attribute
        self.cycles_settings.ao_samples = self.ao_samples.attribute
        self.cycles_settings.blur_glossy = self.blur_glossy.attribute
        self.cycles_settings.debug_bvh_type = self.debug_bvh_type.attribute

        self.cycles_settings.device = self.device.attribute
        self.cycles_settings.diffuse_bounces = self.diffuse_bounces.attribute
        self.cycles_settings.diffuse_samples = self.diffuse_samples.attribute
        self.cycles_settings.filter_type = self.filter_type.attribute
        self.cycles_settings.filter_width = self.filter_width.attribute
        self.cycles_settings.glossy_bounces = self.glossy_bounces.attribute
        self.cycles_settings.glossy_samples = self.glossy_samples.attribute
        self.cycles_settings.max_bounces = self.max_bounces.attribute
        self.cycles_settings.mesh_light_samples = self.mesh_light_samples.attribute
        self.cycles_settings.min_light_bounces = self.min_light_bounces.attribute
        #self.cycles_settings.no_caustics = self.no_caustics.attribute
        self.cycles_settings.progressive = self.progressive.attribute
        #self.cycles_settings.sample_clamp = self.sample_clamp.attribute



        self.cycles_settings.samples = self.samples.attribute
        self.cycles_settings.seed = self.seed.attribute
        self.cycles_settings.shading_system = self.shading_system.attribute
        self.cycles_settings.transmission_bounces = self.transmission_bounces.attribute
        self.cycles_settings.transparent_max_bounces = self.transparent_max_bounces.attribute
        self.cycles_settings.min_transparent_bounces = self.min_transparent_bounces.attribute
        #self.cycles_settings.use_cache = self.use_cache.attribute



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
        self.int_strand(1)


    def print_strand(self):
        if len(self.DNA_Strand) > 3:
            for letter in self.DNA_Strand:
                print (str(letter.name) + ' ' + str(letter.attribute))
        else:
            print ('Defualted settings')


    def measure_fitness(self, path, file_name):
        '''
        Measures the fitness of an image in ralation to the master image.
        Returns the absolute difference in pixels as a floating percentage.
        '''
        if file_name != 'master':
            differences = []
            master = Img(path,'master.png')
            image = Img(path, (file_name + '.png'))
            possible_colors = float(len(master.pixels) * 4)
            both_images = zip(image.pixels, master.pixels)
            for (pixel_color, master_color) in both_images:
                color_difference = abs(pixel_color - master_color)
                differences.append(color_difference)

            # Total similarity as percent.
            accuracy = sum(differences) / float(len(master.pixels))
            percent_accuracy = 100 - (accuracy * 100)
            self.image_fitness.attribute = percent_accuracy
    
        else:
            self.image_fitness.attribute = 100.0


    def import_settings(self, list_of_attributes):
        '''
        Imports settings from a list of attributes that are text-strings.
        '''
        if len(self.DNA_Strand) > 1:
            self.name = convert_type(list_of_attributes[0])
            list_of_attributes = list_of_attributes[1:]
            both_lists = zip(list_of_attributes, self.DNA_Strand)
            for (attribute, dna) in both_lists:
                dna.attribute = convert_type(attribute)
        else:
            print ("Couldn't import data from csv")


def convert_type(a_string):
    '''
    Converts a string to the proper data type.
    This is for getting raw data from a CSV.

    In other words, it parses the string and returns it as the proper data
    format because they are inputted as text-strings.
    '''
    a_string = str(a_string)
    alphabet = string.ascii_letters
    numbers = string.digits
    for character in a_string:
        if character in alphabet:
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
    def __init__(self, image_path, image_name):
        bimages = bpy.data.images
        bimages.load(image_path + image_name)
        self.image = bimages[image_name]
        self.width = self.image.size[0]
        self.height = self.image.size[1]
        self.pixel_count = (self.width * self.height)
        self.pixels = self.image.pixels[:]


def roll_dice(odds):
    '''
    Rolls the dice, returns true or false if the roll is less than the odds.
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