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
renderer.setClearColor(0x000033); // deep metallic royal blue
document.body.appendChild(renderer.domElement);

// LIGHT
const light = new THREE.DirectionalLight(0xfff6c0, 1.2); // metallic gold
light.position.set(5, 3, 5);
scene.add(light);

const texture = new THREE.TextureLoader().load(
  "https://eoimages.gsfc.nasa.gov/images/imagerecords/74000/74497/world.topo.bathy.200412.3x5400x2700.jpg"
);

const earthMaterial = new THREE.MeshPhongMaterial({
  map: texture,
  shininess: 80,
  color: 0x001133, // deep metallic blue tint
});

const earth = new THREE.Mesh(
  new THREE.SphereGeometry(2, 128, 128),
  earthMaterial
);

scene.add(earth);
// GOLD MICRO-STARS BACKGROUND
const starCount = 2000;
const starPositions = [];

for (let i = 0; i < starCount; i++) {
  const r = 10 + Math.random() * 5; // distance from Earth
  const phi = Math.random() * Math.PI * 2;
  const theta = Math.random() * Math.PI;

  starPositions.push(
    r * Math.sin(theta) * Math.cos(phi),
    r * Math.cos(theta),
    r * Math.sin(theta) * Math.sin(phi)
  );
}

const starGeom = new THREE.BufferGeometry();
starGeom.setAttribute("position", new THREE.Float32BufferAttribute(starPositions, 3));

const starMat = new THREE.PointsMaterial({
  color: 0xffd700, // metallic gold
  size: 0.02
});

const stars = new THREE.Points(starGeom, starMat);
scene.add(stars);


camera.position.z = 6;

// ANIMATION LOOP
function animate() {
  requestAnimationFrame(animate);
  earth.rotation.y += 0.0015;
  stars.rotation.y += 0.0005;
  renderer.render(scene, camera);
}

animate();
function updateHUD(packet) {
  document.getElementById("hud-tick").innerText = `Tick ${packet.tick}`;
  document.getElementById("hud-headline").innerText = packet.headline;
  document.getElementById("hud-health").innerText = `Health: ${packet.overallHealth.toFixed(3)}`;

  document.getElementById("rams-score").innerText = packet.rams.toFixed(3);
  document.getElementById("rsdv-score").innerText = packet.rsdv.toFixed(3);
  document.getElementById("par-cap").innerText = packet.parCap;
  document.getElementById("dem-rate").innerText = packet.dem.toFixed(3);
  document.getElementById("stag-index").innerText = packet.stag.toFixed(3);

  document.getElementById("stability").innerText = packet.overallHealth.toFixed(3);
  document.getElementById("scarcity").innerText = packet.scarcity.toFixed(3);
  document.getElementById("recovery").innerText = packet.recovery.toFixed(3);
  document.getElementById("coherence").innerText = packet.coherence.toFixed(3);

  document.getElementById("par-flow").innerText = packet.parFlow.toFixed(3);
}
