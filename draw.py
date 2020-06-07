from display import *
from matrix import *
from gmath import *

def draw_scanline(x0, z0, x1, z1, y, screen, zbuffer, color):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz

    x = x0
    z = z0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0

    while x <= x1:
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z

def scanline_convert(polygons, i, screen, zbuffer, color):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2]) ]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256

    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    while y <= int(points[TOP][1]):
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

        #draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1

def add_polygon( polygons, x0, y0, z0, x1, y1, z1, x2, y2, z2 ):
    add_point(polygons, x0, y0, z0)
    add_point(polygons, x1, y1, z1)
    add_point(polygons, x2, y2, z2)

def pts(point):
    return str(point[0]) + "," + str(point[1]) + "," + str(point[2])

def shaded_scanline(x0, z0, x1, z1, y, screen, zbuffer, c0, c1):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz #lol Mr. DW doesn't know about the quick variable swap in python

        c0,c1 = c1,c0 #as seen here

    x = x0
    z = z0
    color = c0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
    dc = [(c1[e] - c0[e]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0 for e in range(3)]

    while x <= x1:
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z
        color = [color[e] + dc[e] for e in range(3)]


def gouraud_shading(polygons, i, screen, zbuffer, color):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1
    COLOR = 3

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2], color[pts(polygons[i])]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2], color[pts(polygons[i+1])]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2], color[pts(polygons[i+2])]) ]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256
    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    c0 = points[BOT][COLOR]
    c1 = points[BOT][COLOR]

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    cd0 = [(points[TOP][COLOR][e] - points[BOT][COLOR][e]) / distance0 if distance0 != 0 else 0 for e in range(3) ]
    cd1 = [(points[MID][COLOR][e] - points[BOT][COLOR][e]) / distance1 if distance1 != 0 else 0 for e in range(3) ]

    #print ("cd0", cd0, "cd1", cd1)
    #print(points[TOP][COLOR])
    while y <= int(points[TOP][1]):
        #print ("c0:", c0, "c1:", c1)
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

            cd1 = [(points[TOP][COLOR][e] - points[MID][COLOR][e]) / distance2 if distance2 != 0 else 0 for e in range(3)]
            c1 = points[MID][COLOR]

        #draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        #draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        shaded_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, c0[:], c1[:])

        c0 = [c0[e] + cd0[e] for e in range(3)]
        c1 = [c1[e] + cd1[e] for e in range(3)]

        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1

def phong_scanline(x0, z0, x1, z1, y, screen, zbuffer, n0, n1, view, ambient, light, symbols, reflect):
    if x0 > x1:
        tx = x0
        tz = z0
        x0 = x1
        z0 = z1
        x1 = tx
        z1 = tz #lol Mr. DW doesn't know about the quick variable swap in python

        n0,n1 = n1,n0 #as seen here

    x = x0
    z = z0
    delta_z = (z1 - z0) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0
    dn = [(n1[e] - n0[e]) / (x1 - x0 + 1) if (x1 - x0 + 1) != 0 else 0 for e in range(3)]

    normal = n0
    color = [0,0,0]
    while x <= x1:
        color = get_lighting(normal, view, ambient, light, symbols, reflect )
        plot(screen, zbuffer, color, x, y, z)
        x+= 1
        z+= delta_z
        normal = [normal[e] + dn[e] for e in range(3)]


