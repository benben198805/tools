# Tools Index

Comprehensive index of all tools in this repository, structured for quick AI agent scanning. Updated: auto-generated from `tools.json` and `python/README.md`.

## Browser Tools

Single-file HTML pages in the repository root. Open directly in a browser. Each has a companion `{slug}.docs.md` with detailed documentation.

### Data & Time

- **Bluesky Timeline Viewer**
  - File: `bluesky-timeline.html`
  - Purpose: View Bluesky social media timelines by authenticating with your account credentials and retrieving live feed data.

- **Claude Code Timeline Viewer**
  - File: `claude-code-timeline.html`
  - Purpose: View Claude Code session `.

- **Codex Timeline Viewer**
  - File: `codex-timeline.html`
  - Purpose: View Mozilla Codex rollout timeline events from `.

- **Cooking Timer**
  - File: `cooking-timer.html`
  - Purpose: # Cooking Timer Documentation.

- **CSV marker map - use ?csv=URL to CSV to populate**
  - File: `csv-marker-map.html`
  - Purpose: View CSV data as markers on an interactive map using the `?csv=URL` parameter to specify a CSV file containing latitude and longitude columns.

- **Date Calculator**
  - File: `date-calculator.html`
  - Purpose: Calculate the time between two dates with detailed breakdowns and visual representations.

- **Lightning Timer**
  - File: `lightning-timer.html`
  - Purpose: Track time with Lightning Timer, a full-screen countdown application that displays elapsed seconds in large, easy-to-read format.

- **mdn-timelines**
  - File: `mdn-timelines.html`
  - Purpose: View Mozilla's browser compatibility data to track when web APIs were first supported across different browsers.

- **MapLibre GL + OpenFreeMap demo**
  - File: `openfreemap-demo.html`
  - Purpose: Explore an interactive map of San Francisco rendered with MapLibre GL and OpenFreeMap tiles, displaying 1000 randomly distributed markers across the city.

- **Percentage Recalculator**
  - File: `percentage-recalculator.html`
  - Purpose: Calculate and normalize multiple percentages to sum to 100%, with the option to exclude specific values from the recalculation.

- **Reading Time Estimator**
  - File: `reading-time.html`
  - Purpose: Calculate reading time estimates for any text by pasting or typing content into the input area.

- **Species observation map**
  - File: `species-observation-map.html`
  - Purpose: # Documentation.

- **Timezone Meeting Planner**
  - File: `timezones.html`
  - Purpose: Plan meetings across multiple time zones by selecting two locations and viewing their local times side-by-side.

- **Token Usage Calculator**
  - File: `token-usage.html`
  - Purpose: Calculate token usage across your Claude and other LLM API calls by pasting YAML output from the LLM tool's `llm logs -su` command.

- **Transfer time calculator**
  - File: `transfer-time.html`
  - Purpose: Calculate file transfer duration by entering the file size and transfer speed with their respective units.

- **Timestamp Converter**
  - File: `unix-timestamp.html`
  - Purpose: Convert Unix timestamps to human-readable dates and times with this tool.

### Development

- **GitHub Account Info Lookup**
  - File: `github-account.html`
  - Purpose: Look up GitHub user account information by entering a username to retrieve the numeric Account ID and account creation date through the public GitHub API.

- **GitHub API File/Image Writer**
  - File: `github-api-write.html`
  - Purpose: Upload files and images to GitHub repositories using the GitHub API.

- **GitHub GraphQL Explorer**
  - File: `github-graphiql.html`
  - Purpose: Explore GitHub's GraphQL API using an interactive query interface that requires authentication via a personal access token.

- **GitHub Rate Limit Checker**
  - File: `github-ratelimit.html`
  - Purpose: Monitor your GitHub API usage and remaining rate limits with this authentication-based checker.

- **GitHub Repo Size**
  - File: `github-repo-size.html`
  - Purpose: Check the size of any GitHub repository by entering the owner and repository name or pasting a GitHub URL.

- **API Explorer**
  - File: `iframe-api-explorer.html`
  - Purpose: # Documentation.

- **iframe sandbox**
  - File: `iframe-sandbox.html`
  - Purpose: Test and explore HTML, CSS, and JavaScript code in a sandboxed iframe environment with configurable security restrictions.

- **Keyboard Debugger**
  - File: `keyboard-debug.html`
  - Purpose: Monitor keyboard input in real-time with this interactive keyboard debugger that displays pressed keys and their corresponding key codes.

- **Filter Badge Component**
  - File: `keyboard-filters.html`
  - Purpose: # Filter Badge Component Documentation.

- **MicroQuickJS Code Executor**
  - File: `microquickjs.html`
  - Purpose: Execute JavaScript code in a lightweight MicroQuickJS sandbox environment running via WebAssembly, with results displayed directly on the page.

- **Pipfile.lock Dependency Parser**
  - File: `pipfile.html`
  - Purpose: Parse Pipfile.

- **Python Comment Stripper**
  - File: `python-comment-stripper.html`
  - Purpose: Remove all comments from Python source code while preserving strings, docstrings, and code structure using the `tokenize` module running on Pyodide.

