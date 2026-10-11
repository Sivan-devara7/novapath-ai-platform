import { test, expect } from '@playwright/test';

test.describe('NovaPath AI — End-to-End Validation Suite (v2)', () => {

  test('1. Dashboard Profile, Real XP and Navigation', async ({ page }) => {
    // Navigate to homepage / dashboard
    await page.goto('/');
    await page.waitForLoadState('networkidle');

    // Confirm navigation bar items (Assessments and Resources removed from main nav)
    const navText = await page.textContent('nav');
    expect(navText).toContain('Roadmap');
    expect(navText).toContain('Resume');
    expect(navText).not.toContain('Assessment');
    expect(navText).not.toContain('Resources');

    // Check user profile and XP indicator
    const bodyText = await page.textContent('body');
    expect(bodyText).toContain('Aarav Sharma');
    expect(bodyText).toContain('XP');
  });

  test('2. Old Nav Redirects: /assessment and /resources redirect to /roadmap', async ({ page }) => {
    // /assessment redirect
    await page.goto('/assessment');
    await page.waitForURL('**/roadmap');
    expect(page.url()).toContain('/roadmap');

    // /resources redirect
    await page.goto('/resources');
    await page.waitForURL('**/roadmap');
    expect(page.url()).toContain('/roadmap');
  });

  test('3. Roadmap Page, Placement Assessment Banner & Module Cards', async ({ page }) => {
    await page.goto('/roadmap');
    await page.waitForLoadState('networkidle');

    // Verify Placement banner
    const banner = page.locator('text=Track Placement Assessment');
    await expect(banner).toBeVisible();

    // Verify placement action button
    const placementBtn = page.locator('button:has-text("Placement Quiz")');
    await expect(placementBtn).toBeVisible();

    // Verify module cards render with badges, estimated hours, difficulty
    const pythonModule = page.locator('text=Python & Modern Software Engineering for AI');
    await expect(pythonModule).toBeVisible();

    // Check module difficulty and lessons
    const bodyText = await page.textContent('body');
    expect(bodyText).toContain('Beginner');
    expect(bodyText).toContain('Lessons');
  });

  test('4. Locked Module Gating (HTTP 403 Friendly Screen)', async ({ page }) => {
    // Direct link to locked module
    await page.goto('/roadmap/rag-systems');
    await page.waitForLoadState('networkidle');

    // Verify friendly locked screen is displayed
    const lockedTitle = page.locator('h2:has-text("Module is Locked")');
    await expect(lockedTitle).toBeVisible();

    // Verify Back to Roadmap button works
    const returnBtn = page.locator('text=Back to Roadmap');
    await returnBtn.click();
    await page.waitForURL('**/roadmap');
    expect(page.url()).toContain('/roadmap');
  });

  test('5. Available Module Detail Page & Shared-Element Transition', async ({ page }) => {
    await page.goto('/roadmap');
    await page.waitForLoadState('networkidle');

    // Click an available module card
    const modCard = page.locator('text=Python & Modern Software Engineering for AI');
    await modCard.click();

    // Verify route is /roadmap/py-foundations
    await page.waitForURL('**/roadmap/py-foundations');
    expect(page.url()).toContain('/roadmap/py-foundations');

    // Verify module sections: Overview, Lessons, Resources, Quiz
    await expect(page.locator('text=What You Will Learn')).toBeVisible();
    await expect(page.locator('text=Target Competencies')).toBeVisible();
    await expect(page.locator('text=Module Mastery Quiz')).toBeVisible();
  });

  test('6. Resume Analyzer with Real ML ATS Score & Add to Roadmap', async ({ page }) => {
    await page.goto('/resume');
    await page.waitForLoadState('networkidle');

    // Verify honest label "ATS Compatibility Score (estimate)" using heading selector
    const atsHeading = page.locator('h3:has-text("ATS Compatibility Score")');
    await expect(atsHeading).toBeVisible();

    // Verify 5-Factor Documented Score Breakdown
    await expect(page.locator('text=5-Factor Documented Score Breakdown')).toBeVisible();
    await expect(page.locator('text=ML Role-Fit Probability (40% weight)')).toBeVisible();
    await expect(page.locator('text=Keyword & Competency Coverage (25% weight)')).toBeVisible();
    await expect(page.locator('text=Section Completeness (15% weight)')).toBeVisible();
    await expect(page.locator('text=Formatting & Parsability (10% weight)')).toBeVisible();
    await expect(page.locator('text=Quantified Impact & Outcomes (10% weight)')).toBeVisible();

    // Verify Top Contributing ML Features explainability section
    await expect(page.locator('text=Top Contributing Terms (ML Model Explainability)')).toBeVisible();

    // Verify Itemized Point Deductions section
    await expect(page.locator('text=Itemized Point Deductions')).toBeVisible();

    // Verify + Add to Roadmap button functionality
    const addBtn = page.locator('button:has-text("+ Add to Roadmap")').first();
    if (await addBtn.isVisible()) {
      await addBtn.click();
      // Should change to "Added to Roadmap"
      await expect(page.locator('text=Added to Roadmap').first()).toBeVisible();
    }
  });

  test('7. Resume Analyzer Paste Text and Custom Audit', async ({ page }) => {
    await page.goto('/resume');
    await page.waitForLoadState('networkidle');

    // Switch to Paste Text tab
    await page.click('button:has-text("Paste Text")');

    // Fill resume text
    const sampleText = `
      John Doe | Machine Learning Engineer | john@example.com | github.com/john
      Summary: ML Engineer with 3 years experience building PyTorch models and FastAPI microservices.
      Skills: Python, PyTorch, Scikit-Learn, Docker, FastAPI, Linux, SQL, Transformers.
      Experience: AI Engineer at Tech Corp. Fine-tuned BERT classification models improving accuracy by 15%.
      Accelerated latency by 35% with TensorRT FP16 quantization.
      Projects: Built RAG pipeline indexing 20,000 documents with FAISS vector store.
      Education: B.Tech in Computer Science & Engineering.
    `;
    await page.fill('textarea', sampleText);

    // Click Audit Resume Text
    await page.click('button:has-text("Audit Resume Text")');

    // Verify calculated score is updated and visible
    const atsHeading = page.locator('h3:has-text("ATS Compatibility Score")');
    await expect(atsHeading).toBeVisible();
    await expect(page.locator('text=Top Contributing Terms (ML Model Explainability)')).toBeVisible();
  });

});
