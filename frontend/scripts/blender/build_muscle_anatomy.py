"""Build original, deterministic anatomical teaching assets in Blender.
Run: blender --background --python frontend/scripts/blender/build_muscle_anatomy.py
No downloaded geometry; magnification changes between levels. Not patient anatomy.
"""
import bpy, math, random
import numpy as np
from pathlib import Path
from mathutils import Vector

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / 'frontend/public/media/models/svt/muscle'
WORK = ROOT / 'tmp/muscle-anatomy'
OUT.mkdir(parents=True, exist_ok=True); WORK.mkdir(parents=True, exist_ok=True)
random.seed(418)
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
for data in list(bpy.data.materials): bpy.data.materials.remove(data)

# Textures are packed and exported, unlike Blender-only procedural shader nodes.
def tissue(name, base, striated=False, pale=False):
    size=512; u,v=np.meshgrid(np.linspace(0,1,size),np.linspace(0,1,size))
    rng=np.random.default_rng(27)
    grain=rng.normal(0,.015,(size,size))
    fibers=.075*np.sin(v*math.pi*170+2*np.sin(u*math.pi*3))+.035*np.sin(v*math.pi*390)
    mottling=.06*np.sin(u*31+v*19)*np.sin(v*57-u*11)
    bands=.12*np.cos(u*math.pi*24) if striated else .015*np.sin(u*math.pi*43)
    shade=1+fibers+mottling+grain+bands
    rgba=np.ones((size,size,4),dtype=np.float32)
    for c in range(3): rgba[:,:,c]=np.clip(base[c]*shade,0,1)
    im=bpy.data.images.new(name+'_albedo',width=size,height=size)
    im.pixels.foreach_set(rgba.ravel());im.filepath_raw=str(WORK/(name+'.png'));im.file_format='PNG';im.save();im.pack()
    mat=bpy.data.materials.new(name);mat.use_nodes=True
    nodes=mat.node_tree.nodes;nodes.clear();bs=nodes.new('ShaderNodeBsdfPrincipled');out=nodes.new('ShaderNodeOutputMaterial');mat.node_tree.links.new(bs.outputs['BSDF'],out.inputs['Surface'])
    tex=nodes.new('ShaderNodeTexImage');tex.image=im;mat.node_tree.links.new(tex.outputs['Color'],bs.inputs['Base Color'])
    bs.inputs['Roughness'].default_value=.48 if not pale else .62
    # A subtle tangent-space relief makes the longitudinal grain visible in WebGL.
    height=fibers+grain*.5+(bands*.3 if striated else 0)
    dx=np.roll(height,-1,axis=1)-np.roll(height,1,axis=1)
    dy=np.roll(height,-1,axis=0)-np.roll(height,1,axis=0)
    normals=np.stack([-dx*1.8,-dy*1.8,np.ones_like(dx)],axis=-1)
    normals/=np.linalg.norm(normals,axis=-1,keepdims=True)
    rgba[:,:,:3]=normals*.5+.5;rgba[:,:,3]=1
    ni=bpy.data.images.new(name+'_normal',width=size,height=size);ni.colorspace_settings.name='Non-Color'
    ni.pixels.foreach_set(rgba.ravel());ni.filepath_raw=str(WORK/(name+'_normal.png'));ni.file_format='PNG';ni.save();ni.pack()
    nt=nodes.new('ShaderNodeTexImage');nt.image=ni;nm=nodes.new('ShaderNodeNormalMap');nm.inputs['Strength'].default_value=.65
    mat.node_tree.links.new(nt.outputs['Color'],nm.inputs['Color']);mat.node_tree.links.new(nm.outputs['Normal'],bs.inputs['Normal'])
    return mat

def plain(name,color,rough=.45):
    m=bpy.data.materials.new(name);m.diffuse_color=(*color,1);m.use_nodes=True
    m.node_tree.nodes.clear();p=m.node_tree.nodes.new('ShaderNodeBsdfPrincipled');out=m.node_tree.nodes.new('ShaderNodeOutputMaterial');m.node_tree.links.new(p.outputs['BSDF'],out.inputs['Surface']);p.inputs['Base Color'].default_value=(*color,1);p.inputs['Roughness'].default_value=rough
    return m
red=tissue('Tissu_musculaire',(.53,.135,.15))
fiber_mat=tissue('Fibres_longitudinales',(.69,.255,.26))
fascia=tissue('Tissu_conjonctif',(.76,.57,.50),pale=True)
tendon=tissue('Collagene_tendineux',(.88,.81,.67),pale=True)
striated=tissue('Myofibrilles_striees',(.63,.30,.30),striated=True)
nucleus=plain('Noyaux',(.22,.12,.24));nucleus_inner=plain('Nucleoles',(.36,.2,.37))
actin=plain('Actine',(.72,.27,.20));myosin=plain('Myosine',(.20,.38,.47));z_mat=plain('Disques_Z',(.69,.56,.38))
vessel=plain('Capillaires',(.37,.055,.07));reticulum=plain('Reticulum',(.59,.48,.26))