- **Python Vulnerability Lookup**
  - File: `python-vulnerability-lookup.html`
  - Purpose: Search Python packages for known security vulnerabilities by pasting a `pyproject.

- **QuickJS Code Executor**
  - File: `quickjs.html`
  - Purpose: Execute JavaScript code in a sandboxed QuickJS WebAssembly environment with a built-in synchronous `fetch()` function for retrieving remote content.

- **Schema DSL to JSON Converter**
  - File: `schema-dsl.html`
  - Purpose: Convert a compact schema definition language into JSON schema format in real-time.

- **Side Panel Modal with Dialog Element**
  - File: `side-panel-dialog.html`
  - Purpose: Explore a product catalog with interactive item details displayed in a smooth side panel modal.

- **SQLite AST**
  - File: `sqlite-ast.html`
  - Purpose: Parse SQLite SELECT queries into abstract syntax trees and view the results in JSON and Python representations.

- **SQLite Bytecode Explorer**
  - File: `sqlite-bytecode-explorer.html`
  - Purpose: Explore SQLite's Virtual Database Engine (VDBE) by analyzing the bytecode that SQLite generates when compiling SQL queries.

- **SQLite Query Result Formatter Demo**
  - File: `sqlite-qrf.html`
  - Purpose: Format SQLite query results in 20 different styles including box-drawing tables, CSV, JSON, HTML, Markdown, and more using this interactive WebAssembly-based demonstration.

- **Pelican Sightings Query Tool**
  - File: `sqlite-wasm.html`
  - Purpose: Query pelican sighting records from Half Moon Bay using SQL commands against an in-browser SQLite database.

### Image & Media

- **Avatar Web Component**
  - File: `avatar-web-component.html`
  - Purpose: Display and edit images with an interactive cropping interface for creating avatars or profile pictures.

- **BBox Tool - CropperJS Version**
  - File: `bbox-cropper.html`
  - Purpose: Draw bounding boxes on images using an interactive cropping tool powered by CropperJS.

- **Compare PDFs**
  - File: `compare-pdfs.html`
  - Purpose: Compare two PDF documents side-by-side to identify differences between them.

- **FFmpeg video crop**
  - File: `ffmpeg-crop.html`
  - Purpose: Generate FFmpeg crop commands by uploading a video file and interactively defining a crop area using a draggable overlay.

- **Gemini API Image Bounding Box Visualization**
  - File: `gemini-bbox.html`
  - Purpose: Analyze images using the Google Gemini API and visualize detected objects as bounding boxes or points overlaid on the original image with coordinate grid lines.

- **Render JSON from Gemini Image Generation**
  - File: `gemini-image-json.html`
  - Purpose: Parse and visualize JSON responses from the Google Gemini image generation API, extracting and displaying generated images, text content, and usage metadata in a formatted layout.

- **Gemini API Image Mask Visualization**
  - File: `gemini-mask.html`
  - Purpose: Use the Gemini API to analyze images and generate segmentation masks with visual overlays.

- **GIF Dissector**
  - File: `gif-dissector.html`
  - Purpose: Parse and visualize animated GIF files by extracting individual frames, timing data, color palettes, and detailed metadata.

- **GIF Optimizer (gifsicle WASM)**
  - File: `gif-optimizer.html`
  - Purpose: Optimize animated GIF files using gifsicle compiled to WebAssembly, with all processing occurring directly in your browser without server uploads.

- **24×24 Icon Editor**
  - File: `icon-editor.html`
  - Purpose: # Documentation.

- **Seamless Sandboxed Iframe Prototype**
  - File: `iframe-resize.html`
  - Purpose: Embed untrusted content safely within a webpage using a sandboxed iframe that automatically adjusts its height without allowing cross-origin access.

- **Photo print layout**
  - File: `image-print.html`
  - Purpose: Create custom photo print layouts for A4 pages with adjustable grid configurations, image fitting options, and portrait or landscape orientations.

- **Image resize, crop, and quality comparison**
  - File: `image-resize-quality.html`
  - Purpose: Compare images at different sizes and quality levels by uploading a photo, defining a crop area, and generating multiple preview versions with varying dimensions and compression settings.

- **Drag and Drop Image Optimizer**
  - File: `image-to-jpeg.html`
  - Purpose: Compress and optimize image files by uploading them to this web-based tool that applies adjustable JPEG quality settings to reduce file size.

- **Image to SVG**
  - File: `image-to-svg.html`
  - Purpose: Convert raster images to scalable vector graphics using automated tracing technology.

- **Image Token Calculator**
  - File: `jina-embeddings-image-token-calculator.html`
  - Purpose: Calculate the token cost for images used in API requests by uploading or dragging an image file into the tool.

- **Mask Visualizer**
  - File: `mask-visualizer.html`
  - Purpose: Visualize bounding boxes and PNG masks from JSON data with support for multiple coordinate system origins.

- **MicroPython Code Executor**
  - File: `micropython.html`
  - Purpose: Execute Python code in a sandboxed MicroPython WebAssembly environment with output displayed in real-time.

- **OCR PDFs and images directly in your browser**
  - File: `ocr.html`
  - Purpose: Extract text from PDF documents and images using optical character recognition (OCR) directly in your browser.

- **Social Media Card Cropper**
  - File: `social-media-cropper.html`
  - Purpose: Crop and customize images for social media platforms with precise control over composition and framing.

- **Progressively render SVG**
  - File: `svg-progressive-render.html`
  - Purpose: View SVG content being progressively rendered character by character over a specified duration.

- **SVG to JPEG/PNG**
  - File: `svg-render.html`
  - Purpose: Convert SVG images to JPEG or PNG format with customizable dimensions, padding, and background colors.

- **SVG Base64 Embedding Demo**
  - File: `svg-sandbox.html`
  - Purpose: Embed SVG images directly into HTML using base64 data URIs, which eliminates the need for separate image files and reduces HTTP requests.

- **TIFF Orientation Reader**
  - File: `tiff-orientation.html`
  - Purpose: Read TIFF orientation metadata from JPEG images by uploading or dragging files into the drop zone.

- **Make Colors Transparent in PNG**
  - File: `transparent-png.html`
  - Purpose: # Documentation.

- **PDF Viewer**
  - File: `view-pdf.html`
  - Purpose: View PDF files from any CORS-enabled URL with this interactive PDF viewer application.

- **Hyperviz**
  - File: `visualizer.html`
  - Purpose: Create real-time audio-reactive visualizations with eight distinct modes including plasma, particles, tunnel effects, kaleidoscope patterns, Matrix rain, terrain, fire, and starfield animations.

- **YouTube Thumbnail Viewer**
  - File: `youtube-thumbnails.html`
  - Purpose: View YouTube video thumbnails in multiple resolutions by entering a video URL or ID.

### LLM & AI

- **Census Explorer (built using Claude 3.7 Sonnet thinking)**
  - File: `census-reporter-claude.html`
  - Purpose: # Documentation.

- **Census Reporter Explorer (built using Gemini 2.5 Pro)**
  - File: `census-reporter-gemini.html`
  - Purpose: # Documentation.

- **Chrome LanguageModel Playground**
  - File: `chrome-prompt-playground.html`
  - Purpose: Interact with Chrome's built-in language model API through this web-based playground interface.

- **Cleanup Claude Code Paste**
  - File: `cleanup-claude-code-paste.html`
  - Purpose: Clean up Claude Code terminal output by removing the ❯ prompt character, fixing whitespace from line wrapping, and joining broken lines into readable paragraphs.

- **Conference Schedule - ICS File**
  - File: `code-with-claude-2025.html`
  - Purpose: Download and view the complete conference schedule for May 22, 2025, in iCalendar format.

- **Gemini Chat App**
  - File: `gemini-chat.html`
  - Purpose: Chat with Google's Gemini AI models directly in your browser using this interactive chat application.

- **Gemini 3.1 Flash TTS**
  - File: `gemini-flash-tts.html`
  - Purpose: Convert text to natural-sounding speech using Google's Gemini 3.

- **Gemini Prompt**
  - File: `gemini-prompt.html`
  - Purpose: Generate responses from Google's Gemini API with support for system prompts, model selection, and streaming output.

- **Gist Audio Player**
  - File: `gpt-4o-audio-player.html`
  - Purpose: Play audio responses generated by OpenAI's GPT-4 with audio preview model by providing a GitHub Gist URL containing the API response JSON.

- **Haiku**
  - File: `haiku.html`
  - Purpose: # Documentation.

- **llm-lib demo**
  - File: `llm-lib.html`
  - Purpose: This is an interactive demonstration of a unified JavaScript library that provides a consistent interface for working with multiple large language model providers.

- **OpenAI Audio**
  - File: `openai-audio.html`
  - Purpose: Record audio through your microphone and send it to OpenAI's GPT-4o audio model along with a text prompt to receive AI-generated responses.

- **Prompt GPT-4o audio**
  - File: `openai-audio-output.html`
  - Purpose: Interact with OpenAI's GPT-4o audio models to generate spoken responses to your prompts with customizable system instructions and voice selection.

- **OpenAI WebRTC Audio Session**
  - File: `openai-webrtc.html`
  - Purpose: Establish real-time audio conversations with OpenAI's GPT-4o model using WebRTC technology.

- **OpenAI Prompt Caching Playground**
  - File: `prompt-caching.html`
  - Purpose: Explore OpenAI's prompt caching feature by testing different prompt structures and observing cache hit rates across multiple requests.

- **Prompts.js**
  - File: `prompts-js.html`
  - Purpose: Prompts.

- **Render Claude Citations**
  - File: `render-claude-citations.html`
  - Purpose: Render Claude API responses with proper citation formatting by pasting JSON output into this tool.

### Miscellaneous

- **AI Adoption Rolling Avg — Pyodide**
  - File: `ai-adoption.html`
  - Purpose: View AI adoption trends across different firm sizes by analyzing survey data on artificial intelligence usage in the workplace.

- **Site Analytics**
  - File: `analytics.html`
  - Purpose: # Site Analytics Documentation.

- **animated-rainbow-border**
  - File: `animated-rainbow-border.html`
  - Purpose: Display an animated rainbow gradient border effect around a centered box with interactive controls.

- **Annotated Presentation Creator**
  - File: `annotated-presentations.html`
  - Purpose: Create annotated presentation slides with alt text and markdown notes.

- **APSW SQLite query explainer**
  - File: `apsw-query.html`
  - Purpose: Analyze and explain SQLite queries using APSW by entering SQL code and executing it in an in-browser Python environment.

- **Language Model Elo Ratings**
  - File: `arena-animated.html`
  - Purpose: Compare Elo ratings across different language models and dates using this interactive animated bar chart.

- **ARES Phonetic Alphabet Converter**
  - File: `ares.html`
  - Purpose: Convert text to NATO phonetic alphabet equivalents for clear communication in radio, military, and aviation contexts.

- **Live region notification demo**
  - File: `aria-live-regions.html`
  - Purpose: Explore live region notifications with this interactive accessibility demo that allows you to test how screen readers announce dynamic content updates.

- **Audio Spectrum Visualizer**
  - File: `audio-spectrum.html`
  - Purpose: Visualize real-time audio frequency data from your microphone as an animated spectrum display.

- **Badge Drawer — Device-Scale Canvas**
  - File: `badge-drawer.html`
  - Purpose: # Badge Drawer — Device-Scale Canvas.

- **Badge Interactive REPL**
  - File: `badge-repl.html`
  - Purpose: Interact with a MicroPython device via the Web Serial API to execute Python commands in real-time through a browser-based REPL interface.

- **Base64 Gzip Decoder**
  - File: `base64-gzip-decoder.html`
  - Purpose: Decode base64-encoded gzip data to retrieve the original decompressed content.

- **Dual Recipe Cooking Timer**
  - File: `blackened-cauliflower-and-turkish-style-stew.html`
  - Purpose: # Documentation.

- **Blog to Newsletter**
  - File: `blog-to-newsletter.html`
  - Purpose: Convert a blog database into a Substack newsletter by selecting content from the past week or more and arranging stories in your preferred order.

- **Bookmarklets Collection**
  - File: `bookmarklets.html`
  - Purpose: Access a collection of practical bookmarklets for web development and general browsing tasks.

- **Box shadow CSS generator**
  - File: `box-shadow.html`
  - Purpose: Generate custom CSS box-shadow effects with interactive controls and real-time preview.

- **Bugzilla Bug Viewer**
  - File: `bugzilla-bug.html`
  - Purpose: View Mozilla Bugzilla bug reports with a streamlined interface that displays bug details, comments, and change history in an organized timeline format.

- **Bullish vs Bearish - Remember Which is Which!**
  - File: `bullish-bearish.html`
  - Purpose: Learn the difference between bullish and bearish market sentiment through an interactive visual guide featuring animated bull and bear characters.

- **California Clock Change - PST/PDT Only**
  - File: `california-clock-change.html`
  - Purpose: Track California's Daylight Saving Time changes with this tool that displays the most recent clock adjustment and alerts you to the next one.

- **Improved Interactive CSS Grid Layout with Symmetric Animation**
  - File: `click-grid-to-expand.html`
  - Purpose: Explore an interactive CSS grid layout that demonstrates dynamic element expansion with smooth animations.

- **CORS Fetch Tester**
  - File: `cors-fetch.html`
  - Purpose: Test HTTP requests directly from your browser and observe which response headers and body content are accessible under CORS (Cross-Origin Resource Sharing) restrictions.

- **datasette.io news preview**
  - File: `datasette-io-preview.html`
  - Purpose: Preview and validate datasette.

- **Deep Research Session Viewer**
  - File: `deep-research-viewer.html`
  - Purpose: # Deep Research Session Viewer Documentation.

- **Devon Lane Driving Simulator**
  - File: `devon-lanes.html`
  - Purpose: Navigate the treacherous single-track lanes of rural Devon in this interactive driving simulator, where you must manage your sanity while encountering cyclists, tractors, caravans, and other obstacles.

- **DNS Lookup**
  - File: `dns.html`
  - Purpose: # DNS Lookup Documentation.

- **DOT File Renderer**
  - File: `dot.html`
  - Purpose: Render DOT graph files into visual diagrams directly in your browser.

- **Emoji Identifier**
  - File: `emoji-identifier.html`
  - Purpose: Extract and identify all emojis from text by pasting or typing into the input field, and instantly view their names and Unicode codepoint values.

- **Encrypt / decrypt message**
  - File: `encrypt.html`
  - Purpose: Encrypt and decrypt messages using a passphrase with this web application that leverages modern browser cryptography APIs.

- **Event Planner**
  - File: `event-planner.html`
  - Purpose: Plan events with timezone-aware scheduling and countdown tracking.

- **EXIF Data Viewer**
  - File: `exif.html`
  - Purpose: Extract EXIF metadata and GPS coordinates from uploaded images using this viewer.

- **Extract URLs**
  - File: `extract-urls.html`
  - Purpose: Extract URLs from copied web page content by pasting HTML into the input area, which automatically identifies and displays all hyperlinks found in the pasted material.

- **Interactive CSS Flexbox Playground**
  - File: `flexbox-playground.html`
  - Purpose: Experiment with CSS Flexbox properties in real-time using this interactive playground.

- **Interactive Footnotes**
  - File: `footnotes-experiment.html`
  - Purpose: # Documentation.

- **Gradient image generator**
  - File: `gradient-card.html`
  - Purpose: Generate customizable gradient images with multiple pattern overlays and effects.

- **CSS Grid Lanes Polyfill Demo**
  - File: `grid-lanes-polyfill.html`
  - Purpose: # CSS Grid Lanes Polyfill Demo.

- **Hacker News comments for a user**
  - File: `hn-comments-for-user.html`
  - Purpose: View Hacker News comments for any user by entering their handle and fetching up to 1,000 recent comments in a single request.

- **Hugging Face Model Storage Checker**
  - File: `huggingface-storage.html`
  - Purpose: Check the storage size of Hugging Face machine learning models by entering a model URL or repository path.

- **Is it a bird?**
  - File: `is-it-a-bird.html`
  - Purpose: Determine whether images contain birds using OpenAI's CLIP model running directly in your browser through Transformers.

- **Jina Reader**
  - File: `jina-reader.html`
  - Purpose: Convert web pages to structured content using the Jina Reader API, with support for multiple output formats including markdown, HTML, and text.

- **Link Extractor**
  - File: `link-extractor.html`
  - Purpose: Extract hyperlinks from pasted web content and export them in multiple formats including HTML, Markdown, and plain text.

- **link-temp**
  - File: `link-temp.html`
  - Purpose: View Mozilla Bugzilla bug reports directly from your terminal using this LLM plugin for Google's Gemini API.

- **Merge State Visualizer**
  - File: `manyana.html`
  - Purpose: # CRDT Merge State Visualizer.

- **Minesweeper**
  - File: `minesweeper.html`
  - Purpose: Play a classic Minesweeper game directly in your browser with support for three difficulty levels: Easy, Medium, and Hard.

- **Mobile Data Tables: Responsive Patterns Demo**
  - File: `mobile-tables.html`
  - Purpose: # Mobile Data Tables: Responsive Patterns Demo.

- **MP3 Inspector**
  - File: `mp3-inspector.html`
  - Purpose: Extract ID3 metadata and file information from MP3 audio files using this browser-based tool.

- **HTML Header Processor**
  - File: `nav-for-headings.html`
  - Purpose: Process HTML content to automatically generate unique IDs for all header elements and create a table of contents with anchor links.

- **The New Yorker Style Converter**
  - File: `new-yorker-style.html`
  - Purpose: Convert text to match The New Yorker's distinctive typographic style, featuring proper diaereses (such as "coöperate" and "naïve"), curly quotation marks, em dashes, and ellipses.

- **NICAR 2026 Schedule**
  - File: `nicar-2026.html`
  - Purpose: Browse the NICAR 2026 conference schedule with powerful search and filtering capabilities.

- **NumPy Vectors & Matrices — Pyodide Lab**
  - File: `numpy-pyodide-lab.html`
  - Purpose: Execute NumPy vector and matrix operations directly in your browser using an interactive lab powered by Pyodide.

- **The Octave — A Sound Relationship**
  - File: `octave-explainer.html`
  - Purpose: Explore the mathematical and sonic relationship between frequencies through interactive demonstrations and a playable piano keyboard.

- **Open Sauce 2025 Schedule**
  - File: `open-sauce-2025.html`
  - Purpose: Browse the Open Sauce 2025 conference schedule with sessions organized by day, including speaker information, session duration, location, and detailed descriptions.

- **PG&E Outage Map - Half Moon Bay Area**
  - File: `pge-outages-hmb.html`
  - Purpose: Track power outages affecting the Half Moon Bay area with this interactive map displaying real-time PG&E outage data within a 15-mile radius.

- **PHP deserializer**
  - File: `php-deserializer.html`
  - Purpose: Convert serialized PHP data to JSON format for easy viewing and manipulation.

- **Pomodoro Timer**
  - File: `pomodoro.html`
  - Purpose: Track productivity sessions with this Pomodoro timer application that manages timed work intervals with customizable durations.

- **progress**
  - File: `progress.html`
  - Purpose: Track the progress of the current U.

- **Pyodide Bar Chart Demo (pandas + matplotlib)**
  - File: `pyodide-bar-chart.html`
  - Purpose: Execute Python code directly in your browser with Pyodide, a WebAssembly-based Python runtime.

- **Pyodide REPL**
  - File: `pyodide-repl.html`
  - Purpose: Execute Python code directly in your web browser using Pyodide, a port of CPython to WebAssembly.

- **PyPI Package Changelog**
  - File: `pypi-changelog.html`
  - Purpose: # PyPI Package Changelog Documentation.

- **QR Code Decoder**
  - File: `qr.html`
  - Purpose: Decode QR codes from images or your device's camera with this interactive web application.

- **Query String Stripper**
  - File: `query-string-stripper.html`
  - Purpose: Remove query parameters and tracking data from URLs with this Query String Stripper tool.

- **Red Annotation Extractor**
  - File: `red-extractor.html`
  - Purpose: # Red Annotation Extractor Documentation.

- **SLOCCount - Count Lines of Code**
  - File: `sloccount.html`
  - Purpose: # Documentation.

- **Software Heritage Repository Retriever**
  - File: `software-heritage-repo.html`
  - Purpose: Download archived Git repositories from Software Heritage, the universal archive of software source code.

- **Sorting algorithms**
  - File: `sort-algorithms.html`
  - Purpose: Explore and compare different sorting algorithms through interactive animated visualizations that display how each algorithm organizes data in real-time.

- **Speech Synthesis Tester**
  - File: `speech-synthesis.html`
  - Purpose: Test the Web Speech API's speech synthesis capabilities by entering text and configuring voice parameters such as rate, pitch, and volume.

- **Swagger Subset**
  - File: `swagger-subset.html`
  - Purpose: Extract a subset of Swagger/OpenAPI definitions by selecting specific API endpoints and their dependencies.

- **Syntaqlite Playground**
  - File: `syntaqlite.html`
  - Purpose: # Syntaqlite Playground.

- **Tacopy Playground - Tail-Call Optimization for Python**
  - File: `tacopy-playground.html`
  - Purpose: Explore how tail-recursive Python functions are transformed into optimized iterative code using the Tacopy library.

- **TURBO.COM — 39,731 Bytes Deconstructed**
  - File: `turbo-pascal-deconstructed.html`
  - Purpose: Explore an interactive breakdown of Turbo Pascal 3.

- **Unicode Explorer — Binary Search Over HTTP**
  - File: `unicode-binary-search.html`
  - Purpose: View Unicode characters and their properties through an interactive binary search algorithm that makes real HTTP Range requests to fetch individual records from a binary database.

- **User Agent**
  - File: `user-agent.html`
  - Purpose: Display your browser's user agent string, which contains information about your web browser, operating system, and device.

- **v86 Linux Emulator**
  - File: `v86.html`
  - Purpose: Run Linux commands in your browser using x86 emulation powered by v86, a JavaScript/WebAssembly-based x86 emulator.

- **Directory Explorer Demo**
  - File: `webkitdirectory.html`
  - Purpose: Explore the contents of a local directory in your browser with an interactive file tree viewer and search functionality.

- **Writing Style Analyzer**
  - File: `writing-style.html`
  - Purpose: Analyze your writing for common style issues by pasting text into this tool, which detects weasel words (such as "very" and "quite"), passive voice constructions, and duplicate consecutive words.

- **Package File Browser**
  - File: `zip-wheel-explorer.html`
  - Purpose: Browse and view the contents of Python package files (.

### Social

- **Bluesky Favorites Viewer**
  - File: `bluesky-faves.html`
  - Purpose: # Bluesky Favorites Viewer Documentation.

- **Bluesky WebSocket Feed Monitor**
  - File: `bluesky-firehose.html`
  - Purpose: Monitor real-time Bluesky feed data by connecting to the Bluesky Jetstream WebSocket service and viewing incoming posts and events.

- **Bluesky Quote Finder**
  - File: `bluesky-quote-finder.html`
  - Purpose: Search for quote posts on Bluesky by entering a post URL to discover all responses that quote the original post.

- **bluesky-resolve**
  - File: `bluesky-resolve.html`
  - Purpose: View and resolve Bluesky handles to their corresponding Decentralized Identifiers (DIDs) using the AT Protocol API.

- **Bluesky Search**
  - File: `bluesky-search.html`
  - Purpose: Search Bluesky posts using advanced filters and options to organize results by latest or top engagement.

- **Bluesky Thread Viewer**
  - File: `bluesky-thread.html`
  - Purpose: View Bluesky thread conversations with multiple display options including nested thread view, chronological sorting, and media support.

- **Multi-Tab Sync Chat**
  - File: `broadcast-channel-chat.html`
  - Purpose: Send chat messages that synchronize instantly across multiple browser tabs using the Broadcast Channel API.

- **Hacker News, filtered**
  - File: `hacker-news-filtered.html`
  - Purpose: Browse the latest Hacker News stories with customizable content filtering to exclude topics of your choice.

- **Hacker News Multi-Term Histogram**
  - File: `hacker-news-histogram.html`
  - Purpose: Analyze Hacker News stories by searching for multiple terms across a custom time range and visualize the results as an interactive histogram.

- **Hacker News thread export**
  - File: `hacker-news-thread-export.html`
  - Purpose: Export Hacker News discussion threads in a formatted, hierarchical structure by providing a post ID or direct link to the thread.

- **Lobsters Latest Comments Bookmarklet**
  - File: `lobsters-bookmarklet.html`
  - Purpose: Browse Lobste.

- **Passkey Demo | tools.simonwillison.net**
  - File: `passkeys.html`
  - Purpose: Experiment with passkey registration and authentication using the WebAuthn API in your browser.

### Text & Document

- **Alt Text Extractor**
  - File: `alt-text-extractor.html`
  - Purpose: Extract images and their associated metadata from pasted web content with this tool.

- **Animated Word Cloud**
  - File: `animated-word-cloud.html`
  - Purpose: View animated word cloud visualizations that use an Archimedean spiral placement algorithm to position words on a canvas.

- **Token Counter**
  - File: `claude-token-counter.html`
  - Purpose: Count tokens in text and images across multiple Claude models using Anthropic's token counting API.

- **Clipboard Backup**
  - File: `clipboard-backup.html`
  - Purpose: Save and manage clipboard content across multiple formats including text, HTML, RTF, and images with this clipboard backup tool.

- **Clipboard Format Viewer**
  - File: `clipboard-viewer.html`
  - Purpose: Inspect and analyze clipboard data by pasting content into this viewer to see all available formats and their corresponding values.

- **CSS Text Wrapping Properties Guide**
  - File: `css-text-wrapping.html`
  - Purpose: Learn how CSS text wrapping properties control how text flows within containers, including word-wrap, word-break, white-space, text-overflow, hyphens, line-break, and text-wrap.

- **HTML Entity Escaper**
  - File: `escape-entities.html`
  - Purpose: Convert between special characters and their HTML entity representations with this bidirectional encoding tool.

- **Convert GitHub issue to markdown**
  - File: `github-issue-to-markdown.html`
  - Purpose: # Documentation.

- **HTML Live Preview**
  - File: `html-preview.html`
  - Purpose: Write HTML code directly in the editor pane and see the rendered output update in real-time in the preview pane.

- **Contact form**
  - File: `html-validation-demo.html`
  - Purpose: Submit contact information through this responsive form that provides real-time validation using native HTML5 attributes and CSS-only feedback.

- **Incomplete JSON Pretty Printer**
  - File: `incomplete-json-printer.html`
  - Purpose: Format and visualize incomplete or truncated JSON data with automatic live formatting as you type.

- **JSON Diff Tool**
  - File: `json-diff.html`
  - Purpose: Compare JSON documents side-by-side to identify additions, removals, and modifications between two versions.

- **JSON Schema Builder**
  - File: `json-schema-builder.html`
  - Purpose: Create JSON schemas interactively with this builder tool that allows you to define properties, set data types, and configure nested objects through an intuitive form interface.

- **JSON String Extractor**
  - File: `json-string-extractor.html`
  - Purpose: Extract all strings from JSON data that exceed 20 characters in length or contain line breaks.

- **JSON to Markdown Converter**
  - File: `json-to-markdown-transcript.html`
  - Purpose: Convert JSON transcripts from audio into formatted Markdown with speaker names and timestamps.

- **JSON to YAML Converter**
  - File: `json-to-yaml.html`
  - Purpose: Convert JSON data into multiple YAML formats with a single paste.

- **JustHTML Playground - HTML5 Parser**
  - File: `justhtml.html`
  - Purpose: Test the JustHTML Python HTML5 parser directly in your browser with this interactive playground.

- **markdown-copy component**
  - File: `markdown-copy-component.html`
  - Purpose: The `<markdown-copy>` component renders markdown content with built-in controls for viewing the rendered output and copying or viewing the source code.

- **Markdown and Math Live Renderer**
  - File: `markdown-math.html`
  - Purpose: Render Markdown text with integrated LaTeX mathematical equations in real-time as you type.

- **Notes to Markdown**
  - File: `notes-to-markdown.html`
  - Purpose: Convert Apple Notes content to Markdown and HTML formats while preserving hyperlinks and formatting.

- **Omit needless words**
  - File: `omit-needless-words.html`
  - Purpose: # Documentation.

- **Rich Paste to HTML Subset**
  - File: `paste-html-subset.html`
  - Purpose: Convert rich text content from clipboard into clean, filtered HTML containing only semantic elements like paragraphs, headings, lists, links, and text formatting.

- **Rich Text HTML Extractor**
  - File: `paste-rich-text.html`
  - Purpose: Extract HTML code from formatted text by pasting rich content into this tool, which automatically captures and displays the underlying HTML markup.

- **Pretext — Under the Hood**
  - File: `pretext-explainer.html`
  - Purpose: Explore how pure-JavaScript text measurement and line breaking work through an interactive visualization of the Pretext library's pipeline.

- **Render Markdown**
  - File: `render-markdown.html`
  - Purpose: Convert Markdown text to HTML using GitHub's official Markdown API, with options to render standard Markdown or GitHub Flavored Markdown (GFM).

- **Rich Text to Markdown**
  - File: `rich-text-to-markdown.html`
  - Purpose: Convert rich text formats into properly formatted Markdown by pasting content into the text area.

- **RTF to HTML Converter**
  - File: `rtf-to-html.html`
  - Purpose: Convert Rich Text Format (RTF) documents to HTML with preserved formatting, colors, and styling.

- **SQL Pretty Printer**
  - File: `sql-pretty-printer.html`
  - Purpose: Format and beautify SQL queries with customizable styling options.

- **Terminal to HTML**
  - File: `terminal-to-html.html`
  - Purpose: Convert terminal output into shareable HTML documents with support for colored text formatting.

- **Text Diff Tool**
  - File: `text-diff.html`
  - Purpose: Compare two blocks of text to identify character-level differences between them.

- **Text Indentation Tool**
  - File: `text-indentation.html`
  - Purpose: Adjust indentation levels in your text with this tool that offers multiple formatting options.

- **Navigation Bar with Text-Wrap Balance**
  - File: `text-wrap-balance-nav.html`
  - Purpose: Explore how the CSS `text-wrap: balance` property affects navigation layout and text distribution across multiple lines.

- **Wikipedia Wikitext Fetcher**
  - File: `wikipedia-wikitext.html`
  - Purpose: Retrieve the raw wikitext source code from Wikipedia articles by searching for a page title or pasting a direct article URL.

- **Word & Character Counter**
  - File: `word-counter.html`
  - Purpose: Track word and character counts across multiple writing sections with automatic saving to browser storage.

- **XML Well-Formedness Validator**
  - File: `xml-validator.html`
  - Purpose: Check XML documents for well-formedness by pasting content into the input area and clicking the validate button.

- **YAML Explorer**
  - File: `yaml-explorer.html`
  - Purpose: Parse and visualize YAML files in an interactive tree format with collapsible sections for easy navigation of nested data structures.

---

## Python CLI Scripts

Standalone Python scripts for CLI use. Run with `uv run` — dependencies are fetched automatically via PEP 723 inline metadata.

- **`all_gcp_buckets.py`** — View the size of the files in all of your Google Cloud buckets.
  - Run: `uv run https://tools.simonwillison.net/python/all_gcp_buckets.py`

