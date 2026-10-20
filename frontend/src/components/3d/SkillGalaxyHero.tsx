import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { useTheme } from '../../context/ThemeContext';

interface NodeData {
  id: string;
  name: string;
  category: string;
  status: 'completed' | 'in_progress' | 'ready' | 'locked';
  x: number;
  y: number;
  z: number;
  size: number;
}

const SKILL_NODES: NodeData[] = [
  // Core AI / ML Cluster
  { id: '1', name: 'Python Foundations', category: 'Core CS', status: 'completed', x: -6, y: 2, z: 0, size: 1.4 },
  { id: '2', name: 'Linear Algebra', category: 'Math', status: 'completed', x: -3, y: 4, z: 2, size: 1.2 },
  { id: '3', name: 'PyTorch Deep Learning', category: 'Deep Learning', status: 'completed', x: 0, y: 1, z: 0, size: 1.6 },
  { id: '4', name: 'Transformers & Attention', category: 'GenAI', status: 'in_progress', x: 3, y: 3, z: -1, size: 1.5 },
  { id: '5', name: 'Vector DB & Hybrid RAG', category: 'Applied AI', status: 'ready', x: 6, y: 1, z: 1, size: 1.3 },
  { id: '6', name: 'TensorRT Inference', category: 'Production', status: 'locked', x: 8, y: -2, z: 2, size: 1.1 },
  { id: '7', name: 'Kubernetes & MLOps', category: 'Cloud', status: 'locked', x: 5, y: -4, z: -2, size: 1.2 },

  // Satellite Sub-Competencies
  { id: '8', name: 'Calculus & Optimization', category: 'Math', status: 'completed', x: -4, y: 6, z: -2, size: 0.9 },
  { id: '9', name: 'Computer Vision (ViT)', category: 'Deep Learning', status: 'in_progress', x: -1, y: -3, z: 3, size: 1.1 },
  { id: '10', name: 'LoRA & PEFT Tuning', category: 'GenAI', status: 'ready', x: 2, y: 5, z: 2, size: 1.0 },
  { id: '11', name: 'LangChain & LlamaIndex', category: 'Applied AI', status: 'ready', x: 5, y: 3, z: 3, size: 1.0 },
  { id: '12', name: 'FastAPI Microservices', category: 'Engineering', status: 'completed', x: -3, y: -2, z: -3, size: 1.2 },
  { id: '13', name: 'Docker Containers', category: 'DevOps', status: 'completed', x: -5, y: -4, z: 1, size: 1.0 },
  { id: '14', name: 'Hugging Face Hub', category: 'GenAI', status: 'in_progress', x: 1, y: 4, z: -3, size: 1.1 },
  { id: '15', name: 'CUDA GPU Kernels', category: 'High Perf', status: 'locked', x: 2, y: -3, z: -2, size: 0.9 },
];

const EDGES: Array<[number, number]> = [
  [0, 1], // Python -> Linear Algebra
  [1, 2], // Linear Algebra -> PyTorch
  [2, 3], // PyTorch -> Transformers
  [3, 4], // Transformers -> Vector DB / RAG
  [4, 5], // RAG -> TensorRT
  [5, 6], // TensorRT -> Kubernetes
  [1, 7], // Linear Algebra -> Calculus
  [2, 8], // PyTorch -> ViT
  [3, 9], // Transformers -> LoRA
  [4, 10], // RAG -> LangChain
  [0, 11], // Python -> FastAPI
  [11, 12], // FastAPI -> Docker
  [3, 13], // Transformers -> HF Hub
  [2, 14], // PyTorch -> CUDA
];