def phong_shading(polygons, i, screen, zbuffer, norms, view, ambient, light, symbols, reflect):
    flip = False
    BOT = 0
    TOP = 2
    MID = 1
    NORM = 3

    points = [ (polygons[i][0], polygons[i][1], polygons[i][2], norms[pts(polygons[i])]),
               (polygons[i+1][0], polygons[i+1][1], polygons[i+1][2], norms[pts(polygons[i+1])]),
               (polygons[i+2][0], polygons[i+2][1], polygons[i+2][2], norms[pts(polygons[i+2])]) ]

    # alas random color, we hardly knew ye
    #color = [0,0,0]
    #color[RED] = (23*(i/3)) %256
    #color[GREEN] = (109*(i/3)) %256
    #color[BLUE] = (227*(i/3)) %256
    points.sort(key = lambda x: x[1])
    x0 = points[BOT][0]
    z0 = points[BOT][2]
    x1 = points[BOT][0]
    z1 = points[BOT][2]
    y = int(points[BOT][1])

    c0 = points[BOT][NORM]
    c1 = points[BOT][NORM]

    distance0 = int(points[TOP][1]) - y * 1.0 + 1
    distance1 = int(points[MID][1]) - y * 1.0 + 1
    distance2 = int(points[TOP][1]) - int(points[MID][1]) * 1.0 + 1

    dx0 = (points[TOP][0] - points[BOT][0]) / distance0 if distance0 != 0 else 0
    dz0 = (points[TOP][2] - points[BOT][2]) / distance0 if distance0 != 0 else 0
    dx1 = (points[MID][0] - points[BOT][0]) / distance1 if distance1 != 0 else 0
    dz1 = (points[MID][2] - points[BOT][2]) / distance1 if distance1 != 0 else 0

    cd0 = [(points[TOP][NORM][e] - points[BOT][NORM][e]) / distance0 if distance0 != 0 else 0 for e in range(3) ]
    cd1 = [(points[MID][NORM][e] - points[BOT][NORM][e]) / distance1 if distance1 != 0 else 0 for e in range(3) ]

    #print ("cd0", cd0, "cd1", cd1)
    #print(points[TOP][NORM])
    while y <= int(points[TOP][1]):
        #print ("c0:", c0, "c1:", c1)
        if ( not flip and y >= int(points[MID][1])):
            flip = True

            dx1 = (points[TOP][0] - points[MID][0]) / distance2 if distance2 != 0 else 0
            dz1 = (points[TOP][2] - points[MID][2]) / distance2 if distance2 != 0 else 0
            x1 = points[MID][0]
            z1 = points[MID][2]

            cd1 = [(points[TOP][NORM][e] - points[MID][NORM][e]) / distance2 if distance2 != 0 else 0 for e in range(3)]
            c1 = points[MID][NORM]

        #draw_line(int(x0), y, z0, int(x1), y, z1, screen, zbuffer, color)
        #draw_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, color)
        phong_scanline(int(x0), z0, int(x1), z1, y, screen, zbuffer, c0[:], c1[:], view, ambient, light, symbols, reflect)

        c0 = [c0[e] + cd0[e] for e in range(3)]
        c1 = [c1[e] + cd1[e] for e in range(3)]

        x0+= dx0
        z0+= dz0
        x1+= dx1
        z1+= dz1
        y+= 1
    return
def draw_polygons( polygons, screen, zbuffer, view, ambient, light, symbols, reflect):
    if len(polygons) < 2:
        print('Need at least 3 points to draw')
        return
    vertices = {}
    #print(vertices.keys())
    norms = {}
    for p in polygons:
        if not p[:3] in list(vertices.keys()):
            vertices[pts(p[:3])] = []
    point = 0
    while point < len(polygons) - 2:
        normal = calculate_normal(polygons, point)[:]
        #print (vertices[pts(polygons[point])])
        if normal[2] > 0:
            vertices[pts(polygons[point])].append(normal)
            vertices[pts(polygons[point+1])].append(normal)
            vertices[pts(polygons[point+2])].append(normal)
        point += 3
    for key in list(vertices.keys()):
        avg = [0,0,0]
        for n in vertices[key]:
            for i in range(3):
                avg[i] += n[i]
        if len(vertices[key]) != 0:
            for i in range(3):
                avg[i] /= len(vertices[key])
        norms[key] = avg
    for key in list(norms.keys()): 
        vertices[key] = get_lighting(norms[key], view, ambient, light, symbols, reflect )

    point = 0
    while point < len(polygons) - 2:

        normal = calculate_normal(polygons, point)[:]

        #print normal
        if normal[2] > 0:
            #normal color
            # color = get_lighting(normal, view, ambient, light, symbols, reflect )
            # scanline_convert(polygons, point, screen, zbuffer, color)

            #gouraud shading
            # gouraud_shading(polygons, point, screen, zbuffer, vertices)

            #phone shading
            phong_shading(polygons, point, screen, zbuffer, norms, view, ambient, light, symbols, reflect)
            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            polygons[point][2],
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            polygons[point+1][2],
            #            screen, zbuffer, color)
            # draw_line( int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            polygons[point+2][2],
            #            int(polygons[point+1][0]),
            #            int(polygons[point+1][1]),
            #            polygons[point+1][2],
            #            screen, zbuffer, color)
            # draw_line( int(polygons[point][0]),
            #            int(polygons[point][1]),
            #            polygons[point][2],
            #            int(polygons[point+2][0]),
            #            int(polygons[point+2][1]),
            #            polygons[point+2][2],
            #            screen, zbuffer, color)
        point+= 3


