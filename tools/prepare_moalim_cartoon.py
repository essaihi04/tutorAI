"""Turn the cartoon teacher .blend into the web professor GLB.

    blender --background --disable-autoexec --python tools/prepare_moalim_cartoon.py -- SOURCE.blend [OUT_DIR]

- Bones get standard humanoid names (Hips, Head, LeftArm, RightHandIndex1, ...) so that
  Professor3D.tsx can point, write and fly with them; facial bones become Nose, Moustache, Brow*.
- The single source action (pop-in, gestures, pop-out) is cut into two loops:
  `Idle` (calm pose, arms down, gentle sway) and `Talking` (the gestures, without the pop-in/out).
- Exports `moalim-professeur.glb` and renders `moalim-professeur.png` (fallback portrait).
"""
import bpy, math, sys
from pathlib import Path
from mathutils import Vector, Quaternion

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
SOURCE = Path(argv[0])
OUT = (Path(argv[1]) if len(argv) > 1 else Path(__file__).resolve().parents[1] / 'frontend/public/media/avatar').resolve()
TALK_RANGE = (40, 240)        # source frames, after the pop-in and before the pop-out
IDLE_POSES = (60, 120)        # two calm source frames, arms down
IDLE_LENGTH = 96              # frames at 24 fps
import os
# The source gestures wave both arms (up to 117° from the rest pose, above the shoulders) every second
# or two, which reads as a flicker in a small floating tutor: while talking, shoulders, upper arms and
# forearms stay in the rest pose and the hands only move a little (max degrees from the rest pose).
# Pointing and writing move the arms from the app, independently of this clip.
ARM_CAP = {'Shoulder': 0.0, 'Arm': 0.0, 'ForeArm': 0.0, 'Hand': 12.0}
TALK_SMOOTH = float(os.environ.get('TALK_SMOOTH', 3))   # Gaussian sigma, in frames: the source snaps its arms up in one frame


def log(*a): print('[cartoon]', *a, flush=True)


RENAME = {
    'Bone': 'Hips', 'Bone.001': 'Head', 'Bone.046': 'Nose', 'Bone.047': 'Moustache',
    'Bone.042': 'BrowRootRight', 'Bone.045': 'BrowRight', 'Bone.043': 'BrowRootLeft', 'Bone.044': 'BrowLeft',
    'Bone.002': 'RightShoulder', 'Bone.003': 'RightArm', 'Bone.004': 'RightForeArm', 'Bone.005': 'RightHand',
    'Bone.039': 'RightHandThumb1', 'Bone.040': 'RightHandThumb2', 'Bone.041': 'RightHandThumb3',
    'Bone.036': 'RightHandIndex1', 'Bone.037': 'RightHandIndex2', 'Bone.038': 'RightHandIndex3',
    'Bone.033': 'RightHandMiddle1', 'Bone.034': 'RightHandMiddle2', 'Bone.035': 'RightHandMiddle3',
    'Bone.030': 'RightHandPinky1', 'Bone.031': 'RightHandPinky2', 'Bone.032': 'RightHandPinky3',
    'Bone.006': 'LeftShoulder', 'Bone.007': 'LeftArm', 'Bone.008': 'LeftForeArm', 'Bone.009': 'LeftHand',
    'Bone.027': 'LeftHandThumb1', 'Bone.028': 'LeftHandThumb2', 'Bone.029': 'LeftHandThumb3',
    'Bone.024': 'LeftHandIndex1', 'Bone.025': 'LeftHandIndex2', 'Bone.026': 'LeftHandIndex3',
    'Bone.021': 'LeftHandMiddle1', 'Bone.022': 'LeftHandMiddle2', 'Bone.023': 'LeftHandMiddle3',
    'Bone.018': 'LeftHandPinky1', 'Bone.019': 'LeftHandPinky2', 'Bone.020': 'LeftHandPinky3',
    'Bone.010': 'RightHip', 'Bone.014': 'RightUpLeg', 'Bone.015': 'RightLeg', 'Bone.017': 'RightFoot',
    'Bone.011': 'LeftHip', 'Bone.012': 'LeftUpLeg', 'Bone.013': 'LeftLeg', 'Bone.016': 'LeftFoot',
}

