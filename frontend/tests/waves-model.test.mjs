import {test} from 'node:test';
import assert from 'node:assert/strict';
import {pulse, speed, springPosition, arrivals, assess} from '../public/media/simulations/physics/progressive/model.js';
test('les spires ne se traversent pas même à amplitude maximale',()=>{
  for(let x=0;x<10;x+=.01)assert.ok(springPosition(x+.01,5,1.5)>springPosition(x,5,1.5));
});
test('une impulsion revient à zéro et deux opposées se compensent',()=>{
  assert.equal(pulse(4,0),0);assert.equal(pulse(4,4),1);assert.equal(pulse(4,8),0);
  for(let x=0;x<=10;x+=.1)assert.equal(pulse(x,5,1)+pulse(x,5,-1),0);
});
test('la célérité dépend du milieu et les retards de la distance',()=>{
  assert.equal(speed(4,.25),4);assert.equal(speed(9,.25),6);assert.equal(speed(4,1),2);
  const a=arrivals({sensor1:1,sensor2:3,speed:4});const b=arrivals({sensor1:1,sensor2:5,speed:4});
  assert.equal(b.b-b.a,2*(a.b-a.a));
  assert.throws(()=>arrivals({sensor1:4,sensor2:2,speed:0}));
});
test('la validation exige une acquisition et un calcul correct de l’élève',()=>{
  const p={sensor1:2,sensor2:7,speed:4};
  assert.equal(assess(p,0,{delay:1.25,speed:4}).correct,false);
  assert.equal(assess(p,3,{delay:1250,speed:4}).correct,false);
  assert.equal(assess(p,3,{delay:1.25,speed:40}).correct,false);
  assert.equal(assess(p,3,{delay:NaN,speed:4}).correct,false);
  assert.equal(assess(p,3,{delay:1.25,speed:4}).correct,true);
});
