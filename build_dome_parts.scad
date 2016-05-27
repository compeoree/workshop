// build_dome_parts.scad  
// 05/28/2016 

// include <test_dome-521.scad>;
include <pydome_sorted.scad>;

// Debug output flag 
__DEBUG__ = false;


// Distance between two vertices v (x1, y1, z1) and w (x2, y2, z2)
function distance(v, w) = sqrt(
        pow(w[0]-v[0], 2) + pow(w[1]-v[1], 2) + pow(w[2]-v[2], 2)
        );

function indices(vector) = [0 : len(vector)-1]; 

// return number of matches    
function eq(a, b) = (a == b) ? 1 : 0;

// i: size of vector vv
function find(it, vv, i) = i == 0 ? eq(it, vv[0]) : eq(it, vv[i]) + find(it, vv, i-1); 

// alternative method of find()
// result = search(it, vv, num_returns_per_match=0, 0);
// len(result);
function find2(it, vv) = len(search(it, vv, 0, 0)) > 0 ? true : false;

function end(vector) = len(vector)-1; 

function abs_add(x, n) = (x<0) ? x-n : x+n;

// Quicksort 
function quicksort(vector) = !(len(vector)>0) ? [] : 
        let (
            pivot = floor(len(vector)/2),
            pivot_item = vector[pivot],  // [0, 1, 10.7532]
            lesser = [ for (y = vector) if (y < pivot_item) y ],
            equal = [ for (y = vector) if (y == pivot_item) y ],
            greater = [ for (y = vector) if (y > pivot_item) y ]
        ) concat(quicksort(lesser), equal, quicksort(greater));

// Find all edge types to assign colors 
function get_edge_types(vv, tt, i) = i <= end(vv) ?
        let (
            prev = vv[i-1],
            curr = vv[i],
            t = (curr > prev) ? [curr] : []
            ) get_edge_types(vv, concat(tt, t), i+1) : tt;            

default_radius = 0.5;

// Fix the size comparison error for floating point numbers. 
decimal_factor = 10000;


module ECHO(msg, ON=false)
{    
    if (__DEBUG__ || ON) 
    {
        echo();
        echo(msg);
        echo();
    }    
}

module print_index()
{
    for (i = [0 : len(V)-1])
    {
        index = str(i);
        echo(i, V[i]);
    }
}

// p = [x, y, z] 
module dot_vertex(radius, p, c1="red")
{
    translate(p) color(c1) sphere(radius, center=true);    
}


module letter_vertex(s1=5, letter, p, p_offset=5, c1="black")
{
    x = abs_add(p[0], p_offset);
    y = abs_add(p[1], p_offset);
    z = abs_add(p[2], p_offset);
    translate([x, y, z]) color(c1) rotate([90, 0, 45])    
    linear_extrude(height=0.5, center = true, convexity = 10, twist = 0)
            text(letter, size=s1, font="Courier");
}

module triangle(p1, f1=[[0,1,2]])
{
    polyhedron(points=p1, faces=f1);
}

module triangle2(p1, p2, p3, f1=[[0, 1, 2]])
{
    t = [V[p1], V[p2], V[p3]];
    polyhedron(t, faces=f1);
}

module draw_face(face1, c1="gold")
{
    a = face1[0];
    b = face1[1];
    c = face1[2];
    tng = [V[a], V[b], V[c]];
    if (__DEBUG__) echo("<", a, b, c, ">");
    color(c1) polyhedron(tng, faces=[[0, 1, 2]]);
}

// a sphere 
module draw_vertices(vertices, c1="gray")
{
    last = len(vertices)-1;
    for (i = indices(vertices))
    {
        dot_vertex(default_radius, V[i], c1);
    } 
    dot_vertex(default_radius*1.1, V[last], "red");
}

module draw_letter_vertices(vertices, font_size=1.5, c1="gray")
{
    last = len(vertices)-1;
    for (i = indices(vertices))
    {
        index = str(i);
        p = V[i];
        letter_vertex(font_size, index, p, 1, c1);
        if (__DEBUG__) echo(index, p);
    }
    letter_vertex(font_size, str(last), V[last], 1, "red");
    
}

module draw_faces(fromto, c1="yellow")
{
    ECHO_STR("draw_faces()");    
    for (i = fromto)
    {
        draw_face(Face[i], c1);
    }
}

// size: radius of edge tube 
module draw_edge(v, w, size=1, c1="green")
{
    color(c1) hull()
    {  
        translate(v) sphere(r=size);
        translate(w) sphere(r=size);
    }
}

// Use pydome's ET vector 
module draw_edges2(edges, edgetypes, r1)
{
    for (i = indices(edges))
    {
        _i = E[i][0];
        _j = E[i][1];
        v = V[_i];
        w = V[_j];
        length = E[i][2];
        for (t = edgetypes)
        {
            length2 = t[0];
            code = [t[2], t[3], t[4]];
            if (length == length2) draw_edge(v, w, r1, code);                     
        }       
    }
}


// draw_letter_vertices(V, 0.8, "gray");
// draw_vertices(V, "blue");
draw_edges2(E, ET, 1/2);

// #draw_faces([0 : len(Face)-1], "silver");