bpy.ops.wm.open_mainfile(filepath=str(SOURCE), load_ui=False)
scene = bpy.context.scene
rig = bpy.data.objects['Armature']
body = next(o for o in scene.objects if o.type == 'MESH' and o.find_armature() == rig)
source_action = rig.animation_data.action
rig.name = 'MoalimRig'; body.name = 'MoalimProfessor'

# Sanity check of the side convention before renaming: the character faces -Y, so his left is +X.
left_x = (rig.matrix_world @ rig.data.bones['Bone.007'].head_local).x
right_x = (rig.matrix_world @ rig.data.bones['Bone.003'].head_local).x
assert left_x > right_x, 'unexpected side convention'
for old, new in RENAME.items():
    rig.data.bones[old].name = new           # also renames the vertex groups and the action channels
missing = [b.name for b in rig.data.bones if b.name.startswith('Bone')]
assert not missing, f'unmapped bones: {missing}'

# ---------------------------------------------------------------- sample the source animation
def sample(frame):
    scene.frame_set(frame)
    return {pb.name: (pb.location.copy(), pb.matrix_basis.to_quaternion(), pb.scale.copy()) for pb in rig.pose.bones}

talk_frames = list(range(TALK_RANGE[0], TALK_RANGE[1] + 1))
talk = [sample(f) for f in talk_frames]
idle_a, idle_b = sample(IDLE_POSES[0]), sample(IDLE_POSES[1])
root_drift = max((p['Hips'][0] - talk[0]['Hips'][0]).length for p in talk)
log('talk frames', len(talk), 'root drift', round(root_drift, 3))

for pb in rig.pose.bones:
    pb.rotation_mode = 'QUATERNION'


def bake(name, poses, lock_root=True):
    action = bpy.data.actions.new(name)
    rig.animation_data.action = action
    base_root = poses[0][1]['Hips'][0]
    for frame, pose in poses:
        for pb in rig.pose.bones:
            loc, quat, scale = pose[pb.name]
            if pb.name == 'Hips' and lock_root: loc = base_root     # stays on the spot (the source hops around)
            pb.location, pb.rotation_quaternion, pb.scale = loc, quat, Vector((1, 1, 1)) if pb.name == 'Hips' else scale
            pb.keyframe_insert('location', frame=frame, group=pb.name)
            pb.keyframe_insert('rotation_quaternion', frame=frame, group=pb.name)
            pb.keyframe_insert('scale', frame=frame, group=pb.name)
    action.use_fake_user = True
    track = rig.animation_data.nla_tracks.new(); track.name = name
    track.strips.new(name, int(poses[0][0]), action); track.mute = True
    rig.animation_data.action = None
    log('baked', name, 'frames', len(poses))
    return action


def mix(a, b, t):
    out = {}
    for k in a:
        la, qa, sa = a[k]; lb, qb, sb = b[k]
        out[k] = (la.lerp(lb, t), qa.slerp(qb, t), sa.lerp(sb, t))
    return out


# Talking: the source gestures, closed into a loop by easing the last 12 frames back to the first pose.
talk_poses = []
for i, pose in enumerate(talk):
    tail = len(talk) - 1 - i
    if tail < 12: pose = mix(pose, talk[0], 1 - tail / 12)
    talk_poses.append((i + 1, pose))


def cap_arms(pose):
    out = dict(pose)
    for side in ('Left', 'Right'):
        for part, cap in ARM_CAP.items():
            bone = side + part
            loc, quat, scale = pose[bone]; rest = idle_a[bone][1]
            if rest.dot(quat) < 0: quat = -quat
            angle = math.degrees(rest.rotation_difference(quat).angle)
            if angle > cap: out[bone] = (loc, rest.slerp(quat, cap / angle), scale)
    return out


def smooth_loop(poses, sigma):
    """Gaussian smoothing over a looping sequence of poses: snappy cartoon moves become quick but continuous."""
    if sigma <= 0: return poses
    radius = int(math.ceil(sigma * 3)); n = len(poses)
    weights = [math.exp(-(k * k) / (2 * sigma * sigma)) for k in range(-radius, radius + 1)]
    out = []
    for i in range(n):
        frame, centre = poses[i]
        pose = {}
        for bone, (_, q0, _) in centre.items():
            loc, quat, scale = Vector(), Quaternion((0, 0, 0, 0)), Vector()
            for w, k in zip(weights, range(-radius, radius + 1)):
                l, q, sc = poses[(i + k) % n][1][bone]
                if q.dot(q0) < 0: q = -q
                loc += l * w; scale += sc * w
                quat = Quaternion([a + b * w for a, b in zip(quat, q)])
            total = sum(weights)
            quat.normalize()
            pose[bone] = (loc / total, quat, scale / total)
        out.append((frame, pose))
    return out