export const SkillGalaxyHero: React.FC = () => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [hoveredNode, setHoveredNode] = useState<NodeData | null>(null);
  const [webGLError, setWebGLError] = useState(false);
  const { themeMeta } = useTheme();
  const light1Ref = useRef<THREE.PointLight | null>(null);
  const light2Ref = useRef<THREE.PointLight | null>(null);

  useEffect(() => {
    if (light1Ref.current) light1Ref.current.color.set(themeMeta.secondaryColor);
    if (light2Ref.current) light2Ref.current.color.set(themeMeta.primaryColor);
  }, [themeMeta.primaryColor, themeMeta.secondaryColor]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 800;
    const height = container.clientHeight || 500;

    // 1. Scene, Camera, Renderer with WebGL error safety
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
    camera.position.set(0, 0, 18);

    let renderer: THREE.WebGLRenderer;
    try {
      renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true, powerPreference: 'high-performance' });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.toneMapping = THREE.ACESFilmicToneMapping;
      container.appendChild(renderer.domElement);
    } catch (e) {
      console.warn('WebGL initialization failed, using topological fallback:', e);
      setWebGLError(true);
      return;
    }

    // 2. Ambient & Directional Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
    scene.add(ambientLight);

    const blueLight = new THREE.PointLight(themeMeta.secondaryColor, 3, 50);
    blueLight.position.set(-10, 8, 10);
    scene.add(blueLight);
    light1Ref.current = blueLight;

    const violetLight = new THREE.PointLight(themeMeta.primaryColor, 3, 50);
    violetLight.position.set(10, -8, 8);
    scene.add(violetLight);
    light2Ref.current = violetLight;

    // 3. Background Dust Particles / Starfield
    const starsCount = 600;
    const starGeometry = new THREE.BufferGeometry();
    const starPositions = new Float32Array(starsCount * 3);
    const starColors = new Float32Array(starsCount * 3);

    for (let i = 0; i < starsCount; i++) {
      starPositions[i * 3] = (Math.random() - 0.5) * 60;
      starPositions[i * 3 + 1] = (Math.random() - 0.5) * 60;
      starPositions[i * 3 + 2] = (Math.random() - 0.5) * 40;

      // Color variation (ice blue to violet)
      const mix = Math.random();
      starColors[i * 3] = 0.2 + mix * 0.4;
      starColors[i * 3 + 1] = 0.5 + mix * 0.3;
      starColors[i * 3 + 2] = 0.9;
    }

    starGeometry.setAttribute('position', new THREE.BufferAttribute(starPositions, 3));
    starGeometry.setAttribute('color', new THREE.BufferAttribute(starColors, 3));

    const starMaterial = new THREE.PointsMaterial({
      size: 0.12,
      vertexColors: true,
      transparent: true,
      opacity: 0.7,
    });
    const starField = new THREE.Points(starGeometry, starMaterial);
    scene.add(starField);

    // 4. Galaxy Graph Group (for rotation & cursor parallax)
    const galaxyGroup = new THREE.Group();
    scene.add(galaxyGroup);

    // 5. Build 3D Skill Spheres
    const sphereGeometry = new THREE.SphereGeometry(1, 32, 32);
    const meshList: THREE.Mesh[] = [];

    SKILL_NODES.forEach((node) => {
      let nodeColor = 0x38bdf8;
      let emissiveColor = 0x0284c7;
      let emissiveIntensity = 0.6;
      let opacity = 0.95;

      if (node.status === 'completed') {
        nodeColor = 0x38bdf8;
        emissiveColor = 0x0284c7;
        emissiveIntensity = 0.8;
      } else if (node.status === 'in_progress') {
        nodeColor = 0xa855f7;
        emissiveColor = 0x7e22ce;
        emissiveIntensity = 0.7;
      } else if (node.status === 'ready') {
        nodeColor = 0x10b981;
        emissiveColor = 0x047857;
        emissiveIntensity = 0.5;
      } else {
        // Locked
        nodeColor = 0x334155;
        emissiveColor = 0x1e293b;
        emissiveIntensity = 0.15;
        opacity = 0.45;
      }

      const material = new THREE.MeshStandardMaterial({
        color: nodeColor,
        emissive: emissiveColor,
        emissiveIntensity: emissiveIntensity,
        metalness: 0.3,
        roughness: 0.2,
        transparent: true,
        opacity: opacity,
      });

      const mesh = new THREE.Mesh(sphereGeometry, material);
      mesh.position.set(node.x, node.y, node.z);
      mesh.scale.setScalar(node.size * 0.75);
      mesh.userData = { nodeData: node };

      // Outer wireframe orbit ring for active/in-progress nodes
      if (node.status === 'completed' || node.status === 'in_progress') {
        const ringGeo = new THREE.RingGeometry(node.size * 0.9, node.size * 1.05, 32);
        const ringMat = new THREE.MeshBasicMaterial({
          color: nodeColor,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.35,
        });
        const ringMesh = new THREE.Mesh(ringGeo, ringMat);
        ringMesh.rotation.x = Math.PI / 3;
        mesh.add(ringMesh);
      }

      galaxyGroup.add(mesh);
      meshList.push(mesh);
    });

    // 6. Connecting Edge Lines
    const lineMaterial = new THREE.LineBasicMaterial({
      color: 0x4f46e5,
      transparent: true,
      opacity: 0.45,
      linewidth: 1,
    });

    EDGES.forEach(([srcIdx, dstIdx]) => {
      const src = SKILL_NODES[srcIdx];
      const dst = SKILL_NODES[dstIdx];
      const points = [
        new THREE.Vector3(src.x, src.y, src.z),
        new THREE.Vector3(dst.x, dst.y, dst.z),
      ];
      const lineGeo = new THREE.BufferGeometry().setFromPoints(points);
      const line = new THREE.Line(lineGeo, lineMaterial);
      galaxyGroup.add(line);
    });

    // 7. Raycaster & Mouse Parallax
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2();
    let targetRotationX = 0;
    let targetRotationY = 0;

    const handleMouseMove = (e: MouseEvent) => {
      const rect = container.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / rect.width) * 2 - 1;
      const y = -((e.clientY - rect.top) / rect.height) * 2 + 1;

      mouse.x = x;
      mouse.y = y;

      // Subtle parallax angles
      targetRotationY = x * 0.35;
      targetRotationX = -y * 0.25;

      // Raycast for hovering over nodes
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(meshList);

      if (intersects.length > 0) {
        const hit = intersects[0].object as THREE.Mesh;
        setHoveredNode(hit.userData.nodeData);
      } else {
        setHoveredNode(null);
      }
    };

    container.addEventListener('mousemove', handleMouseMove);

    // 8. Animation Loop
    let animationFrameId: number;
    const startTime = performance.now();

    const animate = () => {
      const elapsedTime = (performance.now() - startTime) / 1000;

      // Smooth camera / group rotation toward mouse parallax target
      galaxyGroup.rotation.y += (targetRotationY - galaxyGroup.rotation.y) * 0.05;
      galaxyGroup.rotation.x += (targetRotationX - galaxyGroup.rotation.x) * 0.05;

      // Gentle continuous ambient drift
      galaxyGroup.rotation.y += 0.0015;
      starField.rotation.y -= 0.0005;

      // Pulse node scales slightly
      meshList.forEach((mesh, index) => {
        const offset = index * 0.5;
        const pulse = 1 + Math.sin(elapsedTime * 2 + offset) * 0.04;
        const baseScale = mesh.userData.nodeData.size * 0.75;
        mesh.scale.setScalar(baseScale * pulse);
      });

      renderer.render(scene, camera);
      animationFrameId = requestAnimationFrame(animate);
    };

    animate();

    // 9. Resize Handling
    const handleResize = () => {
      if (!container) return;
      const w = container.clientWidth;
      const h = container.clientHeight;
      camera.aspect = w / h;
      camera.updateProjectionMatrix();
      renderer.setSize(w, h);
    };

    window.addEventListener('resize', handleResize);

    return () => {
      cancelAnimationFrame(animationFrameId);
      container.removeEventListener('mousemove', handleMouseMove);
      window.removeEventListener('resize', handleResize);
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, []);

  if (webGLError) {
    return (
      <div className="relative h-full min-h-[320px] w-full select-none overflow-hidden rounded-2xl border border-white/[0.08] bg-slate-950/80 p-5 shadow-2xl flex flex-col justify-between">
        <div className="flex items-center justify-between border-b border-white/[0.06] pb-3">
          <div className="flex items-center gap-2">
            <span className="h-2 w-2 rounded-full bg-sky-400 animate-pulse" />
            <span className="text-xs font-bold text-sky-300">Topological Skill Matrix</span>
          </div>
          <span className="text-[11px] text-slate-400">High-Performance 2D Mode</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-3 gap-2.5 my-4">
          {SKILL_NODES.slice(0, 9).map((node) => (
            <div
              key={node.id}
              className={`rounded-xl p-2.5 border transition-all ${
                node.status === 'completed'
                  ? 'bg-sky-500/10 border-sky-400/30 text-sky-200'
                  : node.status === 'in_progress'
                  ? 'bg-violet-500/10 border-violet-400/30 text-violet-200'
                  : node.status === 'ready'
                  ? 'bg-emerald-500/10 border-emerald-400/30 text-emerald-200'
                  : 'bg-slate-900/40 border-slate-800 text-slate-400'
              }`}
            >
              <div className="text-[10px] uppercase font-bold text-slate-400">{node.category}</div>
              <div className="text-xs font-bold text-white truncate mt-0.5">{node.name}</div>
              <div className="text-[10px] mt-1 capitalize font-medium">{node.status.replace('_', ' ')}</div>
            </div>
          ))}
        </div>

        <div className="flex items-center justify-between text-[11px] text-slate-400 pt-2 border-t border-white/[0.06]">
          <span>🔵 Cyan: Verified • 🟣 Purple: Focus • 🟢 Green: Ready</span>
          <span>15 Active Nodes Mapped</span>
        </div>
      </div>
    );
  }

  return (
    <div className="relative h-[550px] w-full select-none overflow-hidden rounded-3xl border border-white/[0.08] bg-[#070b14]/80 shadow-2xl">
      {/* 3D WebGL Canvas Container */}
      <div ref={mountRef} className="h-full w-full cursor-crosshair" />

      {/* Floating Ambient Info Overlay */}
      <div className="pointer-events-none absolute left-6 top-6 flex items-center gap-3">
        <div className="flex items-center gap-2 rounded-full border border-sky-500/30 bg-sky-950/40 px-3 py-1 text-xs font-semibold text-sky-300 backdrop-blur-md">
          <span className="h-2 w-2 animate-pulse rounded-full bg-sky-400" />
          Interactive 3D Skill Galaxy
        </div>
        <span className="text-xs text-slate-400">Move cursor to orbit & inspect nodes</span>
      </div>

      {/* Node Status Legend */}
      <div className="pointer-events-none absolute bottom-6 left-6 flex flex-wrap items-center gap-4 rounded-xl border border-white/[0.06] bg-slate-950/60 px-4 py-2 text-xs backdrop-blur-md">
        <div className="flex items-center gap-1.5 text-slate-300">
          <span className="h-2.5 w-2.5 rounded-full bg-sky-400 shadow-[0_0_8px_#38bdf8]" />
          Verified / Completed
        </div>
        <div className="flex items-center gap-1.5 text-slate-300">
          <span className="h-2.5 w-2.5 rounded-full bg-violet-400 shadow-[0_0_8px_#a855f7]" />
          In Progress
        </div>
        <div className="flex items-center gap-1.5 text-slate-300">
          <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_#10b981]" />
          Ready to Learn
        </div>
        <div className="flex items-center gap-1.5 text-slate-400">
          <span className="h-2.5 w-2.5 rounded-full bg-slate-600" />
          Prerequisite Locked
        </div>
      </div>

      {/* Dynamic Hover Tooltip Popover */}
      {hoveredNode && (
        <div className="pointer-events-none absolute right-6 top-6 max-w-xs animate-in fade-in zoom-in-95 duration-200 rounded-2xl border border-sky-400/30 bg-slate-900/90 p-4 shadow-2xl backdrop-blur-xl">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <span>{hoveredNode.category}</span>
            <span
              className={`rounded-full px-2 py-0.5 text-[10px] font-semibold uppercase ${
                hoveredNode.status === 'completed'
                  ? 'bg-sky-500/20 text-sky-300'
                  : hoveredNode.status === 'in_progress'
                  ? 'bg-violet-500/20 text-violet-300'
                  : hoveredNode.status === 'ready'
                  ? 'bg-emerald-500/20 text-emerald-300'
                  : 'bg-slate-800 text-slate-400'
              }`}
            >
              {hoveredNode.status.replace('_', ' ')}
            </span>
          </div>
          <h4 className="mt-1.5 text-base font-bold text-white">{hoveredNode.name}</h4>
          <p className="mt-1 text-xs text-slate-300">
            {hoveredNode.status === 'completed'
              ? 'Mastery verified through academic credits & project portfolio.'
              : hoveredNode.status === 'in_progress'
              ? 'Current active focus milestone. Adaptive assessment ready.'
              : hoveredNode.status === 'ready'
              ? 'Prerequisites met! Next unlock in your personalized AI roadmap.'
              : 'Complete preceding foundational tensor & deep learning nodes to unlock.'}
          </p>
        </div>
      )}
    </div>
  );
};
