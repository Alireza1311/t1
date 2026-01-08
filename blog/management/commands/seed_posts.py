import os
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from blog.models import Post

SEED_POSTS = [
    {
        "title": "Date Masamune on Horseback: The Spirit of Sendai",
        "slug": "date-masamune-sendai-statue",
        "country": "Japan",
        "city_or_region": "Sendai, Miyagi",
        "image_filename": "date-masamune-sendai.jpg",
        "short_description": "A mounted statue can feel like a city’s signature. In Sendai, the figure of Date Masamune stands as a reminder of strategy, ambition, and local identity—one silhouette that carries centuries of memory.",
        "full_description": "## Overview\nFrom a distance, the statue reads like a postcard: a rider against open sky. Up close, it feels like a statement—less decoration, more presence. Date Masamune is remembered as a powerful daimyo associated with Sendai’s rise, and the monument works because it communicates authority instantly.\n\n## What You’re Looking At\nA mounted warrior in a commanding pose. The elevated placement is part of the design: it turns the horizon into a stage and the city into context.\n\n## Historical Context\nFeudal Japan was shaped by alliances, rivalries, and rapid shifts in power. Figures like Masamune are remembered not only for battles but for governance, patronage, and the branding of a region.\n\n## Why It Matters Today\nEven if you don’t know the full biography, the statue acts as a landmark of identity. People use it as a meeting point, a viewpoint, and a symbol—heritage that still participates in daily life.\n\n## Visitor Notes\n- Best light is late afternoon for longer shadows.\n- Step back and include the skyline in your frame: the view is part of the story.\n",
    },
    {
        "title": "Hampi: Ruins That Stretch Into a Landscape",
        "slug": "hampi-ruins-karnataka",
        "country": "India",
        "city_or_region": "Karnataka",
        "image_filename": "hampi-ruins-karnataka.jpg",
        "short_description": "Hampi isn’t one ruin—it’s a whole world of stone. Temples, fragments, and pathways scatter across a dramatic landscape, hinting at a capital that once pulsed with ritual, trade, and royal ambition.",
        "full_description": "## Overview\nSome historic places are compact. Hampi is expansive—monuments spread across a terrain of boulders and open sky. The scale changes how you read the past: not as a single building, but as a living system of routes, thresholds, and gathering spaces.\n\n## What You’re Looking At\nWeathered stone structures with textures that record time: worn steps, cracked blocks, softened edges. These details turn ruins into evidence of real use.\n\n## Historical Context\nHampi is associated with the Vijayanagara era and a rich cultural landscape that blended religion, commerce, and state power. Even when structures are broken, the planning remains visible.\n\n## How to Explore a Ruined City\n- Look for paths and alignments: where people moved matters.\n- Notice entrances and courtyards: they reveal social rhythm.\n- Pause at water features if present: they often anchored daily life.\n\n## Why It Stays With You\nHampi’s impact is spatial. You feel distance and time at once—heritage experienced through walking.\n",
    },
    {
        "title": "Teotihuacan in Miniature: A City Explained by a Model",
        "slug": "teotihuacan-model-mexico-city-museum",
        "country": "Mexico",
        "city_or_region": "Mexico City",
        "image_filename": "teotihuacan-model-mna.jpg",
        "short_description": "Inside a museum, a miniature version of Teotihuacan turns overwhelming scale into clarity. A model can be a map for the imagination—helping you understand layout, power, and urban design at a glance.",
        "full_description": "## Overview\nTeotihuacan is one of the most iconic ancient cities in the Americas. But scale can be hard to grasp on-site. A museum model does something powerful: it makes the city readable.\n\n## What You’re Looking At\nA detailed museum reproduction showing major structures and the city’s overall plan. Viewed from above, it becomes geometry—avenues, plazas, and pyramids arranged with intention.\n\n## Why Models Matter\n- They restore proportion.\n- They reveal urban logic.\n- They help you connect a single building to the larger city.\n\n## How to Read the Layout\nThink in layers:\n1) Main avenue as a spine\n2) Monumental structures as statements of authority\n3) Residential zones as proof of everyday life\n\n## Takeaway\nSometimes the fastest way to understand the past is to shrink it—so your mind can hold the whole story at once.\n",
    },
    {
        "title": "Key West: Where Sunset Becomes a Tradition",
        "slug": "key-west-sunset-tradition",
        "country": "United States",
        "city_or_region": "Key West, Florida",
        "image_filename": "key-west-mallory-square.jpg",
        "short_description": "Not all heritage is ancient stone. In Key West, the shoreline and the daily sunset ritual create a cultural landmark—shared time, shared light, and a place built around gathering.",
        "full_description": "## Overview\nKey West is known for ocean air, bright color, and a rhythm that feels slightly outside ordinary time. Here, sunset is not just an event—it’s a communal habit.\n\n## What You’re Looking At\nA coastal scene that frames the horizon as the main stage. Even without a monument, the place feels iconic because people repeatedly return to it.\n\n## Cultural Context\nModern heritage includes traditions that shape identity. A daily gathering can become a landmark when it becomes part of how a city tells its story.\n\n## Why It Works as a Post\n- It’s visually strong (sky + water + city edge).\n- It’s emotionally accessible.\n- It shows that history also lives in repeated rituals.\n\n## Visitor Notes\n- Arrive early, watch the shift in light.\n- Photograph both the horizon and the crowd: heritage is human.\n",
    },
    {
        "title": "Florence and the Duomo: A Skyline That Defines an Era",
        "slug": "florence-duomo-skyline",
        "country": "Italy",
        "city_or_region": "Florence, Tuscany",
        "image_filename": "florence-duomo-skyline.jpg",
        "short_description": "Florence feels engineered for memory: rooftops like a pattern, the Duomo as a signature. This is a skyline where craft, ambition, and patience turned architecture into identity.",
        "full_description": "## Overview\nFlorence is one of the world’s most influential art-and-architecture cities. Its skyline tells the story immediately: dense historic fabric anchored by a monumental dome.\n\n## What You’re Looking At\nA panoramic view of Florence with the Duomo rising above the city. The effect is intentional: the building becomes orientation, symbol, and destination.\n\n## Historical Context\nFlorence’s Renaissance legacy isn’t just museums—it’s built form. Proportion, detail, and urban harmony show how design shaped civic pride.\n\n## How to Read the Skyline\n- Dome and towers = civic ambition\n- Dense roofs = medieval roots\n- Harmony of scale = a city designed to be remembered\n\n## Takeaway\nFlorence rewards slow looking. A single view contains centuries of choices.\n",
    },
    {
        "title": "Hollywood Walk of Fame: A Sidewalk Turned Monument",
        "slug": "hollywood-walk-of-fame-los-angeles",
        "country": "United States",
        "city_or_region": "Los Angeles, California",
        "image_filename": "hollywood-walk-of-fame.jpg",
        "short_description": "Fame is usually abstract. On Hollywood Boulevard, it becomes architecture—names embedded in the city itself. It’s a modern landmark where culture is walked over, searched for, and photographed.",
        "full_description": "## Overview\nThe Walk of Fame is a global symbol of entertainment history. It’s unusual as a monument because it’s flat, public, and activated by crowds.\n\n## What You’re Looking At\nA section of boulevard where recognition becomes design. The stars create a visual rhythm that invites searching: people scan the ground like reading a map.\n\n## Cultural Context\nThis is modern heritage: a place where memory is curated and commercial, but still meaningful. It proves a city can preserve culture through interaction.\n\n## Why It Stays Iconic\n- It’s participatory: you don’t just observe.\n- It’s repeatable: everyone takes their own version of the same photo.\n- It’s public: the monument belongs to movement.\n\n## Visitor Notes\n- Photograph wide for context, then close for detail.\n- Expect the landmark to be noisy—that’s part of the experience.\n",
    },
    {
        "title": "Rome’s Roman Forum: Where Ruins Still Argue With Time",
        "slug": "roman-forum-rome",
        "country": "Italy",
        "city_or_region": "Rome, Lazio",
        "image_filename": "roman-forum-rome.jpg",
        "short_description": "The Roman Forum isn’t a single building—it’s a civic memory field: temples, arches, foundations, and pathways that once carried speeches, rituals, and the mechanics of empire.",
        "full_description": "## Overview\nThe Roman Forum was once the center of public life in ancient Rome. Today, it reads as layered fragments—but the layout still suggests movement, authority, and ceremony.\n\n## What You’re Looking At\nColumns without roofs, foundations without walls, and corridors of stone that guide your eye through the site.\n\n## Historical Context\nForums were not just markets—they were political theaters. Decisions were made, celebrated, contested, and recorded here.\n\n## How to Experience It\nTry imagining sound:\n- speeches\n- footsteps\n- public debate\n- religious processions\n\n## Why It Matters\nThe Forum shows how built space can carry power. Even as ruins, the geometry remains persuasive.\n",
    },
    {
        "title": "Córdoba: A City View That Contains Centuries",
        "slug": "cordoba-mezquita-cathedral-bridge",
        "country": "Spain",
        "city_or_region": "Córdoba, Andalusia",
        "image_filename": "cordoba-mezquita-bridge.jpg",
        "short_description": "In Córdoba, a single view can stack civilizations: river, bridge, tower, and old streets. Architecture becomes a timeline—showing how cities carry memory without choosing only one past.",
        "full_description": "## Overview\nCórdoba’s historic character comes from layering rather than replacing. Different eras remain visible in the same frame.\n\n## What You’re Looking At\nA composed city scene: river as foreground, bridge as connector, and the Mezquita-Cathedral tower as a vertical anchor.\n\n## Cultural Context\nFew places demonstrate continuity like this. The city becomes an archive where structure and meaning shift over time, yet the skyline stays recognizable.\n\n## How to Read the Scene\n- Water = trade, movement, boundary\n- Bridge = connection and control\n- Tower = identity and navigation\n\n## Takeaway\nCórdoba teaches a simple lesson: heritage can be multiple, not singular.\n",
    },
    {
        "title": "Prague from Above: Old Town as Living Geometry",
        "slug": "prague-old-town-square-aerial",
        "country": "Czechia",
        "city_or_region": "Prague",
        "image_filename": "prague-old-town-square.jpg",
        "short_description": "From above, Prague’s Old Town feels like a crafted map: rooftops, streets, and landmarks arranged with harmony. It’s a city where history is visible as pattern—and still lived daily.",
        "full_description": "## Overview\nPrague’s historic center is famous for its architectural continuity and dramatic urban scenes. An aerial view reveals what street-level walking can hide: structure.\n\n## What You’re Looking At\nA top-down view of Old Town: dense roofs, open squares, and the geometry of streets that funnel people into shared space.\n\n## Why the Aerial Angle Matters\n- You see planning and growth together.\n- You understand how landmarks act like compass points.\n- You notice how narrow lanes open into public squares.\n\n## How to Explore After Seeing This\nWalk it slowly:\n- move from a quiet side street into a wide square\n- look up at towers after studying the map-like view\n\n## Takeaway\nCities can be functional and poetic at once—Prague proves it.\n",
    },
    {
        "title": "The Cenacle on Mount Zion: A Room of Memory",
        "slug": "cenacle-upper-room-mount-zion",
        "country": "Israel / Palestine",
        "city_or_region": "Jerusalem",
        "image_filename": "cenacle-mount-zion.jpg",
        "short_description": "Some landmarks aren’t powerful because they’re huge, but because they’re remembered. The Cenacle (Upper Room) is a space shaped by tradition, pilgrimage, and layered meaning.",
        "full_description": "## Overview\nThe Cenacle—often referred to as the Upper Room—holds significance through tradition and spiritual memory. The architecture supports that feeling: quiet, enclosed, reflective.\n\n## What You’re Looking At\nAn interior defined by stone and arches, designed to hold attention. The space feels deliberate: not decorative, but weight-bearing.\n\n## Cultural Context\nSacred sites often carry multiple narratives. Over time, meaning accumulates—turning a room into a symbol.\n\n## How to Experience It\n- Notice how light interacts with stone.\n- Pay attention to silence and acoustics.\n- Read the space as much as the story.\n\n## Takeaway\nHeritage is not only what we build—it’s what we choose to remember.\n",
    },
]

