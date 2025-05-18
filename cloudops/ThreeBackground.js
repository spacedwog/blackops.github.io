// ThreeBackground.js
import React from 'react';
import { GLView } from 'expo-gl';
import { Renderer } from 'expo-three';
import * as THREE from 'three';

export default function ThreeBackground() {
  return (
    <GLView
      style={{ flex: 1 }}
      onContextCreate={async (gl) => {
        const scene = new THREE.Scene();
        const camera = new THREE.PerspectiveCamera(70, width / height, 0.01, 1000);
        camera.position.z = 5;

        const renderer = new Renderer({ gl });
        renderer.setSize(gl.drawingBufferWidth, gl.drawingBufferHeight);

        const geometry = new THREE.TorusGeometry(1.5, 0.4, 16, 100);
        const material = new THREE.MeshStandardMaterial({ color: 'purple' });
        const torus = new THREE.Mesh(geometry, material);
        scene.add(torus);

        const light = new THREE.PointLight(0xffffff, 1, 100);
        light.position.set(10, 10, 10);
        scene.add(light);

        const render = () => {
          requestAnimationFrame(render);
          torus.rotation.x += 0.01;
          torus.rotation.y += 0.01;
          renderer.render(scene, camera);
          gl.endFrameEXP();
        };
        render();
      }}
    />
  );
}
