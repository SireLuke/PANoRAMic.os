import * as THREE from "https://cdn.skypack.dev/three@0.152.2";

// SCENE + CAMERA
const scene = new THREE.Scene();
const camera = new THREE.PerspectiveCamera(
  60,
  window.innerWidth / window.innerHeight,
  0.1,
  1000
);
camera.position.set(0, 0, 6);

// RENDERER
const renderer = new THREE.WebGLRenderer({ antialias: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setClearColor(0x000033); // deep metallic royal blue
document.body.appendChild(renderer.domElement);

// LIGHTING
const light = new THREE.PointLight(0xffffff, 1.2);
light.position.set(5, 5, 5);
scene.add(light);

const ambient = new THREE.AmbientLight(0x333333);
scene.add(ambient);

// ===============================
// EARTH (NASA BLUE MARBLE 4K)
// ===============================
const texture = new THREE.TextureLoader().load(
  "./textures/earth_global_5400.jpg",
  () => console.log("Earth texture loaded"),
  undefined,
  (err) => console.error("Texture failed to load", err)
);


const earthMaterial = new THREE.MeshPhongMaterial({
  map: texture,
  shininess: 40,
  color: 0x3366ff,          // adds a bright blue tint
  emissive: 0x111111,       // subtle self‑illumination
  emissiveIntensity: 0.4,   // brighten the dark areas
});


const earth = new THREE.Mesh(
  new THREE.SphereGeometry(2, 128, 128),
  earthMaterial
);

scene.add(earth);

// ===============================
// GOLD MICRO‑STARS BACKGROUND
// ===============================
const starCount = 2000;
const starPositions = [];

for (let i = 0; i < starCount; i++) {
  const r = 12 + Math.random() * 6; // distance from Earth
  const phi = Math.random() * Math.PI * 2;
  const theta = Math.random() * Math.PI;

  starPositions.push(
    r * Math.sin(theta) * Math.cos(phi),
    r * Math.cos(theta),
    r * Math.sin(theta) * Math.sin(phi)
  );
}

const starGeom = new THREE.BufferGeometry();
starGeom.setAttribute(
  "position",
  new THREE.Float32BufferAttribute(starPositions, 3)
);

const starMat = new THREE.PointsMaterial({
  color: 0xffd700, // gold
  size: 0.02
});

const stars = new THREE.Points(starGeom, starMat);
scene.add(stars);

// ===============================
// ANIMATION LOOP
// ===============================
function animate() {
  requestAnimationFrame(animate);

  earth.rotation.y += 0.0015;
  stars.rotation.y += 0.0005;

  renderer.render(scene, camera);
}

animate();

// ===============================
// HUD UPDATE HOOK
// ===============================
export function updateHUD(packet) {
  document.getElementById("hud-tick").innerText = `Tick ${packet.tick}`;
  document.getElementById("hud-headline").innerText = packet.headline;
  document.getElementById("hud-health").innerText =
    `Health: ${packet.overallHealth.toFixed(3)}`;

  document.getElementById("rams-score").innerText = packet.rams.toFixed(3);
  document.getElementById("rsdv-score").innerText = packet.rsdv.toFixed(3);
  document.getElementById("par-cap").innerText = packet.parCap;
  document.getElementById("dem-rate").innerText = packet.dem.toFixed(3);
  document.getElementById("stag-index").innerText = packet.stag.toFixed(3);

  document.getElementById("stability").innerText =
    packet.overallHealth.toFixed(3);
  document.getElementById("scarcity").innerText = packet.scarcity.toFixed(3);
  document.getElementById("recovery").innerText = packet.recovery.toFixed(3);
  document.getElementById("coherence").innerText = packet.coherence.toFixed(3);

  document.getElementById("par-flow").innerText = packet.parFlow.toFixed(3);
}