- **`asus_status.py`** — Fetch network status from an ASUS ZenWiFi XT8 router via its HTTP API.
  - Run: `uv run https://tools.simonwillison.net/python/asus_status.py \
  --username admin`

- **`check_invisible_text.py`** — Check a PDF file for possibly instances of invisible text.
  - Run: `uv run https://tools.simonwillison.net/python/check_invisible_text.py \
  my-file.pdf`

- **`claude_code_to_gist.py`** — 
  - Run: `uv run https://tools.simonwillison.net/python/claude_code_to_gist.py`

- **`claude_to_markdown.py`** — Convert a Claude `.
  - Run: `uv run https://tools.simonwillison.net/python/claude_to_markdown.py \
  aed89565-d168-4ff9-bb03-13ea532969ea.jsonl`

- **`codex_to_markdown.py`** — Convert a Codex CLI session JSONL log into Markdown.
  - Run: `uv run https://tools.simonwillison.net/python/codex_to_markdown.py \
  ~/.codex/sessions/2025/09/24/rollout-2025-09-24T15-33-49-01997ddc-88f4-7e40-8dac-d558f31dd3ca.jsonl`

- **`debug_s3_access.py`** — Use this with a URL to an object in an S3 bucket to try and debug why that object cannot be accessed via its public URL.
  - Run: `uv run https://tools.simonwillison.net/python/debug_s3_access.py \
  https://test-public-bucket-simonw.s3.us-east-1.amazonaws.com/0f550b7b28264d7ea2b3d360e3381a95.jpg`

