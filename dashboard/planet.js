import * as THREE from "https://cdn.skypack.dev/three@0.152.2";

// SCENE + CAMERA
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);

const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
// deep royal blue background
renderer.setClearColor(0x000822); 
document.body.appendChild(renderer.domElement);

// LIGHTS (soft metallic feel)
const ambient = new THREE.AmbientLight(0xffffff, 0.4);
scene.add(ambient);

const directional = new THREE.DirectionalLight(0xfff6c0, 1.2);
directional.position.set(5, 3, 5);
scene.add(directional);

// EARTH WIREFRAME (metallic gold grid)
const radius = 2;
const segments = 64;

const sphereGeom = new THREE.SphereGeometry(radius, segments, segments);
const wireMaterial = new THREE.MeshBasicMaterial({
  color: 0xffd700, // metallic gold
  wireframe: true
});
const earthWire = new THREE.Mesh(sphereGeom, wireMaterial);
scene.add(earthWire);

// subtle sparkle: small gold points on the grid
const sparkleGeom = new THREE.BufferGeometry();
const sparkleCount = 400;
const positions = [];

for (let i = 0; i < sparkleCount; i++) {
  const phi = Math.random() * Math.PI * 2;
  const theta = Math.random() * Math.PI;
  const r = radius + 0.01;

  const x = r * Math.sin(theta) * Math.cos(phi);
  const y = r * Math.cos(theta);
  const z = r * Math.sin(theta) * Math.sin(phi);

  positions.push(x, y, z);
}

sparkleGeom.setAttribute(
  "position",
  new THREE.Float32BufferAttribute(positions, 3)
);

const sparkleMaterial = new THREE.PointsMaterial({
  color: 0xfff6c0,
  size: 0.03
});

const sparkles = new THREE.Points(sparkleGeom, sparkleMaterial);
scene.add(sparkles);

// CAMERA
camera.position.z = 6;
camera.lookAt(scene.position);

// HANDLE RESIZE
window.addEventListener("resize", () => {
  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();
  renderer.setSize(window.innerWidth, window.innerHeight);
});

// ANIMATE (slow rotation)
function animate() {
  requestAnimationFrame(animate);

  earthWire.rotation.y += 0.0015;
  sparkles.rotation.y += 0.0015;

  renderer.render(scene, camera);
}

animate();

}


animate();
