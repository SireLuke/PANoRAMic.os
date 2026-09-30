import * as THREE from "https://cdn.skypack.dev/three@0.152.2";
let metrics = { stability: 0.8, rsdv: 0.8, parMax: 0, stagnation: 0.2 };

async function loadMetrics() {
  const res = await fetch("/metrics");
  metrics = await res.json();
}
await loadMetrics();

const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(75, innerWidth / innerHeight, 0.1, 1000);
const renderer = new THREE.WebGLRenderer();
renderer.setSize(innerWidth, innerHeight);
document.body.appendChild(renderer.domElement);

const geometry = new THREE.SphereGeometry(2, 64, 64);
const texture = new THREE.TextureLoader().load(
  "https://raw.githubusercontent.com/itsLuke/SampleTextures/main/earth_daymap.jpg"
);
const material = new THREE.MeshBasicMaterial({ map: texture });
const earth = new THREE.Mesh(geometry, material);
scene.add(earth);

camera.position.z = 5;

function animate() {
  requestAnimationFrame(animate);

  // rotation speed from RAMS stability
  earth.rotation.y += 0.001 + metrics.stability * 0.002;

  // glow intensity from RSDV scarcity
  earth.material.emissive = new THREE.Color(0x222200);
  earth.material.emissiveIntensity = metrics.rsdv;

  // brightness from PAR supply
  earth.material.color.setHSL(0.15, 1.0, 0.3 + metrics.parMax / 1e10);

  // pulse color from stagnation
  const pulse = Math.sin(Date.now() * 0.001) * metrics.stagnation;
  earth.material.color.offsetHSL(pulse * 0.02, 0, 0);

  renderer.render(scene, camera);
}


animate();
