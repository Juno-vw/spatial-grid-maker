import decimal
import operator
import functools
import json
import os
""" Creates a geographic grid, built for the Maidenhead Grid """


def char_range(c1, c2):
    """Generates the characters from `c1` to `c2`, inclusive."""
    characters = []
    for c in xrange(ord(c1), ord(c2)+1):
        characters.append(chr(c))
    return characters


## SETTUP YOUR GRID HERE

grid ={
        "false_easting":180,
        "false_northing":90,
        "x_min":-180,
        "x_max":180,
        "y_min":-90,
        "y_max":90,
        "levels":{
             0:char_range('A','R'),
             1:range(0,10),
             2:char_range('a','x')
         },
        "prj":"urn:ogc:def:crs:OGC:1.3:CRS84"
     }

# If it is a large grid, set an areo of interest
#aoi = {'x_min':-96, 'x_max':-88,'y_min':32,'y_max':38}
aoi = {}





def grid_level_dimensions(level):
    """ Returns the height and width of the grid level """
    count = functools.reduce(operator.mul,[len(grid['levels'][i]) for i in xrange(0,level+1)] , 1)
    dimension = {'x': float(grid["x_max"] - grid["x_min"])/float(count),
                 'y': float(grid["y_max"] - grid["y_min"])/float(count)
                 }
    return dimension


def make_poly_from_point(pt, x_step, y_step):
    " Returns geojson polygon from the bottom left coordinate "
    
    feature = {
        'type':'Feature',
        'geometry': {
            'type':'Polygon',
            'coordinates':[
                            [
                                 [pt['x'], pt['y']],
                                 [pt['x'] + x_step, pt['y']],
                                 [pt['x'] + x_step, pt['y'] + y_step],
                                 [pt['x'], pt['y'] + y_step],
                                 [pt['x'], pt['y']]
                            ]
                           ],
            },
        'properties': {'label':pt['label']}
        }
    return feature


def get_max_label(level):
    lbl = ''
    for x in range(0,level+1):
        lbl += str(grid['levels'][x][len(grid['levels'][x])-1]) *2

def coords_in_aoi(poly,aoi):
    """ Test if grid is inside our area of interest """
    
    if poly['geometry']['coordinates'][0][0][0] <= aoi['x_max']:
        #print 1
        if poly['geometry']['coordinates'][0][2][0] >=  aoi['x_min']:
            #print 2
            if poly['geometry']['coordinates'][0][0][1] <= aoi['y_max']:
                #print 3
                if poly['geometry']['coordinates'][0][2][1] >=  aoi['y_min']:
                    #print 4
                    return True
    return False
            

def create_grid(level, current_level, pt, f, max_label):
    """ Loop through and write grid to geojson """
    
    grid_dim = grid_level_dimensions(current_level)

    pt_in = dict(pt)
    pt = dict(pt)
    label_in = pt['label']
    x_coord = pt['x']
    
    for x in grid['levels'][current_level]:
        pt['y'] = pt_in['y']
        for y in grid['levels'][current_level]:
            pt['label'] = '{}{}{}'.format(label_in,x,y)
            poly = make_poly_from_point(pt, grid_dim['x'], grid_dim['y'])
            if coords_in_aoi(poly,aoi):
                if level == current_level:
                     f.write(json.dumps(poly))
                     f.write(',')
                else:
                    create_grid(level,current_level+1,pt, f, max_label)

            
            pt['y'] += grid_dim['y']
        pt['x'] += grid_dim['x']


def main(level):
    
    pt = {'x':grid['x_min'], 'y':grid['y_min'], 'label':''}
    max_label = get_max_label(level)

    global aoi
    if aoi == {}:
        aoi = {'x_min':grid['x_min'], 'x_max':grid['x_max'],
               'y_min':grid['y_min'],'y_max':grid['y_max']}
    
    with open('grid.json','wb') as f:
        f.write('{ "type": "FeatureCollection",')
        f.write('"crs": { "type": "name", "properties": { "name": "' + grid['prj'] + '" } },')
        f.write('"features": [')
        create_grid(level,0,pt,f, max_label)
        f.seek(-1, os.SEEK_END)
        f.truncate()
        f.write(']}')
    

if __name__ == "__main__":
    main(1)

