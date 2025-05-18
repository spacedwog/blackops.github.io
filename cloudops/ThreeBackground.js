import React, { useRef } from 'react';
import { GLView } from 'expo-gl';
import { Renderer } from 'expo-three';
import * as THREE from 'three';
import { PanResponder, TouchableOpacity, Text, View } from 'react-native';
import Voice from 'react-native-voice';
import * as Linking from 'expo-linking';

export default function ThreeBackground() {
  const torusRef = useRef();

  // Comando de voz
  const startVoiceSearch = () => {
    Voice.onSpeechResults = (event) => {
      if (event.value && event.value.length > 0) {
        const query = event.value[0];
        const url = `https://www.google.com/search?q=${encodeURIComponent(query)}`;
        Linking.openURL(url);
      }
    };
    Voice.start('en-US');
  };

  // Gesto de toque
  const panResponder = useRef(
    PanResponder.create({
      onMoveShouldSetPanResponder: () => true,
      onPanResponderMove: (_, gesture) => {
        if (torusRef.current) {
          torusRef.current.rotation.y += gesture.dx * 0.005;
          torusRef.current.rotation.x += gesture.dy * 0.005;
        }
      },
    })
  ).current;

  return (
    <View style={{ flex: 1 }}>
      <GLView
        style={{ flex: 1 }}
        {...panResponder.panHandlers}
        onContextCreate={async (gl) => {
          const scene = new THREE.Scene();
          const camera = new THREE.PerspectiveCamera(
            75,
            gl.drawingBufferWidth / gl.drawingBufferHeight,
            0.1,
            1000
          );
          camera.position.z = 5;

          const renderer = new Renderer({ gl });
          renderer.setSize(gl.drawingBufferWidth, gl.drawingBufferHeight);

          const geometry = new THREE.TorusGeometry(1.5, 0.4, 16, 100);
          const material = new THREE.MeshStandardMaterial({ color: 'purple' });
          const torus = new THREE.Mesh(geometry, material);
          torusRef.current = torus;
          scene.add(torus);

          const light = new THREE.PointLight(0xffffff, 1, 100);
          light.position.set(10, 10, 10);
          scene.add(light);

          const animate = () => {
            requestAnimationFrame(animate);
            renderer.render(scene, camera);
            gl.endFrameEXP();
          };
          animate();
        }}
      />

      <TouchableOpacity
        onPress={startVoiceSearch}
        style={{
          position: 'absolute',
          bottom: 30,
          right: 30,
          backgroundColor: 'purple',
          padding: 15,
          borderRadius: 30,
          elevation: 5,
        }}
      >
        <Text style={{ color: 'white', fontSize: 18 }}>🎤</Text>
      </TouchableOpacity>
    </View>
  );
}