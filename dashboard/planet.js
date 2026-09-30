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
renderer.setClearColor(0x000822); // deep royal blue
document.body.appendChild(renderer.domElement);

// LIGHT
const light = new THREE.DirectionalLight(0xfff6c0, 1.2); // metallic gold
light.position.set(5, 3, 5);
scene.add(light);

// GOLD WIREFRAME EARTH
const geometry = new THREE.SphereGeometry(2, 64, 64);
const material = new THREE.MeshBasicMaterial({
  color: 0xffd700, // metallic gold
  wireframe: true
});
const earth = new THREE.Mesh(geometry, material);
scene.add(earth);

camera.position.z = 6;

// ANIMATION LOOP
function animate() {
  requestAnimationFrame(animate);
  earth.rotation.y += 0.0015;
  renderer.render(scene, camera);
}

animate();