collections=[]
current=None

def part(obj,label,cover=False):
    obj['anatomical_label']=label;obj['cover']=cover
    for col in list(obj.users_collection):col.objects.unlink(obj)
    current.objects.link(obj)
    return obj

def uvmesh(name,vertices,faces,uvs,mat,label,cover=False):
    data=bpy.data.meshes.new(name);data.from_pydata(vertices,[],faces);data.update()
    ob=bpy.data.objects.new(name,data);bpy.context.collection.objects.link(ob);part(ob,label,cover)
    uv=data.uv_layers.new(name='UVMap')
    for poly in data.polygons:
        poly.use_smooth=True
        for li in poly.loop_indices: uv.data[li].uv=uvs[data.loops[li].vertex_index]
    ob.data.materials.append(mat);return ob

# Tubes have fine circumferential ridges, mild asymmetry and variable taper.
def tube(name,start,end,radius,center,mat,label,segments=60,sides=32,angles=(0,math.tau),profile=None,cover=False,phase=0,caps=True):
    verts=[];uvs=[];faces=[]
    for i in range(segments+1):
        t=i/segments;x=start+(end-start)*t
        cy,cz=center(t);r=radius*(profile(t) if profile else 1)
        for j in range(sides+1):
            a=angles[0]+(angles[1]-angles[0])*j/sides
            rr=r*(1+.018*math.sin(7*a+phase)+.009*math.sin(19*a+4*t))
            verts.append((x,cy+rr*math.cos(a),cz+rr*math.sin(a)))
            uvs.append((t,j/sides))
    for i in range(segments):
        for j in range(sides):
            k=i*(sides+1)+j;faces.append((k,k+1,k+sides+2,k+sides+1))
    if caps and angles[1]-angles[0]>6.28:
        # Triangulated end sections, perpendicular to the fibre axis.
        for end_i in [0,segments]:
            t=end_i/segments;cy,cz=center(t);c=len(verts);verts.append((start+(end-start)*t,cy,cz));uvs.append((t,.5))
            off=end_i*(sides+1)
            for j in range(sides):faces.append((c,off+j+1,off+j) if end_i==0 else (c,off+j,off+j+1))
    return uvmesh(name,verts,faces,uvs,mat,label,cover)

def path(name,points,radius,mat,label,cover=False):
    verts=[];uvs=[];faces=[];sides=8
    for i,p in enumerate(points):
        tangent=Vector(points[min(i+1,len(points)-1)])-Vector(points[max(0,i-1)])
        tangent.normalize();ref=Vector((0,0,1)) if abs(tangent.z)<.9 else Vector((0,1,0))
        n=tangent.cross(ref).normalized();bi=tangent.cross(n).normalized()
        for j in range(sides):
            a=j*math.tau/sides;v=Vector(p)+radius*(math.cos(a)*n+math.sin(a)*bi)
            verts.append(tuple(v));uvs.append((i/(len(points)-1),j/sides))
    for i in range(len(points)-1):
        for j in range(sides):faces.append((i*sides+j,i*sides+(j+1)%sides,(i+1)*sides+(j+1)%sides,(i+1)*sides+j))
    return uvmesh(name,verts,faces,uvs,mat,label,cover)

_spheres={}
def ellipsoid(name,loc,scale,mat,label,segments=16):
    key=(segments,mat.name)
    if key not in _spheres:
        vertices=[];faces=[];rings=8
        for i in range(rings+1):
            phi=math.pi*i/rings
            for j in range(segments):
                a=math.tau*j/segments;vertices.append((math.sin(phi)*math.cos(a),math.sin(phi)*math.sin(a),math.cos(phi)))
        for i in range(rings):
            for j in range(segments):faces.append((i*segments+j,i*segments+(j+1)%segments,(i+1)*segments+(j+1)%segments,(i+1)*segments+j))
        me=bpy.data.meshes.new('Protein_'+mat.name);me.from_pydata(vertices,[],faces);me.update();me.materials.append(mat)
        for p in me.polygons:p.use_smooth=True
        _spheres[key]=me
    ob=bpy.data.objects.new(name,_spheres[key]);bpy.context.collection.objects.link(ob);ob.location=loc;ob.scale=scale;part(ob,label)
    return ob

