# JSON-LD Snippets — Alici “UGC Ads” Hub

These are *templates*. Replace placeholders and ensure all fields are truthful.

## 1) BreadcrumbList
```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Solutions",
      "item": "https://alici.ai/solutions/"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "UGC Ads",
      "item": "https://alici.ai/solutions/ugc-ads/"
    }
  ]
}
```

## 2) HowTo (3 steps)
```json
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to create UGC-style video ads with Alici",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Describe your product & offer",
      "text": "Add your product name, audience, key benefit, proof point, and call-to-action."
    },
    {
      "@type": "HowToStep",
      "name": "Choose a UGC format",
      "text": "Pick a format like product demo, testimonial, unboxing, before/after, or problem-solution."
    },
    {
      "@type": "HowToStep",
      "name": "Generate variants & export",
      "text": "Generate multiple hooks and angles and export versions for short-form platforms."
    }
  ]
}
```

## 3) FAQPage
```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What is a UGC ad?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "A UGC ad is a short-form video ad that looks and sounds like creator content, often using a simple demo, a personal story, or a testimonial-style script."
      }
    },
    {
      "@type": "Question",
      "name": "How do I make UGC ads with Alici?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Add your product brief, pick a UGC format, generate a script and shot list, then create multiple hook/angle variants for testing."
      }
    }
  ]
}
```

## 4) VideoObject (only if you have a real demo video URL)
```json
{
  "@context": "https://schema.org",
  "@type": "VideoObject",
  "name": "Alici UGC Ad Generator demo",
  "description": "Demo of generating a UGC-style ad script and shot list, then exporting short-form variants.",
  "thumbnailUrl": "https://alici.ai/static/ugc-ads-demo-thumb.jpg",
  "uploadDate": "2026-02-04",
  "contentUrl": "https://alici.ai/static/ugc-ads-demo.mp4",
  "embedUrl": "https://alici.ai/solutions/ugc-ads/"
}
```

## 5) SoftwareApplication (optional; keep minimal and accurate)
```json
{
  "@context": "https://schema.org",
  "@type": "SoftwareApplication",
  "name": "Alici",
  "applicationCategory": "BusinessApplication",
  "operatingSystem": "Web",
  "url": "https://alici.ai/"
}
```

