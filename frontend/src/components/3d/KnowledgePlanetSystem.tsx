import React, { useEffect, useRef, useState } from 'react';
import * as THREE from 'three';
import { CourseModule } from '../../types';
import { Award, Sparkles, CheckCircle2, Lock, Zap, Eye } from 'lucide-react';

interface KnowledgePlanetSystemProps {
  modules: CourseModule[];
  overallMastery?: number;
  streak?: number;
  onSelectModule?: (mod: CourseModule) => void;
}

interface PlanetNode {
  id: string;
  name: string;
  order: number;
  status: 'passed' | 'in_progress' | 'available' | 'locked';
  score: number;
  radius: number;
  distance: number;
  speed: number;
  baseColor: number;
  emissiveColor: number;
  ringColor: number;
  angle: number;
  modRef?: CourseModule;
}

export const KnowledgePlanetSystem: React.FC<KnowledgePlanetSystemProps> = ({
  modules,
  overallMastery = 72,
  streak = 14,
  onSelectModule
}) => {
  const mountRef = useRef<HTMLDivElement>(null);
  const [hoveredPlanet, setHoveredPlanet] = useState<PlanetNode | null>(null);
  const [activeTier, setActiveTier] = useState<string>('Intermediate');

  // Determine core star color and tier from mastery
  const getCoreStarDetails = (mastery: number) => {
    if (mastery >= 85) {
      return {
        color: 0x38bdf8, // Radiant Cyan Celestial
        emissive: 0x0284c7,
        tier: 'Master Architect',
        haloColor: 0x0ea5e9,
        coreName: 'Cosmic Core of Mastery'
      };
    } else if (mastery >= 65) {
      return {
        color: 0x818cf8, // Indigo / Sapphire Luminary
        emissive: 0x4f46e5,
        tier: 'Advanced Practitioner',
        haloColor: 0x6366f1,
        coreName: 'Sapphire Core of Knowledge'
      };
    } else if (mastery >= 40) {
      return {
        color: 0xa855f7, // Radiant Violet
        emissive: 0x7e22ce,
        tier: 'Intermediate Explorer',
        haloColor: 0x9333ea,
        coreName: 'Violet Core of Progress'
      };
    } else {
      return {
        color: 0xf59e0b, // Warm Amber / Copper
        emissive: 0xd97706,
        tier: 'Foundation Initiate',
        haloColor: 0xf59e0b,
        coreName: 'Solar Core of Fundamentals'
      };
    }
  };

  const coreDetails = getCoreStarDetails(overallMastery);

  useEffect(() => {
    setActiveTier(coreDetails.tier);
  }, [overallMastery]);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 600;
    const height = container.clientHeight || 420;

    // 1. Three.js Scene Setup
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 1000);
    camera.position.set(0, 16, 26);
    camera.lookAt(0, 0, 0);

    const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    renderer.toneMapping = THREE.ACESFilmicToneMapping;
    renderer.toneMappingExposure = 1.2;
    container.innerHTML = '';
    container.appendChild(renderer.domElement);

    // 2. Lighting Setup
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.7);
    scene.add(ambientLight);

    const centralLight = new THREE.PointLight(coreDetails.color, 4.5, 45);
    centralLight.position.set(0, 0, 0);
    scene.add(centralLight);

    const rimLight = new THREE.DirectionalLight(0xffffff, 1.0);
    rimLight.position.set(15, 20, 15);
    scene.add(rimLight);

    // 3. Central Core Planet
    const coreRadius = 2.4;
    const coreGeo = new THREE.SphereGeometry(coreRadius, 32, 32);
    const coreMat = new THREE.MeshStandardMaterial({
      color: coreDetails.color,
      emissive: coreDetails.emissive,
      emissiveIntensity: 0.9,
      roughness: 0.2,
      metalness: 0.3
    });
    const coreMesh = new THREE.Mesh(coreGeo, coreMat);
    scene.add(coreMesh);

    // Core Pulsing Halo
    const haloGeo = new THREE.RingGeometry(coreRadius * 1.15, coreRadius * 1.45, 64);
    const haloMat = new THREE.MeshBasicMaterial({
      color: coreDetails.haloColor,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.38
    });
    const haloMesh = new THREE.Mesh(haloGeo, haloMat);
    haloMesh.rotation.x = Math.PI / 2;
    scene.add(haloMesh);

    // Atmospheric Particle Dust around Core
    const particleCount = 450;
    const particleGeo = new THREE.BufferGeometry();
    const particlePos = new Float32Array(particleCount * 3);
    for (let i = 0; i < particleCount; i++) {
      const radius = 3.5 + Math.random() * 12;
      const angle = Math.random() * Math.PI * 2;
      const y = (Math.random() - 0.5) * 3;
      particlePos[i * 3] = Math.cos(angle) * radius;
      particlePos[i * 3 + 1] = y;
      particlePos[i * 3 + 2] = Math.sin(angle) * radius;
    }
    particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePos, 3));
    const particleMat = new THREE.PointsMaterial({
      color: 0x93c5fd,
      size: 0.12,
      transparent: true,
      opacity: 0.6
    });
    const particleSystem = new THREE.Points(particleGeo, particleMat);
    scene.add(particleSystem);

    // 4. Build Orbiting Planetary Nodes from real module analytics
    const planetsList: {
      mesh: THREE.Mesh;
      ringMesh: THREE.Line;
      nodeData: PlanetNode;
    }[] = [];

    // Fallback module definitions if empty
    const sourceModules = modules.length > 0 ? modules : [
      { id: 'py-foundations', title: 'Python Foundations', status: 'passed', best_score: 14, order_index: 1 },
      { id: 'math-tensors', title: 'Linear Algebra & Tensors', status: 'passed', best_score: 12, order_index: 2 },
      { id: 'pytorch-deep-learning', title: 'PyTorch Deep Learning', status: 'in_progress', best_score: 8, order_index: 3 },
      { id: 'transformers-nlp', title: 'Transformers & GenAI', status: 'available', best_score: 0, order_index: 4 },
      { id: 'vector-rag', title: 'Vector DB & Hybrid RAG', status: 'locked', best_score: 0, order_index: 5 },
      { id: 'mlops-production', title: 'MLOps & Inference', status: 'locked', best_score: 0, order_index: 6 },
    ];

    sourceModules.slice(0, 6).forEach((mod, idx) => {
      const dist = 5.2 + idx * 2.3;
      const speed = 0.008 / (1 + idx * 0.35);
      const angle = (idx / 6) * Math.PI * 2;

      let baseColor = 0x475569;
      let emissiveColor = 0x1e293b;
      let ringColor = 0x334155;
      let pRadius = 0.75 + (idx % 3) * 0.15;

      const modStatus = mod.status as 'passed' | 'in_progress' | 'available' | 'locked';

      // Dynamic Color Upgrades based on learning analytics!
      if (modStatus === 'passed') {
        // UPGRADED TIER: Radiant Emerald / Cyan with luminous golden ring
        baseColor = 0x10b981;
        emissiveColor = 0x059669;
        ringColor = 0x34d399;
        pRadius += 0.2;
      } else if (modStatus === 'in_progress') {
        // ACTIVE TIER: Electric Violet / Magenta aura
        baseColor = 0xa855f7;
        emissiveColor = 0x7e22ce;
        ringColor = 0xc084fc;
        pRadius += 0.1;
      } else if (modStatus === 'available') {
        // AVAILABLE TIER: Sky Blue
        baseColor = 0x38bdf8;
        emissiveColor = 0x0284c7;
        ringColor = 0x7dd3fc;
      } else {
        // LOCKED TIER: Dim Slate
        baseColor = 0x475569;
        emissiveColor = 0x1e293b;
        ringColor = 0x334155;
      }

      // Orbital Ring Path
      const ringSegments = 90;
      const ringPoints: THREE.Vector3[] = [];
      for (let j = 0; j <= ringSegments; j++) {
        const theta = (j / ringSegments) * Math.PI * 2;
        ringPoints.push(new THREE.Vector3(Math.cos(theta) * dist, 0, Math.sin(theta) * dist));
      }
      const ringGeo = new THREE.BufferGeometry().setFromPoints(ringPoints);
      const ringMat = new THREE.LineBasicMaterial({
        color: ringColor,
        transparent: true,
        opacity: modStatus === 'passed' ? 0.65 : modStatus === 'in_progress' ? 0.5 : 0.2
      });
      const orbitRing = new THREE.Line(ringGeo, ringMat);
      scene.add(orbitRing);

      // Planet Sphere Mesh
      const pGeo = new THREE.SphereGeometry(pRadius, 24, 24);
      const pMat = new THREE.MeshStandardMaterial({
        color: baseColor,
        emissive: emissiveColor,
        emissiveIntensity: modStatus === 'passed' ? 0.8 : modStatus === 'in_progress' ? 0.6 : 0.2,
        roughness: 0.3,
        metalness: 0.2
      });
      const pMesh = new THREE.Mesh(pGeo, pMat);
      pMesh.position.set(Math.cos(angle) * dist, 0, Math.sin(angle) * dist);

      // If passed or in_progress, add a decorative planetary ring
      if (modStatus === 'passed' || modStatus === 'in_progress') {
        const satRingGeo = new THREE.RingGeometry(pRadius * 1.3, pRadius * 1.65, 32);
        const satRingMat = new THREE.MeshBasicMaterial({
          color: baseColor,
          side: THREE.DoubleSide,
          transparent: true,
          opacity: 0.5
        });
        const satRing = new THREE.Mesh(satRingGeo, satRingMat);
        satRing.rotation.x = Math.PI / 3;
        pMesh.add(satRing);
      }

      const nodeData: PlanetNode = {
        id: mod.id,
        name: mod.title,
        order: (mod as any).order_index || idx + 1,
        status: modStatus,
        score: (mod as any).best_score || 0,
        radius: pRadius,
        distance: dist,
        speed,
        baseColor,
        emissiveColor,
        ringColor,
        angle,
        modRef: mod as CourseModule
      };

      pMesh.userData = { nodeData };
      scene.add(pMesh);

      planetsList.push({
        mesh: pMesh,
        ringMesh: orbitRing,
        nodeData
      });
    });

    // 5. Mouse Raycasting for Interactive Inspection
    const raycaster = new THREE.Raycaster();
    const mouse = new THREE.Vector2(-999, -999);

    const onMouseMove = (event: MouseEvent) => {
      const rect = renderer.domElement.getBoundingClientRect();
      mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
      mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    };

    const onClick = () => {
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(planetsList.map(p => p.mesh));
      if (intersects.length > 0) {
        const clicked = intersects[0].object.userData.nodeData as PlanetNode;
        if (clicked && clicked.modRef && onSelectModule) {
          onSelectModule(clicked.modRef);
        }
      }
    };

    container.addEventListener('mousemove', onMouseMove);
    container.addEventListener('click', onClick);

    // 6. Animation Loop
    let animationFrameId: number;
    let clock = new THREE.Clock();

    const animate = () => {
      animationFrameId = requestAnimationFrame(animate);
      const delta = clock.getDelta();

      // Core rotation
      coreMesh.rotation.y += delta * 0.35;
      haloMesh.rotation.z += delta * 0.15;
      particleSystem.rotation.y += delta * 0.05;

      // Orbit planets
      planetsList.forEach((item) => {
        item.nodeData.angle += item.nodeData.speed;
        item.mesh.position.x = Math.cos(item.nodeData.angle) * item.nodeData.distance;
        item.mesh.position.z = Math.sin(item.nodeData.angle) * item.nodeData.distance;
        item.mesh.rotation.y += delta * 0.6;
      });

      // Raycasting check
      raycaster.setFromCamera(mouse, camera);
      const intersects = raycaster.intersectObjects(planetsList.map(p => p.mesh));
      if (intersects.length > 0) {
        const hovered = intersects[0].object.userData.nodeData as PlanetNode;
        setHoveredPlanet(hovered);
        renderer.domElement.style.cursor = 'pointer';
      } else {
        setHoveredPlanet(null);
        renderer.domElement.style.cursor = 'default';
      }

      renderer.render(scene, camera);
    };

    animate();

    // Resize Handler
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
      window.removeEventListener('resize', handleResize);
      container.removeEventListener('mousemove', onMouseMove);
      container.removeEventListener('click', onClick);
      renderer.dispose();
      if (container.contains(renderer.domElement)) {
        container.removeChild(renderer.domElement);
      }
    };
  }, [modules, overallMastery]);

  return (
    <div className="relative w-full h-[460px] rounded-3xl overflow-hidden border border-white/[0.08] bg-slate-950/80 backdrop-blur-xl shadow-2xl flex flex-col justify-between">
      {/* Top Overlay: Level Rank & System Status */}
      <div className="relative z-10 flex items-center justify-between p-5 border-b border-white/[0.06] bg-slate-900/50 backdrop-blur-md">
        <div>
          <div className="flex items-center gap-2">
            <span className="flex h-2 w-2 rounded-full bg-sky-400 animate-ping" />
            <span className="text-xs font-bold uppercase tracking-wider text-sky-400">
              Live Knowledge Solar System
            </span>
          </div>
          <h3 className="text-lg font-black text-white mt-0.5">
            {coreDetails.coreName}
          </h3>
        </div>

        <div className="flex items-center gap-2">
          <div className="rounded-xl border border-sky-400/30 bg-sky-500/10 px-3 py-1 text-right">
            <span className="text-[10px] text-slate-400 block uppercase font-bold">Current Tier</span>
            <span className="text-xs font-extrabold text-sky-300">{activeTier}</span>
          </div>
          <div className="rounded-xl border border-emerald-400/30 bg-emerald-500/10 px-3 py-1 text-right">
            <span className="text-[10px] text-slate-400 block uppercase font-bold">Overall Mastery</span>
            <span className="text-xs font-extrabold text-emerald-300">{overallMastery}%</span>
          </div>
        </div>
      </div>

      {/* 3D WebGL Canvas Container */}
      <div ref={mountRef} className="relative w-full flex-1" />

      {/* Interactive Holographic Tooltip on Hover */}
      {hoveredPlanet && (
        <div className="absolute top-20 left-6 z-20 max-w-xs rounded-2xl border border-white/20 bg-slate-900/90 p-4 backdrop-blur-xl shadow-2xl pointer-events-none transition-all">
          <div className="flex items-center justify-between">
            <span className="text-[10px] font-bold uppercase tracking-wider text-sky-400">
              Planetary Module #{hoveredPlanet.order}
            </span>
            <span
              className={`rounded-full px-2 py-0.5 text-[10px] font-bold uppercase ${
                hoveredPlanet.status === 'passed'
                  ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                  : hoveredPlanet.status === 'in_progress'
                  ? 'bg-violet-500/20 text-violet-300 border border-violet-500/30'
                  : hoveredPlanet.status === 'available'
                  ? 'bg-sky-500/20 text-sky-300 border border-sky-500/30'
                  : 'bg-slate-800 text-slate-400 border border-slate-700'
              }`}
            >
              {hoveredPlanet.status.replace('_', ' ')}
            </span>
          </div>

          <h4 className="mt-1 text-sm font-bold text-white">{hoveredPlanet.name}</h4>

          <div className="mt-3 flex items-center justify-between border-t border-white/[0.08] pt-2 text-xs text-slate-300">
            <span>Validated Score:</span>
            <span className="font-bold text-white">
              {hoveredPlanet.score > 0 ? `${hoveredPlanet.score}/15 Questions` : 'Not cleared yet'}
            </span>
          </div>

          <p className="mt-2 text-[11px] text-slate-400">
            {hoveredPlanet.status === 'passed'
              ? '✨ Upgraded to radiant celestial emerald! Fully verified competency.'
              : hoveredPlanet.status === 'in_progress'
              ? '⚡ Active orbital trajectory. Clear the module quiz to upgrade color!'
              : hoveredPlanet.status === 'available'
              ? 'Ready to begin lesson curriculum.'
              : 'Locked. Pass previous module with >= 65% score to unlock.'}
          </p>
        </div>
      )}

      {/* Bottom Color Upgrade Legend */}
      <div className="relative z-10 flex flex-wrap items-center justify-between gap-3 p-4 border-t border-white/[0.06] bg-slate-900/60 backdrop-blur-md text-[11px]">
        <div className="flex items-center gap-4">
          <span className="text-slate-400 font-semibold">Color Progression:</span>
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-slate-500" />
            <span className="text-slate-400">Locked</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-sky-400" />
            <span className="text-sky-300">Available</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-violet-400 animate-pulse" />
            <span className="text-violet-300">In Progress</span>
          </div>
          <div className="flex items-center gap-1.5">
            <span className="h-2.5 w-2.5 rounded-full bg-emerald-400 shadow-[0_0_8px_rgba(16,185,129,0.8)]" />
            <span className="text-emerald-300 font-bold">Mastered (Upgraded)</span>
          </div>
        </div>

        <span className="text-slate-400 hidden sm:inline">
          💡 Click any orbiting planet to open its lesson curriculum
        </span>
      </div>
    </div>
  );
};

export default KnowledgePlanetSystem;