def add_box( polygons, x, y, z, width, height, depth ):
    x1 = x + width
    y1 = y - height
    z1 = z - depth

    #front
    add_polygon(polygons, x, y, z, x1, y1, z, x1, y, z)
    add_polygon(polygons, x, y, z, x, y1, z, x1, y1, z)

    #back
    add_polygon(polygons, x1, y, z1, x, y1, z1, x, y, z1)
    add_polygon(polygons, x1, y, z1, x1, y1, z1, x, y1, z1)

    #right side
    add_polygon(polygons, x1, y, z, x1, y1, z1, x1, y, z1)
    add_polygon(polygons, x1, y, z, x1, y1, z, x1, y1, z1)
    #left side
    add_polygon(polygons, x, y, z1, x, y1, z, x, y, z)
    add_polygon(polygons, x, y, z1, x, y1, z1, x, y1, z)

    #top
    add_polygon(polygons, x, y, z1, x1, y, z, x1, y, z1)
    add_polygon(polygons, x, y, z1, x, y, z, x1, y, z)
    #bottom
    add_polygon(polygons, x, y1, z, x1, y1, z1, x1, y1, z)
    add_polygon(polygons, x, y1, z, x, y1, z1, x1, y1, z1)

def add_cylinder(polygons, cx, cy, cz, r, h, step):
    points = generate_cylinder(cx, cy, cz, r, h, step)
    for i in range(1, step + 1):
        p = i % step + 1
        add_polygon(polygons, points[0][0][0], points[0][0][1], points[0][0][2],
                    points[0][p][0], points[0][p][1], points[0][p][2],
                    points[0][i][0], points[0][i][1], points[0][i][2])
        add_polygon(polygons, points[1][0][0], points[1][0][1], points[1][0][2],
                    points[1][i][0], points[1][i][1], points[1][i][2],
                    points[1][p][0], points[1][p][1], points[1][p][2])
        add_polygon(polygons, points[0][i][0], points[0][i][1], points[0][i][2],
                    points[1][p][0], points[1][p][1], points[1][p][2],
                    points[1][i][0], points[1][i][1], points[1][i][2])
        add_polygon(polygons, points[1][p][0], points[1][p][1], points[1][p][2],
                    points[0][i][0], points[0][i][1], points[0][i][2],
                    points[0][p][0], points[0][p][1], points[0][p][2])



def generate_cylinder(cx, cy, cz, r, h, step ):
    points = []
    temp = []
    temp.append([cx, cy, cz])
    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        z1 = r * math.sin(2*math.pi * t) + cz;
        temp.append([x1, cy, z1])
        i+= 1
    i = 1
    points.append(temp)
    temp = []
    temp.append([cx, cy - h, cz])
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        z1 = r * math.sin(2*math.pi * t) + cz;
        temp.append([x1, cy - h, z1])
        i+= 1
    points.append(temp)
    return points

def add_cone(polygons, cx, cy, cz, r, h, step ):
    points = generate_cone(cx, cy, cz, r, h, step )
    for i in range(1, step + 1):
        p = i % step + 1
        add_polygon(polygons, cx, cy, cz,
                    points[i][0], points[i][1], points[i][2],
                    points[p][0], points[p][1], points[p][2])
        add_polygon(polygons, points[i][0], points[i][1], points[i][2],
                    cx, cy - h, cz,
                    points[p][0], points[p][1], points[p][2])