def hexpoints(n,spacing):
    pts=[]
    for row in range(-n,n+1):
        for col in range(-n,n+1):
            y=(col+.5*(row%2))*spacing;z=row*spacing*.866
            if math.hypot(y,z)<=n*spacing+.01:pts.append((y,z))
    return pts

def begin(name):
    global current
    current=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(current);collections.append(current)

def envelope(name,radius,length,mat,label,profile=None):
    # The missing upper/front quarter is a removable cutaway, not an alpha trick.
    tube(name+'_coupe',-length/2,length/2,radius,lambda t:(0,0),mat,label,angles=(math.pi,math.pi*2.5),profile=profile,caps=False)
    tube(name+'_volet',-length/2,length/2,radius,lambda t:(0,0),mat,label,angles=(math.pi*.5,math.pi),profile=profile,cover=True,caps=False)

begin('muscle')
def belly(t):return .19+.81*math.sin(math.pi*t)**.72
# The organ has an organic belly with converging fibres and continuous tendons.
envelope('Epimysium',1.32,6.5,red,'Épimysium',belly)
for k,(y,z) in enumerate(hexpoints(2,.49)):
    tube('Faisceau_%02d'%k,-3.22,3.22,.215,lambda t,y=y,z=z:(y*belly(t),z*belly(t)),fiber_mat,'Faisceau',profile=belly,phase=k)
# Fine collagen strands follow the outer surface and gather into the tendon.
for a in np.linspace(math.pi,math.pi*2.5,52):
    pts=[]
    for t in np.linspace(0,1,64):
        r=1.324*belly(t);pts.append((-3.25+6.5*t,r*math.cos(a+.02*math.sin(t*8)),r*math.sin(a+.02*math.sin(t*8))))
    path('Fibres_epimysiales',pts,.006,fascia,'Épimysium')
for side in [-1,1]:
    tube('Tendon',3.16*side,4.38*side,.25,lambda t:(.045*math.sin(t*2),-.025*t),tendon,'Tendon',profile=lambda t:1-.5*t,segments=24)
    for q in range(22):
        a=q*math.tau/22
        pts=[(side*(2.75+t*1.6),(.42*(1-t)+.12*t)*math.cos(a),(.42*(1-t)+.12*t)*math.sin(a)) for t in np.linspace(0,1,35)]
        path('Collagene',pts,.009,tendon,'Tendon')
# A restrained surface vessel gives tissue context without obscuring the cut.
pts=[]
for t in np.linspace(.15,.82,55):
    a=3.4+.1*math.sin(t*12);r=1.34*belly(t);pts.append((-3.25+6.5*t,r*math.cos(a),r*math.sin(a)))
path('Vaisseau_surface',pts,.022,vessel,'Vaisseau sanguin')

begin('fascicle')
envelope('Perimysium',1.15,6.2,fascia,'Périmysium',lambda t:1+.025*math.sin(t*8))
for k,(y,z) in enumerate(hexpoints(3,.30)):
    rr=.135*(1+.06*math.sin(k*5))
    tube('Endomysium_%02d'%k,-3.09,3.09,rr+.012,lambda t,y=y,z=z:(y+.008*math.sin(t*7),z),tendon,'Endomysium',sides=18,segments=24)
    tube('Fibre_%02d'%k,-3.105,3.105,rr,lambda t,y=y,z=z:(y+.008*math.sin(t*7),z),fiber_mat,'Fibre musculaire',sides=18,segments=40,phase=k)
    # Red, finely striated ends visible inside each individual fibre.
for a in np.linspace(math.pi,math.pi*2.5,35):
    path('Collagene_perimysial',[(x,1.16*math.cos(a+.015*math.sin(x*5)),1.16*math.sin(a+.015*math.sin(x*5))) for x in np.linspace(-3.1,3.1,35)],.006,tendon,'Périmysium')

begin('fiber')
envelope('Sarcolemme',1.22,6.2,fascia,'Sarcolemme')
for k,(y,z) in enumerate(hexpoints(3,.30)):
    tube('Myofibrille_%02d'%k,-3.08,3.08,.135,lambda t,y=y,z=z:(y,z),striated,'Myofibrille',sides=16,segments=48,phase=k)
# Subsarcolemmal nuclei are peripheral, never inside the myofibrils.
for x in [-2.2,-.3,1.7]:
    ellipsoid('Noyau',(x,-.72,.86),(.33,.15,.14),nucleus,'Noyau périphérique')
    ellipsoid('Nucleole',(x+.055,-.79,.94),(.062,.025,.024),nucleus_inner,'Noyau périphérique')
