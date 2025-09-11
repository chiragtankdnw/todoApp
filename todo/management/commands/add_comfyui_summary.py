from django.core.management.base import BaseCommand
from datetime import date
from todo.models import BlogPostSummary


class Command(BaseCommand):
    help = 'Add the ComfyUI blog post summary from the issue'

    def handle(self, *args, **options):
        # Check if the blog post already exists
        if BlogPostSummary.objects.filter(
            url='https://hoangyell.com/fulfill-your-dirty-fantasies-with-comfy-ui/'
        ).exists():
            self.stdout.write(
                self.style.WARNING('ComfyUI blog post summary already exists')
            )
            return

        # Create the blog post summary
        blog_post = BlogPostSummary.objects.create(
            title='Fulfill your dirty fantasies with Comfy UI',
            url='https://hoangyell.com/fulfill-your-dirty-fantasies-with-comfy-ui/',
            date_published=date(2025, 5, 27),
            summary='''High-level summary (tech-focused):
- Overview of ComfyUI as a flexible, modular local text-to-image client, compared with A1111 and Forge.
- Hardware guidance: NVIDIA GPU (8–16GB+ VRAM recommended), 16–32GB RAM, SSD space for models and outputs.
- Quick-start setup: cloning ComfyUI, installing dependencies, and optional manager nodes.
- Model choices: SD 1.5, SDXL 1.0, SD 3.5 Large, and Flux.1-dev; guidance on picking checkpoints and verifying model files.
- Prompting basics and productivity hotkeys within ComfyUI.
- Advanced topics: using LoRAs and recommended resources; general tips for improving quality.

Note: The original article's theme includes adult-oriented phrasing, but this summary only focuses on the technical setup and usage of ComfyUI.''',
            tags='ComfyUI, AI, text-to-image, stable-diffusion, machine-learning',
            location_timezone='Asia/Kuala_Lumpur'
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully added blog post summary: {blog_post.title}')
        )