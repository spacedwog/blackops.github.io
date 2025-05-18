import React, { useRef } from 'react';
import { Canvas, useFrame } from '@react-three/fiber';
import { OrbitControls, Stars, Float, Html } from '@react-three/drei';
import { loadAsync } from 'expo-three';

function SpinningTorus() {
  const meshRef = useRef();

  useFrame(() => {
    if (meshRef.current) {
      meshRef.current.rotation.x += 0.005;
      meshRef.current.rotation.y += 0.005;
    }
  });

  return (
    <mesh ref={meshRef} position={[0, 0, 0]}>
      <torusGeometry args={[1.5, 0.4, 16, 100]} />
      <meshStandardMaterial color="purple" emissive="black" metalness={0.8} roughness={0.2} />
    </mesh>
  );
}

function DataNodes() {
  return (
    <group>
      {[...Array(20)].map((_, i) => (
        <Float key={i} speed={1.5} rotationIntensity={1} floatIntensity={2}>
          <mesh position={[Math.sin(i) * 3, Math.cos(i) * 3, (i - 10) * 0.5]}>
            <boxGeometry args={[0.2, 0.2, 0.2]} />
            <meshStandardMaterial
              color="#00ffcc"
              emissive="#005f5f"
              metalness={0.6}
              roughness={0.3}
            />
          </mesh>
        </Float>
      ))}
    </group>
  );
}

export default function ThreeBackground() {
  return (
    <Canvas style={{ position: 'absolute', zIndex: -1 }} camera={{ position: [0, 0, 10], fov: 60 }}>
      <color attach="background" args={["#000011"]} />
      <ambientLight intensity={0.3} />
      <pointLight position={[10, 10, 10]} intensity={1} />
      <Stars radius={100} depth={50} count={5000} factor={4} saturation={0} fade />

      <SpinningTorus />
      <DataNodes />

      <OrbitControls enableZoom={false} autoRotate autoRotateSpeed={0.5} />
    </Canvas>
  );
}