- **`extract_issues.py`** — 
  - Run: `cd datasette
uv run https://tools.simonwillison.net/python/extract_issues.py 1.0a19
# or
uv run https://tools.simonwillison.net/python/extract_issues.py 1.0a19..1.0a20`

- **`gguf_inspect.py`** — Inspect a GGUF file (a format used by llama.
  - Run: `uv run https://tools.simonwillison.net/python/gguf_inspect.py \
  ~/.ollama/models/blobs/sha256-b158411543050d042608cef16fdfeec0d9bc1cf2e63a3625f3887fc0c4249521 \
  --json --exclude tokenizer.ggml.`

- **`git_read_only_http.py`** — Serve a local Git repository over HTTP in read-only mode.
  - Run: `uv run https://tools.simonwillison.net/python/git_read_only_http.py \
  /path/to/repo`

- **`heic2jpg.py`** — Convert HEIC/HEIF photos (commonly from iPhones) to compressed JPEG files.
  - Run: `# Single file
uv run python/heic2jpg.py photo.heic

# With custom quality (1-100, default 50)
uv run python/heic2jpg.py photo.heic -q 80

# Batch convert a whole directory
uv run python/heic2jpg.py ./photos/

# Shrink dimensions by 20% for smaller files
uv run python/heic2jpg.py photo.heic --scale 0.8 -q 40`

- **`highlight.py`** — Given input text to stdin and search/highlight terms, outputs matches plus context with colors to highlight them.
  - Run: `cat myfile.py | uv run https://tools.simonwillison.net/python/highlight.py re search`

- **`http_check.py`** — Check if a given URL supports gzip, ETags and Last-modified conditional GET requests.
  - Run: `uv run https://tools.simonwillison.net/python/http_check.py \
  https://simonw.github.io/ollama-models-atom-feed/atom.xml`

- **`image_crop_compress.py`** — Port of an Azure Blob ImageCropFunction plus EnvironmentConfig: magic-byte detection (PNG / JPEG / WebP), extension fallback, EXIF transpose, center crop with the same rules as the Java code (wide images → width `ceil(1.
  - Run: `uv run python/image_crop_compress.py ./photo.jpg -o ./out.jpg
uv run python/image_crop_compress.py ./wide.png --compression-ratio 0.5 --max-dimension 2048`

- **`json_extractor.py`** — Given a text file that includes JSON syntax but is not valid JSON - a Markdown README file for example - this tool finds all valid JSON objects within that text and returns the largest, or all of them if you specify `-a`.
  - Run: `uv run https://tools.simonwillison.net/python/json_extractor.py \
  README.md`

- **`list_llm_model_ids.py`** — List available model IDs from OpenAI, Anthropic, and Gemini.
  - Run: `uv run https://tools.simonwillison.net/python/list_llm_model_ids.py`

- **`livestream-gif.py`** — Convert a YouTube livestream to an animated GIF or MP4.
  - Run: `uv run https://tools.simonwillison.net/python/livestream-gif.py \
  "https://www.youtube.com/watch?v=BfGL7A2YgUY" \
  --frames 200  -o livestream.mp4 --fps 10 --mp4`

- **`mistral_ocr.py`** — Run PDF files through the Mistral OCR API:.
  - Run: `uv run https://tools.simonwillison.net/python/mistral_ocr.py \
  my-file.pdf > output.md`

- **`modelscope_size.py`** — Calculate the size of a model on ModelScope.
  - Run: `uv run https://tools.simonwillison.net/python/modelscope_size.py \
  https://modelscope.cn/models/Qwen/Qwen3-Coder-480B-A35B-Instruct-FP8`

- **`openai_background_prompt.py`** — 
  - Run: `OPENAI_API_KEY=$(llm keys get openai) uv run https://tools.simonwillison.net/python/openai_background_prompt.py \
  o4-mini-deep-research 'Describe a research task here'`

- **`openai_image.py`** — Generate an image from a text prompt using OpenAI's image models.
  - Run: `uv run https://tools.simonwillison.net/python/openai_image.py \
  'A racoon eating cheese wearing an inappropriate hat'`

- **`pdf_to_jpg.py`** — Rasterize every page of one or more PDFs to JPEG files using PyMuPDF.
  - Run: `uv run python/pdf_to_jpg.py -i ./my_pdfs -o ./jpg_out`

- **`q3_tts.py`** — Generate speech audio using Qwen3-TTS and MLX Audio on macOS.
  - Run: `uv run https://tools.simonwillison.net/python/q3_tts.py 'Say this out loud'`

- **`query_word_in_db.py`** — Scan a whitelist of MySQL tables and, for each text-like column, count rows where the column contains a given substring.
  - Run: `uv run python/query_word_in_db.py \
  --search 'needle' \
  --host db.example.com --user app --database myapp \
  --password "$MYSQL_PASSWORD" \
  -f tables.txt`

- **`show_image.py`** — Display an image in the terminal using rich-pixels:.
  - Run: `uv run https://tools.simonwillison.net/python/show_image.py \
  image.jpg`

- **`streaming_textual_markdown.py`** — Stream the Markdown result of an LLM prompt using Textual's streaming Markdown feature.
  - Run: `uv run https://tools.simonwillison.net/python/streaming_textual_markdown.py \
  'Epic saga of a pelican and a wolf becoming friends over their love for welding'`

- **`update_git_repos.py`** — Recursively find Git work trees under a directory.
  - Run: `uv run python/update_git_repos.py ~/code
uv run python/update_git_repos.py ~/code --branch main
uv run python/update_git_repos.py ~/code --remote origin --dry-run`

- **`webc_inspect.py`** — Inspect Wasmer WebC archives (.
  - Run: `uv run https://tools.simonwillison.net/python/webc_inspect.py \
  ~/.wasmer/cache/checkout/47ff83d2d205df14e7f057a1f0a1c1da70c565d2e32c052f2970a150f5a9b407.bin`

- **`whitespace_cleaner.py`** — Replace any lines that are entirely whitespace with blank lines in specified files or folders:.
  - Run: `uv run https://tools.simonwillison.net/python/whitespace_cleaner.py \
  my-file.txt my-folder`

---

## For AI Agents

This index is designed for quick lookup. To find a tool for a specific task:

1. Scan the category headers in **Browser Tools** or **Python CLI Scripts**.
2. Read the **Purpose** line to see if the tool matches.
3. Open `{slug}.html` for browser tools or `python/{filename}` for CLI scripts to see implementation.
4. Browser tools also have `{slug}.docs.md` with detailed docs.

When adding a new tool, update this index by running:
```bash
python build_tools_index.py
```