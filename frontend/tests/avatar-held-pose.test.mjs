import test from 'node:test';
import assert from 'node:assert/strict';
import { AnimationClip, AnimationMixer, Bone, Quaternion, QuaternionKeyframeTrack, Vector3 } from 'three';

// three.js only writes a bone when its animated value changes from the previous frame (PropertyMixer.apply:
// "value has changed -> update scene graph"). Professor3D resets every bone before updating the mixer, so a
// held pose must be restored from the mixer's last output, not from the bind pose, or the bone snaps back.
const held = new Quaternion().setFromAxisAngle(new Vector3(1, 0, 0), 0.8);
const makeRig = () => {
  const bone = new Bone(); bone.name = 'RightArm';
  const track = new QuaternionKeyframeTrack('RightArm.quaternion', [0, 1, 2], [...held.toArray(), ...held.toArray(), ...held.toArray()]);
  const mixer = new AnimationMixer(bone);
  mixer.clipAction(new AnimationClip('Talking', 2, [track])).play();
  return { bone, mixer };
};

test('resetting to the bind pose before the mixer loses a held pose (the defect)', () => {
  const { bone, mixer } = makeRig();
  const bind = bone.quaternion.clone();
  let snapped = 0;
  for (let frame = 0; frame < 30; frame++) {
    bone.quaternion.copy(bind);
    mixer.update(1 / 60);
    if (bone.quaternion.angleTo(held) > 1e-3) snapped++;
  }
  assert.ok(snapped > 20, `the bone sits in the bind pose on ${snapped} of 30 frames`);
});

test('restoring the last pose written by the mixer keeps a held pose on every frame (the fix)', () => {
  const { bone, mixer } = makeRig();
  const last = bone.quaternion.clone();
  for (let frame = 0; frame < 30; frame++) {
    bone.quaternion.copy(last);
    mixer.update(1 / 60);
    last.copy(bone.quaternion);
    bone.quaternion.multiply(new Quaternion().setFromAxisAngle(new Vector3(0, 1, 0), 0.2));   // additive gesture, as in Professor3D
    assert.ok(last.angleTo(held) < 1e-3, `frame ${frame} keeps the animated pose`);
  }
});
