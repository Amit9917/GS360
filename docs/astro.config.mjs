import { defineConfig } from "astro/config";
import starlight from "@astrojs/starlight";

export default defineConfig({
  site: "https://jina-code-systems.github.io",
  base: "/GS360",
  integrations: [
    starlight({
      title: "GS360 Docs",
      description:
        "The open-source, AI-powered UPSC Command Center — documentation for developers and contributors.",
      social: [
        {
          icon: "github",
          label: "GitHub",
          href: "https://github.com/JINA-CODE-SYSTEMS/GS360",
        },
      ],
      sidebar: [
        {
          label: "Getting Started",
          items: [
            { label: "Introduction", slug: "getting-started/introduction" },
            { label: "Quickstart", slug: "getting-started/quickstart" },
            { label: "Configuration", slug: "getting-started/configuration" },
          ],
        },
        {
          label: "Architecture",
          items: [
            { label: "Overview", slug: "architecture/overview" },
            { label: "API Reference", slug: "architecture/api-reference" },
          ],
        },
        {
          label: "Content Packs",
          items: [
            { label: "Content Guide", slug: "content-packs/guide" },
          ],
        },
        {
          label: "Contributing",
          items: [
            {
              label: "Contribution Guide",
              slug: "contributing/guide",
            },
          ],
        },
      ],
    }),
  ],
});
