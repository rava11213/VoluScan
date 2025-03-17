<template>
    <div>
      <h1>3D Mesh Volume Calculator</h1>
      <input type="file" @change="handleFileUpload" accept=".obj,.stl" />
      <div ref="threejsContainer" class="threejs-container"></div>
      <div v-if="volume !== null">
        <h2>Volume: {{ volume.toFixed(2) }} cubic units</h2>
      </div>
    </div>
  </template>
  
  <script lang="ts">
  import { defineComponent, ref, onMounted } from 'vue';
  import * as THREE from 'three';
  import { OBJLoader } from 'three/examples/jsm/loaders/OBJLoader.js';
  import { STLLoader } from 'three/examples/jsm/loaders/STLLoader.js';
  
  export default defineComponent({
    name: 'MeshVolumeCalculator',
    setup() {
      const threejsContainer = ref<HTMLElement | null>(null);
      const scene = ref<THREE.Scene | null>(null);
      const camera = ref<THREE.PerspectiveCamera | null>(null);
      const renderer = ref<THREE.WebGLRenderer | null>(null);
      const mesh = ref<THREE.Object3D | null>(null);
      const volume = ref<number | null>(null);
  
      // Initialize Three.js scene
      const initThreeJS = () => {
        if (!threejsContainer.value) return;
  
        // Scene
        scene.value = new THREE.Scene();
  
        // Camera
        camera.value = new THREE.PerspectiveCamera(
          75,
          threejsContainer.value.clientWidth / threejsContainer.value.clientHeight,
          0.1,
          1000
        );
        camera.value.position.z = 5;
  
        // Renderer
        renderer.value = new THREE.WebGLRenderer({ antialias: true });
        renderer.value.setSize(threejsContainer.value.clientWidth, threejsContainer.value.clientHeight);
        threejsContainer.value.appendChild(renderer.value.domElement);
  
        // Lighting
        const light = new THREE.DirectionalLight(0xffffff, 1);
        light.position.set(1, 1, 1).normalize();
        scene.value.add(light);
  
        // Animation loop
        const animate = () => {
          requestAnimationFrame(animate);
          if (renderer.value && scene.value && camera.value) {
            renderer.value.render(scene.value, camera.value);
          }
        };
        animate();
      };
  
      // Handle file upload
      const handleFileUpload = (event: Event) => {
        const input = event.target as HTMLInputElement;
        if (!input.files || input.files.length === 0) return;
  
        const file = input.files[0];
        const reader = new FileReader();
        reader.onload = (e) => {
          const loader = file.name.endsWith('.obj') ? new OBJLoader() : new STLLoader();
          loader.load(e.target?.result as string, (object) => {
            if (mesh.value && scene.value) {
              scene.value.remove(mesh.value); // Clear previous mesh
            }
  
            mesh.value = object;
            if (scene.value) {
              scene.value.add(mesh.value);
            }
  
            // Fit the camera to the new mesh
            fitCameraToMesh(mesh.value);
  
            // Calculate volume
            volume.value = calculateVolume(mesh.value);
          });
        };
        reader.readAsDataURL(file);
      };
  
      // Calculate volume of the mesh
      const calculateVolume = (mesh: THREE.Object3D): number => {
        let totalVolume = 0;
  
        mesh.traverse((child) => {
          if (child instanceof THREE.Mesh && child.geometry) {
            const geometry = child.geometry;
  
            if (geometry.index) {
              const indices = geometry.index.array;
              const vertices = geometry.attributes.position.array;
  
              for (let i = 0; i < indices.length; i += 3) {
                const i0 = indices[i] * 3;
                const i1 = indices[i + 1] * 3;
                const i2 = indices[i + 2] * 3;
  
                const v0 = new THREE.Vector3(vertices[i0], vertices[i0 + 1], vertices[i0 + 2]);
                const v1 = new THREE.Vector3(vertices[i1], vertices[i1 + 1], vertices[i1 + 2]);
                const v2 = new THREE.Vector3(vertices[i2], vertices[i2 + 1], vertices[i2 + 2]);
  
                // Calculate tetrahedron volume
                const volume = volumeOfTetrahedron(v0, v1, v2);
                totalVolume += volume;
              }
            }
          }
        });
  
        return Math.abs(totalVolume); // Ensure positive volume
      };
  
      // Volume of tetrahedron formula
      const volumeOfTetrahedron = (a: THREE.Vector3, b: THREE.Vector3, c: THREE.Vector3): number => {
        const cx_by_az = -(c.x * b.y * a.z);
        const bx_cy_az = b.x * c.y * a.z;
        const cx_ay_bz = c.x * a.y * b.z;
        const ax_cy_bz = -(a.x * c.y * b.z);
        const bx_ay_cz = -(b.x * a.y * c.z);
        const ax_by_cz = a.x * b.y * c.z;
        const sum = cx_by_az + bx_cy_az + cx_ay_bz + ax_cy_bz + bx_ay_cz + ax_by_cz;
  
        return (1.0 / 6.0) * sum;
      };
  
      // Adjust camera position based on the mesh size
      const fitCameraToMesh = (mesh: THREE.Object3D) => {
        if (!camera.value || !mesh) return;
  
        const boundingBox = new THREE.Box3().setFromObject(mesh);
        const size = boundingBox.getSize(new THREE.Vector3());
        const center = boundingBox.getCenter(new THREE.Vector3());
  
        // Make the camera fit the mesh
        camera.value.position.z = size.length() * 1.5;
        camera.value.lookAt(center);
      };
  
      // Resize handling
      onMounted(() => {
        initThreeJS();
        window.addEventListener('resize', handleResize);
      });
  
      // Cleanup when component is unmounted
      onUnmounted(() => {
        window.removeEventListener('resize', handleResize);
      });
  
      return {
        threejsContainer,
        handleFileUpload,
        volume,
      };
    },
  });
  </script>
  
  <style scoped>
  .threejs-container {
    width: 100%;
    height: 500px;
    border: 1px solid #ccc;
  }
  </style>
  