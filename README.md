Ich schreibe doch keine eigene Webseite mehr... 

---

### **Prompt for Coding Agent**

**Role:**
You are an expert Frontend Developer and UI/UX Designer.

**Task:**
Create a personal portfolio homepage for **Markus Wondrak**. The site will be hosted on GitHub Pages, so it must be **easy to maintain**. Ideally, provide a **single HTML file** (index.html) containing all necessary CSS and JavaScript.

**Design Requirements:**

* **Vibe:** Minimalistic, "Developer Chic."
* **Typography:** Use a monospaced "coding" font (like 'Fira Code', 'Roboto Mono', or 'Courier New') for headings to give it a technical feel. Use a clean sans-serif for body text if needed for readability.
* **Color Palette:** Dark mode by default (e.g., VS Code dark theme style: dark charcoal background, off-white text, and nice syntax-highlighting accent colors).
* **Responsiveness:** Must look great on mobile and desktop.
* **Tone:** Professional but relaxed and authentic.

**Content to Insert:**

**1. Header:**

* **Name:** Markus Wondrak
* **Tagline:** Domain Architect | Software Engineering Enthusiast

**2. About Me:**
Please format this text to be easy to read (perhaps 2 short paragraphs):

> "I am a software engineering enthusiast with a clear mission: making life easier for developers and producing good quality software. My path took me from a classic vocational training ('Fachinformatiker') and a Master's degree at Frankfurt University to 9 years in consultancy. Since 2024, I’ve been working as a Domain Architect at a large German bank. I am currently focused on exploring how AI can best assist developers in creating better software.
> When I’m away from the keyboard, I prioritize my family, reading, playing basketball and watching football."

**3. Social Links:**

* **GitHub:** [https://github.com/markuswondrak](https://github.com/markuswondrak)
* **LinkedIn:** [https://www.linkedin.com/in/markus-wondrak-53b1881a3/](https://www.linkedin.com/in/markus-wondrak-53b1881a3/)

**4. Top Projects:**
Create a clean grid or card layout for these projects:

* **Finance App**
* *Description:* A modern personal finance tracking application built with Vue.js 3 and Go. Features include wealth tracking, fixed costs management, and financial forecasting with a fintech-inspired dark theme.
* *Link:* [https://github.com/markuswondrak/finance-app](https://github.com/markuswondrak/finance-app)


* **Pokemon Collector**
* *Description:* A React-based Pokemon collection organizer. Built to demonstrate the SpecKit development workflow, it features strict TDD, architectural planning, and automated specification-driven implementation.
* *Link:* [https://github.com/markuswondrak/pokemon-collector](https://github.com/markuswondrak/pokemon-collector)


* **Faststring**
* *Description:* My Master's thesis project featuring an algorithm to exchange arbitrary types in Java bytecode. It identifies safe boundaries to seamlessly convert legacy data structures at runtime.
* *Link:* [https://github.com/markuswondrak/faststring](https://github.com/markuswondrak/faststring)


* **Wondrax Platform**
* *Description:* Coming soon.
* *Link:* #



**Technical Implementation:**

* Use semantic HTML5.
* Use CSS variables for colors (so I can easily tweak them later).
* Add a blinking cursor at the end of the bio paragraph. 
* Ensure all external links open in a new tab (`target="_blank"`).
* Use the `favicon_cursor.png` as the favicon for this page. 

**Output:**
Please provide the full code for `index.html`.