def generate_cone(cx, cy, cz, r, h, step ):
    #points = []
    temp = []
    temp.append([cx, cy, cz])
    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        z1 = r * math.sin(2*math.pi * t) + cz;
        temp.append([x1, cy - h, z1])
        i+= 1
    return temp

def add_oblicone(polygons, px, py, pz, cx, cy, cz, r, step ):
    if cy > py:
        px, cx = cx, px
        py, cy = cy, py
        pz, cz = cz, pz
    points = generate_oblicone(cx, cy, cz, r, step )
    for i in range(1, step + 1):
        p = i % step + 1
        add_polygon(polygons, px, py, pz,
                    points[i][0], points[i][1], points[i][2],
                    points[p][0], points[p][1], points[p][2])
        add_polygon(polygons, points[i][0], points[i][1], points[i][2],
                    cx, cy, cz,
                    points[p][0], points[p][1], points[p][2])

def generate_oblicone(cx, cy, cz, r, step ):
    #points = []
    temp = []
    temp.append([cx, cy, cz])
    i = 1
    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        z1 = r * math.sin(2*math.pi * t) + cz;
        temp.append([x1, cy, z1])
        i+= 1
    return temp

def add_sphere(polygons, cx, cy, cz, r, step ):
    points = generate_sphere(cx, cy, cz, r, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    step+= 1
    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt
            p1 = p0+1
            p2 = (p1+step) % (step * (step-1))
            p3 = (p0+step) % (step * (step-1))

            if longt != step - 2:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p1][0],
                             points[p1][1],
                             points[p1][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2])
            if longt != 0:
                add_polygon( polygons, points[p0][0],
                             points[p0][1],
                             points[p0][2],
                             points[p2][0],
                             points[p2][1],
                             points[p2][2],
                             points[p3][0],
                             points[p3][1],
                             points[p3][2])


def generate_sphere( cx, cy, cz, r, step ):
    points = []

    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop+1):
            circ = circle/float(step)

            x = r * math.cos(math.pi * circ) + cx
            y = r * math.sin(math.pi * circ) * math.cos(2*math.pi * rot) + cy
            z = r * math.sin(math.pi * circ) * math.sin(2*math.pi * rot) + cz

            points.append([x, y, z])
            #print 'rotation: %d\tcircle%d'%(rotation, circle)
    return points

def add_torus(polygons, cx, cy, cz, r0, r1, step ):
    points = generate_torus(cx, cy, cz, r0, r1, step)

    lat_start = 0
    lat_stop = step
    longt_start = 0
    longt_stop = step

    for lat in range(lat_start, lat_stop):
        for longt in range(longt_start, longt_stop):

            p0 = lat * step + longt;
            if (longt == (step - 1)):
                p1 = p0 - longt;
            else:
                p1 = p0 + 1;
            p2 = (p1 + step) % (step * step);
            p3 = (p0 + step) % (step * step);

            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p3][0],
                        points[p3][1],
                        points[p3][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2] )
            add_polygon(polygons,
                        points[p0][0],
                        points[p0][1],
                        points[p0][2],
                        points[p2][0],
                        points[p2][1],
                        points[p2][2],
                        points[p1][0],
                        points[p1][1],
                        points[p1][2] )