talk_poses = smooth_loop([(frame, cap_arms(pose)) for frame, pose in talk_poses], TALK_SMOOTH)
# Idle: calm pose A → calm pose B → A, eased.
idle_poses = []
for f in range(1, IDLE_LENGTH + 2, 4):
    t = (1 - math.cos(2 * math.pi * (f - 1) / IDLE_LENGTH)) / 2
    idle_poses.append((f, mix(idle_a, idle_b, t * 0.6)))
bake('Talking', talk_poses)
bake('Idle', idle_poses)
rig.animation_data.action = None
source_action.use_fake_user = False
bpy.data.actions.remove(source_action)
for pb in rig.pose.bones:
    pb.location = (0, 0, 0); pb.rotation_quaternion = (1, 0, 0, 0); pb.scale = (1, 1, 1)

# ---------------------------------------------------------------- materials
# Each source material has two outputs (Principled and Diffuse); the glTF exporter only understands
# Principled, so that output becomes the active one, otherwise every colour exports as default grey.
for material in body.data.materials:
    if not material or not material.use_nodes: continue
    tree = material.node_tree
    for node in tree.nodes:
        if node.type == 'OUTPUT_MATERIAL':
            fed = [link.from_node.type for link in tree.links if link.to_node == node]
            node.is_active_output = 'BSDF_PRINCIPLED' in fed
            node.target = 'ALL'

# ---------------------------------------------------------------- export
OUT.mkdir(parents=True, exist_ok=True)
glb = OUT / 'moalim-professeur.glb'
bpy.ops.object.select_all(action='DESELECT')
rig.select_set(True); body.select_set(True)
bpy.context.view_layer.objects.active = rig
bpy.ops.export_scene.gltf(filepath=str(glb), use_selection=True, export_format='GLB', export_yup=True,
                          export_skins=True, export_morph=True, export_animations=True,
                          export_animation_mode='NLA_TRACKS', export_cameras=False, export_lights=False)
log('exported', glb, round(glb.stat().st_size / 1e6, 2), 'MB')

# ---------------------------------------------------------------- fallback portrait (idle pose)
for track in rig.animation_data.nla_tracks: track.mute = track.name != 'Idle'
scene.frame_set(1)
depsgraph = bpy.context.evaluated_depsgraph_get()
evaluated = body.evaluated_get(depsgraph)
points = [evaluated.matrix_world @ v.co for v in evaluated.to_mesh().vertices]
lo = Vector((min(p.x for p in points), min(p.y for p in points), min(p.z for p in points)))
hi = Vector((max(p.x for p in points), max(p.y for p in points), max(p.z for p in points)))
evaluated.to_mesh_clear()
centre = (lo + hi) / 2
height, width = hi.z - lo.z, hi.x - lo.x
cam = bpy.data.objects.new('PortraitCamera', bpy.data.cameras.new('PortraitCamera'))
scene.collection.objects.link(cam); scene.camera = cam
cam.data.sensor_fit = 'VERTICAL'; cam.data.angle_y = math.radians(30)
aspect = 360 / 520
distance = max((height * 1.15 / 2) / math.tan(math.radians(15)), (width * 1.15 / 2) / (math.tan(math.radians(15)) * aspect))
cam.location = (centre.x, centre.y - distance, centre.z)
cam.rotation_euler = (Vector(centre) - cam.location).to_track_quat('-Z', 'Y').to_euler()
for name, energy, rot in (('key', 3.2, (50, 0, -30)), ('fill', 1.3, (65, 0, 40)), ('rim', 1.0, (110, 0, 180))):
    light = bpy.data.objects.new(name, bpy.data.lights.new(name, 'SUN')); light.data.energy = energy
    light.rotation_euler = [math.radians(x) for x in rot]; scene.collection.objects.link(light)
scene.render.engine = 'BLENDER_EEVEE'; scene.render.resolution_x = 360; scene.render.resolution_y = 520
scene.render.film_transparent = True
scene.render.filepath = str(OUT / 'moalim-professeur.png')
bpy.ops.render.render(write_still=True)
log('portrait', scene.render.filepath, 'height', round(height, 3))
