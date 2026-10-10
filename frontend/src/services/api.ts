import {
  UserProfile,
  SkillGraphResponse,
  ResourceItem,
  AssessmentQuestion,
  AssessmentFeedback,
  ResumeAnalysisResponse,
  RecommendationItem
} from '../types';

const API_BASE = '/api';

export const api = {
  // Auth
  async login(): Promise<{ user: UserProfile; access_token: string }> {
    try {
      const res = await fetch(`${API_BASE}/auth/demo-login`, { method: 'POST' });
      if (!res.ok) throw new Error('API request failed');
      return await res.json();
    } catch {
      return {
        access_token: 'mock-jwt-token-fallback',
        user: {
          id: 'usr-aarav-sharma',
          name: 'Aarav Sharma',
          email: 'aarav.sharma@vizag.edu',
          role: 'student',
          career_goal: 'AI Engineer',
          avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
          streak: 14,
          points: 860,
          mastery_overall: 72,
          radar_data: [
            { subject: 'Deep Learning', A: 85, fullMark: 100 },
            { subject: 'System Design', A: 65, fullMark: 100 },
            { subject: 'Algorithms', A: 90, fullMark: 100 },
            { subject: 'MLOps', A: 55, fullMark: 100 },
            { subject: 'Cloud & Infra', A: 70, fullMark: 100 },
            { subject: 'Applied RAG', A: 68, fullMark: 100 },
          ],
          verified_skills: ['Python', 'PyTorch', 'Linear Algebra', 'Git', 'Docker']
        }
      };
    }
  },

  // Roadmap & Skill Graph
  async getRoadmap(careerGoal = 'AI Engineer'): Promise<SkillGraphResponse> {
    try {
      const res = await fetch(`${API_BASE}/roadmap/graph?career_goal=${encodeURIComponent(careerGoal)}`);
      if (!res.ok) throw new Error('Failed to fetch roadmap');
      return await res.json();
    } catch {
      return {
        career_goal: careerGoal,
        completion_rate: 66,
        nodes: [
          {
            id: 'py-foundations',
            name: 'Python & Algorithmic Foundations',
            category: 'Core CS',
            prerequisites: [],
            mastery_level: 92,
            status: 'completed',
            verified_via: 'Resume & GitHub Verification',
            icon: 'Code2',
            estimated_hours: 20,
            milestone_project: 'High-throughput Async Data Pipeline'
          },
          {
            id: 'math-linear-algebra',
            name: 'Linear Algebra & Tensor Calculus',
            category: 'Foundations',
            prerequisites: ['py-foundations'],
            mastery_level: 85,
            status: 'completed',
            verified_via: 'Academic Marksheet OCR',
            icon: 'Binary',
            estimated_hours: 25,
            milestone_project: 'Custom Matrix Eigen-decomposition Engine'
          },
          {
            id: 'pytorch-deep-learning',
            name: 'PyTorch & Deep Neural Networks',
            category: 'Deep Learning',
            prerequisites: ['math-linear-algebra'],
            mastery_level: 74,
            status: 'in_progress',
            verified_via: 'In Progress (Module 3/5)',
            icon: 'Brain',
            estimated_hours: 35,
            milestone_project: 'Vision Transformer (ViT) Classifier from Scratch'
          },
          {
            id: 'transformers-nlp',
            name: 'Transformers & Attention Architectures',
            category: 'GenAI',
            prerequisites: ['pytorch-deep-learning'],
            mastery_level: 40,
            status: 'ready',
            verified_via: null,
            icon: 'Sparkles',
            estimated_hours: 30,
            milestone_project: 'Fine-Tuned LLaMA-3 with QLoRA on Domain Corpus'
          },
          {
            id: 'rag-vector-db',
            name: 'RAG Systems & Vector Databases',
            category: 'Applied AI',
            prerequisites: ['transformers-nlp'],
            mastery_level: 0,
            status: 'locked',
            verified_via: null,
            icon: 'Database',
            estimated_hours: 25,
            milestone_project: 'Production Multi-Tenant Hybrid RAG with Re-ranking'
          },
          {
            id: 'mlops-deployment',
            name: 'MLOps, TensorRT & Model Serving',
            category: 'Production',
            prerequisites: ['rag-vector-db'],
            mastery_level: 0,
            status: 'locked',
            verified_via: null,
            icon: 'Cpu',
            estimated_hours: 30,
            milestone_project: 'Kubernetes-Orchestrated Triton Inference Cluster'
          }
        ],
        edges: [
          { source: 'py-foundations', target: 'math-linear-algebra' },
          { source: 'math-linear-algebra', target: 'pytorch-deep-learning' },
          { source: 'pytorch-deep-learning', target: 'transformers-nlp' },
          { source: 'transformers-nlp', target: 'rag-vector-db' },
          { source: 'rag-vector-db', target: 'mlops-deployment' }
        ]
      };
    }
  },

  // Resources
  async getResources(skillId = 'all', query = '', type = 'all'): Promise<ResourceItem[]> {
    try {
      const url = skillId === 'all'
        ? `${API_BASE}/resources/?q=${encodeURIComponent(query)}&type=${encodeURIComponent(type)}`
        : `${API_BASE}/resources/${skillId}?q=${encodeURIComponent(query)}&type=${encodeURIComponent(type)}`;
      const res = await fetch(url);
      if (!res.ok) throw new Error('Failed to fetch resources');
      return await res.json();
    } catch {
      return [
        {
          id: 'res-py-1',
          skill_id: 'python',
          title: 'Python for High-Performance Scientific Computing & ML',
          type: 'video',
          url: 'https://www.youtube.com/watch?v=rfscVS0vtbw',
          provider: 'Stanford Online',
          estimated_time: '2h 45m',
          difficulty: 'Intermediate',
          summary: 'Covers vectorized operations with NumPy, memory layout, GIL internals, and asynchronous concurrency patterns.',
          grounding_reason: 'Directly reinforces foundational algorithmic data structures required for PyTorch tensor manipulation.',
          rating: 4.9,
          match_score: 98
        },
        {
          id: 'res-pytorch-1',
          skill_id: 'pytorch',
          title: 'Deep Learning with PyTorch: From Tensors to Neural Nets',
          type: 'interactive',
          url: 'https://pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html',
          provider: 'PyTorch Official Blitz',
          estimated_time: '3h 30m',
          difficulty: 'Intermediate',
          summary: 'Hands-on autograd execution, custom Module layers, backpropagation mathematics, and CUDA GPU acceleration.',
          grounding_reason: 'Essential prerequisite for Deep Learning and LLM fine-tuning milestones on your AI Engineer path.',
          rating: 5.0,
          match_score: 99
        },
        {
          id: 'res-transformers-1',
          skill_id: 'transformers',
          title: 'Hugging Face Transformers: Audio, Vision & NLP Mastery',
          type: 'course',
          url: 'https://huggingface.co/learn/nlp-course',
          provider: 'Hugging Face Academy',
          estimated_time: '8h 00m',
          difficulty: 'Intermediate',
          summary: 'Tokenizer internals, pipeline abstraction, attention mechanisms, LoRA / QLoRA parameter-efficient fine-tuning.',
          grounding_reason: 'Core requirement for modern generative AI applications and career goal: AI Engineer.',
          rating: 4.9,
          match_score: 99
        }
      ];
    }
  },

  // Assessment
  async getQuestions(skillId = 'pytorch'): Promise<AssessmentQuestion[]> {
    try {
      const res = await fetch(`${API_BASE}/assessment/${skillId}/questions`);
      if (!res.ok) throw new Error('Failed to fetch questions');
      return await res.json();
    } catch {
      return [
        {
          id: 'q-torch-e1',
          skill_id: 'pytorch',
          difficulty: 'Easy',
          question: 'What is the primary role of tensor.backward() in PyTorch?',
          code_snippet: 'loss = criterion(output, target)\nloss.backward()\noptimizer.step()',
          options: [
            'It automatically calculates and accumulates the gradients of the loss with respect to graph leaves',
            'It zeroes out the gradients stored in model parameters',
            'It updates parameter weights using the configured learning rate',
            'It moves the tensor memory from CPU RAM to GPU VRAM'
          ],
          type: 'multiple_choice',
          hint: 'Think about what needs to happen before optimizer.step() updates weights.'
        },
        {
          id: 'q-torch-m1',
          skill_id: 'pytorch',
          difficulty: 'Medium',
          question: 'Why must you invoke optimizer.zero_grad() before computing gradients in a training iteration?',
          code_snippet: 'for x, y in dataloader:\n    optimizer.zero_grad() # Why is this essential?\n    out = model(x)\n    loss = criterion(out, y)\n    loss.backward()',
          options: [
            'PyTorch default behavior accumulates gradients on successive backward passes instead of overwriting them',
            'To release GPU VRAM occupied by the activation caches from forward pass',
            'To reset the models dropout layers and batch normalization running statistics',
            'It compiles the graph into a TorchScript C++ execution plan'
          ],
          type: 'multiple_choice',
          hint: 'Consider what happens if multiple backward() calls occur without clearing buffers.'
        }
      ];
    }
  },

  async submitAnswer(skillId: string, questionId: string, selectedIndex: number, consecutive: number): Promise<AssessmentFeedback> {
    try {
      const res = await fetch(`${API_BASE}/assessment/${skillId}/submit`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question_id: questionId,
          selected_option_index: selectedIndex,
          consecutive_correct: consecutive
        })
      });
      if (!res.ok) throw new Error('Failed to submit');
      return await res.json();
    } catch {
      const isCorrect = selectedIndex === 0;
      return {
        is_correct: isCorrect,
        correct_option_index: 0,
        explanation: 'PyTorch autograd builds a directed acyclic computational graph during the forward pass and evaluates vector-Jacobian products in reverse.',
        grounded_source: 'PyTorch Official Autograd Blitz & Documentation',
        new_difficulty: isCorrect ? 'Medium' : 'Easy',
        points_earned: isCorrect ? 50 : 10,
        current_score: isCorrect ? 50 : 10
      };
    }
  },

  // Resume Intelligence
  async analyzeResume(text?: string, targetRole = 'AI Engineer'): Promise<ResumeAnalysisResponse> {
    try {
      if (text) {
        const res = await fetch(`${API_BASE}/resume/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ resume_text: text, target_role: targetRole })
        });
        if (!res.ok) throw new Error('Analysis failed');
        return await res.json();
      } else {
        const res = await fetch(`${API_BASE}/resume/sample-analysis?target_role=${encodeURIComponent(targetRole)}`);
        if (!res.ok) throw new Error('Analysis failed');
        return await res.json();
      }
    } catch {
      return {
        ats_score: 84,
        formatting_score: 92,
        skills_match_score: 82,
        impact_score: 78,
        extracted_skills: ['Python', 'PyTorch', 'C++', 'FastAPI', 'Docker', 'Git', 'Linux', 'Transformers', 'CUDA'],
        missing_skills: ['Vector Database', 'RAG Architecture', 'Kubernetes'],
        matched_skills: ['Python', 'PyTorch', 'FastAPI', 'Docker', 'Transformers', 'CUDA'],
        action_verb_count: 9,
        quantifiable_metrics_count: 6,
        summary_critique: "Your resume shows a strong technical foundation for 'AI Engineer' with high-impact quantifiable bullet points (e.g. 45% latency improvement). Incorporating RAG architectures and Vector DB keywords will push you past the 90th percentile.",
        actionable_recommendations: [
          {
            category: 'Skill Gap',
            priority: 'High',
            title: 'Add proof of competency in Vector Databases & RAG',
            description: 'Recruiter search filters for AI Engineer prioritize candidates with demonstrated experience in embeddings and hybrid retrieval.'
          },
          {
            category: 'Action Verbs',
            priority: 'Medium',
            title: 'Expand MLOps orchestration phrasing',
            description: 'Use targeted production verbs like "benchmarked", "orchestrated", and "containerized".'
          }
        ]
      };
    }
  },

  // Recommendations
  async getRecommendations(): Promise<RecommendationItem[]> {
    try {
      const res = await fetch(`${API_BASE}/recommendations/`);
      if (!res.ok) throw new Error('Failed to fetch recommendations');
      return await res.json();
    } catch {
      return [
        {
          id: 'rec-proj-1',
          type: 'project',
          title: 'Production Hybrid RAG with Cross-Encoder Re-Ranking',
          organization: 'Open Source AI Labs',
          difficulty: 'Advanced',
          duration: '3 Weeks (Est. 25h)',
          match_percentage: 98,
          why_this_matches: "Addresses the critical missing keyword 'Vector Database & RAG' detected in your resume ATS audit. Recruiters specifically seek portfolio proof of real-world chunking and re-ranking.",
          prerequisites: ['PyTorch', 'Python', 'Transformers'],
          tags: ['Vector DB', 'FAISS', 'LlamaIndex', 'FastAPI'],
          action_url: '/roadmap'
        },
        {
          id: 'rec-cert-1',
          type: 'certification',
          title: 'AWS Certified Machine Learning - Specialty',
          organization: 'Amazon Web Services',
          difficulty: 'Intermediate',
          duration: '6 Weeks Study Path',
          match_percentage: 92,
          why_this_matches: 'Reinforces your cloud infrastructure verification badge and increases ATS recruiter search filtering by 3.2x.',
          prerequisites: ['Python', 'Cloud Fundamentals'],
          tags: ['Cloud AI', 'SageMaker', 'Feature Store', 'Security'],
          action_url: 'https://aws.amazon.com/certification/certified-machine-learning-specialty/'
        },
        {
          id: 'rec-intern-1',
          type: 'internship',
          title: 'Applied AI Research Intern (Fall 2026)',
          organization: 'Anthropic / Cohere Campus Lab',
          difficulty: 'High Impact',
          duration: '6 Months',
          match_percentage: 91,
          why_this_matches: 'Your 85/100 Deep Learning score and PyTorch project portfolio meet 92% of candidate baseline qualifications.',
          prerequisites: ['PyTorch', 'Transformer Architecture', 'Git'],
          tags: ['Research', 'Inference Optimization', 'CUDA'],
          action_url: '#'
        }
      ];
    }
  }
};