EXTRA_POSTS = [
    {
        "title": "Marrakesh Medina: The Labyrinth of Memory",
        "slug": "marrakesh-medina-labyrinth",
        "country": "Morocco",
        "city_or_region": "Marrakesh",
        "short_description": "Marrakesh’s medina is a living archive of pathways, courtyards, and market rhythms. It is a place where orientation comes from sound, scent, and the pulse of daily trade.",
        "full_description": "## Overview\nThe medina is more than a historic district—it is a structure that teaches you how to move. The narrow lanes amplify voices and aromas, guiding you through informal routes that have evolved for centuries.\n\n## Spatial Experience\nWalking here means reading thresholds, archways, and sudden openings into shared courtyards. The city reveals itself in segments, not panoramas.\n\n## Cultural Context\nMarkets, mosques, and workshops exist in layered proximity. The medina shows how heritage persists by remaining functional and woven into everyday life.\n\n## How to Explore\n- Follow the sound of artisans at work.\n- Pause at fountain courts for a sense of scale.\n- Notice how light changes as you move between open plazas and enclosed streets.\n\n## Takeaway\nThe medina’s density is not chaos—it is a deliberate memory system that keeps history active.\n",
    },
    {
        "title": "Petra’s Treasury: A Facade Carved into Time",
        "slug": "petra-treasury-facade",
        "country": "Jordan",
        "city_or_region": "Petra",
        "short_description": "A single façade in Petra can carry the weight of an entire civilization. The Treasury is an entrance, a monument, and a testament to stone as storytelling.",
        "full_description": "## Overview\nPetra’s Treasury emerges after a long passage through the Siq. The reveal is theatrical: stone suddenly opens into a carved surface that feels both precise and monumental.\n\n## Architectural Notes\nThe façade reads like a narrative in relief. Columns, pediments, and carved figures create a sense of order in a natural cliff face.\n\n## Context and Legacy\nThe Nabataean city blended trade, cosmopolitan influence, and engineering. The Treasury is a symbol of that synthesis, merging natural geology with crafted architecture.\n\n## Visitor Notes\n- Arrive early for soft, angled light.\n- Stay long enough to watch shadows reshape the carvings.\n\n## Takeaway\nPetra’s power is the fusion of environment and design—heritage cut directly into landscape.\n",
    },
    {
        "title": "Athens Acropolis at Dusk: Geometry Above the City",
        "slug": "athens-acropolis-dusk",
        "country": "Greece",
        "city_or_region": "Athens",
        "short_description": "When the sun falls behind the hills, the Acropolis becomes a floating silhouette. This is an ancient crown still visible in modern daily life.",
        "full_description": "## Overview\nThe Acropolis stands above Athens as an intentional stage. At dusk, its geometry becomes more pronounced, revealing the logic of temple placement.\n\n## Spatial Impact\nThis is heritage as skyline. The elevation ensures that history remains in view, even as the city expands below.\n\n## Cultural Context\nThe Acropolis represents civic identity, governance, and art. Its presence anchors Athens across millennia.\n\n## How to Experience It\n- Watch the city lights rise while the temple remains still.\n- Observe the transition from stone detail to silhouette.\n\n## Takeaway\nA city can change entirely, yet still orbit around a single historic point.\n",
    },
    {
        "title": "Angkor Wat: The Moat as Mirror",
        "slug": "angkor-wat-moat",
        "country": "Cambodia",
        "city_or_region": "Siem Reap",
        "short_description": "Angkor Wat is legendary for its towers, but the surrounding moat is the quiet frame that doubles the monument in reflection.",
        "full_description": "## Overview\nAngkor Wat’s moat is a boundary and a visual device. It separates sacred space while reflecting the temple back to the viewer.\n\n## Visual Reading\nThe towers rise like a stone lotus. The reflection in the water creates symmetry that emphasizes intention and scale.\n\n## Historical Context\nThe temple was part of an expansive sacred landscape. Water controlled the experience of arrival, reinforcing spiritual separation.\n\n## Visitor Notes\n- Visit at sunrise for the strongest reflections.\n- Walk the perimeter to understand the temple’s relationship to water.\n\n## Takeaway\nWater here is architecture: it shapes the way history is seen.\n",
    },
    {
        "title": "Cartagena Walls: The City as a Fortress Line",
        "slug": "cartagena-walls-fortress",
        "country": "Colombia",
        "city_or_region": "Cartagena",
        "short_description": "Cartagena’s walls outline a city shaped by trade, defense, and maritime history. The fortifications are both barrier and promenade.",
        "full_description": "## Overview\nThe walls wrap around Cartagena like a stone ribbon. They define an edge between sea and city, history and present.\n\n## What You’re Looking At\nA continuous line of ramparts, bastions, and viewpoints. The stonework records centuries of coastal defense.\n\n## Cultural Context\nCartagena was a major port in the Spanish empire. The walls speak to commerce, conflict, and the value of location.\n\n## How to Explore\n- Walk the walls at golden hour for wide horizon views.\n- Notice how neighborhoods shift just inside the ramparts.\n\n## Takeaway\nFortifications can become places of leisure—heritage that adapts to new rhythms.\n",
    },
    {
        "title": "Lisbon Tram Lines: Heritage in Motion",
        "slug": "lisbon-tram-lines",
        "country": "Portugal",
        "city_or_region": "Lisbon",
        "short_description": "Lisbon’s iconic trams trace the city’s steepest routes, turning transit into a moving landmark that connects neighborhoods and stories.",
        "full_description": "## Overview\nThe trams of Lisbon are more than vehicles—they are part of the city’s visual identity. Their routes reveal the city’s dramatic topography.\n\n## Urban Context\nRails run through narrow lanes, past tiled facades, and across small plazas. The tram is a thread that ties together Lisbon’s districts.\n\n## Why It Matters\nHeritage can be kinetic. The tram lines show how historic infrastructure remains central to daily life.\n\n## Visitor Notes\n- Ride early to avoid crowds.\n- Listen for the sound of brakes on steep climbs.\n\n## Takeaway\nThe most memorable landmarks sometimes move right past you.\n",
    },
    {
        "title": "Istanbul’s Blue Mosque Courtyard: Rhythm and Light",
        "slug": "istanbul-blue-mosque-courtyard",
        "country": "Turkey",
        "city_or_region": "Istanbul",
        "short_description": "The courtyard of the Blue Mosque creates a quiet threshold between the city and the sacred, using light and repetition to guide movement.",
        "full_description": "## Overview\nCourtyards are transitional spaces. At the Blue Mosque, the expansive court allows visitors to reset before entering the prayer hall.\n\n## What You’re Looking At\nArcades, domes, and a patterned stone floor. The geometry repeats, creating a rhythm that feels meditative.\n\n## Cultural Context\nOttoman architecture emphasized balance and procession. The courtyard is part of a designed sequence.\n\n## How to Experience\n- Pause at the fountain and observe the axis of the space.\n- Notice how the arcades frame the sky.\n\n## Takeaway\nHeritage is often experienced through transitions, not just destinations.\n",
    },
    {
        "title": "Cusco’s Plaza de Armas: A Stage for Continuity",
        "slug": "cusco-plaza-de-armas",
        "country": "Peru",
        "city_or_region": "Cusco",
        "short_description": "Cusco’s main square has been a ceremonial stage since the Inca era, proving that public space can carry multiple histories at once.",
        "full_description": "## Overview\nThe Plaza de Armas is the heart of Cusco. It is framed by colonial architecture atop Inca foundations, representing layered histories.\n\n## Spatial Reading\nOpen plaza, arcaded edges, and surrounding hills create a natural amphitheater for civic life.\n\n## Cultural Context\nFestivals, protests, and daily markets all converge here. The plaza remains a living center rather than a static monument.\n\n## How to Explore\n- Visit morning and night to see different rhythms.\n- Look for traces of Inca stonework beneath colonial facades.\n\n## Takeaway\nCivic spaces can outlast empires by staying useful.\n",
    },
    {
        "title": "Edinburgh Castle: Stone Above the Cloud Line",
        "slug": "edinburgh-castle-rock",
        "country": "Scotland",
        "city_or_region": "Edinburgh",
        "short_description": "Perched on volcanic rock, Edinburgh Castle commands the skyline and organizes the city’s sense of direction.",
        "full_description": "## Overview\nEdinburgh Castle rises above the Royal Mile as a fortress and a symbol. The volcanic rock foundation makes the silhouette unmistakable.\n\n## What You’re Looking At\nLayered stone structures, defensive walls, and a steep drop to the city below. The elevation shapes how the city orbits the site.\n\n## Historical Context\nThe castle has witnessed royal ceremonies, military conflict, and civic celebration. It embodies Scotland’s resilience.\n\n## Visitor Notes\n- Stand on the esplanade to see the city fan out below.\n- Observe how the castle frames the horizon from almost every district.\n\n## Takeaway\nTopography can be destiny—heritage anchored in geology.\n",
    },
    {
        "title": "Havana Malecón: A Seawall of Daily Life",
        "slug": "havana-malecon-seawall",
        "country": "Cuba",
        "city_or_region": "Havana",
        "short_description": "The Malecón is both barrier and boulevard, a seawall that hosts conversations, music, and the city’s evening breeze.",
        "full_description": "## Overview\nHavana’s Malecón stretches along the coast as a linear public space. It is where the city meets the sea and lets its guard down.\n\n## What You’re Looking At\nA broad seawall, lamps, and the Atlantic horizon. The geometry is simple, but the social life is rich.\n\n## Cultural Context\nThe Malecón is a stage for daily ritual: fishing, music, and conversation. It turns infrastructure into a cultural landmark.\n\n## How to Experience\n- Visit at dusk when the light softens and the city gathers.\n- Listen for the layers of music and conversation.\n\n## Takeaway\nHeritage can be about atmosphere as much as architecture.\n",
    },
]


class Command(BaseCommand):
    help = "Seed the database with initial Heritage Atlas posts."

    def handle(self, *args, **options):
        user_model = get_user_model()
        author = user_model.objects.first()
        if not author:
            author = user_model.objects.create_user(
                username="atlas_admin",
                email="admin@heritageatlas.com",
                password="ChangeMe123!",
            )

        created = 0
        for post_data in SEED_POSTS + EXTRA_POSTS:
            slug = post_data["slug"]
            if Post.objects.filter(slug=slug).exists():
                continue
            image_filename = post_data.pop("image_filename", None)
            hero_image = None
            if image_filename:
                image_path = os.path.join(settings.MEDIA_ROOT, "posts", image_filename)
                if os.path.exists(image_path):
                    hero_image = f"posts/{image_filename}"

            Post.objects.create(
                author=author,
                hero_image=hero_image,
                **post_data,
            )
            created += 1

        self.stdout.write(self.style.SUCCESS(f"Seed complete. Created {created} posts."))