def generate_torus( cx, cy, cz, r0, r1, step ):
    points = []
    rot_start = 0
    rot_stop = step
    circ_start = 0
    circ_stop = step

    for rotation in range(rot_start, rot_stop):
        rot = rotation/float(step)
        for circle in range(circ_start, circ_stop):
            circ = circle/float(step)

            x = math.cos(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cx;
            y = r0 * math.sin(2*math.pi * circ) + cy;
            z = -1*math.sin(2*math.pi * rot) * (r0 * math.cos(2*math.pi * circ) + r1) + cz;

            points.append([x, y, z])
    return points


def add_circle( points, cx, cy, cz, r, step ):
    x0 = r + cx
    y0 = cy
    i = 1

    while i <= step:
        t = float(i)/step
        x1 = r * math.cos(2*math.pi * t) + cx;
        y1 = r * math.sin(2*math.pi * t) + cy;

        add_edge(points, x0, y0, cz, x1, y1, cz)
        x0 = x1
        y0 = y1
        i+= 1

def add_curve( points, x0, y0, x1, y1, x2, y2, x3, y3, step, curve_type ):

    xcoefs = generate_curve_coefs(x0, x1, x2, x3, curve_type)[0]
    ycoefs = generate_curve_coefs(y0, y1, y2, y3, curve_type)[0]

    i = 1
    while i <= step:
        t = float(i)/step
        x = t * (t * (xcoefs[0] * t + xcoefs[1]) + xcoefs[2]) + xcoefs[3]
        y = t * (t * (ycoefs[0] * t + ycoefs[1]) + ycoefs[2]) + ycoefs[3]
        #x = xcoefs[0] * t*t*t + xcoefs[1] * t*t + xcoefs[2] * t + xcoefs[3]
        #y = ycoefs[0] * t*t*t + ycoefs[1] * t*t + ycoefs[2] * t + ycoefs[3]

        add_edge(points, x0, y0, 0, x, y, 0)
        x0 = x
        y0 = y
        i+= 1


def draw_lines( matrix, screen, zbuffer, color ):
    if len(matrix) < 2:
        print('Need at least 2 points to draw')
        return

    point = 0
    while point < len(matrix) - 1:
        draw_line( int(matrix[point][0]),
                   int(matrix[point][1]),
                   matrix[point][2],
                   int(matrix[point+1][0]),
                   int(matrix[point+1][1]),
                   matrix[point+1][2],
                   screen, zbuffer, color)
        point+= 2

def add_edge( matrix, x0, y0, z0, x1, y1, z1 ):
    add_point(matrix, x0, y0, z0)
    add_point(matrix, x1, y1, z1)

def add_point( matrix, x, y, z=0 ):
    matrix.append( [x, y, z, 1] )



def draw_line( x0, y0, z0, x1, y1, z1, screen, zbuffer, color ):

    #swap points if going right -> left
    if x0 > x1:
        xt = x0
        yt = y0
        zt = z0
        x0 = x1
        y0 = y1
        z0 = z1
        x1 = xt
        y1 = yt
        z1 = zt

    x = x0
    y = y0
    z = z0
    A = 2 * (y1 - y0)
    B = -2 * (x1 - x0)
    wide = False
    tall = False

    if ( abs(x1-x0) >= abs(y1 - y0) ): #octants 1/8
        wide = True
        loop_start = x
        loop_end = x1
        dx_east = dx_northeast = 1
        dy_east = 0
        d_east = A
        distance = x1 - x + 1
        if ( A > 0 ): #octant 1
            d = A + B/2
            dy_northeast = 1
            d_northeast = A + B
        else: #octant 8
            d = A - B/2
            dy_northeast = -1
            d_northeast = A - B

    else: #octants 2/7
        tall = True
        dx_east = 0
        dx_northeast = 1
        distance = abs(y1 - y) + 1
        if ( A > 0 ): #octant 2
            d = A/2 + B
            dy_east = dy_northeast = 1
            d_northeast = A + B
            d_east = B
            loop_start = y
            loop_end = y1
        else: #octant 7
            d = A/2 - B
            dy_east = dy_northeast = -1
            d_northeast = A - B
            d_east = -1 * B
            loop_start = y1
            loop_end = y

    dz = (z1 - z0) / distance if distance != 0 else 0

    while ( loop_start < loop_end ):
        plot( screen, zbuffer, color, x, y, z )
        if ( (wide and ((A > 0 and d > 0) or (A < 0 and d < 0))) or
             (tall and ((A > 0 and d < 0) or (A < 0 and d > 0 )))):

            x+= dx_northeast
            y+= dy_northeast
            d+= d_northeast
        else:
            x+= dx_east
            y+= dy_east
            d+= d_east
        z+= dz
        loop_start+= 1
    plot( screen, zbuffer, color, x, y, z )