# A sparse reticular mesh around exposed myofibrils, not free-floating rings.
for j in range(12):
    x=-2.85+j*.51
    pts=[(x+.02*math.sin(a*6),.99*math.cos(a),.99*math.sin(a)) for a in np.linspace(math.pi*.5,math.pi,36)]
    path('Reticulum_transversal',pts,.017,reticulum,'Réticulum sarcoplasmique')
for a in [1.7,2.0,2.3,2.6,2.9]:
    path('Reticulum_longitudinal',[(x,.99*math.cos(a),.99*math.sin(a)) for x in np.linspace(-3,3,20)],.012,reticulum,'Réticulum sarcoplasmique')

begin('myofibril')
# Dense parallel myofilaments resolve the ends instead of a solid capped tube.
for k,(y,z) in enumerate(hexpoints(4,.14)):
    tube('Filament_contractile_%02d'%k,-3.2,3.2,.057,lambda t,y=y,z=z:(y,z),striated,'Myofilaments',segments=72,sides=10,phase=k)
for j,x in enumerate(np.linspace(-3.2,3.2,7)):
    tube('Strie_Z_%d'%j,x-.018,x+.018,.69,lambda t:(0,0),z_mat,'Strie Z',segments=1,sides=48)
# Faint A bands, with no thick yellow cartoon rings.
for x in np.linspace(-2.667,2.667,6):
    tube('Bande_A',x-.29,x+.29,.675,lambda t:(0,0),red,'Bande A',segments=8,sides=48,caps=False)
path('Repere_sarcomere',[(0,-.03,.93),(0,-.03,1.12),(1.067,-.03,1.12),(1.067,-.03,.93)],.016,tendon,'Un sarcomère')

begin('sarcomere')
# A lattice of proteins, with molecular bead chains and bipolar myosin heads.
for x in [-2.8,2.8]:
    for y in np.linspace(-.8,.8,7):path('Reseau_Z',[(x,y,-1),(x,y,1)],.022,z_mat,'Strie Z')
    for z in np.linspace(-1,1,8):path('Reseau_Z',[(x,-.8,z),(x,.8,z)],.022,z_mat,'Strie Z')
for y in [-.48,.48]:
    for z in [-.66,.66]:
        for side in [-1,1]:
            for strand in [0,1]:
                for k in range(37):
                    x=side*(2.8-k*2.43/36);angle=k*.82+strand*math.pi
                    ellipsoid('Actine_globulaire',(x,y+.035*math.cos(angle),z+.035*math.sin(angle)),(.041,.041,.041),actin,'Actine',segments=10)
    tube('Myosine',-1.64,1.64,.092,lambda t,y=y:(y,0),myosin,'Myosine',sides=18,segments=35,profile=lambda t:.3+.7*math.sin(math.pi*t)**.28)
    for side in [-1,1]:
        for k in range(7):
            x=side*(.45+k*.17)
            for zsign in [-1,1]:
                pts=[(x,y,0),(x-side*.035,y,zsign*.18),(x-side*.1,y,zsign*.38),(x-side*.16,y,zsign*.49)]
                path('Bras_myosine',pts,.025,myosin,'Tête de myosine')
                ellipsoid('Tete_myosine',pts[-1],(.07,.045,.09),myosin,'Tête de myosine',segments=12)

# Merge by anatomical identity and cover state to avoid hundreds of browser draw calls.
for col in collections:
    groups={}
    for ob in list(col.objects):
        groups.setdefault((ob.get('anatomical_label',''),ob.get('cover',False)),[]).append(ob)
    for objects in groups.values():
        if len(objects)<2: continue
        bpy.ops.object.select_all(action='DESELECT')
        for ob in objects:ob.select_set(True)
        bpy.context.view_layer.objects.active=objects[0]
        bpy.ops.object.join()
# All exported files carry only geometry, packed maps, materials and safe metadata.
for col in collections:
    bpy.ops.object.select_all(action='DESELECT')
    for ob in col.objects:ob.select_set(True)
    bpy.ops.export_scene.gltf(filepath=str(OUT/(col.name+'.glb')),export_format='GLB',use_selection=True,export_extras=True,export_yup=True,export_apply=True,export_texcoords=True,export_normals=True)
    print('ASSET',col.name,(OUT/(col.name+'.glb')).stat().st_size,flush=True)
# Preserve all original assets in separate named collections for future Blender work.
for col in collections:
    sc=bpy.data.scenes.new(col.name);sc.collection.children.link(col)
bpy.context.window.scene=bpy.data.scenes['muscle']
bpy.ops.wm.save_as_mainfile(filepath=str(WORK/'muscle-anatomy.blend'))
print('ANATOMY_ASSETS_COMPLETE',flush=True)
